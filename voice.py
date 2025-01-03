import threading
import torch
import torchaudio
import scipy.io.wavfile as wav
import sounddevice as sd
import pyttsx3
from ui import ui


# Initialize the speech engine (for voice responses)
engine = pyttsx3.init()

# Set the bot's voice to a female voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


filename = "aivoice.wav"
def speak(text):
    print(text)
    engine.setProperty('rate', 150)  # Set to 150 WPM (slower)
    engine.save_to_file(text, filename)
    engine.runAndWait()

    # Start the `ui()` function in a separate thread
    ui_thread = threading.Thread(target=ui, args=(text,))
    ui_thread.start()

    # Play the speech synchronously
    engine.say(text)
    engine.runAndWait()

    # Wait for `ui()` to complete (join the thread)
    ui_thread.join()

