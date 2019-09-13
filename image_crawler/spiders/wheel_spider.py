import scrapy
import os

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from .utils import *
from image_crawler.items import ImageCrawlerItem

class WheelSpider(scrapy.Spider):
    name = 'wheelspider'
    allowed_domains = ['maluzen.com']
    start_urls = generate_query_urls()
    print('\n======List of urls to crawl from: ======\n')
    print(start_urls, '\n')

    image_src_url_prefix = 'https://www.maluzen.com/_upimages/photos/'

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.wait = WebDriverWait(self.driver, 100)
    
    def retrieve_image_link(self, disply_image_url: str):
        '''
        Form full-resolution (800x800) download-able link from display
        image url (which shown in the webpage)

        For ex:
            display url: //file.maluzen.com/www/_upimages/200/01_011706_00_00_00000_%23_%23_000_00.jpg
            full-res url wiil be: https://www.maluzen.com/_upimages/photos/01_011706_00_00_00000_%23_%23_000_00.jpg
        '''
        basename = os.path.basename(disply_image_url)
        return (WheelSpider.image_src_url_prefix + basename)

    def scroll_until_loaded(self):
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except TimeoutException:
                break
        # pass

    def parse(self, response):
        self.driver.get(response.url)
        self.scroll_until_loaded()
        print('Processing ', response.url)

        # Extract data using xpath
        pages = int(float(response.xpath('count(//*[@id="catalog-list"]//ul[contains(@class, "page")])').extract()[0]))
        img_src_list = response.xpath('//*[@id="catalog-list"]//ul//li//a//img//@src').extract()
        img_name_list = response.xpath('//*[@id="catalog-list"]//ul//li//a//img//@alt').extract()

        img_info = zip(img_src_list, img_name_list)

        print('\n===============================\n')
        print(len(img_src_list))
        print('\n===============================\n')

        for src, name in img_info:
            item = ImageCrawlerItem()
            link = self.retrieve_image_link(src)
   
            # Extract link to image source to download
            item['url'] = response.url
            item['img_link'] = link
            item['img_name'] = name

            yield item

        for i in range(pages - 1):
            n_url = 'https://www.maluzen.com/wheelcatalog/?pg={}&wd=4&wz=&wc=2&wb=&wm=&wma=&wyo='.format(i + 2)
            yield scrapy.http.Request(
                url=n_url,
                callback=self.parse
            )
