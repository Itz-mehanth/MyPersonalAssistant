import torch
import torchaudio
from ChatTTS import ChatTTS
import scipy.io.wavfile as wav
import sounddevice as sd
import pyttsx3


def speakai(text):
    chat = ChatTTS.Chat()
    chat.load(compile = True)
    torch.manual_seed(10)

    input = text
    params_refine_text = {
        'prompt': '[oral_2][laugh_4][break_4]'
    }

    audio_array_en = chat.infer(input)
    # Reshape to 2D (1, N) if the output is 1D (mono)
    audio_array_en_2d = torch.from_numpy(audio_array_en[0]).unsqueeze(0)
    
    # Save the audio
    torchaudio.save("output3.wav", audio_array_en_2d, 24000)
    # Read the .wav file
    rate, data = wav.read("output3.wav")

    # Play the sound
    sd.play(data, rate)

    # Wait for the sound to finish
    sd.wait()


# Initialize the speech engine (for voice responses)
engine = pyttsx3.init()

# Set the bot's voice to a female voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function to make the bot speak
def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()