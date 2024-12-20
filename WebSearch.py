import re
import pyautogui
import time
from googlesearch import search
from voice import speak
import wikipediaapi, requests
from API_KEY import API_TOKEN

repo_id = "Qwen/Qwen2.5-Coder-32B-Instruct"

def web_search(query, type):
    print(f"Searching for: {query}")
    try:
        for result in search(query, num=10):
            print(result)
            if "spotify" in result and "song" in type:
                return result
            if ("youtube" in result or "instagram" in result or "facebook" in result or "smule" in result) and "play" in type:
                return result
    except Exception as e:
        print(f"Error occurred while searching: {e}")
        return None

def play(link):
    pyautogui.press("win")  # Press the Windows key to open the Start menu
    time.sleep(1)  # Wait for the browser to open
    pyautogui.typewrite(link)  # Type 'chrome' to open Google Chrome (or your browser of choice)
    time.sleep(1)  # Wait for the browser to open
    pyautogui.press("enter")  # Press Enter to open the browser
    time.sleep(3)  # Wait for the browser to open

    # List of images to search for
    icon_paths = ["playbuttonspotify.png"]  # Add paths to all images you want to search for
    
    # Track the start time
    start_time = time.time()

    # Run the while loop for 10 seconds
    while time.time() - start_time < 30:
        for icon_path in icon_paths:
            try:
                # Locate the app icon on the screen
                icon_location = pyautogui.locateOnScreen(icon_path, confidence=0.9)  # Adjust confidence if needed
                
                if icon_location:
                    # Get the center coordinates of the icon
                    x, y = pyautogui.center(icon_location)
                    pyautogui.click(x, y)  # Click the icon
                    print(f"Clicked on icon '{icon_path}' at: ({x}, {y})")
                    return  # Exit the loop once an icon is clicked
            except Exception as error:
                print(f"Error locating app icon '{icon_path}': {error}")
        
        # Wait for a moment before searching again
        time.sleep(1)
def search_wikipedia(query):
    try:
       # Set a custom user-agent
        user_agent = 'MyBot/1.0 (mehanth362@gmail.com)'  # Replace with your details
        
        # Use requests to set the headers with the user-agent
        wiki = wikipediaapi.Wikipedia(user_agent, 'en')
        page = wiki.page(query)

        if page.exists():
            print(f"Title: {page.title}")
            print(f"Summary: {page.summary[:500]}")  # Show first 500 characters of the summary
            return page.summary
        else:
            print("No page found.")
            return "No results found."
   
    except Exception as e:
        # Catch any other general exceptions
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred. Please try again."
    
def search_duckduckgo(query):
    # Define the full API URL
    API_URL = "https://api-inference.huggingface.co/models/" + repo_id

    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    data = {
        "inputs": query,
        "parameters": {"max_new_tokens": 250},
        "task": "text-generation"
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        # Extract and clean up the response
        generated_text = response.json()[0]["generated_text"][len(query):]
        return generated_text
    else:
        print(f"Error {response.status_code}: {response.text}")
        return "I'm sorry, but I couldn't process your request at this time."
    
def extract_function_call(response_text):
    functions = ["generateCode", "playOnline", "playSong", "search_and_open_file", 
                 "chatWithBot", "send_whatsapp_message", "searchYouTubeAndPlay", "splitScreen"]
    
    # Create a regular expression to match any of the function calls
    function_regex = r'(\w+)\s*\((.*?)\)'
    
    # Search for function calls in the response_text
    matches = re.findall(function_regex, response_text)
    
    # Filter out the matches to only include the functions from the list
    valid_matches = [match for match in matches if match[0] in functions]
    
    if valid_matches:
        # Return the first valid function call
        return True
    else:
        return False
    
def playSong(prompt):
    link = web_search(prompt, "song")
    print(link)
    if link:
        play(link)

def playOnline(prompt):
    link = web_search(prompt, "play")
    if link:
        play(link)

def chatWithBot(query):
    result = search_duckduckgo(query)
    print(result)
    speak(result)
    return result