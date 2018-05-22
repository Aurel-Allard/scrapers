# -*- coding: utf-8 -*-
import scrapy


class InsoliteEtGourmandSpider(scrapy.Spider):
    name = 'insolite-et-gourmand'
    allowed_domains = ['https://www.wonderbox.fr']
    start_urls = ['https://www.wonderbox.fr/b/week-end-insolite-et-gourmand/']

    def parse(self, response):
        self.log('Scraping ' + response.url)
        for activity in response.css('div.activity-item'):
          items = {
            'activity-title': activity.css('h3.activity-title::text').extract(),
          }
          yield items

          next_page_url = response.css('div.pagination > a.js-pagination-next::attr(href)').extract()
          if next_page_url:
            next_page_url = next_page_url[0].rsplit('/', 1)[1]
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url = next_page_url, callback = self.parse)


# class QuotesSpider(scrapy.Spider):
#     name = 'quotes'
#     allowed_domains = ['toscrape.com']
#     start_urls = ['http://quotes.toscrape.com']

#     def parse(self, response):
#         self.log('Scraping ' + response.url)
#         for quote in response.css('div.quote'):
#           item = {
#             'author_name': quote.css('small.author::text').extract_first(),
#             'text': quote.css('span.text::text').extract_first(),
#             'tags': quote.css('a.tag::text').extract(),
#           }
#           yield item

#         if next_page_url:
#           next_page_url = reponse.css('li.next > a::attr(href)').extract_first()
#           next_page_url = response.urljoin(next_page_url)
#           yield scrapy.Request(url = next_page_url, callback = self.parse)
