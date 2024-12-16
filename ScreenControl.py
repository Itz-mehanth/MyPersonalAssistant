import pyautogui
import time

def search_youtube():
    pyautogui.press("win")  # Press the Windows key to open the Start menu # Wait for the browser to open
    pyautogui.typewrite("https://www.youtube.com")  # Type the YouTube URL
    pyautogui.press("enter")  # Press Enter to go to YouTube
    time.sleep(5)  # Wait for YouTube to load
    pyautogui.press("tab")  # Press Tab to go to search
    pyautogui.press("tab")  # Press Tab to go to search
    pyautogui.press("tab")  # Press Tab to go to search
    pyautogui.press("tab")  # Press Tab to go to search
    pyautogui.typewrite("Parithanbangal")  # Type 'Parithanbangal' in the search bar
    pyautogui.press("enter")  # Press Enter to search

# Run the function
search_youtube()
