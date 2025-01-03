import time
import pyautogui
import cv2
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
from selenium.webdriver.chrome.service import Service
from systemControl import openWebDriver, driver
from geopy.geocoders import Nominatim
import geocoder
from selenium.webdriver.common.action_chains import ActionChains


# Function to take a screenshot
def capture_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')
    return 'screenshot.png'

# Function to capture an image from the camera
def capture_camera_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        image_path = 'camera_image.jpg'
        cv2.imwrite(image_path, frame)
        cap.release()
        return image_path
    else:
        cap.release()
        return None

# Function to send image on WhatsApp using Selenium
def send_camera_image_on_whatsapp():
    image_path = capture_camera_image()

    driver = openWebDriver()
  
    # Find the attach button and click it
    attach_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[4]/div/footer/div[1]/div/span/div/div[1]/div/button/span")
    attach_button.click()

    # Wait for attach menu to appear
    time.sleep(2)

    # Find and click the "Gallery" option
    gallery_option = driver.find_element(By.XPATH, "//input[@type='file']")
    gallery_option.send_keys(os.path.abspath(image_path))  # Send the image path

    # Wait for the image to load and click send
    time.sleep(2)
    send_button = driver.find_element(By.XPATH, "//span[@data-icon='send']")
    send_button.click()

    print(f"Image sent.")


# Function to send image on WhatsApp using Selenium
def send_screenshot_on_whatsapp():
    image_path = capture_screenshot()

    driver = openWebDriver()
 
    # Find the attach button and click it
    attach_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[4]/div/footer/div[1]/div/span/div/div[1]/div/button/span")
    attach_button.click()

    # Wait for attach menu to appear
    time.sleep(2)

    # Find and click the "Gallery" option
    gallery_option = driver.find_element(By.XPATH, "//input[@type='file']")
    gallery_option.send_keys(os.path.abspath(image_path))  # Send the image path

    # Wait for the image to load and click send
    time.sleep(2)
    send_button = driver.find_element(By.XPATH, "//span[@data-icon='send']")
    send_button.click()

    print(f"Image sent.")

# Function to get the current coordinates
def get_location():
    g = geocoder.ip('me')  # This gets the current IP-based location
    if g.latlng:  # Check if coordinates are found
        lat, lon = g.latlng
        print(f"Location found: Latitude={lat}, Longitude={lon}")
        return lat, lon
    else:
        print("Location not found.")
        return None, None

