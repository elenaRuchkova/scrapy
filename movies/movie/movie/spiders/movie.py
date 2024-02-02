import scrapy
import requests
from lxml import html
from fake_useragent import UserAgent
UserAgent().chrome

class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["ru.wikipedia.org"]

    def start_requests(self):
        alfabet = ['А','Б','В','Г','Д','Е','Ж','З','И','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Э','Ю','Я']
        for letter in alfabet:        
            URL = f'https://ru.wikipedia.org/w/index.php?title=Категория%3AФильмы_по_алфавиту&from={letter}'
            yield scrapy.Request(url=URL, callback=self.parse_pages)
    
    def parse_pages(self, response, **kwards): 
        for href in response.xpath("//*[@id='mw-pages']//a/@href").extract():
            url = 'https://ru.wikipedia.org' + href
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwards):
        print(response.body)


        for selector in response.xpath("//*[@id='mw-content-text']/div/table"):

            title = selector.xpath("//*[@id='mw-content-text']//th").css("::text").extract_first()          
            #genre = selector.xpath("//*[@id='mw-content-text']//tbody/tr[contains(., 'Жанр')]/td/span/a/@title").extract()
            genre = selector.xpath("//*[@id='mw-content-text']//tbody/tr[contains(., 'Жанр')]//a/@title").extract()
            producer = selector.xpath("//*[@id='mw-content-text']/div[1]/table/tbody/tr[contains(., 'Режиссёр')]/td/span/a/@title").extract(),
            country = selector.xpath("//*[@id='mw-content-text']//tbody/tr[contains(., 'Стран')]/td//a/span/text()").extract()
            country_duble = selector.xpath("//*[@id='mw-content-text']//tbody/tr[contains(., 'Стран')]/td/ul/li//a/@title").extract()
            year = selector.xpath("//*[@id='mw-content-text']//tbody/tr[contains(., 'Год')]/td//span/a/text()").extract()
            year_duble = selector.xpath("//*[@id='mw-content-text']//tbody/tr[contains(., 'Год')]/td//span/text()").extract()

            imdb_href = selector.xpath("//*[@id='mw-content-text']//tbody//a[contains(@href, 'https://www.imdb.com/')]/@href").extract_first()
            
            response_imdb = requests.get(url=imdb_href, headers={'User-Agent': UserAgent().chrome})
            page_content = response_imdb.content
            tree = html.fromstring(page_content) 
            imdb = tree.xpath("//*[@id='__next']//span/div/div[2]/div[1]/span/text()")[0]

            item =  { 'title': title,
                        'genre': genre,
                        'producer' : producer,
                        'country': country,
                        'year': year,
                        'year_duble': year_duble, 
                        'imdb': imdb #  imdb_href 
                    }

        yield item
