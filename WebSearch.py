import pyautogui
import time
from googlesearch import search
import wikipediaapi

def web_search(query, type):
    print(f"Searching for: {query}")
    for result in search(query, num_results=10):
        print(result)
        if "spotify" in result and "song" in type:
            return result
        if ("youtube" in result or "instagram" in result or "facebook" in result or "smule" in result) and "play" in type:
            return result

def play(link):
    pyautogui.press("win")  # Press the Windows key to open the Start menu
    time.sleep(1)  # Wait for the browser to open
    pyautogui.typewrite(link)  # Type 'chrome' to open Google Chrome (or your browser of choice)
    pyautogui.press("enter")  # Press Enter to open the browser
    time.sleep(3)  # Wait for the browser to open

    # List of images to search for
    icon_paths = ["playbuttonspotify.png"]  # Add paths to all images you want to search for
    
    # Track the start time
    start_time = time.time()

    # Run the while loop for 10 seconds
    while time.time() - start_time < 20:
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
        wiki = wikipediaapi.Wikipedia('en')  # 'en' for English Wikipedia
        page = wiki.page(query)

        if page.exists():
            print(f"Title: {page.title}")
            print(f"Summary: {page.summary[:500]}")  # Show first 500 characters of the summary
            return page.summary
        else:
            print("No page found.")
            return "No results found."
    except wikipediaapi.WikipediaException as e:
        # Handle specific Wikipedia API exceptions
        print(f"Error accessing Wikipedia: {e}")
        return "There was an error accessing Wikipedia. Please try again."
    except Exception as e:
        # Catch any other general exceptions
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred. Please try again."

def playSong(prompt):
    link = web_search(prompt, "song")
    if link:
        play(link)

def playOnline(prompt):
    link = web_search(prompt, "play")
    if link:
        play(link)

def chatWithBot(query):
    print(result)
    result = search_wikipedia(query)
    return result