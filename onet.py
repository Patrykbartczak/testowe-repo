from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime

def create_driver():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=options
    )
    return driver


def scrap_website():

    data = []

    driver = create_driver()
    url = "https://www.onet.pl/"
    driver.get(url)

    wait = WebDriverWait(driver,10)
    wait.until(
        EC.presence_of_all_elements_located((
            By.TAG_NAME,"article"
        ))
    )

    articles = driver.find_elements(By.TAG_NAME,"article")
    for article in articles:

        title = article.find_element(By.TAG_NAME,"h3").get_attribute("textContent")
        try:
            link = article.find_element(By.TAG_NAME,"a").get_attribute("href")
        except:
            'Nie podano'
        try:
            image = article.find_element(By.TAG_NAME,"img").get_attribute("src")
        except:
            image = "Nie podano"

        element = {
            "tytuł": title,
            "link": link,
            "zdjęcie": image
        }

        data.append(element)

    return data


data = scrap_website()

def create_excel(dataset):
    filename = datetime.now().strftime('%Y-%m-%d')
    try:
        df = pd.DataFrame(dataset)
        df.to_excel(f'{filename}.xlsx', index=False)
        df.to_csv(f'{filename}.csv', index=False)
        print('Zapisano dane!')
    except Exception as e:
        print(e)

create_excel(data)








