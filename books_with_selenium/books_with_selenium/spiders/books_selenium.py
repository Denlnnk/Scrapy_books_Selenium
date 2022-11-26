import time

import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from .Webdriver_options import Webdriver_options


class BooksSeleniumSpider(scrapy.Spider):
    name = 'books_selenium'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        self.driver = webdriver.Chrome(executable_path=Webdriver_options.chromedriver_path(),
                                       options=Webdriver_options.configuration())
        self.base_url = 'https://books.toscrape.com/'
        self.driver.get(self.base_url)
        time.sleep(6)

        count = 1
        while True:
            try:
                count += 1
                sel = Selector(text=self.driver.page_source)

                books = sel.css('div.image_container a::attr(href)').getall()
                for book_url in books:
                    full_book_url = self.base_url + 'catalogue/' + book_url
                    yield Request(full_book_url, callback=self.parse_book)
                self.logger.info(f'Collected {count} pages')
                self.driver.find_element(By.CLASS_NAME, 'next a').click()

            except NoSuchElementException:
                self.logger.info('All pages scraped')
                self.driver.quit()
                break

    def parse_book(self, response):
        self.logger.info('Parsing book........................................................................')
