from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

class Scraper:

    # Default the scraper as headless, if you want to see it search for terms
    # pass false to the construction
    def __init__(self, headless = True):

        self.headless = headless

        options = webdriver.ChromeOptions()

        if self.headless:
            options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options=options)

    # Full scraping function
    def scrape(cls, term):
        articles = []
        articles = cls.googleSearch(term)
        title, url = cls.wikiSearch(term)
        articles.append({'title': title, 'url':url})

        return articles
    
    # Scraping off google
    def googleSearch(cls, term):
        # Wait to allow webpage elements to generate, can likely be smaller to increase speed
        cls.driver.implicitly_wait(0.5)
        cls.driver.get("https://www.google.com/search?q=" + term)

        # Google elements seem to be randomly named but they aren't, so far any relevent link off
        # google uses this js class 'UWckNB'
        titleElements = cls.driver.find_elements(by=By.XPATH, value="(//a[@jsname ='UWckNb']/h3)[position()<6]")
        urlElements = cls.driver.find_elements(by=By.XPATH, value="(//a[@jsname ='UWckNb'])[position() < 6]")

        articles = []
        for text in titleElements:
            url = urlElements[titleElements.index(text)]
            articles.append({'title': text.text, 'url':url.get_attribute('href')})

        return articles
    
    def wikiSearch(cls, term):

        cls.driver.implicitly_wait(0.5)
        cls.driver.get("https://www.wikipedia.org/")

        inputElement = cls.driver.find_element(by=By.ID, value = "searchInput")
        inputElement.send_keys(term)
        inputElement.submit()

        title = "Wikipedia result: " + cls.driver.find_element(by=By.ID, value="firstHeading").text
        url = cls.driver.current_url

        return title, url