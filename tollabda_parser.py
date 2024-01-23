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
        "--ignore-certificate-errors"

        # More possible options:
        #"--headless",
        #"--disable-gpu",
        #"--window-size=1920,1200",
        #"--ignore-certificate-errors",
        #"--disable-extensions",
        #"--no-sandbox",
        #"--disable-dev-shm-usage",
        #'--remote-debugging-port=9222'
    ]

    for option in options:
        chrome_options.add_argument(option)

    driver = webdriver.Chrome(options = chrome_options)
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
