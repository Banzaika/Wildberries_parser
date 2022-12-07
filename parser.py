from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def get_photos(url):
    driver.get(url)

    try:
        myElem = WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'details-section__header'), 'О товаре'))
    except TimeoutException:
        print(f'Пропуск товара {url}')
        return

    elems = driver.find_elements(By.TAG_NAME, 'img')
    photos = set()

    for el in elems:
        photo = el.get_attribute('src')
        if 'big' in photo:
            photos.add(photo)
    return photos
