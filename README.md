# Stepwise Assistant

A voice-controlled AI assistant that guides users through tasks step-by-step using Google's Gemini AI. This floating interface provides visual feedback during interactions and makes complex tasks more manageable through guided instruction.

![stepwise assistant](<stepwise assistant.png>)

---

## Features

### Implemented
- **Voice-Driven Interaction**: Seamless voice communication with text-to-speech output and speech-to-text input
- **Step-by-Step Guidance**: AI breaks down complex tasks into manageable steps, waiting for user confirmation before proceeding
- **Visual State Indication**: Color-coded interface provides clear visual feedback:
  - Blue (deepskyblue): Idle/ready state
  - Green (mediumseagreen): Speaking state
  - Gold: Listening state
- **Wave Animation**: Dynamic wave animations during active speaking and listening states
- **Floating Interface**: Always-on-top, draggable interface that remains accessible while following instructions
- **Transparent Background**: Clean design that minimizes screen obstruction
- **One-Click Termination**: Easy close button for ending the session

### Planned Enhancements
- **Enhanced Speech Recognition**: Integration with improved speech recognition models for better accuracy
- **Multi-language Support**: Recognition and response in multiple languages
- **Visual Task Tracking**: Progress indicators for multi-step tasks
- **Customizable Appearance**: User-defined themes and sizes
- **Task History**: Storage and retrieval of previously completed tasks
- **Screen Region Focus**: Ability to highlight specific screen areas relevant to the current step
- **Screenshot Integration**: Capability to capture and analyze screen content for contextual assistance

---

## Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Setup
1. Clone this repository
```bash
git clone https://github.com/eslammohamedtolba/Stepwise-Assistant.git
cd Stepwise-Assistant
```

2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies
```bash
pip install google-generativeai speech_recognition pyttsx3 python-dotenv
```

4. Create a `.env` file in the project root with your Gemini API key
```
GEMINI_API_KEY=your_api_key_here
```

---

## Usage

Run the application:
```bash
python main.py
```

- **To start**: Speak your task or goal when prompted
- **During guidance**: Say "done" after completing each step to proceed
- **To end session**: Say "stop" or click the red X button

---

## Project Structure

```
stepwise_assistant/
├── main.py                # Entry point
├── config.py              # Configuration settings
├── ui/
│   ├── __init__.py
│   ├── app_window.py      # Main window UI
│   └── circle_ui.py       # Circular UI components
├── services/
│   ├── __init__.py
│   ├── speech.py          # TTS and STT functionality
│   └── ai.py              # AI model integration
└── utils/
    ├── __init__.py
    └── threading_utils.py # Thread management utilities
```

---

## Technical Details

- **UI**: Tkinter-based custom circular interface
- **Speech Recognition**: Google Speech Recognition API via SpeechRecognition library
- **Text-to-Speech**: pyttsx3 engine
- **AI Integration**: Google Generative AI (Gemini)

---

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
