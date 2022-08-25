from selenium import webdriver
from pathlib import Path
import time


class InstrumentsFileDownloader:
    def __init__(self):
        self.DOWNLOAD_PATH = Path.cwd() / 'data' / 'traded_instruments' / 'InstrumentsConsolidated'

        if not self.DOWNLOAD_PATH.exists():
            self.DOWNLOAD_PATH.mkdir(parents=True, exist_ok=False)

        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': str(self.DOWNLOAD_PATH)}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://arquivos.b3.com.br/Web/Consolidated')
        driver.implicitly_wait(6)
        driver.find_element_by_xpath('/html/body/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/div/div[1]/div[2]/p[2]/a[1]').click()
        time.sleep(12)
        driver.quit()
