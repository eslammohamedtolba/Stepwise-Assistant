from services.speech import speak, listen
from services.ai import get_response
from ui.app_window import create_app_window
from utils.threading_utils import run_in_thread

def chatbot_loop(animate_circle):
    """Main chatbot interaction loop"""
    speak("Hello! Tell me what you want to achieve, and I'll guide you step by step.", animate_circle)
    step_mode = False
    
    while True:
        user_input = listen(animate_circle)
        if "stop" in user_input.lower():
            speak("Goodbye!", animate_circle)
            break

        if not step_mode:
            if user_input:
                goal = user_input
                step_mode = True
                prompt = f"I want to do this: {goal}. Please guide me one step at a time. After each step, wait for me to say 'done' before giving the next one."
                response = get_response(prompt)
                speak(response, animate_circle)
        else:
            if "done" in user_input.lower():
                response = get_response("I finished that step. What is the next step?")
                speak(response, animate_circle)
            else:
                speak("Say 'done' when you're ready for the next step.", animate_circle)

def main():
    """Application entry point"""
    root, animate_circle = create_app_window()
    
    # Run chatbot loop in background thread
    run_in_thread(chatbot_loop, animate_circle)
    
    # Start the UI event loop
    root.mainloop()

if __name__ == "__main__":
    main()