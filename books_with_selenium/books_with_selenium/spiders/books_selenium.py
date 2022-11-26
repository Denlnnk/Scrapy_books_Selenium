import scrapy
from selenium import webdriver
from Webdriver_options import Webdriver_options


class BooksSeleniumSpider(scrapy.Spider):
    name = 'books_selenium'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        return None
