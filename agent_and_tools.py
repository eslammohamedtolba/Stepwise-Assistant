import os
import shutil
import pyperclip  # pip install pyperclip
import pyautogui # pip install pyautogui
from datetime import datetime
from langchain_core.tools import tool
from langchain_community.tools import TavilySearchResults
import platform
import socket
import base64
from io import BytesIO
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

# Create llm
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash-preview-05-20",
    temperature = 0
)

@tool
def Save(clipboard_content: str):
    """This is a function to save the content to the user clipboard.
    
    Args:
        clipboard_content: The content to be saved.
    """
    pyperclip.copy(clipboard_content)

    return "Content has been copied to the clipboard."

@tool
def list_directory_tree(path: str, depth: int = 0) -> str:
    """
    Returns the folder and file tree of a given directory up to a specified depth.

    Args:
        path: The root directory path to explore.
        depth: How many levels deep to explore (default: 0).
    """
    tree_lines = []

    def walk(current_path, current_depth):
        if current_depth > depth:
            return
        try:
            items = os.listdir(current_path)
        except (PermissionError, FileNotFoundError):
            return
        for item in items:
            item_path = os.path.join(current_path, item)
            tree_lines.append("  " * current_depth + f"- {item}")
            if os.path.isdir(item_path):
                walk(item_path, current_depth + 1)

    if not os.path.exists(path):
        return f"Path does not exist: {path}"
    if not os.path.isdir(path):
        return f"Path is not a directory: {path}"

    walk(path, 0)
    return "\n".join(tree_lines)

@tool
def Create(path: str, name: str) -> str:
    """
    Create a new file or folder with the specified name at the given path.
    If the name contains a dot (e.g., 'file.txt'), it is treated as a file.
    Otherwise, it is treated as a folder.

    Args:
        path: The directory in which to create the file or folder.
        name: The name of the file (with extension) or folder.
    """
    try:
        full_path = os.path.join(path, name)

        if "." in name:
            # It's a file
            with open(full_path, 'w') as f:
                pass
            return f"File created: {full_path}"
        else:
            # It's a folder
            os.makedirs(full_path, exist_ok=True)
            return f"Folder created: {full_path}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def Delete(path: str, name: str) -> str:
    """
    Delete a file or folder by specifying its path and name.

    Args:
        path: The directory where the file or folder is located.
        name: The name of the file or folder to delete.
    """
    try:
        target = os.path.join(path, name)
        if os.path.isfile(target):
            os.remove(target)
            return f"File deleted: {target}"
        elif os.path.isdir(target):
            shutil.rmtree(target)
            return f"Folder deleted: {target}"
        else:
            return "Item not found at specified path."
    except Exception as e:
        return f"Error: {str(e)}"
    
@tool
def Move(source: str, destination: str, name: str) -> str:
    """
    Move a file or folder by specifying its current name and source/destination paths.

    Args:
        source: The directory where the file or folder currently exists.
        destination: The directory where the file or folder should be moved.
        name: The current name of the file or folder to move.
    """
    try:
        source_path = os.path.join(source, name)
        destination_path = os.path.join(destination, name)
        shutil.move(source_path, destination_path)
        return f"Moved to: {destination_path}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def Rename(path: str, old_name: str, new_name: str) -> str:
    """
    Rename a file or folder from old_name to new_name within the specified path.

    Args:
        path: The directory containing the file or folder.
        old_name: The current name of the file or folder.
        new_name: The new name to assign.
    """
    try:
        old_path = os.path.join(path, old_name)
        new_path = os.path.join(path, new_name)
        os.rename(old_path, new_path)
        return f"Renamed to: {new_path}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def Write(path: str, file_name: str, content: str) -> str:
    """
    Write content to a file at the specified path and file name.

    Args:
        path: The directory where the file is located or should be created.
        file_name: The name of the file (including extension).
        content: The text content to write into the file.
    """
    try:
        full_path = os.path.join(path, file_name)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Content written to: {full_path}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def Read(path: str, file_name: str) -> str:
    """
    Read content from a file.

    Args:
        path: The directory where the file is located.
        file_name: The name of the file (including extension).
    """
    try:
        full_path = os.path.join(path, file_name)
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def Current_time() -> str:
    """Returns the current date and time as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Create the Tavily search tool
search_tool = TavilySearchResults(max_results=5)

@tool
def GetSystemInfo() -> str:
    """
    Get basic information about the current system of the user laptop or computer.

    Returns:
        str: A string containing OS, version, architecture, processor, and hostname.
    """
    return f"OS: {platform.system()}, \
            OS Version: {platform.version()}, \
            Architecture: {platform.machine()}, \
            Processor: {platform.processor()}, \
            Hostname: {socket.gethostname()}"

@tool
def SeeScreen() -> str:
    """
    SeeScreen is a powerful visual perception tool that allows the agent to observe the current screen context
    through an in-memory screenshot and interpret its content using Gemini's advanced vision-language capabilities.

    The tool captures the entire screen without saving the image to disk and immediately processes it with
    a multimodal LLM to extract a detailed description of what is visually present, including UI elements,
    open windows, visual cues, and text content.

    This tool is especially useful for agents needing to:
    - Understand the current user interface
    - Respond to visual prompts on the screen
    - Monitor workflows, apps, or web pages in real time
    - Provide contextual assistance based on what the user is viewing

    Agents are strongly encouraged to call this tool **whenever screen context is important**, 
    especially when decisions, suggestions, or actions depend on what is being visually displayed.

    Returns:
        str: A rich and structured textual description of the current screen content.
    """
    # Capture screenshot using pyautogui
    screenshot = pyautogui.screenshot()

    # Convert screenshot to base64 data URL (in-memory)
    buffered = BytesIO()
    screenshot.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    data_url = f"data:image/png;base64,{img_base64}"

    # Compose professional multimodal prompt
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": (
                    "You are an expert visual assistant. Analyze the following screenshot and provide a clear, structured "
                    "description of what is visible. Mention any open applications, UI components, readable text, and "
                    "overall screen layout. Be as detailed and organized as possible to help another agent understand "
                    "what the user is currently seeing."
                )
            },
            {"type": "image_url", "image_url": data_url}
        ]
    )

    # Send to Gemini and return description
    response = llm.invoke([message])
    return response.content



# Combine all tools
all_tools = [Save, 
        list_directory_tree,
        Delete, Create, Move, Rename, 
        Write, Read,
        search_tool,
        Current_time,
        GetSystemInfo,
        SeeScreen]


# Create agent 🤖
agent = llm.bind_tools(all_tools)


