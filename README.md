# Stepwise AI Desktop Assistant

A powerful, tool-augmented desktop AI assistant featuring a custom floating GUI. Powered by Google's Gemini model and built with LangGraph, this agent can see your screen, manage your file system, execute commands, browse the web, and process documents, all through an intuitive chat interface.

![stepwise agent](<stepwise agent.png>)

---

## Features

This project has evolved into a robust desktop agent with a focus on usability and powerful, real-world capabilities.

### Implemented Features

  - **Advanced AI Core**:

      - Utilizes **Google's Gemini (`gemini-2.5-flash-preview-05-20`)** model for sophisticated reasoning and instruction following.
      - Built on **LangChain's LangGraph** to create a reliable, stateful agent that can use tools and maintain conversation history.

  - **Powerful Tool-Augmented Agent**: The agent can go beyond simple chat and interact with your system:

      - **Screen & Window Awareness**: Can see and describe screen content (`SeeScreen`) and identify the currently active window (`get_active_window_title`).
      - **Full File System Control**:
          - **CRUD Operations**: `Create`, `Read`, `Write`, `Delete`, `Move`, and `Rename` files and folders.
          - **Advanced I/O**: The `Write` and `Read` tools support multiple formats, including `.txt`, `.docx`, `.pdf`, and `.xlsx`.
          - **Navigation & Search**: `list_directory_tree` to view folder structures and `find_files` to locate files with pattern matching.
          - **Archive Management**: `zip_files` to compress and `unzip_file` to extract archives.
      - **System Interaction & Automation**:
          - **Command Execution**: `execute_shell_command` runs any command in the system's terminal.
          - **Application Control**: `open_file_or_app` to launch files and applications, and `type_on_screen` to simulate keyboard input.
          - **System Awareness**: Can retrieve current system information and the date/time.
          - **Clipboard Integration**: Can save content to and read from the system's clipboard.
      - **Web & Content Processing**:
          - **Smart Web Scraping**: Extracts clean, readable content from web pages.
          - **Web Search & Image Downloads**: Integrated with Tavily to search the web and download images based on descriptions.
          - **Document Analysis (RAG)**: The `ask_document` tool can answer specific questions based on the content of a file or text.
          - **Summarization**: Can provide concise summaries of long documents or articles.

  - **Polished Graphical User Interface (GUI)**:

      - A custom **Tkinter/TTK** interface with a professional dark theme.
      - A main **floating, draggable circle** for easy access.
      - A full-featured **chat window** that supports markdown (`**bold**`, bullets) and can be moved, minimized, or closed.
      - **Smart UI Behavior**: The chat window automatically minimizes when it loses focus and intelligently positions itself based on available screen space.
      - **Visual Feedback**: Displays an "AI is thinking..." message and disables the send button during processing.
      - **Hover effects** and custom styling for a responsive user experience.

  - **Robust Architecture**:

      - **Multithreaded design** runs the GUI on the main thread and the agent on a background thread, ensuring a smooth, non-blocking experience.
      - **Stateful Sessions**: Remembers the entire conversation within a single session.
      - **Clean Session Reset**: Closing a chat window completely resets the agent's memory, ensuring new conversations start fresh.

### Planned Enhancements

  - **Voice Interaction**: Implement the "Speak" button with reliable text-to-speech and speech-to-text functionality, and add recognition and response capabilities in multiple languages.
  - **Customizable Appearance**: Allow users to change themes, colors, and window sizes.
  - **Conversation History**: Implement a feature to save and load past conversations.

---

## Tech Stack

  - **Backend**: Python
  - **AI & Orchestration**: LangChain, LangGraph, Google Generative AI
  - **GUI**: Tkinter, ttk
  - **Core Tools**: `pyautogui`, `pyperclip`, `mss`, `pygetwindow`
  - **File I/O**: `pypdf`, `python-docx`, `openpyxl`, `fpdf`, `pandas`
  - **Web & Search**: `Tavily Search`, `BeautifulSoup`
  - **Document Analysis (RAG)**: `langchain-chroma`, `sentence-transformers`

---

## Project Structure

The project is organized into a modular, multi-file structure for clarity and scalability:

```
stepwise-agent/
│
├── venv/
│
├── chatbot.py           # Main entry point to launch the application
├── AgentGUI.py          # Contains all Tkinter UI code
├── AgentGraph.py        # Defines the LangGraph agent logic and state
├── agent_and_tools.py   # Defines all agent tools and initializes the AI model
│
├── .env                 # API keys and environment variables
├── requirements.txt     # Project dependencies
├── README.md            # Project overview and documentation
│
├── Agent Graph.png      # Diagram of the agent's logic graph
└── stepwise agent.png   # Screenshot of the application GUI
```

---

## Installation

### Prerequisites

  - Python 3.8+
  - A Google API Key and a Tavily API Key

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

4.  **Create a `.env` file** in the root directory and add your API keys:

    ```
    GOOGLE_API_KEY="your_google_api_key"
    TAVILY_API_KEY="your_tavily_api_key"
    ```

---

## Usage

1.  Run the main application file from your terminal:
    ```bash
    python chatbot.py
    ```
2.  The floating circle will appear on your screen.
3.  Click the **"Chat"** button to open the chat window.
4.  Type your requests to the AI. You can ask it to perform any of its tool-based actions, like "what do you see on my screen?" or "summarize the content of the file at C:/docs/report.pdf".
5.  Use the chat window controls (`—`, `X`) or click away from the window to manage the session.

---

## Contributing

Contributions are welcome! Please feel free to submit a pull request for bug fixes or new features, or open an issue if you encounter any problems.
