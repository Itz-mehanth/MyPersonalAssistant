import pyttsx3

engine = pyttsx3.init()

def respond(text):
    engine.say(text)
    engine.runAndWait()

respond("How can I assist you today?")
