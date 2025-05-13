import speech_recognition as sr
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

# Initialize speech recognizer
recognizer = sr.Recognizer()

def speak(text, animate_circle=None):
    """Text-to-speech function"""
    print("Bot:", text)
    
    if animate_circle:
        animate_circle("speaking")
        
    engine.say(text)
    engine.runAndWait()
    
    if animate_circle:
        animate_circle("normal")

def listen(animate_circle=None):
    """Speech-to-text function"""
    print("Listening...")
    
    if animate_circle:
        animate_circle("listening")
        
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print("You:", query)
            
            if animate_circle:
                animate_circle("normal")
                
            return query
        except Exception as e:
            print(f"Recognition error: {e}")
            
            if animate_circle:
                animate_circle("normal")
                
            return ""