import threading
import queue
from AgentGUI import FloatingCircle
from AgentGraph import run_agent_loop

if __name__ == "__main__":
    # The queues allow safe communication between the GUI and the agent thread
    input_queue = queue.Queue()  # GUI -> Agent
    output_queue = queue.Queue() # Agent -> GUI

    # --- Start the agent thread ---
    # This runs the 'run_agent_loop' function in the background.
    # 'daemon=True' ensures the thread closes when the main GUI window is closed.
    agent_thread = threading.Thread(
        target=run_agent_loop,
        args=(input_queue, output_queue),
        daemon=True
    )
    agent_thread.start()

    # --- Start the GUI ---
    # This creates the floating circle and runs its main loop.
    # It must run in the main thread.
    gui_app = FloatingCircle(input_queue, output_queue)
    gui_app.mainloop()

