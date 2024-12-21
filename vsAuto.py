import sys
import pyautogui
import subprocess
import time
import os
from systemControl import open_chatgpt_and_ask

# Step 1: Open VSCode
def open_vscode():
    # Open VSCode using subprocess
    subprocess.run(['code', '.'])
    time.sleep(2)  # Wait for VSCode to open

# Step 2: Create a new folder
def create_new_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)
    print(f"Folder {folder_name} created")

# Step 3: Open the new folder in VSCode
def open_in_vscode(folder_name):
    subprocess.run(['code', folder_name])
    time.sleep(2)  # Wait for the folder to open in VSCode

# Step 4: Create a new file in VSCode
def create_new_file(folder_name, filename):
    file_path = os.path.join(folder_name, filename)
    if os.path.exists(file_path):
        print(f"File {filename} already exists")
        open_in_vscode(file_path)
        return
    pyautogui.hotkey('ctrl', 'alt', 'win', 'n')  # Create new file
    pyautogui.write(filename)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

# Step 5: Ask ChatGPT (in this case, the code is predefined) and paste code
def paste_code_in_file(code):
    pyautogui.hotkey('ctrl', 'a')  # Paste clipboard contents
    pyautogui.hotkey('ctrl', 'v')  # Paste clipboard contents
    time.sleep(1)

# Step 6: Open the terminal and run the file
def run_in_terminal(command):
    pyautogui.hotkey('ctrl', '`')  # Open integrated terminal
    time.sleep(1)
    pyautogui.write(command)  # Command to run Python file (adjust for other languages)
    pyautogui.press('enter')
    time.sleep(2)

# Main function to automate the entire process
def automate_development_process(query):
    folder_name = 'C:\\VsAuto\\text_reader'
    file_name = 'main.py'

    code = open_chatgpt_and_ask(query, True)

    # Create and open folder
    create_new_folder(folder_name)
    open_in_vscode(folder_name)
    
    # Create new file and paste code
    create_new_file(folder_name, file_name)
    paste_code_in_file(code)

    # Run code in terminal
    run_in_terminal('python3 main.py')

