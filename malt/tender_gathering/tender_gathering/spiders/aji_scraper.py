# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import re
import time
import datetime

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
        yield Request(url= base_url, callback=self.choose_page)

    def choose_page(self, response):
        # To be changed
        for page in range(1, 10):
          page_url = 'https://mapa.aji-france.com/mapa/marche/?page=' + str(page)
          yield Request(url= page_url, callback=self.action)

    def action(self, response):
        blocks = response.xpath('//div[@id="container-content"]/a')
        i = 0
        for block in blocks:
          i += 1
          product_type = response.xpath('//span[@class="typeproduit"]/text()')[i - 1].extract()
          str_tender_date = response.xpath('//span[@class="label label-primary pull-right"]/b/text()').re('\d{2}\/\d{2}\/\d{4}')[i - 1]
          tender_date = datetime.datetime.strptime(str_tender_date, '%d/%m/%Y').date()
          today = datetime.datetime.today().date()
          if product_type == 'Sorties et voyages' and tender_date == today:
            tender_url = block.xpath('//div[@id="container-content"]/a/@href')[i - 1].extract()
            url = 'https://mapa.aji-france.com' + tender_url
            yield scrapy.Request(url = url, callback=self.parse_details)
          # elif tender_date < today:

    def parse_details(self, response):
        test = response.xpath('//div[@class="col-sm-7"]/text()').extract()
        self.log('******** ' + test[0] + ' *********')

        raw_reference = response.xpath('//div[contains(text(),"PAJI")]/text()').extract()
        reference = raw_reference[0].strip()
        raw_title = response.xpath('//div[@class="page-header"]/h1/text()').extract()[0]
        title = raw_title.capitalize()
        raw_publication = response.xpath('//div[contains(text(),"Date de d")]/following::div[1]/text()').extract()
        publication = raw_publication[0].strip()
        raw_expiry = response.xpath('//div[contains(text(),"Date de fin")]/following::div[1]/text()').extract()
        expiry = raw_expiry[0].strip()
        current_url = response.request.url
        prospect_name = response.xpath('//div[contains(text(),"Etablissement")]/following::div[1]/table[@class="table"]/tbody/tr[1]/td/text()').extract_first()
        raw_prospect_address = response.xpath('//div[contains(text(),"Etablissement")]/following::div[1]/table[@class="table"]/tbody/tr[2]/td/text()').extract()
        prospect_address = raw_prospect_address[0] if len(raw_prospect_address) > 0 else 'n.a.'
        prospect_city = raw_prospect_address[1] if len(raw_prospect_address) > 1 and re.compile('\d{5}\s\w*').match(raw_prospect_address[1]) else 'n.a.'
        if prospect_city == 'n.a.':
          prospect_city = raw_prospect_address[2] if prospect_city == 'n.a.' and len(raw_prospect_address) > 2 and re.compile('\d{5}\s\w*').match(raw_prospect_address[2]) else 'n.a.'
        contact_name = response.xpath('//div[contains(text(),"Contact")]/following::div[1]/table[@class="table"]/tbody/tr[1]/td/text()').extract_first()
        contact_phone = response.xpath('//div[contains(text(),"Contact")]/following::div[1]/table[@class="table"]/tbody/tr[2]/td/text()').extract_first()
        contact_mail = response.xpath('//div[contains(text(),"Contact")]/following::div[1]/table[@class="table"]/tbody/tr[4]/td/text()').extract_first()

        items = {
          'References': reference,
          'Titres': title,
          'Date de publications': publication,
          'Date d\'expiration': expiry,
          'Url': current_url,
          'Nom prospect': prospect_name,
          'Adresse prospect': prospect_address,
          'BP': prospect_city,
          'Contact': contact_name,
          'Telephone': contact_phone,
          'Courriel': contact_mail,
        }

        yield items
