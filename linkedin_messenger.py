import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def send_linkedin_message(linkedin_url, name, sector):
    message = f"""
Hi {name},

It was great speaking earlier. As someone working in {sector}, I believe the 2026 Intercontinental Commodity Exchange in Dubai could be a great strategic opportunity for you.

Happy to connect!

– Vijayendra
""".strip()

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)

    try:
        # Step 1: Login
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        driver.find_element(By.ID, "username").send_keys(EMAIL)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        time.sleep(3)

        # Step 2: Visit profile
        driver.get(linkedin_url)
        time.sleep(4)

        sent = False

        # Step 3: Try Connect
        try:
            connect_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Connect')]")
            connect_button.click()
            time.sleep(2)
            driver.find_element(By.XPATH, "//button[contains(text(), 'Add a note')]").click()
            time.sleep(1)
            textarea = driver.find_element(By.TAG_NAME, "textarea")
            textarea.send_keys(message)
            driver.find_element(By.XPATH, "//button[contains(text(), 'Send')]").click()
            print(f"✅ LinkedIn connect + note sent to {name}")
            sent = True

        except:
            # Step 4: If Connect fails, try Message
            try:
                message_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Message')]")
                message_button.click()
                time.sleep(2)
                message_box = driver.find_element(By.XPATH, "//div[contains(@class, 'msg-form__contenteditable')]")
                message_box.send_keys(message)
                message_box.send_keys(Keys.RETURN)
                print(f"✅ LinkedIn message sent to {name} (already connected)")
                sent = True
            except:
                print(f"⚠️ Could not message or connect {name} — may be restricted profile")

        if not sent:
            raise Exception("Neither Connect nor Message options were available.")

    except Exception as e:
        print(f"❌ Error sending to {name}: {e}")
    finally:
        driver.quit()
