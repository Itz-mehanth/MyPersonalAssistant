import os
import re
import subprocess
import pyautogui
import ctypes
import pyperclip
import requests
from API_KEY import API_TOKEN
from comtypes import CoInitializeEx, COINIT_APARTMENTTHREADED
from voice import speak
# Initialize COM in the apartment-threaded model
ctypes.windll.ole32.CoInitializeEx(0, COINIT_APARTMENTTHREADED)
from generateCode import BOT_NAME
import screen_brightness_control as sbc
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pywinauto.application import Application
import pygetwindow as gw
import time
from PIL import ImageGrab
import pytesseract
from transformers import pipeline
from WebSearch import playSong
import webbrowser

def control_brightness(brightness: int):
    """
    Controls the screen brightness.
    Args:
        brightness (int): The brightness value (0 to 100).
    """
    try:
        # Set the screen brightness (0 to 100 scale)
        sbc.set_brightness(brightness)
        print(f"Brightness set to {brightness}%")
    except Exception as e:
        print(f"Error occurred while setting brightness: {e}")

def control_volume(volume: int):
    try:
        # Get the default audio output device (speakers)
        devices = AudioUtilities.GetSpeakers()
        
        # Activate the IAudioEndpointVolume interface
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        volume_control = interface.QueryInterface(IAudioEndpointVolume)

        # Ensure the volume level is within the valid range (0 to 100)
        volume = max(0, min(volume, 100))

        # Set the volume level (0.0 to 1.0 scale)
        volume_control.SetMasterVolumeLevelScalar(volume / 100.0, None)
        print(f"Volume set to {volume}%")
    except Exception as e:
        print(f"Error occurred while setting volume: {e}")


def search_and_open_file(search_path, file_name_substring):
    video_audio_extensions = ['.mp4', '.mkv', '.avi', '.mp3', '.wav', '.flac', '.aac']  # Supported media formats
    vlc_path = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"

    print(f"Searching for files containing '{file_name_substring}' in '{search_path}'...")
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file_name_substring.lower() in file.lower():  # Case-insensitive substring match
                file_path = os.path.join(root, file)
                print(f"File found: {file_path}")
                try:
                    # Check if the file is a video or audio file
                    if any(file.lower().endswith(ext) for ext in video_audio_extensions):
                        # Open in VLC media player
                        subprocess.Popen([vlc_path, file_path])
                        return f"Media file opened in VLC: {file_path}"
                    else:
                        # Open non-media file with default program
                        subprocess.Popen(["start", file_path], shell=True)
                        return f"File opened: {file_path}"
                except Exception as e:
                    return f"Error opening file: {e}"
    return f"No file containing '{file_name_substring}' found in '{search_path}'."

def send_whatsapp_message(contact_name, message):
    # Open Start menu and search for WhatsApp
    pyautogui.press("win")  # Press the Windows key
    time.sleep(1)  # Wait for the Start menu to appear
    pyautogui.typewrite("WhatsApp")  # Type "WhatsApp" to search for the app
    pyautogui.press("enter")  # Press Enter to open WhatsApp
    time.sleep(5)  # Wait for WhatsApp to load

    # Focus on the search bar to find the contact
    pyautogui.hotkey("ctrl", "f")  # Open search bar
    time.sleep(1)  # Wait for the search bar to appear
    pyautogui.typewrite(contact_name)  # Type the contact's name
    pyautogui.press("tab")  # Press Enter to search for the contact
    time.sleep(1)  # Wait for the contact to appear
    pyautogui.press("enter")  # Select the contact

    # Type the message in the message box
    time.sleep(1)  # Wait for the contact to appear
    pyautogui.typewrite(message)  # Type the message
    time.sleep(0.5)  # Wait for the contact to appear
    pyautogui.press("enter")  # Send the message

def getYoutubeTabPos():
    # List all open windows
    all_windows = gw.getAllTitles()

    # Find the YouTube window (replace "YouTube" with the actual title of the tab)
    youtube_window = None
    for window in gw.getAllWindows():
        if "YouTube" in window.title:  # Adjust if needed to match your YouTube tab title
            youtube_window = window
            break

    if youtube_window:
        # Get the window's geometry
        left = youtube_window.left
        top = youtube_window.top
        right = youtube_window.left + youtube_window.width

        # Print X coordinates
        xPos = (left + right) // 4
        yPos = top + 290

        return xPos, yPos
    else:
        print("YouTube tab not found.")

def getChatgptTabPos():
    # List all open windows
    all_windows = gw.getAllTitles()

    # Find the ChatGPT window (replace "ChatGPT" with the actual title of the tab)
    chatgpt_window = None
    for window in gw.getAllWindows():
        if "ChatGPT" in window.title:  # Adjust if needed to match your ChatGPT tab title
            chatgpt_window = window
            break

    if chatgpt_window:
        # Get the window's center
        center = chatgpt_window.center  # This returns a tuple (x, y)
        return center
    else:
        print("ChatGPT tab not found.")
        return None

def searchYouTubeAndPlay(query):
    # Open YouTube in the default web browser
    webbrowser.open("https://www.youtube.com")
    time.sleep(5)  # Wait for YouTube to load
    
    # Navigate to the search bar and perform the search
    pyautogui.press("/")  # Tab to focus on the search bar
    time.sleep(0.5)  # Small delay for the search bar to focus
    pyautogui.typewrite(query)  # Type the search query
    pyautogui.press("enter")  # Press Enter to search
    time.sleep(5)  # Wait for search results to load
    
    # Open the first video result
    x, y = getYoutubeTabPos()
    pyautogui.moveTo(x, y)  # Adjust the X, Y coordinates as needed
    time.sleep(1)  # Pause briefly
    pyautogui.click()  # Click on the first video
    time.sleep(2)  # Pause briefly
    pyautogui.press('f')  # Play the video


def splitScreen(window_names):
    window_names = ["Youtube", "Chatgpt", "Spotify", "VSCode"]
    # Ensure we have exactly 4 window names
    print("It game time...")

    song_name = "EP MONTAGEM VOZES PROFUNDAS (Remixes) DJ MAXZZ . DJ JL3 DAZN . DJ CD"


    def snap_window_left():
        pyautogui.hotkey('win', 'left')  # Windows key + Left arrow

    def snap_window_right():
        pyautogui.hotkey('win', 'right')  # Windows key + Right arrow

    def maximize_window():
        pyautogui.hotkey('win', 'up')  # Windows key + Up arrow

    def minimize_window():
        pyautogui.hotkey('win', 'down')  # Windows key + Down arrow

    def restore_window():
        pyautogui.hotkey('win', 'down')  # Windows key + Down arrow (restores maximized window)
        
    if len(window_names) != 4:
        print("Please provide exactly 4 window names.")
        return


    # Launch applications and arrange them
    for i, window_name in enumerate(window_names):
        if window_name.lower() == "youtube":
            app = Application().start(r"C:\Program Files\Google\Chrome\Application\chrome.exe --new-window https://www.youtube.com")
        elif window_name.lower() == "chatgpt":
            app = Application().start(r"C:\Program Files\Google\Chrome\Application\chrome.exe --new-window https://www.chatgpt.com")
        elif window_name.lower() == "spotify":
            playSong("Play song in spotify named " + song_name)
            # app = Application().start(r"C:\Program Files\Google\Chrome\Application\chrome.exe --new-window https://www.spotify.com")
        elif window_name.lower() == "vscode":
            app = Application().start(r"C:\Users\mehan\AppData\Local\Programs\Microsoft VS Code\code.exe --new-window")
        else:
            print(f"Unsupported application: {window_name}")
            continue


        time.sleep(1)  # Wait for the application to launch

        # Set the position and size based on index
        if i == 0:
            snap_window_left()
            maximize_window()
        elif i == 1:
            snap_window_right()
            maximize_window()
        elif i == 2:
            snap_window_left()
            minimize_window()
        elif i == 3:
            snap_window_right()
            minimize_window()

def getInference(query):
    repo_id = "Qwen/QwQ-32B-Preview"

    # Define the full API URL
    API_URL = "https://api-inference.huggingface.co/models/" + repo_id

    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
                
    data = {
        "inputs": query,
        "parameters": {"max_new_tokens": 500},
        "task": "text-generation"
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        # print("window details: ", response.json()[0]["generated_text"])
        # Extract the code from the generated response

        return response.json()[0]
    else:
        print(f"Error {response.status_code}: {response.text}")
        return "I'm sorry, but I couldn't process your request at this time."
    
def analyze_windows_with_query(query):
    print("Scanning windows...")
    open_windows = gw.getAllWindows()
    if not open_windows:
        print("No windows found!")
        return
    
    # To keep track of processed window positions
    processed_positions = set()
    combined_details = "Analyzed Windows:\n"

    for window in open_windows:
        # Filter out duplicate window positions
        position_key = (window.left, window.top, window.right, window.bottom)
        if position_key in processed_positions:
            print(f"Skipping duplicate window at position: {position_key}")
            continue

        # Mark the position as processed
        processed_positions.add(position_key)

        # Process the window if it's not minimized or a duplicate
        print(f"Processing window: {window.title}")

        # Step 1: Capture the window's screenshot
        try:
            bbox = (window.left, window.top, window.right, window.bottom)
            screenshot = ImageGrab.grab(bbox)
            screenshot.save(f"windows/{window.title}.png")
            print(f"Screenshot captured for {window.title}")

            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

            # Step 2: Extract text using OCR
            extracted_text = pytesseract.image_to_string(screenshot)
            if not extracted_text.strip():
                print(f"No text found in {window.title}")
                extracted_text = "No significant text detected."

            # Combine details for the final query
            combined_details += f"\nWindow Title: {window.title}\nExtracted Content:\n{extracted_text}\n"

        except Exception as e:
            print(f"Error processing {window.title}: {e}")
            combined_details += f"\nWindow Title: {window.title}\nError: Unable to process this window.\n"

    # Final prompt to the LLM
    final_prompt = (
        "You are a screen analysis assistant. Your job is to analyze the extracted details from different windows\n "
        "and answer the user's query in plain language. Avoid providing code or unnecessary details unless explicitly requested.\n "
        "If the question is about a particular window focus on that window's content\n"
        "Here are the details of the extracted screen content: use this content to answer the query you don't need to perform any coding because the answer lies in the follwing content\n\n"
        f"{combined_details}\n\n"
        "Query: {query}\n\n"
        "Answer concisely in plain text, focusing only on what the user is asking."
    )

    print("final prompt:\n" + final_prompt)
    def clean_text(text, remove_chars="*#"):
        # Escape special characters to make them safe for regex
        escaped_chars = re.escape(remove_chars)
        # Remove the unwanted characters using regex
        cleaned_text = re.sub(f"[{escaped_chars}]", "", text)
        return cleaned_text

    # Replace `getInference` with the function or pipeline for LLM inference
    llm_response = getInference(final_prompt)
    llm_response = clean_text(llm_response["generated_text"][len(final_prompt):])
    print("\nLLM Response:")
    # print(llm_response["generated_text"][len(final_prompt):])
    speak(llm_response)
    return llm_response


def getChatgptTabPos():

    # Find the ChatGPT window (replace "ChatGPT" with the actual title of the tab)
    chatgpt_window = None
    for window in gw.getAllWindows():
        if "ChatGPT" in window.title:  # Adjust if needed to match your ChatGPT tab title
            chatgpt_window = window
            break

    if chatgpt_window:
        # Get the window's center
        center = chatgpt_window.center  # This returns a tuple (x, y)
        return center[0], center[1], chatgpt_window
    else:
        print("ChatGPT tab not found.")
        return None, None, None

def open_chatgpt_and_ask(question, getCode = False):
    # Check if ChatGPT tab is already open
    x, y, chatgpt_window = getChatgptTabPos()

    if chatgpt_window and x > 0 and y > 0:
        # If a ChatGPT window is found, bring it to the front
        # Click on the window to focus the input
        print("window found")
        print(x, y, chatgpt_window)
        pyautogui.click(x, y)
        time.sleep(1)  # Wait a bit to ensure the window is focused
    else:
        # If no ChatGPT window is open, open a new one
        pyautogui.press('win')  # Press the Windows key to open the Start menu
        time.sleep(1)
        pyautogui.typewrite('chatgpt')  # Type the ChatGPT URL
        pyautogui.press('enter')  # Press Enter to go to ChatGPT
        time.sleep(10)  # Wait for ChatGPT to load

        # Find the new ChatGPT window
        x, y, chatgpt_window = getChatgptTabPos()
        pyautogui.click(x, y)
      
        time.sleep(1)

    

    pyautogui.hotkey('shift', 'esc')  # Focus chat input

    # Type the question in ChatGPT's input field
    pyautogui.typewrite(question)
    pyautogui.press('enter')  # Press Enter to send the question
    time.sleep(10)  # Wait for the response

    # Copy the last response
    if getCode:
        pyautogui.hotkey('ctrl', 'shift', ';')  # Copy the last response
    else:
        pyautogui.hotkey('ctrl', 'shift', 'c')  # Copy the last response
    time.sleep(1)  # Wait for the response to be copied

    # Get text from the clipboard
    clipboard_text = pyperclip.paste()

    print("According to ChatGPT: ", clipboard_text)

    return clipboard_text


def close_window_by_title(window_title):
    """Closes a window with a specific title."""
    windows = gw.getAllTitles()
    for title in windows:
        try:
            if re.search(window_title, title, re.IGNORECASE):
                print(f"Closing window: {title}")
                gw.getWindowsWithTitle(title)[0].close()
        except Exception as e:
            print(f"Could not close window '{title}': {e}")


def close_all_windows_except(except_title):
    """Closes all windows except the one with a specific title."""
    windows = gw.getAllTitles()
    for title in windows:
        if re.search(except_title, title, re.IGNORECASE):
            print(f"Closing window: {title}")
            try:
                gw.getWindowsWithTitle(title)[0].close()
            except Exception as e:
                print(f"Could not close window '{title}': {e}")


def close_all_windows():
    """Closes all open windows."""
    windows = gw.getAllTitles()
    for title in windows:
        print(f"Closing window: {title}")
        try:
            gw.getWindowsWithTitle(title)[0].close()
        except Exception as e:
            print(f"Could not close window '{title}': {e}")

