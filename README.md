# Stepwise AI Desktop Assistant

A powerful, tool-augmented desktop AI assistant featuring a custom floating GUI. Powered by Google's Gemini Pro and built with LangGraph, this agent can see your screen, control your file system, browse the web, and more, all through an intuitive chat interface.

![stepwise agent](<stepwise agent.png>)

---

## Features

This project has evolved into a robust desktop agent with a focus on usability and powerful, real-world capabilities.

### Implemented Features

-   **Advanced AI Core**:
    -   Utilizes **Google's Gemini** model for sophisticated reasoning and instruction following.
    -   Built on **LangChain's LangGraph** to create a reliable, stateful agent that can use tools and maintain conversation history.

-   **Powerful Tool-Augmented Agent**: The agent can go beyond simple chat and interact with your system:
    -   **Screen Perception**: Can see and describe the contents of your screen, providing contextual awareness for tasks.
    -   **Full File System Control**: Create, read, write, delete, move, and rename files and folders directly through chat commands.
    -   **Web Search**: Integrated with Tavily Search to find real-time information online.
    -   **System Awareness**: Can retrieve current system information and time.
    -   **Clipboard Integration**: Can write to your system's clipboard.

-   **Polished Graphical User Interface (GUI)**:
    -   A custom **Tkinter/TTK** interface with a professional dark theme.
    -   A main **floating, draggable circle** for easy access.
    -   A full-featured **chat window** that can be moved, minimized, or closed.
    -   **Smart UI Behavior**: The chat window automatically minimizes when it loses focus and intelligently positions itself based on available screen space.
    -   **Hover effects** and custom styling for a responsive user experience.

-   **Robust Architecture**:
    -   **Multithreaded design** runs the GUI on the main thread and the agent on a background thread, ensuring a smooth, non-blocking experience.
    -   **Stateful Sessions**: Remembers the entire conversation within a single session.
    -   **Clean Session Reset**: Closing a chat window completely resets the agent's memory, ensuring new conversations start fresh.

### Planned Enhancements

-   **Voice Interaction**: Implement the "Speak" button with reliable text-to-speech and speech-to-text functionality.
-   **Proactive Assistance**: Enable the agent to automatically move the floating circle to relevant parts of the screen to guide the user's focus.
-   **Visual Task Tracking**: Add UI elements to show when the agent is using a tool or thinking.
-   **Customizable Appearance**: Allow users to change themes, colors, and window sizes.
-   **Conversation History**: Implement a feature to save and load past conversations.
-   **Multi-language Support**: Add recognition and response capabilities in multiple languages.

---

## Tech Stack

-   **Backend**: Python
-   **AI & Orchestration**: LangChain, LangGraph, Google Generative AI
-   **GUI**: Tkinter, ttk
-   **Tools**: PyAutoGUI, Pyperclip, Tavily Search

---

## Project Structure

The project is now organized into a modular, multi-file structure for clarity and scalability:

```
stepwise-agent/
│
├── chatbot.py               # Main entry point to launch the application
├── AgentGUI.py              # Contains all Tkinter UI code for the floating circle and chat window
├── AgentGraph.py            # Defines the LangGraph agent logic, state, and conversation flow
├── agent_and_tools.py       # Defines all agent tools (SeeScreen, file I/O, etc.) and initializes the AI model
│
├── requirements.txt         # Project dependencies
├── Agent Graph.png          # Diagram of the agent's logic graph
└── stepwise agent.png       # Screenshot of the application GUI
```

---

## Installation

### Prerequisites

-   Python 3.8+
-   A Google Gemini API Key

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/eslammohamedtolba/Stepwise-Assistant.git
    cd Stepwise-Assistant
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies from `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file** in the root directory of the project and add your API key:
    ```
    GOOGLE_API_KEY="your_gemini_api_key"
    tavily_api_key="your_tavily_api_key"
    ```

---

## Usage

1.  Run the main application file from your terminal:
    ```bash
    python chatbot.py
    ```
2.  The floating circle will appear on the top-right of your screen.
3.  Click the **"Chat"** button to open the chat window.
4.  Type your requests to the AI. You can ask it to perform any of its tool-based actions, like "what do you see on my screen?" or "create a folder named 'test' on my desktop".
5.  Use the chat window controls (`—`, `X`) or click away from the window to manage the session.

---

## Contributing

Contributions are welcome! Please feel free to submit a pull request for bug fixes or new features, or open an issue if you encounter any problems.
