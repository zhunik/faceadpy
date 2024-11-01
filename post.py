from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json
import os


# Load configuration from a JSON file
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)


def post_to_facebook(account):
    # Set up Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Open browser in full screen
    # Disable notifications
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
    # options.add_argument("--headless")  # Uncomment to run in headless mode

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Navigate to Facebook
        driver.get("https://www.facebook.com")
        sleep(3)

        # Log in
        driver.find_element(By.ID, "email").send_keys(account["username"])
        driver.find_element(By.ID, "pass").send_keys(account["password"])
        driver.find_element(By.NAME, "login").click()
        sleep(10)

        # # Navigate to the group or profile page
        for group_url in account["groups"]:
            driver.get(group_url)
            sleep(5)

            # Create a new post
            # post_box = driver.find_element(By.XPATH, "//*[contains(text(), 'Що у вас на думці,')]")
            post_box = driver.find_element(By.XPATH, "//*[contains(text(), 'Напишіть щось...')]")
            post_box.click()
            sleep(5)

            # Enter post text
            post_input = driver.find_element(By.CSS_SELECTOR, "[aria-label='Створіть публічний допис…']")
            post_input.send_keys(account["post"]["text"])
            sleep(2)

            # Upload an image
            image_button = driver.find_element(By.CSS_SELECTOR, "[aria-label='Світлина/відео']")
            image_button.click()
            sleep(2)
            upload_image = driver.find_element(By.XPATH, "//input[@multiple='']")
            image_path = os.path.abspath(account["post"]["imagePath"]) 

            upload_image.send_keys(image_path)
            sleep(2)

            # Publish the post
            publish_button = driver.find_element(By.CSS_SELECTOR, "[aria-label='Опублікувати']")
            publish_button.click()
            sleep(5)

        profile_button = driver.find_element(By.CSS_SELECTOR, "[aria-label='Ваш профіль']")
        profile_button.click()
        sleep(2)

        exit_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Вийти')]")
        exit_button.click()
        sleep(4)

    finally:
        driver.quit()


# Iterate through accounts in the config file and post for each one
for account in config["accounts"]:
    print(f"Posting for account {account['username']}")
    post_to_facebook(account)
    print(f"Post successful for account {account['username']}")
