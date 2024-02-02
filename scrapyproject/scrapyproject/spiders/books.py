import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def start_requests(self):
        URL = "https://books.toscrape.com"
        yield scrapy.Requests(url=URL, callback=self.books_page_parse())

    def books_page_parse(self, response):
        print(response.body)
