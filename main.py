# This is a sample Python script.
import json
import time

import requests
import schedule
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import settings

PUSHOVER_API: str = 'https://api.pushover.net/1/messages.json'
in_stock: bool = False


def check_stock(url: str):
    logger.info("checking stock for {item}", item=item_name(url))
    options = Options()
    options.add_argument('--headless')

    # needed for docker, since chrome doesn't like being run as root
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.WebDriver(service=Service(ChromeDriverManager().install()), options=options)
    browser.get(url)

    global in_stock
    in_stock = browser.find_element(By.ID, 'AddToCartText-product-template').text != 'SOLD OUT'
    if in_stock:
        logger.info("{item} is in stock", item=item_name(url))
        notify(url)


def notify(url: str):
    data: dict[str, str | int] = {
        'token': settings.PUSHOVER_API_TOKEN,
        'user': settings.PUSHOVER_USER_TOKEN,
        'title': 'JK9 IN STOCK!',
        'url': url,
        'message': item_name(url) + ' is in stock',
        'priority': '2',
        'expire': ' 10800',  # seconds
        'retry': 30  # seconds
    }
    headers: dict[str, str] = {'Content-type': 'application/json', 'Accept': 'application/json'}

    requests.post(PUSHOVER_API, data=json.dumps(data), headers=headers)
    logger.info("pushover alert sent for {item}", item=item_name(url))


def item_name(url: str):
    return url.rsplit('/', 1)[1]


def main():
    logger.debug('app startup')
    schedule.every(1).to(5).seconds.do(
        check_stock,
        'https://usa.juliusk9.com/collections/bite-pad/products/julius-k9-cotton-nylon-soft-bite-pad'
    )
    while not in_stock:
        schedule.run_pending()
        time.sleep(1)


main()
