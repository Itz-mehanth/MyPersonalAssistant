import os
import re
import speech_recognition as sr
import pyttsx3
import requests
import time
from huggingface_hub import InferenceClient
import threading
from PIL import Image
import mss
from pydub import AudioSegment
from io import BytesIO
import pygame
import sqlite3
import whisper
import pyaudio
import numpy as np
from generateCode import generateCode
from WebSearch import playOnline, playSong, chatWithBot
from systemControl import search_and_open_file
from API_KEY import API_TOKEN
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and a stream handler
file_handler = logging.FileHandler('jarvis.log')
stream_handler = logging.StreamHandler()

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Modify the existing functions to include logging
def speak(text):
    logger.info(f'Speaking: {text}')
    print(text)
    engine.say(text)
    engine


repo_id = "meta-llama/Llama-3.3-70B-Instruct"
repo_id = "openai-community/gpt2"
repo_id = "Qwen/QwQ-32B-Preview"
repo_id = "Qwen/Qwen2.5-Coder-32B-Instruct"

# Set the bot's name
BOT_NAME = "Pulse"

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

# Set your ElevenLabs API key
API_KEY = "sk_10bd287e4ce3f9f6af6bc73dff5150d2d840e66ddf108438"
VOICE_ID = "bIHbv24MWmeRgasZH58o"  # You can find the voice ID in your ElevenLabs dashboard

def listen_for_command(duration = 10):
    model = whisper.load_model("base")
    while True:
        try:
            """Capture microphone input and transcribe it using Whisper."""
            chunk = 1024  # Buffer size
            format = pyaudio.paInt16  # Audio format
            channels = 1  # Mono audio
            rate = 16000  # Sampling rate

            p = pyaudio.PyAudio()
            stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

            speak("Listening...")
            frames = []

            # Record audio in chunks for the given duration
            for _ in range(0, int(rate / chunk * duration)):
                data = stream.read(chunk)
                frames.append(np.frombuffer(data, dtype=np.int16))

            print("Recording complete.")
            stream.stop_stream()
            stream.close()
            p.terminate()

            # Combine all chunks into a single audio array
            audio_data = np.hstack(frames).astype(np.float32) / 32768.0  # Normalize PCM values to [-1, 1]

            # Transcribe the audio using Whisper
            print("Transcribing...")
            result = model.transcribe(audio_data, fp16=False)
            print("Transcription:")
            speak("You said" + result["text"])
            return result["text"]
        except sr.UnknownValueError:
            # Handle cases where speech could not be understood
            print("unknown command")
            continue  # Continue listening
        except sr.RequestError:
            speak("Could not request results; check your internet connection.")
            continue  # Continue listening
        except Exception as e:
            print(f"Error: {e}")
            continue  # Continue listening


# Predefined functions with their parameter details
FUNCTIONS = {
    "generateCode": {
        "module": "generateCode",
        "description": "Generates code based on user-provided requirements, like opening any application or works like interacting with the system.",
        "parameters": ["task_description"],
        "example": 'generateCode("Implement a quicksort algorithm")',
    },
    "playOnline": {
        "module": "WebSearch",
        "description": "Plays a video from web based on the search query.",
        "parameters": ["query"],
        "example": 'playOnline("lofi beats to relax to")',
    },
    "playSong": {
        "module": "WebSearch",
        "description": "Plays a song based on the search query from spotify.",
        "parameters": ["song_name"],
        "example": 'playSong("Bohemian Rhapsody by Queen")',
    },
    "search_and_open_file": {
        "module": "systemControl",
        "description": "Searches for a file in the system inside a specific folder and opens it.",
        "parameters": ["search_path", "file_name"],
        "example": 'search_and_open_file("C:\\Users\\mehan\\Downloads","project_report.pdf")',
    },
    "chatWithBot": {
        "module": "chatBot",
        "description": "Acts as a chatbot to answer the user's questions and doubts in natural language.",
        "parameters": ["user_query"],
        "example": 'chatWithBot("What is the capital of France?")',
    },
}

def validResponse(response):
    functions = ["generateCode", "playOnline", "playSong", "search_and_open_file", "chatWithBot"]
    # Check if any function call exists in the string
    if any(re.search(fr"{func}\s*\(", response) for func in functions):
        print("A function call exists in the string.")
        return True
    else:
        speak("No results found")
        return False
    
# Function to generate a response using Hugging Face's GPT-2 API
def generate_response(prompt):
    # Define the full API URL
    API_URL = "https://api-inference.huggingface.co/models/" + repo_id

    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    # Fine-tune the prompt to include the AI's role and identity
    enhanced_prompt = (
        "You are a programming assistant named {BOT_NAME}. Your job is to generate Python code based on the user's query.\n"
        "The user will provide a natural language query, and you must decide which function to call from the following options:\n"
        f"{list(FUNCTIONS.keys())}.\n"
        f"Each function and its parameters are: {FUNCTIONS}.\n"
        "Respond with a Python code snippet that contains the function call, and make sure to include all required arguments. place the code inside triple quotes\n"
        "Here is the user's query:\n"
        f"{prompt}"
    )

    data = {
        "inputs": enhanced_prompt,
        "parameters": {"max_new_tokens": 150},
        "task": "text-generation"
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        # Extract and clean up the response
        generated_text = response.json()[0]["generated_text"]
        print("Generated Response:", generated_text)
        # Extract the code block (if applicable)

        

        code_start = generated_text.find('"""')
        code_end = generated_text.find('"""', code_start + 1)
        if code_start != -1 and code_end != -1:
            result = generated_text[code_start + len('"""'):code_end].strip()
            if validResponse(result):
                return result
        code_start = generated_text.find("```python")
        code_end = generated_text.find("```", code_start + 1)
        if code_start != -1 and code_end != -1:
            result =  generated_text[code_start + len("```python"):code_end].strip()
            if validResponse(result):
                return result
        return generated_text.strip()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return "I'm sorry, but I couldn't process your request at this time."

# Function to check if the bot's name was mentioned
def listen_for_bot_name():
    while True:
        command = listen_for_command()  # Listen for the command
        if "stop" in command.lower():
            speak("Goodbye! Mehanth")
            return
        if command and BOT_NAME.lower() in command.lower():  # Check if the bot's name is mentioned
            process_command(command)  # Process any further command after bot's name is detected

# Process Commands
def process_command(command):
    generated_code = generate_response(command)

    if generated_code:
        print("Executing the generated code..." + generated_code)
        execute_function(generated_code)


# listen_for_bot_name()
# Function to execute the generated code
def execute_function(generated_code):
    try:
        # Define the global namespace for `exec` to access the functions
        global_namespace = globals()
        exec(generated_code, global_namespace)
    except Exception as e:
        print("Error executing code:", e)


listen_for_bot_name()