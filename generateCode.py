# from voice_commands import BOT_NAME
import requests
import re
import os
import subprocess
import time
import pyautogui
from API_KEY import API_TOKEN


def extract_code(text):
    # Regular expression to match code inside triple quotes
    pattern = r'```python(.*?)```'
    
    # Find all occurrences of the pattern
    matches = re.findall(pattern, text, re.DOTALL)

    if not matches:
        pattern = r'[code](.*?)[/code]'
        matches = re.findall(pattern, text, re.DOTALL)
    
    return matches

BOT_NAME = 'Siri'

def generateCode(prompt):
    repo_id = "openai-community/gpt2"
    repo_id = "Qwen/QwQ-32B-Preview"

    # Define the full API URL
    API_URL = "https://api-inference.huggingface.co/models/" + repo_id

    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    # Fine-tune the prompt to include the AI's role, identity, and clear instructions
    enhanced_prompt = (
        f"You are a powerful AI coding assistant named {BOT_NAME}. Your task is to generate Python scripts based on user queries. "
        f"Always provide Python code within square brackets [ ] without any additional comments, explanations, or text outside the brackets. "
        f"Ensure the code is syntactically correct and ready to execute.\n\n"
        f"- User files location: C:\\Users\\mehan\n"
        f"Important libraries available for use:\n"
        f"- pyautogui (for keyboard and mouse automation)\n"
        f"- time (for delays and timing operations)\n"
        f"- os (for file system operations)\n"
        f"- subprocess (for process handling)\n\n"
        f"Sample code: def search_youtube(): pyautogui.press(\"win\")  # Press the Windows key to open the Start menu pyautogui.typewrite(\"chrome\")  # Type 'chrome' to open Google Chrome (or your browser of choice) pyautogui.press(\"enter\")  # Press Enter to open the browser time.sleep(2)  # Wait for the browser to open pyautogui.typewrite(\"https://www.youtube.com\")  # Type the YouTube URL pyautogui.press(\"enter\")  # Press Enter to go to YouTube time.sleep(3)  # Wait for YouTube to load pyautogui.click(x=500, y=150)  # Click on the YouTube search bar (adjust the coordinates if needed) pyautogui.typewrite(\"Parithanbangal\")  # Type 'Parithanbangal' in the search bar pyautogui.press(\"enter\")  # Press Enter to search"
        f"Here is my request:\n"
        f"Generate Python code to {prompt} using the pyautogui library and the win key to search for the results or any application to automate the process of performing the operation on my laptop."
    )
                
    data = {
        "inputs": enhanced_prompt,
        "parameters": {"max_new_tokens": 350},
        "task": "text-generation"
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        print("Response:", response.json()[0]["generated_text"].strip()[len(enhanced_prompt):])
        # Extract the code from the generated response
        code = extract_code(response.json()[0]["generated_text"].strip()[len(enhanced_prompt):])
        print(code)
        if code:
            print(code[0])
            exec(code[0])
        # Return the generated response text
        return response.json()[0]["generated_text"].strip()[len(enhanced_prompt):]
    else:
        print(f"Error {response.status_code}: {response.text}")
        return "I'm sorry, but I couldn't process your request at this time."
    