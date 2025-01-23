"""Parses website for new events."""

import asyncio
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from pyvirtualdisplay import Display

from tg import send_message_to_channel


async def parse_tollabda():
    print("Starting parse_tollabda...")

    display = Display(visible=0, size=(800, 800))  
    display.start()

    # Check if the current version of chromedriver exists
    # and if it doesn't exist, download it automatically,
    # then add chromedriver to path
    chromedriver_autoinstaller.install()

    chrome_options = webdriver.ChromeOptions()    

    options = [
        "--window-size=1200,1200",
        "--ignore-certificate-errors",
        "--headless",  # Run in headless mode for CI
        "--no-sandbox",  # Required for running in Docker/CI
        "--disable-dev-shm-usage",  # Overcome limited resource problems
        "--disable-gpu",  # Disable GPU hardware acceleration
        f"--user-data-dir=/tmp/chrome-data-{time.time()}"  # Use unique data directory
    ]

    for option in options:
        chrome_options.add_argument(option)

    # Add these additional preferences
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://tollabda.hu/Calendar")
    _, button_forward = driver.find_elements(By.CLASS_NAME, 'monthNavigate')
    button_forward.click()
    
    time.sleep(5)
    
    if 'KEZDŐ' in driver.page_source or 'EDZÉS' in driver.page_source:
        print('Found events')
        await send_message_to_channel('New events on tollabda.hu found')
    else:
        print('Nothing found')
    
    # Close the browser
    driver.quit()


if __name__=="__main__":
    asyncio.run(parse_tollabda())
