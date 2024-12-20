import os
import re
from ChatTTS import ChatTTS
import speech_recognition as sr
import pyttsx3
import sounddevice as sd
from bark import generate_audio
import requests
from transformers import pipeline
import time
from google.cloud import texttospeech
from huggingface_hub import InferenceClient
import threading
from PIL import Image
import scipy.io.wavfile as wav
import mss
import torch
import scipy
from pydub import AudioSegment
from io import BytesIO
import torchaudio
import pygame
import scipy.io.wavfile as wav
import sqlite3
import whisper
from transformers import AutoProcessor, AutoModel
import pyaudio
from voice import speak
import numpy as np
from generateCode import generateCode
from WebSearch import playOnline, playSong, chatWithBot
from systemControl import search_and_open_file, send_whatsapp_message, searchYouTubeAndPlay, splitScreen, control_brightness, control_volume, analyze_windows_with_query
from API_KEY import API_TOKEN
import logging

AI_status = False

def start_ai():
    global AI_status
    AI_status = True

def stop_ai():
    global AI_status
    AI_status = False

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


repo_id = "meta-llama/Llama-3.3-70B-Instruct"
repo_id = "openai-community/gpt2"
repo_id = "Qwen/QwQ-32B-Preview"
repo_id = "Qwen/Qwen2.5-Coder-32B-Instruct"

# Set the bot's name
BOT_NAME = "Google"

# Set your ElevenLabs API key
API_KEY = "sk_10bd287e4ce3f9f6af6bc73dff5150d2d840e66ddf108438"
VOICE_ID = "bIHbv24MWmeRgasZH58o"  # You can find the voice ID in your ElevenLabs dashboard

def listen_for_command(silence_duration = 5):
    model = whisper.load_model("base")
    while True:
        try:
            """Capture microphone input and transcribe it using Whisper."""
            chunk = 512  # Buffer size
            format = pyaudio.paInt16  # Audio format
            channels = 1  # Mono audio
            rate = 16000  # Sampling rate

            p = pyaudio.PyAudio()
            stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

            speak("Listening...")
            frames = []

            silent_frames = 0
            max_silent_frames = int(16000 * silence_duration / 1024)
            # Record audio in chunks for the given duration
            while True:
                data = stream.read(chunk)
                # Convert to numpy array of int16 values
                data_array = np.frombuffer(data, dtype=np.int16)
                rms = np.sqrt(np.mean(data_array**2))
                print(f"RMS: {rms}")
                if rms < 12:
                    silent_frames += 1
                    print("silent_frames count" + str(silent_frames))
                else: 
                    silent_frames = 0
                frames.append(np.frombuffer(data, dtype=np.int16))
                if silent_frames >= max_silent_frames:
                    break

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
            # return result["text"]
            # voiceCommand = input("Enter your command: ")
            return  result["text"]
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
        "description": "Searches for a file in the system inside a specific folder and just opens it not for deletion and other operations.",
        "parameters": ["search_path", "file_name"],
        "example": 'search_and_open_file("C:\\Users\\mehan\\Downloads","project_report.pdf")',
    },
    "chatWithBot": {
        "module": "chatBot",
        "description": "Acts as a chatbot to answer the user's questions and doubts in natural language.",
        "parameters": ["user_query"],
        "example": 'chatWithBot("What is the capital of France?")',
    },
    "send_whatsapp_message": {
        "module": "systemControl",
        "description": "Opens WhatsApp, searches for a contact, types the message, and sends it automatically.",
        "parameters": ["contact_name", "message"],
        "example": 'send_whatsapp_message("John Doe", "Hello, how are you?")',
    },
    "searchYouTubeAndPlay": {
        "module": "WebSearch",
        "description": "Opens YouTube in a browser, searches for a video based on a query, and plays it.",
        "parameters": ["query"],
        "example": 'searchYouTubeAndPlay("Parithanbangal")',
    },
     "splitScreen": {
        "module": "systemControl",
        "description": "Splits the screen into four sections and arranges specified windows in the top-left, top-right, bottom-left, and bottom-right positions. Also call this function if seen a keyword 'Game on'",
        "parameters": ["windows_titles"],
        "example": 'splitScreen(["YouTube", "Chrome", "Spotify", "VS Code"])',
    },
    "control_brightness": {
        "module": "systemControl",
        "description": "Controls the screen brightness based on the provided brightness value.",
        "parameters": ["brightness"],
        "example": 'control_brightness(50)',  # Set brightness to 50%
    },
    "control_volume": {
        "module": "systemControl",
        "description": "Controls the system volume based on the provided volume level.",
        "parameters": ["volume"],
        "example": 'control_volume(70)',  # Set volume to 70%
    },
    "analyze_windows_with_query": {
        "module": "systemControl",
        "description": "Analyzes all open windows, extracts text content using OCR, and sends the details along with a user-provided query to the LLM for insights.",
        "parameters": ["query"],
        "example": 'analyze_windows_with_query("What errors are visible on the current windows?")',
    },
}

    
def extract_function_call(response_text):
    functions = ["generateCode", "playOnline", "playSong", "search_and_open_file", 
                 "chatWithBot", "send_whatsapp_message", "searchYouTubeAndPlay", 
                 "splitScreen", "control_volume", "control_brightness", "analyze_windows_with_query"]
    
    # Create a regular expression to match any of the function calls
    function_regex = r'(\w+)\s*\((.*?)\)'
    
    # Search for function calls in the response_text
    matches = re.findall(function_regex, response_text)
    
    # Filter out the matches to only include the functions from the list
    valid_matches = [match for match in matches if match[0] in functions]
    
    if valid_matches:
        # Return all valid function calls
        return '\n'.join([f"{match[0]}({match[1]})" for match in valid_matches])
    else:
        return None
    
# Function to generate a response using Hugging Face's GPT-2 API
def generate_response(prompt):
    # Define the full API URL
    API_URL = "https://api-inference.huggingface.co/models/" + repo_id

    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    # Fine-tune the prompt to include the AI's role and identity
    enhanced_prompt = (
        f"You are a programming assistant named {BOT_NAME}. Your job is to generate Python code based on the user's query.\n"
        "The user will provide a natural language query, and you must decide which function to call from the following options:\n"
        f"{list(FUNCTIONS.keys())}.\n"
        f"Each function and its parameters are: {FUNCTIONS}.\n"
        'Respond with a Python code snippet that contains the function call, and make sure to include all required arguments. place the code inside triple quotes for example triple quotes(""")function("query")triple quotes(""")\n'
        "If need multiple function calls for a query give me all of them"
        "If no information could be gathered from the query return empty string"
        "Here is the user's query:\n"
        f"{prompt}"
    )

    data = {
        "inputs": enhanced_prompt,
        "parameters": {"max_new_tokens": 250},
        "task": "text-generation"
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        # Extract and clean up the response
        generated_text = response.json()[0]["generated_text"][len(enhanced_prompt):]
        print("Generated Response:", generated_text)
        # Extract the code block (if applicable)
        
        return extract_function_call(generated_text)
    else:
        print(f"Error {response.status_code}: {response.text}")
        return "I'm sorry, but I couldn't process your request at this time."

# Function to check if the bot's name was mentioned
def listen_for_bot_name():
    speak("Welcome! How can i help you?")
    while True:
        # command = listen_for_command()  # Listen for the command
        command = input("Enter command: ")
        if "stop" in command.lower():
            stop_ai()
            speak("Goodbye! Mehanth")
            return
        if command and (BOT_NAME.lower() in command.lower() or AI_status):  # Check if the bot's name is mentioned
            start_ai()
            process_command(command)  # Process any further command after bot's name is detected

# Process Commands
def process_command(command):
    generated_code = generate_response(command)

    if generated_code:
        # print("Executing the generated code..." + generated_code)
        execute_function(generated_code)
    else:
        speak(generated_code)


# listen_for_bot_name()
# Function to execute the generated code
def execute_function(generated_code):
    try:
        # Define the global namespace for `exec` to access the functions
        global_namespace = globals()
        print("Executing...\n " + generated_code)
        result = exec(generated_code, global_namespace)
        speak(result)
    except Exception as e:
        print("Error executing code:", e)


listen_for_bot_name()