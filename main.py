import time
import argparse
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
visible = EC.visibility_of_element_located
presence = EC.presence_of_element_located

parser = argparse.ArgumentParser(
    description='Play YouTube video in an embeded chrome window, using chromedrive')
parser.add_argument('-p', '--Http-Proxy', type=str, nargs=1, dest='http_proxy')
parser.add_argument('-k', '--Keywords', type=str, nargs='+', dest='keywords', required=True)


def watch_video_embed(keyword: str, proxy: str = ''):
    url: str = ''

    if re.compile(r'http://.+').match(proxy[0] if proxy else ''):
        chrome_options.add_argument(f'--proxy-server={proxy[0]}')

    chrome_options.headless = True
    with webdriver.Chrome(options=chrome_options) as driver:
        wait = WebDriverWait(driver, 3)
        driver.get(f"https://www.youtube.com/results?search_query={keyword}")
        url = wait.until(presence((By.ID, "video-title"))
                         ).get_attribute('href')

    chrome_options.headless = False
    with webdriver.Chrome(options=chrome_options) as driver:
        wait = WebDriverWait(driver, 3)
        driver.get(f"https://www.youtube.com/embed/{url.split('=')[-1]}")
        wait.until(visible((By.CLASS_NAME, 'ytp-large-play-button'))).click()

        current_url = driver.current_url
        element = None
        while not element and current_url:
            try:
                element = driver.find_element(By.CLASS_NAME, 'ended-mode')
            except:
                try:
                    current_url = driver.current_url
                except:
                    current_url = None
                time.sleep(1)


if __name__ == '__main__':
    args = parser.parse_args()
    watch_video_embed(args.keywords, args.http_proxy)
