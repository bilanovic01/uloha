import time
import scrapy


class SrealitySpider(scrapy.Spider):
    name = 'sreality'
    page=1
    flats=0
    start_urls = [f'https://www.sreality.cz/hledani/prodej/byty?strana={page}']
    custom_settings = {
          'DOWNLOADER_MIDDLEWARES': {
              'middlewares.SeleniumMiddleware': 543,
          }
      }

    def parse(self, response):
        items = response.xpath('//div[@class="property ng-scope"]')
        self.flats += len(items)
        for item in items:
            title = item.xpath('.//span[@class="name ng-binding"]/text()').get()
            image_url = item.xpath('.//img/@src').get()
            yield {
                'title': title,
                'image_url': image_url
            }

        if self.flats < 500:
            self.page += 1
            next_page_url = f'https://www.sreality.cz/hledani/prodej/byty?strana={self.page}'
            time.sleep(5)
            yield response.follow(next_page_url, self.parse)