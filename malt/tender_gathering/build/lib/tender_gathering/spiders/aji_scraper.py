# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import re
import time
import datetime
from datetime import timedelta
import unicodedata

class AjiScraperSpider(scrapy.Spider):
    name = 'aji_scraper'
    allowed_domains = ['mapa.aji-france.com']
    start_urls = ['https://mapa.aji-france.com/login']

    def parse(self, response):
        self.log('******** Scraping ' + response.url + ' *********')
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                '_username': 'mije.webacc@gmail.com',
                '_password': 'Mijewebacc75000',
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

          if day != 'Monday':
            included_dates = [today - timedelta(days=1)]
          else:
            included_dates = [today - timedelta(days=1), today - timedelta(days=2)]

          for iter_date in included_dates:
            if product_type == 'Sorties et voyages' and tender_date == iter_date:
              tender_url = block.xpath('//div[@id="container-content"]/a/@href')[i - 1].extract()
              url = 'https://mapa.aji-france.com' + tender_url
              yield scrapy.Request(url = url, callback=self.parse_details)

    def parse_details(self, response):
        cnt_list = ['grande-bretagne', 'grande bretagne', 'angleterre', 'uk', 'gb', 'ru', 'r-u', 'afghanistan', 'afghanistan', 'afrique du sud', 'afrique du sud', 'albanie', 'albanie', 'algerie', 'algerie', 'allemagne', 'allemagne', 'andorre', 'andorre', 'angola', 'angola', 'antigua-et-barbuda', 'antigua-et-barbuda', 'arabie saoudite', 'arabie saoudite', 'argentine', 'argentine', 'armenie', 'armenie', 'australie', 'australie', 'autriche', 'autriche', 'azerbaidjan', 'azerbaidjan', 'bahamas', 'bahamas', 'bahrein', 'bahrein', 'bangladesh', 'bangladesh', 'barbade', 'barbade', 'belgique', 'belgique', 'belize', 'belize', 'benin', 'benin', 'bhoutan', 'bhoutan', 'bielorussie', 'bielorussie', 'birmanie', 'birmanie', 'bolivie', 'bolivie', 'bosnie-herzegovine', 'bosnie-herzegovine', 'botswana', 'botswana', 'bresil', 'bresil', 'brunei', 'brunei', 'bulgarie', 'bulgarie', 'burkina faso', 'burkina faso', 'burundi', 'burundi', 'cambodge', 'cambodge', 'cameroun', 'cameroun', 'canada', 'canada', 'cap-vert', 'cap-vert', 'republique centrafricaine', 'republique centrafricaine', 'chili', 'chili', 'chine', 'chine', 'chypre', 'chypre (pays)', 'colombie', 'colombie', 'comores', 'comores (pays)', 'republique du congo', 'republique du congo', 'republique democratique du congo', 'republique democratique du congo', 'iles cook', 'iles cook', 'coree du nord', 'coree du nord', 'coree du sud', 'coree du sud', 'costa rica', 'costa rica', "cote d'ivoire", "cote d'ivoire", 'croatie', 'croatie', 'cuba', 'cuba', 'danemark', 'danemark', 'djibouti', 'djibouti', 'republique dominicaine', 'republique dominicaine', 'dominique', 'dominique (pays)', 'egypte', 'egypte', 'emirats arabes unis', 'emirats arabes unis', 'equateur', 'equateur (pays)', 'erythree', 'erythree', 'espagne', 'espagne', 'estonie', 'estonie', 'etats-unis', 'etats-unis', 'ethiopie', 'ethiopie', 'fidji', 'fidji', 'finlande', 'finlande', 'france', 'france', 'gabon', 'gabon', 'gambie', 'gambie', 'georgie', 'georgie', 'ghana', 'ghana', 'grece', 'grece', 'grenade', 'grenade (pays)', 'guatemala', 'guatemala', 'guinee', 'guinee', 'guinee-bissau', 'guinee-bissau', 'guinee equatoriale', 'guinee equatoriale', 'guyana', 'guyana', 'haiti', 'haiti', 'honduras', 'honduras', 'hongrie', 'hongrie', 'inde', 'inde', 'indonesie', 'indonesie', 'irak', 'irak', 'iran', 'iran', 'irlande', 'irlande (pays)', 'islande', 'islande', 'israel', 'israel', 'italie', 'italie', 'jamaique', 'jamaique', 'japon', 'japon', 'jordanie', 'jordanie', 'kazakhstan', 'kazakhstan', 'kenya', 'kenya', 'kirghizistan', 'kirghizistan', 'kiribati', 'kiribati', 'koweit', 'koweit', 'laos', 'laos', 'lesotho', 'lesotho', 'lettonie', 'lettonie', 'liban', 'liban', 'liberia', 'liberia', 'libye', 'libye', 'liechtenstein', 'liechtenstein', 'lituanie', 'lituanie', 'luxembourg', 'luxembourg', 'macedoine', 'macedoine (pays)', 'madagascar', 'madagascar', 'malaisie', 'malaisie', 'malawi', 'malawi', 'maldives', 'maldives', 'mali', 'mali', 'malte', 'malte', 'maroc', 'maroc', 'iles marshall', 'iles marshall', 'maurice', 'maurice (pays)', 'mauritanie', 'mauritanie', 'mexique', 'mexique', 'micronesie', 'micronesie (pays)', 'moldavie', 'moldavie', 'monaco', 'monaco', 'mongolie', 'mongolie', 'montenegro', 'montenegro', 'mozambique', 'mozambique', 'namibie', 'namibie', 'nauru', 'nauru', 'nepal', 'nepal', 'nicaragua', 'nicaragua', 'niger', 'niger', 'nigeria', 'nigeria', 'niue', 'niue', 'norvege', 'norvege', 'nouvelle-zelande', 'nouvelle-zelande', 'oman', 'oman', 'ouganda', 'ouganda', 'ouzbekistan', 'ouzbekistan', 'pakistan', 'pakistan', 'palaos', 'palaos', 'etat de palestine', 'etat de palestine', 'panama', 'panama', 'papouasie-nouvelle-guinee', 'papouasie-nouvelle-guinee', 'paraguay', 'paraguay', 'pays-bas', 'pays-bas', 'perou', 'perou', 'philippines', 'philippines', 'pologne', 'pologne', 'portugal', 'portugal', 'qatar', 'qatar', 'roumanie', 'roumanie', 'royaume-uni', 'royaume-uni', 'russie', 'russie', 'rwanda', 'rwanda', 'saint-christophe-et-nieves', 'saint-christophe-et-nieves', 'saint-marin', 'saint-marin', 'saint-vincent-et-les grenadines', 'saint-vincent-et-les grenadines', 'sainte-lucie', 'sainte-lucie', 'iles salomon', 'iles salomon', 'salvador', 'salvador', 'samoa', 'samoa', 'sao tome-et-principe', 'sao tome-et-principe', 'senegal', 'senegal', 'serbie', 'serbie', 'seychelles', 'seychelles', 'sierra leone', 'sierra leone', 'singapour', 'singapour', 'slovaquie', 'slovaquie', 'slovenie', 'slovenie', 'somalie', 'somalie', 'soudan', 'soudan', 'soudan du sud', 'soudan du sud', 'sri lanka', 'sri lanka', 'suede', 'suede', 'suisse', 'suisse', 'suriname', 'suriname', 'swaziland', 'swaziland', 'syrie', 'syrie', 'tadjikistan', 'tadjikistan', 'tanzanie', 'tanzanie', 'tchad', 'tchad', 'republique tcheque', 'republique tcheque', 'thailande', 'thailande', 'timor oriental', 'timor oriental', 'togo', 'togo', 'tonga', 'tonga', 'trinite-et-tobago', 'trinite-et-tobago', 'tunisie', 'tunisie', 'turkmenistan', 'turkmenistan', 'turquie', 'turquie', 'tuvalu', 'tuvalu', 'ukraine', 'ukraine', 'uruguay', 'uruguay', 'vanuatu', 'vanuatu', 'vatican', 'vatican', 'venezuela', 'venezuela', 'viet nam', 'viet nam', 'yemen', 'yemen', 'zambie', 'zambie', 'zimbabwe', 'zimbabwe']
        dest_list = ['ain', 'aisne', 'allier', 'alpes-de-haute-provence', 'hautes-alpes', 'alpes-maritimes', 'ardeche', 'ardennes', 'ariege', 'aube', 'aude', 'aveyron', 'bouches-du-rhone', 'calvados', 'cantal', 'charente', 'charente-maritime', 'cher', 'correze', 'corse-du-sud', 'haute-corse', "cote-d'or", "cotes-d'armor", 'creuse', 'dordogne', 'doubs', 'drome', 'eure', 'eure-et-loir', 'finistere', 'gard', 'haute-garonne', 'gers', 'gironde', 'herault', 'ille-et-vilaine', 'indre', 'indre-et-loire', 'isere', 'jura', 'landes', 'loir-et-cher', 'loire', 'haute-loire', 'loire-atlantique', 'loiret', 'lot-et-garonne', 'lozere', 'maine-et-loire', 'manche', 'marne', 'haute-marne', 'mayenne', 'meurthe-et-moselle', 'meuse', 'morbihan', 'moselle', 'nievre', 'nord', 'oise', 'orne', 'pas-de-calais', 'puy-de-dome', 'pyrenees-atlantiques', 'hautes-pyrenees', 'pyrenees-orientales', 'bas-rhin', 'haut-rhin', 'rhone', 'metropole', 'haute-saone', 'saone-et-loire', 'sarthe', 'savoie', 'haute-savoie', 'paris', 'seine-maritime', 'seine-et-marne', 'yvelines', 'deux-sevres', 'somme', 'tarn', 'tarn-et-garonne', 'var', 'vaucluse', 'vendee', 'vienne', 'haute-vienne', 'vosges', 'yonne', 'territoire', 'essonne', 'hauts-de-seine', 'seine-saint-denis', 'val-de-marne', "val-d'oise", 'guadeloupe', 'martinique', 'guyane', 'saint-pierre-et-miquelon', 'mayotte', 'ain', 'aisne', 'allier', 'hautes-alpes', 'alpes-de-haute-provence', 'alpes-maritimes', 'ardeche', 'ardennes', 'ariege', 'aube', 'aude', 'aveyron', 'bouches-du-rhone', 'calvados', 'cantal', 'charente', 'charente-maritime', 'cher', 'correze', 'corse-du-sud', 'haute-corse', 'cote-dor', 'cotes-darmor', 'creuse', 'dordogne', 'doubs', 'drome', 'eure', 'eure-et-loir', 'finistere', 'gard', 'haute-garonne', 'gers', 'gironde', 'herault', 'ile-et-vilaine', 'indre', 'indre-et-loire', 'isere', 'jura', 'landes', 'loir-et-cher', 'loire', 'haute-loire', 'loire-atlantique', 'loiret', 'lot-et-garonne', 'lozere', 'maine-et-loire', 'manche', 'marne', 'haute-marne', 'mayenne', 'meurthe-et-moselle', 'meuse', 'morbihan', 'moselle', 'nievre', 'nord', 'oise', 'orne', 'pas-de-calais', 'puy-de-dome', 'pyrenees-atlantiques', 'hautes-pyrenees', 'pyrenees-orientales', 'bas-rhin', 'haut-rhin', 'rhone', 'haute-saone', 'saone-et-loire', 'sarthe', 'savoie', 'haute-savoie', 'paris', 'seine-maritime', 'seine-et-marne', 'yvelines', 'deux-sevres', 'somme', 'tarn', 'tarn-et-garonne', 'var', 'vaucluse', 'vendee', 'vienne', 'haute-vienne', 'vosges', 'yonne', 'territoire-de-belfort', 'essonne', 'hauts-de-seine', 'seine-saint-denis', 'val-de-marne', 'val-doise', 'mayotte', 'guadeloupe', 'guyane', 'martinique', 'reunion', 'hambourg', 'barcelone', 'munich', 'milan', 'birmingham', 'cologne', 'naples', 'turin', 'marseille', 'valence', 'leeds', 'cracovie', 'francfort-sur-le-main', 'odz', 'seville', 'palerme', 'saragosse', 'wrocaw', 'rotterdam', 'stuttgart', 'berlin', 'glasgow', 'dusseldorf', 'dortmund', 'essen', 'genes', 'sheffield', 'goteborg', 'leipzig', 'malaga', 'breme', 'dresde', 'manchester', 'poznan', 'hanovre', 'anvers', 'lyon', 'nuremberg', 'edimbourg', 'duisbourg', 'liverpool', 'toulouse', 'gdansk', 'bristol', 'murcie', 'leicester', 'palma', 'szczecin', 'bologne', 'florence', 'brno', 'las', 'bochum', 'coventry', 'bydgoszcz', 'wuppertal', 'bradford', 'cardiff', 'bilbao', 'utrecht', 'plovdiv', 'nice', 'lublin', 'varna', 'malmo', 'bielefeld', 'belfast', 'alicante', 'cordoue', 'bari', 'cluj-napoca', 'bonn', 'timisoara', 'catane', 'thessalonique', 'kaunas', 'munster', 'karlsruhe', 'nottingham', 'mannheim', 'nantes', 'vila', 'valladolid', 'katowice', 'biaystok', 'vigo', 'ostrava', 'iasi', 'augsbourg', 'brighton', 'kingston-upon-hull', 'constanta', 'graz', 'newcastle', 'montpellier', 'wiesbaden', 'espoo', 'strasbourg', 'stoke-on-trent', 'gijon', 'southampton', 'craiova', 'aarhus', 'plymouth', 'derby', 'gelsenkirchen', 'venise', 'monchengladbach', 'gand', "l'hospitalet", 'verone', 'reading', 'brasov', 'bordeaux', 'galati', 'brunswick', 'kiel', 'vitoria-gasteiz', 'gdynia', 'chemnitz', 'aix-la-chapelle', 'wolverhampton', 'kosice', 'magdebourg', 'halle', 'porto', 'messine', 'grenade', 'lille', 'tampere', 'portsmouth', 'northampton', 'elche', 'eindhoven', 'fribourg-en-brisgau', 'czestochowa', 'krefeld', 'luton', 'vantaa', 'oviedo', 'lubeck', 'terrassa', 'badalona', 'radom', 'rennes', 'tilbourg', 'carthagene', 'mayence', 'jerez', 'oberhausen', 'aalborg', 'erfurt', 'padoue', 'uppsala', 'ploiesti', 'sabadell', 'rostock', 'mostoles', 'trieste', 'santa', 'bourgas', 'linz', 'almere', 'torun', 'debrecen', 'bournemouth', 'charleroi', 'oulu', 'groningue', 'odense', 'cassel', 'tarente', 'liege', 'kielce', 'pampelune', 'aberdeen', 'oradea', 'fuenlabrada', 'alcala', 'brescia', 'norwich', 'parme', 'almeria', 'prato', 'sosnowiec', 'rzeszow', 'swindon', 'hagen', 'leganes', 'turku', 'saint-sebastien', 'modene', 'swansea', 'reims', 'sarrebruck', 'breda', 'milton', 'gliwice', 'southend-on-sea', 'reggio', 'braila', 'hamm', 'getafe', 'middlesbrough', 'bolton', 'zabrze', 'burgos', 'sunderland', 'amadora', 'nimegue', 'peterborough', 'olsztyn', 'albacete', 'bielsko-biaa', 'santander', 'potsdam', 'reggio', 'warrington', 'saint-etienne', 'ravenne', 'mulheim', 'plzen', 'oxford', 'huddersfield', 'bytom', 'castellon', 'alcorcon', 'patras', 'toulon', 'split', 'perouse', 'ludwigshafen', 'oldenbourg', 'klaipeda', 'osnabruck', 'leverkusen', 'york', 'szeged', 'apeldoorn', 'grenoble', 'heidelberg', 'rousse', 'haarlem', 'arad', 'solingen', 'poole', 'linkoping', 'livourne', 'enschede', 'darmstadt', 'miskolc', 'herne', 'arnhem', 'cambridge', 'slough', 'pitesti', 'dijon', 'amersfoort', 'zaanstad', 'cagliari', 'san', 'bois-le-duc', 'neuss', 'salzbourg', 'foggia', 'angers', 'logrono', 'nimes', 'badajoz', 'orebro', 'vasteras', 'rimini', 'stara', 'paderborn', 'villeurbanne', 'ratisbonne', 'dundee', 'ipswich', 'sibiu', 'telford', 'saint-denis', 'haarlemmermeer', 'huelva', 'blackpool', 'pecs', 'salamanque', 'larissa', 'gloucester', 'bacau', 'aix-en-provence', 'clermont-ferrand', 'marbella', 'norrkoping', 'heraklion', 'peristeri', 'rybnik', 'ruda', 'jyvaskyla', 'brest', 'lerida', 'tours', 'salerne', 'targu', 'sale', 'limoges', 'tarragone', 'ferrare', 'amiens', 'helsingborg', 'watford', 'jonkoping', 'leon', 'schaerbeek', 'dos', 'tychy', 'gyor', 'rijeka', 'newport', 'ingolstadt', 'sassari', 'annecy', 'parla', 'latina', 'braga', 'innsbruck', 'wurtzbourg', 'gorzow', 'exeter', 'mataro', 'dabrowa', 'torrejon', 'baia', 'zoetermeer', 'solihull', 'zwolle', 'monza', 'cadix', 'elblag', 'pock', 'maastricht', 'syracuse', 'wolfsbourg', 'pescara', 'leyde', 'high', 'giugliano', 'opole', 'gateshead', 'santa', 'metz', 'colchester', 'lahti', 'cork', 'bergame', 'dordrecht', 'zielona', 'forli', 'furth', 'umea', 'perpignan', 'anderlecht', 'nyiregyhaza', 'ulm', 'blackburn', 'boulogne-billancourt', 'wabrzych', 'kuopio', 'bruges', 'heilbronn', 'trente', 'offenbach-sur-le-main', 'gottingen', 'bottrop', 'cheltenham', 'pforzheim', 'besancon', 'maidstone', 'buzau', 'chelmsford', 'reutlingen', 'wocawek', 'orleans', 'lund', 'jaen', 'alcobendas', 'basildon', 'algesiras', 'ede', 'recklinghausen', 'basingstoke', 'vicence', 'coblence', 'worthing', 'eastbourne', 'doncaster', 'bremerhaven', 'funchal', 'crawley', 'pleven', 'bergisch', 'terni', 'kecskemet', 'saint-denis', 'namur', 'remscheid', 'argenteuil', 'mulhouse', 'iena', 'erlangen', 'rotherham', 'rochdale', 'rouen', 'treves', 'huddinge', 'stockport', 'alphen-sur-le-rhin', 'chorzow', 'gillingham', 'tarnow', 'leeuwarden', 'sutton', 'koszalin', 'emmen', 'bolzano', 'siauliai', 'botosani', 'westland', 'montreuil', 'caen', 'saint-paul', 'orense', 'nancy', 'st', 'novare', 'liberec', 'worcester', 'moers', 'reus', 'plaisance', 'satu', 'telde', 'kalisz', 'woking', 'byfleet', 'delft', 'venlo', 'limassol', 'ancone', 'kallithea', 'legnica', 'barakaldo']
        trs_list = ['autocar', 'avion', 'bus', 'aéroport', 'aeroport']
        ppl_list = ['personne', 'personnes', 'élèves', 'élève', 'eleves', 'eleve']
        acc_list = ['accompagnateurs', 'accompagnateur', 'accompagnants', 'accompagnant']
        slp_list = ['hôtel', 'hotel', 'auberges', 'auberge', 'famille']

        all_lists = cnt_list + dest_list + trs_list + ppl_list

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
        criteria = response.xpath(u'//div[contains(text(),"Critères d\'attribution")]/following::div[1]').extract_first()
        criteria = criteria.split() if not criteria is None else []
        sf = title.split() + description + criteria
        sf = [k.lower() for k in sf]
        sf = [k.strip(':') for k in sf]
        sf = [re.sub('<.+>', '', k) for k in sf]
        sf = [re.sub('\.', '', k) for k in sf]
        sf = [re.sub(',', '', k) for k in sf]
        sf = [re.sub('.\'', '', k) for k in sf]
        search_fields = [unicodedata.normalize('NFKD', k).encode('ASCII', 'ignore').decode('ascii') for k in sf if k]
        temp_location = []
        temp_destination = []
        temp_transport = []
        temp_slp = []
        nb_people = 'n.a.'
        nb_acc = 'n.a.'
        if any(word in search_fields for word in all_lists):
          for word in search_fields:
            if word in cnt_list:
              temp_location.append(word.capitalize())
            if word in dest_list:
              temp_destination.append(word.capitalize())
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
        destination = ', '.join(set(temp_destination)) if len(temp_destination) > 0 else 'n.a.'
        transport = ', '.join(set(temp_transport)) if len(temp_transport) > 0 else 'n.a.'
        slp_place = ', '.join(set(temp_slp)) if len(temp_slp) > 0 else 'n.a.'

        journey_date = 'n.a.'
        lenght_stay = []
        jf = ' '.join(search_fields)

        lot = list(re.findall('lot(s)?.?(\d)', jf))
        lot = max(lot) if len(lot) > 0 else '1'

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
          'A': '',
          'B': '',
          'C - Date de publications': publication,
          'D - Date d\'expiration': expiry,
          'E - Url': current_url,
          'F - References': reference,
          'G': '',
          'H': '',
          'I - Etablissement': prospect_name,
          'J - Adresse prospect': prospect_address,
          'K - Ville prospect': prospect_city,
          'L - CP': zip_code,
          'M - Nombre de lots': lot,
          'N - Pays': location,
          'O - Dates du voyage': journey_date,
          'P - Ville/Région': destination,
          'Q - Transport': transport,
          'R - Hébergement': slp_place,
          'S - Nombre d\'eleves': nb_people,
          'T - Accompagnateur(s)': nb_acc,
          'U - Durée du séjour': '',
          'V - Contact': contact_name,
          'W': '',
          'X - Telephone': contact_phone,
          'Y - Courriel': contact_mail,
        }

        yield items
