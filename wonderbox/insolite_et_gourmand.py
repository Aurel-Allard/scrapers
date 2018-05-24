# -*- coding: utf-8 -*-
import scrapy
import parsel
import re


class InsoliteEtGourmandSpider(scrapy.Spider):
    name = 'insolite-et-gourmand'
    allowed_domains = ['wonderbox.fr']
    start_urls = ['https://www.wonderbox.fr/b/week-end-insolite-et-gourmand/']

    def parse(self, response):
        self.log('Scraping ' + response.url)
        for activity in response.css('.activity-item'):

          act = activity.css('.activity-title::text').extract_first()
          loc = activity.css('.activity-title::text').extract_first().split()
          zip_code = activity.xpath('.//h3[@class="activity-title"]/text()').re('[0-9]{2}')
          rating = activity.xpath('.//span[@class="count"]/text()').re('[0-9]+')

          if zip_code:
            zc = activity.xpath('.//h3[@class="activity-title"]/text()').re('[0-9]{2}')[0]
          else:
            zc = 'n.a.'

          if rating:
            rat = len(activity.css('span.full').extract())
            ratc = activity.xpath('.//span[@class="count"]/text()').re('[0-9]+')[0]
          else:
            rat = 'n.a.'
            ratc = '0'

          items = {
            'activity-title': act,
            'location': loc[len(loc)-2],
            'ZIP': zc,
            'rating': rat,
            'rating-count': ratc,
          }

          yield items

        next_page_url = response.css('div.pagination > a.js-pagination-next::attr(href)').extract_first()

        if next_page_url:
          next_page_url = response.urljoin(next_page_url)
          yield scrapy.Request(url = next_page_url, callback = self.parse)
