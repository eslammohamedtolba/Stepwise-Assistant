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
        Determines the next step. 
        It has access to 'output_queue' from the parent function's scope.
        """
        last_message = state['messages'][-1]

        if last_message.tool_calls:
            return "tools_node"

        # The final response from the LLM can be a list of content blocks or a simple string.
        # We must convert it to a single string before any further processing
        final_content = ""
        if isinstance(last_message.content, list):
            # Join list items with a newline for better readability in the GUI
            final_content = "\n".join(
                part.get('text', '') if isinstance(part, dict) else str(part)
                for part in last_message.content
            )
        else:
            # If it's already a string, use it directly (use str() for safety)
            final_content = str(last_message.content)

        # If no tool call, send the agent's final answer to the GUI
        output_queue.put(("AI", final_content))

        # Check for exit condition to terminate the entire application
        if "exit" in final_content.lower():
            output_queue.put(("__EXIT__", "Conversation ended."))
        
        return "end"

    # Build the graph
    graph = StateGraph(MyState)
    graph.add_node("process_node", process_node)
    graph.add_node("tools_node", ToolNode(all_tools))
    
    graph.set_entry_point("process_node")
    
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
    
    # Pass the output_queue when creating the app
    app = create_graph_app(output_queue)

    # --- FIX: Use a raw string (r"..."") to prevent unicode escape errors ---
    system_message = SystemMessage(content=r"""You are an advanced AI assistant integrated into the user's operating system. Your primary goal is to understand the user's requests in the context of what they are currently seeing on their screen. You must follow these rules without exception:

**Core Directive: The Screen is the Ground Truth**

1.  **"Here" or "Current Folder" means the visual directory:** When the user refers to "here", "this folder", or "the current directory", they are ALWAYS referring to the folder path visible in the active window on their screen (e.g., in File Explorer, VS Code's file panel, or a terminal).
2.  **Mandatory Visual Check:** Before executing ANY file system command (like `Create`, `Delete`, `Write`, `find_files`, `list_directory_tree`), you MUST first determine the current visual path.

**Execution Logic for Sequential Commands**

* **No Assumptions:** NEVER assume the user is in the same folder as they were in the previous turn. The user can move directories between commands.
* **Re-evaluate Context Every Time:** You MUST perform the "Mandatory Visual Check" procedure for **every single command**, even if it's the same type of command requested sequentially.
    * **Example Scenario:**
        1.  User says: "Create a file named `report.txt` here."
        2.  *Your Action:* Perform the visual check to find the path (e.g., `C:\Users\hp\Documents`). Execute `Create(path='C:\\Users\\hp\\Documents', name='report.txt')`.
        3.  User then says: "Now create a folder named `Images` here."
        4.  *Your Action:* **DO NOT** assume the path is still `C:\Users\hp\Documents`. The user might have navigated elsewhere. **You must repeat the full visual check procedure** to get the new current path before executing `Create(path='...', name='Images')`.

**General Responsibilities**

* Be helpful and proactive. If a path cannot be determined, inform the user and ask for clarification.
* Use other tools as needed to fulfill requests, but always prioritize the visual context for file operations.
* If the user says 'exit', 'end', or 'stop', respond with a message that clearly includes the word 'exit' to terminate the application.
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
