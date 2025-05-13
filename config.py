import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# UI Settings
WINDOW_WIDTH = 170
WINDOW_HEIGHT = 170
WINDOW_POSITION_X = 100
WINDOW_POSITION_Y = 100
BACKGROUND_COLOR = "skyblue"
CIRCLE_COLOR = "deepskyblue"
SPEAKING_COLOR = "mediumseagreen"
LISTENING_COLOR = "gold"

# Wave Animation Settings
WAVE_RADIUS = 80
WAVE_STEP = 10
WAVE_INTERVAL = 100
WAVE_MAX = 3
WAVE_COLORS = {
    "speaking": "white",
    "listening": "orange"
}

# Close Button Settings
CLOSE_BUTTON_RADIUS = 15
CLOSE_BUTTON_X = 86
CLOSE_BUTTON_Y = 25

# AI Model Settings
GEMINI_MODEL = "gemini-1.5-flash"