# This is a sample Python script.
import json
import requests
import schedule
import time

from selenium import webdriver
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import settings

PUSHOVER_API = 'https://api.pushover.net/1/messages.json'


def check_stock(url):
    options = Options()
    options.add_argument("--headless")

    # needed for docker, since chrome doesn't like being run as root
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.WebDriver(service=Service(ChromeDriverManager().install()), options=options)

    browser.get(url)
    in_stock = browser.find_element(By.ID, "AddToCartText-product-template").text != 'SOLD OUT'
    if in_stock:
        notify(url)


def notify(url):
    data = {
        'token': settings.PUSHOVER_API_TOKEN,
        'user': settings.PUSHOVER_USER_TOKEN,
        'title': 'JK9 IN STOCK!',
        'url': url,
        'message': 'JK9 bite pillow in stock',
        'priority': '1',
        'expire': ' 10800',  # seconds
        'retry': 30  # seconds
    }
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    requests.post(PUSHOVER_API, data=json.dumps(data), headers=headers)


# if __name__ == '__main__':
# check_stock('https://usa.juliusk9.com/collections/bite-pad/products/julius-k9-cotton-nylon-soft-bite-pad')
# schedule.every(10).seconds.do(
#     check_stock,
#     url='https://usa.juliusk9.com/collections/bite-pad/products/julius-k9-cotton-nylon-soft-bite-pad'
# )
# See PyCharm help at https://www.jetbrains.com/help/
# /

def main():
    schedule.every(1).to(5).minutes.do(
        check_stock,
        "https://usa.juliusk9.com/collections/bite-pad/products/julius-k9-cotton-nylon-soft-bite-pad"
    )
    while True:
        schedule.run_pending()
        time.sleep(1)


main()
