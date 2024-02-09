from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

class Scraper:

    def __init__(self, headless = True):

        self.headless = headless

        options = webdriver.ChromeOptions()

        if self.headless:
            options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options=options)

    def scrape(self, term):
        self.driver.implicitly_wait(0.5)
        self.driver.get("https://www.google.com/search?q=" + term)
        titleElement = self.driver.find_element(by=By.XPATH, value="//a[@jsname ='UWckNb']/h3")
        urlElement = self.driver.find_element(by=By.XPATH, value="//a[@jsname ='UWckNb']")
        return titleElement.text, urlElement.get_attribute('href')