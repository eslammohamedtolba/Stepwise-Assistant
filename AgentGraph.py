from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from agent_and_tools import all_tools, agent

# The state schema remains the same. `add_messages` is key.
class MyState(TypedDict):
    messages: Annotated[Sequence, add_messages]

def create_graph_app(output_queue):
    """
    Creates and compiles a new instance of the agent graph.
    This ensures no state is carried over between sessions.
    
    Args:
        output_queue: The queue to send messages back to the GUI.
    """
    # --- Graph Definition ---
    
    def process_node(state: MyState) -> MyState:
        """Invokes the agent with the current conversation history."""
        response = agent.invoke(state["messages"])
        return {"messages": [response]}

    def should_continue(state: MyState):
        """
        Determines the next step. It has access to 'output_queue'
        from the parent function's scope.
        """
        last_message = state['messages'][-1]

        if last_message.tool_calls:
            return "tools_node"

        # If no tool call, send the agent's final answer to the GUI
        output_queue.put(("AI", last_message.content))

        # Check for exit condition to terminate the entire application
        if "exit" in last_message.content.lower():
            output_queue.put(("__EXIT__", "Conversation ended."))
        
        return "end"

    # Build the graph
    graph = StateGraph(MyState)
    graph.add_node("process_node", process_node)
    graph.add_node("tools_node", ToolNode(all_tools))
    
    graph.set_entry_point("process_node")
    
    # --- FIX: Pass the 'should_continue' function directly. ---
    # It now correctly captures 'output_queue' from its defining scope.
    graph.add_conditional_edges(
        "process_node",
        should_continue,
        {
            "tools_node": "tools_node",
            "end": END
        }
    )
    graph.add_edge("tools_node", "process_node")
    
    return graph.compile()


def run_agent_loop(input_queue, output_queue):
    """
    This function runs in a separate thread, managing the agent's logic
    and maintaining conversation history.
    """
    
    # ass the output_queue when creating the app
    app = create_graph_app(output_queue)

    system_message = SystemMessage(content="""
    You are a helpful assistant running in a continuous loop.

    Your main responsibilities are:
    - Respond helpfully to any user input, whether or not a tool is required.
    - If a request can be answered without using any tools, generate a direct natural response.
    - Use the available tools **only if they are needed** to complete the task.
    - If a tool is helpful for the task, call it and wait for the tool result before continuing.
    - If the user says 'exit', 'end', or 'stop', **respond with a message that clearly includes the word 'exit'**.
    Only then will the application stop.

    Make sure to always try to help. If no tool is needed, still provide a thoughtful and useful reply.
    """)
    
    # Initialize conversation history
    conversation_history = [system_message]
    
    while True:
        # Wait for an input from the GUI's queue
        user_input = input_queue.get()

        if user_input == "__EXIT__":
            break
        
        if user_input == "__RESET__":

            conversation_history = [system_message]

            # Pass the output_queue again when recompiling 
            app = create_graph_app(output_queue)
            continue
        
        # Send the user's message back to the GUI to be displayed
        output_queue.put(("You", user_input))
        
        # Append the new user message to the persistent history
        conversation_history.append(HumanMessage(content=user_input))
        
        # Invoke the graph with the full conversation history
        result = app.invoke({"messages": conversation_history})
        
        # Update our persistent history with the new state for the next turn.
        conversation_history = result['messages']

