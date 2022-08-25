from selenium import webdriver
from pathlib import Path
import time


class ISINDownloader:
    def __init__(self):
        self.DOWNLOAD_PATH = Path.cwd() / 'data' / 'traded_instruments'
        self.FINAL_ISIN_FILE = self.DOWNLOAD_PATH / 'isinp.zip'

        if not self.DOWNLOAD_PATH.exists():
            self.DOWNLOAD_PATH.mkdir(parents=True, exist_ok=False)

        if self.FINAL_ISIN_FILE.exists():
            Path.unlink(self.FINAL_ISIN_FILE)

        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': str(self.DOWNLOAD_PATH)}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://sistemaswebb3-listados.b3.com.br/isinPage/#accordionBodyTwo')
        driver.implicitly_wait(6)
        driver.find_element_by_xpath('/html/body/app-root/app-isin-home/div/form/div/div/div[1]/div[2]/div[1]/div/div/a/h6').click()
        time.sleep(10)
        driver.find_element_by_xpath('/html/body/app-root/app-isin-home/div/form/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]/p[1]/a').click()
        time.sleep(5)
        driver.quit()
