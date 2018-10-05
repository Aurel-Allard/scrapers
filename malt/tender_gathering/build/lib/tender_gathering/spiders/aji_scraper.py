# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import re

class AjiScraperSpider(scrapy.Spider):
    name = 'aji_scraper'
    allowed_domains = ['mapa.aji-france.com']
    start_urls = ['https://mapa.aji-france.com/login']

    def parse(self, response):
        self.log('******** Scraping ' + response.url + ' *********')
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                '_username': 'allard.au@gmail.com',
                '_password': '-Mapa59-',
            },
            callback=self.after_login
        )

    def after_login(self, response):
        self.log('******** Login Successful *********')
        base_url = 'https://mapa.aji-france.com/mapa/marche/'
        yield Request(url= base_url, callback=self.category)

    def category(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formxpath='//form[@name="aji_mpbundle_filter"]',
            formdata={
              's2id_autogen1': 'Energie',
            },
            clickdata={
              'name': 'aji_mpbundle_filter[submit]',
            },
            callback=self.choose_page
        )

    def choose_page(self, response):
        # To be changed
        for page in range(1, 2):
          page_url = 'https://mapa.aji-france.com/mapa/marche/?page=' + str(page)
          yield Request(url= page_url, callback=self.action)

    def action(self, response):
        tender_links = response.xpath('//div[@id="container-content"]/a/@href').extract()
        for tender_url in tender_links:
          url = 'https://mapa.aji-france.com' + tender_url
          yield scrapy.Request(url = url, callback=self.parse_details)

    def parse_details(self, response):
        raw_reference = response.xpath('//div[contains(text(),"PAJI")]/text()').extract()
        reference = raw_reference[0].strip()
        raw_title = response.xpath('//div[@class="page-header"]/h1/text()').extract()[0]
        title = raw_title.capitalize()
        raw_publication = response.xpath('//div[contains(text(),"Date de d")]/following::div[1]/text()').extract()
        publication = raw_publication[0].strip()
        raw_expiry = response.xpath('//div[contains(text(),"Date de fin")]/following::div[1]/text()').extract()
        expiry = raw_expiry[0].strip()
        current_url = response.request.url
        # prospect_name = response.xpath('//td[contains(text(),"Collège Pierre Deley")]/text()').extract()
        # prospect_address = response.xpath('//div[contains(text(),"Adresse")]/following::td[0]/text()').extract()
        # prospect_city = response.xpath('//div[contains(text(),"Etablissement")]/td/text()').extract()

        items = {
          'References': reference,
          'Titres': title,
          'Date de publications': publication,
          'Date d\'expiration': expiry,
          'Url': current_url,
          # 'Nom prospect': prospect_name,
          # 'Adresse prospect': prospect_address,
          # 'Ville': prospect_city,
        }

        yield items
