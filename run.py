from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
import json
import os
from dotenv import load_dotenv

# 0. INIT CONFIGURATION FROM FILE

load_dotenv()

PROXY = os.getenv('PROXY')
INPUT_URL = os.getenv('INPUT_URL')
OUTPUT_FILE = os.getenv('OUTPUT_FILE')

# to do: sprawdzic czy na innym kompie da sie to zrobic asapem z .env po prostu


opt = webdriver.ChromeOptions()
opt.add_argument("--start-maximized")
# opt.add_argument('--proxy-server=%s' % PROXY)

chromedriver_autoinstaller.install()


browser = webdriver.Chrome(options=opt)

# PLACEHOLDER FOR ALL DATA
allPagesData = []

print('Scrapping inited...')


# 1. SCRAP ALL PAGES

# browser.maximize_window()

browser.get(INPUT_URL + '/page/1/')
# browser.get('http://quotes.toscrape.com/page/1/')


while(1):
    sleep(randint(12,20))
    # sleep(randint(1,2))

    # grab data 
    quotes_selector = '#quotesPlaceholder > div'
    # quotes_selector = 'body > div > div:nth-child(2) > div.col-md-8 > div'

    quotes = browser.find_elements(By.CSS_SELECTOR, quotes_selector)

    for quote in quotes:
        allPagesData.append(quote.text)
    
    try:    
        nextButton = browser.find_element(By.XPATH, '//*[text()="Next "]')
    except NoSuchElementException:
        nextButton = False

    noNextButton = not nextButton
   
    # add scroll page???

    if(noNextButton):
        # sleep(3)
        break
    
    nextButton.click()
    

print(allPagesData)


# 2. GET DATA IN SHAPE

shapedData = []

for element in allPagesData:
    temp = element.splitlines()
    shapedData.append({
        "text": temp[0].replace("“", ""),
        "by": " ".join(temp[1].split(" ")[1: -1]),
        "tags": temp[2].split(" ")[1:] if len(temp) == 3 else [] ,
    })


print(shapedData)

# 3. SAVE DATA TO A FILE

fullPath = OUTPUT_FILE

with open(fullPath, mode='w', encoding='utf-8') as file:
        for dataPiece in shapedData:
            file.write(json.dumps(dataPiece) + '\n')

print('Done...')
