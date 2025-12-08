import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from voice import speak
from voice_commands import listen_for_bot_name
from systemControl import driver,openWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def monitor_whatsapp_group(group_name):
    driver = openWebDriver()
    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com")
    print("Scan the QR code to log in.")

    # Load cookies if available
    try:
        cookies = pickle.load(open("whatsapp_cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(120)
    except FileNotFoundError:
        print("No cookies found. Please log in first and save the cookies.")

    # Save cookies after login
    pickle.dump(driver.get_cookies(), open("whatsapp_cookies.pkl", "wb"))

    # Search and open the group
    try:
        # Click on the search bar
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true" and @role="textbox"]')
        search_box.click()
        time.sleep(1)

        # Enter the group name
        search_box.send_keys(group_name)
        time.sleep(2)  # Wait for search results to load

        # Click on the group name in the search results
        group = driver.find_element(By.XPATH, f"//span[@title='{group_name}']")
        group.click()
        print(f"Opened group: {group_name}")
    except Exception as e:
        print(f"Error opening group: {e}")
        driver.quit()
        return

    # Monitor the group for new messages
    last_message = None
    print("Monitoring messages...")
    try:
        while True:
            # Find all messages in the group
            messages = driver.find_elements(By.XPATH, "//span[contains(@class, 'selectable-text')]//span")
            if messages:
                # Get the last message text
                new_message = messages[-1].text
                if new_message != last_message:
                    print(f"New message: {new_message}")
                    speak(f"you said! {new_message}")
                    # Call the voice command listener to detect the bot's name
                    listen_for_bot_name(new_message)
                    last_message = new_message
                    
            time.sleep(1)  # Polling interval
    except KeyboardInterrupt:
        print("Stopping monitoring...")
    finally:
        driver.quit()

# Specify the group name
group_name = "My Assistant"  # Replace with your group name
monitor_whatsapp_group(group_name)
