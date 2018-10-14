# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import re
import time
import datetime
from datetime import timedelta

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
        max_page = response.xpath('//ul[@class="pagination"]/li[last()-1]/a/text()').extract_first()
        try:
          max_page = int(max_page)
        except ValueError:
          max_page = 100

        for page in range(1, max_page):
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
          day = today.strftime('%A')

          if day != 'Sunday':
            included_dates = [today - timedelta(days=1)]
          else:
            included_dates = [today - timedelta(days=1), today - timedelta(days=2)]

          for iter_date in included_dates:
            if product_type == 'Sorties et voyages' and tender_date == iter_date:
              tender_url = block.xpath('//div[@id="container-content"]/a/@href')[i - 1].extract()
              url = 'https://mapa.aji-france.com' + tender_url
              yield scrapy.Request(url = url, callback=self.parse_details)

    def parse_details(self, response):
        cnt_list = ['grande-bretagne', 'grande bretagne', 'angleterre', 'uk', 'gb', 'albanie', 'andorre', 'armenie', 'autriche', 'azerbaidjan', 'iles des acores', 'belgique', 'bosnie-herzegovine', 'bulgarie', 'croatie', 'chypre', 'republique tcheque', 'danemark', 'estonie', 'finlande', 'macedoine', 'france', 'allemagne', 'gibraltar', 'grece', 'groenland', 'hongrie', 'islande', 'irlande', 'italie', 'lettonie', 'liechtenstein', 'lituanie', 'luxembourg', 'malte', 'moldavie', 'monaco', 'pays-bas', 'norvege', 'portugal', 'roumanie', 'saint-marin', 'slovaquie', 'slovenie', 'espagne', 'suede', 'suisse', 'turquie', 'ukraine', 'royaume-uni', 'vatican', 'serbie', 'pologne', 'bielorussie', 'tirana', 'andorre la vella', 'erevan', 'vienne', 'bakou', 'ponta delgada', 'bruxelles', 'sarajevo', 'sofia', 'zagreb', 'nicosie', 'prague', 'copenhage', 'tallinn', 'helsinki', 'skopje', 'paris', 'berlin', 'gibraltar', 'athenes', 'nuuk', 'budapest', 'reykjavik', 'dublin', 'rome', 'riga', 'vaduz', 'vilnius', 'luxembourg', 'la vallette', 'chisinau', 'monaco', 'amsterdam', 'oslo', 'lisbonne', 'bucarest', 'saint-marin', 'bratislava', 'ljubljana', 'madrid', 'stockholm', 'berne', 'ankara', 'kiev', 'londres', 'vatican', 'belgrade', 'varsovie', 'minsk', 'albanie', 'andorre', 'armenie', 'autriche', 'azerbaidjan', 'iles des a\x8dores', 'belgique', 'bosnie-herzegovine', 'bulgarie', 'croatie', 'chypre', 'republique tcheque', 'danemark', 'estonie', 'finlande', 'macedoine', 'france', 'allemagne', 'gibraltar', 'grece', 'groenland', 'hongrie', 'islande', 'irlande', 'italie', 'lettonie', 'liechtenstein', 'lituanie', 'luxembourg', 'malte', 'moldavie', 'monaco', 'pays-bas', 'norvege', 'portugal', 'roumanie', 'saint-marin', 'slovaquie', 'slovenie', 'espagne', 'suede', 'suisse', 'turquie', 'ukraine', 'royaume-uni', 'vatican', 'serbie', 'pologne', 'bielorussie', 'tirana', 'andorre la vella', 'erevan', 'vienne', 'bakou', 'ponta delgada', 'bruxelles', 'sarajevo', 'sofia', 'zagreb', 'nicosie', 'prague', 'copenhage', 'tallinn', 'helsinki', 'skopje', 'paris', 'berlin', 'gibraltar', 'athenes', 'nuuk', 'budapest', 'reykjavik', 'dublin', 'rome', 'riga', 'vaduz', 'vilnius', 'luxembourg', 'la vallette', 'chisinau', 'monaco', 'amsterdam', 'oslo', 'lisbonne', 'bucarest', 'saint-marin', 'bratislava', 'ljubljana', 'madrid', 'stockholm', 'berne', 'ankara', 'kiev', 'londres', 'vatican', 'belgrade', 'varsovie', 'minsk']
        dep_list = ['ain', 'aisne', 'allier', 'hautes-alpes', 'alpes-de-haute-provence', 'alpes-maritimes', 'ardeche', 'ardennes', 'ariege', 'aube', 'aude', 'aveyron', 'bouches-du-rhone', 'calvados', 'cantal', 'charente', 'charente-maritime', 'cher', 'correze', 'corse-du-sud', 'haute-corse', 'cote-dor', 'cotes-darmor', 'creuse', 'dordogne', 'doubs', 'drome', 'eure', 'eure-et-loir', 'finistere', 'gard', 'haute-garonne', 'gers', 'gironde', 'herault', 'ile-et-vilaine', 'indre', 'indre-et-loire', 'isere', 'jura', 'landes', 'loir-et-cher', 'loire', 'haute-loire', 'loire-atlantique', 'loiret', 'lot-et-garonne', 'lozere', 'maine-et-loire', 'manche', 'marne', 'haute-marne', 'mayenne', 'meurthe-et-moselle', 'meuse', 'morbihan', 'moselle', 'nievre', 'nord', 'oise', 'orne', 'pas-de-calais', 'puy-de-dome', 'pyrenees-atlantiques', 'hautes-pyrenees', 'pyrenees-orientales', 'bas-rhin', 'haut-rhin', 'rhone', 'haute-saone', 'saone-et-loire', 'sarthe', 'savoie', 'haute-savoie', 'paris', 'seine-maritime', 'seine-et-marne', 'yvelines', 'deux-sevres', 'somme', 'tarn', 'tarn-et-garonne', 'var', 'vaucluse', 'vendee', 'vienne', 'haute-vienne', 'vosges', 'yonne', 'territoire-de-belfort', 'essonne', 'hauts-de-seine', 'seine-saint-denis', 'val-de-marne', 'val-doise', 'mayotte', 'guadeloupe', 'guyane', 'martinique', 'reunion']
        loc_list = cnt_list + dep_list
        trs_list = ['autocar', 'avion', 'bus', 'aéroport', 'aeroport']
        ppl_list = ['personne', 'personnes', 'élèves', 'élève', 'eleves', 'eleve']
        acc_list = ['accompagnateurs', 'accompagnateur', 'accompagnants', 'accompagnant']
        slp_list = ['hôtel', 'hotel', 'auberges', 'auberge', 'famille']

        all_lists = loc_list + trs_list + ppl_list

        test = response.xpath('//div[@class="col-sm-7"]/text()').extract_first()
        self.log('******** ' + test + ' *********')

        raw_reference = response.xpath('//div[contains(text(),"PAJI")]/text()').extract_first()
        reference = raw_reference.strip()

        raw_title = response.xpath('//div[@class="page-header"]/h1/text()').extract_first()
        title = raw_title.title()

        raw_publication = response.xpath('//div[contains(text(),"Date de d")]/following::div[1]/text()').extract_first()
        publication = raw_publication.strip()

        raw_expiry = response.xpath('//div[contains(text(),"Date de fin")]/following::div[1]/text()').extract_first()
        expiry = raw_expiry.strip()

        description = response.xpath('//div[contains(text(),"Description")]/following::div[1]').extract_first().split()
        criteria = response.xpath('//div[contains(text(),"Critères d\'attribution")]/following::div[1]').extract_first()
        criteria = criteria.split() if not criteria is None else []
        sf = title.split() + description + criteria
        sf = [k.lower() for k in sf]
        sf = [k.strip(':') for k in sf]
        sf = [re.sub('<.+>', '', k) for k in sf]
        sf = [re.sub('\.', '', k) for k in sf]
        sf = [re.sub(',', '', k) for k in sf]
        sf = [re.sub('.\'', '', k) for k in sf]
        sf = [k for k in sf if k]
        search_fields = sf
        temp_location = []
        temp_transport = []
        temp_slp = []
        nb_people = 'n.a.'
        nb_acc = 'n.a.'
        if any(word in search_fields for word in all_lists):
          for word in search_fields:
            if word in loc_list:
              temp_location.append(word.capitalize())
            if word in trs_list:
              temp_transport.append(word.capitalize())
            if word in slp_list:
              temp_slp.append(word.capitalize())
            if word in ppl_list:
              nb_one = search_fields[search_fields.index(word) - 1]
              nb_two = search_fields[search_fields.index(word) + 1]
              try:
                int(nb_one)
                nb_people = nb_one
              except ValueError:
                try:
                  int(nb_two)
                  nb_people = nb_two
                except ValueError:
                  pass
            if word in acc_list:
              nb_one = search_fields[search_fields.index(word) - 1]
              nb_two = search_fields[search_fields.index(word) + 1]
              try:
                int(nb_one)
                nb_acc = nb_one
              except ValueError:
                try:
                  int(nb_two)
                  nb_acc = nb_two
                except ValueError:
                  pass
        location = ', '.join(set(temp_location)) if len(temp_location) > 0 else 'n.a.'
        transport = ', '.join(set(temp_transport)) if len(temp_transport) > 0 else 'n.a.'
        slp_place = ', '.join(set(temp_slp)) if len(temp_slp) > 0 else 'n.a.'

        journey_date = 'n.a.'
        lenght_stay = []
        jf = ' '.join(search_fields)

        lot = re.findall('lot(s)?.?(\d)', jf)
        try:
          lot = str(max([int(k) for k in lot]))
        except ValueError:
          lot = '1'

        j_str1 = re.findall('(\d{1,2}\w{0,3})\s(janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|decembre)+\s(20\d{2})?', jf)
        j_str2 = re.findall('(\d{1,2}\w{0,3})\s(au)\s(\d{1,2}\w{0,3})\s(janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|decembre)+\s(20\d{2})?', jf)
        if len(j_str1) > 0 and len(list(set(j_str1))) % 2 == 0:
          j_str1 = [i + j for i, j in zip(j_str1[::2], j_str1[1::2])]
          j_str1 = [list(filter(None, k)) for k in j_str1]
          j_str1 = list([' '.join(k) for k in j_str1])
          journey_date = ' / '.join(set(j_str1))
        elif len(j_str2) > 0:
          j_str2 = [' '.join(k) for k in j_str2]
          journey_date = ' / '.join(set(j_str2))

        current_url = response.request.url

        prospect_name = response.xpath('//div[contains(text(),"Etablissement")]/following::div[1]/table[@class="table"]/tbody/tr[1]/td/text()').extract_first()

        raw_prospect_address = response.xpath('//div[contains(text(),"Etablissement")]/following::div[1]/table[@class="table"]/tbody/tr[2]/td/text()').extract()
        prospect_address = raw_prospect_address[0] if len(raw_prospect_address) > 0 else 'n.a.'

        prospect_loc = raw_prospect_address[1].split() if len(raw_prospect_address) > 1 and re.compile('\d{5}\s\w*').match(raw_prospect_address[1]) else 'n.a.'
        if prospect_loc == 'n.a.':
          prospect_loc = raw_prospect_address[2].split() if prospect_loc == 'n.a.' and len(raw_prospect_address) > 2 and re.compile('\d{5}\s\w*').match(raw_prospect_address[2]) else 'n.a.'
        if prospect_loc == 'n.a.':
          prospect_loc = raw_prospect_address[3].split() if prospect_loc == 'n.a.' and len(raw_prospect_address) > 3 and re.compile('\d{5}\s\w*').match(raw_prospect_address[3]) else 'n.a.'

        if prospect_loc != 'n.a.':
          prospect_city = ' '.join(prospect_loc[1:])
          zip_code = prospect_loc[0]
        else:
          prospect_city = 'n.a.'
          zip_code = 'n.a.'

        contact_name = response.xpath('//div[contains(text(),"Contact")]/following::div[1]/table[@class="table"]/tbody/tr[1]/td/text()').extract_first()

        raw_contact_phone = response.xpath('//div[contains(text(),"Contact")]/following::div[1]/table[@class="table"]/tbody/tr[2]/td/text()').extract_first()
        rcp = ''.join(i for i in raw_contact_phone if i.isdigit())
        rcp = [rcp[i:i+2] for i in range(0, len(rcp), 2)]
        contact_phone = ' '.join(rcp)

        contact_mail = response.xpath('//div[contains(text(),"Contact")]/following::div[1]/table[@class="table"]/tbody/tr[4]/td/text()').extract_first()

        items = {
          'References': reference,
          'Titres': title,
          'Date de publications': publication,
          'Date d\'expiration': expiry,
          'Nombre de lots': lot,
          'Lieu': location,
          'Dates du voyage': journey_date,
          'Transport': transport,
          'Hébergement': slp_place,
          'Nombre d\'eleves': nb_people,
          'Accompagnateur(s)': nb_acc,
          'Durée du séjour': lenght_stay,
          'Url': current_url,
          'Nom prospect': prospect_name,
          'Adresse prospect': prospect_address,
          'Ville prospect': prospect_city,
          'BP': zip_code,
          'Contact': contact_name,
          'Telephone': contact_phone,
          'Courriel': contact_mail,
          'Test': jf,
        }

        yield items
