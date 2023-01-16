from django.shortcuts import render
from . import models
from tyres import models as tyres_models
from django.views.generic import DetailView, View
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import datetime
import re
from tyres import models as tyres_models
from dictionaries import models as dictionaries_models
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from  . import forms

reg_list = [
        #'\d{3}/\d{2}[A-Za-z]\d{2}(\(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}| \(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2})', 
        #'\d{2}(\.|\,)(\d{2}|\d{1})(R|-)\d{2}', 
        #'(\d{3}|\d{2})/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2}[A-Za-z]|\d{2})',  # = '(\d{3}|\d{2})/\d{2}([A-Za-z]|-)\d{2}' +  '\d{3}/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2})',    
        '(\d{3}/\d{2}[A-Za-z]\d{2}(\(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}| \(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}))|(\d{2}(\.|\,)(\d{2}|\d{1})(R|-)\d{2})|((\d{3}|\d{2})/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2}[A-Za-z]|\d{2}))', #3 в одном чтобы избежать повторений двойных в ячейке наподобие #АШ 480/80R42(18.4R42)
        '\d{2}(\.|\,)\d{1}[A-Za-z](R|-)\d{2}',
        '(\d{4}|\d{3})[A-Za-z]\d{3}([A-Za-z]|-)\d{3}',
        '\d{2}[A-Za-z]\d{1}([A-Za-z]|-)\d{1}',
        '\d{2}[A-Za-z]\d{1}(\.|\,)\d{2}([A-Za-z]|-)\d{1}',
        '\d{2}(\.|\,)\d{1}/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2})',                       
        ' \d{1}(\.|\,)\d{2}(([A-Za-z]|-)|[A-Za-z]-)\d{2} ',
         ' \d{1}[A-Za-z]-\d{2} ',
        '\d{3}[A-Za-z]\d{2}[A-Za-z]',
        '\s\d{2}([A-Za-z]|-)\d{2}(\.|\,)\d{1}', 
        '\d{2}[A-Za-z][A-Za-z]\d{2}', 
        ]
goods_dict = {}
onliner_competitors_dict = {}
goods_dict_avtoset = {}
goods_dict_bagoria = {}
class ComparativeAnalysisTableModelDetailView(DetailView):
    model = models.ComparativeAnalysisTableModel
    template_name = 'prices/comparative_prices.html'

    #login_url = reverse_lazy('abc_table_xyz:abctable')

    def get_object(self, queryset=None):                
        # get comparative_analysis_table
        comparative_analysis_table = models.ComparativeAnalysisTableModel.objects.all()[0]              # ПОКА ЧТО ПОЛУЧИМ ПРОСТО ТУПО СОЗДАННУЮ ПЕРВУЮ ТАБЛИЦУ (без филтров по датам и тд)
        #table_id = self.request.session.get('table_id')             
        #comparative_analysis_table, created = models.ComparativeAnalysisTableModel.objects.get_or_create(         
        #pk=table_id,                                       
        #defaults={},
        #)
        #if created:
        #    self.request.session['table_id'] = comparative_analysis_table.pk
        #    #list_of_tyre_comparative_objects = models.ComparativeAnalysisTyresModel.objects.filter(PERIOD)      # ЗАГЛУШКА НА БУДУЩЕЕ ДЛЯ СОРТИРОВКИ ТАБЛИЦ И ДАННЫХ ПО ПЕРИОДАМ 
        #    list_of_tyre_comparative_objects = models.ComparativeAnalysisTyresModel.objects.all()                  # А ПОКА ЧТО БЕРЕМ ПРОСТО DCT
        #    for comparative_object in list_of_tyre_comparative_objects:
        #        models.ComparativeAnalysisTyresModel.objects.bulk_create([models.ComparativeAnalysisTyresModel(tyre=n, table=comparative_analysis_table)])   

        # 1 ###### ПАРСИНГ Onliner:
        url = 'https://catalog.onliner.by/tires?region=bobrujsk'
        #response = requests.get(url)
        #soup = BeautifulSoup(response.text,"lxml")
        ## ПОДКЛЮЧЕНИЕ БИБЛИОТЕКИ SELENIUM
        webdriverr = webdriver.Chrome()
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')
        products = soup.find_all('div', class_='schema-product__group')

        for data_got in products:
            tyre_name = data_got.find('div', class_='schema-product__title')
            price = data_got.find('div', 'schema-product__price')
            if tyre_name and price:
                text_to_delete = tyre_name.text.find('шины') + 5
                tyre_name_cleaned = tyre_name.text[text_to_delete :]
                start_str_serch = price.text.find('от') + 3
                end_str_search = price.text.find('р') - 1
                price_cleaned = price.text[start_str_serch : end_str_search]
                #print('tyre_name', tyre_name_cleaned, 'price', price_cleaned)
                goods_dict[tyre_name_cleaned] = price_cleaned
        # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
        #1. получаем количество страниц:
        pages = soup.find('div', class_='schema-pagination schema-pagination_visible')
        urls = []
        links = pages.find_all('a', class_='schema-pagination__pages-link')
        for link in links:
            pageNum = int(link.text) if link.text.isdigit() else None
            if pageNum != None:
                urls.append(pageNum)
        #2. получаем данные со всех страниц:
        #for slug in urls[1:4]:                              # c 1 по 4 станицы
        for slug in urls[1:2]:
        #for slug in urls:      # рабочий вариант
            newUrl = url.replace('?', f'?page={slug}') 
            webdriverr.get(newUrl)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products = soup.find_all('div', class_='schema-product__group')

            for data_got in products:
                tyre_name = data_got.find('div', class_='schema-product__title')
                price = data_got.find('div', 'schema-product__price')
                if tyre_name and price:
                    text_to_delete1 = tyre_name.text.find('шины') + 5
                    tyre_name_cleaned = tyre_name.text[text_to_delete1 : ]
                    tyre_name_cleaned = tyre_name_cleaned.replace('\n', '')
                    start_str_serch = price.text.find('от') + 3
                    end_str_search = price.text.find('р') - 1
                    price_cleaned = price.text[start_str_serch : end_str_search]
                    #print('tyre_name', tyre_name_cleaned, 'price', price_cleaned)

                ###### дополнительные праметры ищем: 
                #for data_got in products:
                    tyre_season = data_got.find('div', class_='schema-product__description')
                    seas_list = ['летние', 'зимние', 'всесезонные']
                    studded_list = ['без шипов', 'с шипами', 'возможность ошиповки']
                    if tyre_season:
                        for s_el in seas_list:
                            if s_el in tyre_season.text:
                                season = s_el
                        for studded_el in studded_list:
                            if studded_el in tyre_season.text:
                                studded = studded_el
                        #print( season, '          ', studded)         

            # выдираем типоразмер для добавления в словарь
                    tyresize = str
                    for n in reg_list:
                        result = re.search(rf'(?i){n}', tyre_name_cleaned)
                        if result:
                            tyresize = result.group(0)
                            #print(tyresize)
                            ### удаление среза с типоразмером и всем что написано перед типоразмером
                            left_before_size_data_index = tyre_name_cleaned.index(result.group(0))
                            if left_before_size_data_index > 0:
                                str_left_data = tyre_name_cleaned[0:left_before_size_data_index-1]
                                tyresize_length = len(result.group(0)) + 1 
                                right_after_size_data_index = tyre_name_cleaned.index(result.group(0)) + tyresize_length
                                str_right_data = tyre_name_cleaned[right_after_size_data_index : ]
                            product_name = str_left_data
                            company_name = product_name.split(' ')[0]
                            tyre_param = str_right_data

                    values = price_cleaned, tyresize, product_name, tyre_param, company_name, season, #studded 
                    goods_dict[tyre_name_cleaned] = values                                                                      # ПОДПРАВИТЬ КЛЮЧИ _ НЕ ВСЕ ПОПАДУТ ВЕДБ
        #or k, v in goods_dict.items():
        #   print(k, v, 'KV')
        #print(goods_dict.items())

        # формируем отдельный список ПРОИЗВОДИТЕЛИ:
        onliner_companies_list = []  # список компаний-производителей Oliner
        for v in goods_dict.values():
            if v[4] and v[4].isdigit() is False:
                onliner_companies_list.append(v[4])
        onliner_companies_list = list(set(onliner_companies_list))  
        #print(onliner_companies_list, 'onliner_companies_list')

        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые модели шин для работы в таблице:
        #if models.ONLINER_COMPETITORS:
        #    onliner_companies_list = models.ONLINER_COMPETITORS
        #    print('onliner_companies_list', onliner_companies_list )

        chosen_by_company_dict = {}
        for k, v in goods_dict.items():
            if v[4] and v[4] in onliner_companies_list:                 # СЕЙЧАС ВЫДАЕТ ВСЕХ ПРОИЗВОДИТЕЛЕЙ  ВСЕЮ ПРОДУКЦИЮ или подкинутых пользователем
                chosen_by_company_dict[k] = v
        #print('chosen_by_company_dict', chosen_by_company_dict)

        # сопоставление с БД  и запись в БД конкурентов (Onliner):
        tyres_in_bd = tyres_models.Tyre.objects.all()
        for tyre in tyres_in_bd:
            for k, v in chosen_by_company_dict.items():
                #print('v', v)
                if tyre.tyre_size.tyre_size == v[1]:
                    #print('TTTTKKK', k)                                                                                            #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
                    #Cordiant Polar SL 205/55R16 94T ('165,00', '205/55R16', 'Cordiant Polar SL', '94T', 'Cordiant')
                    coma = v[0].find(',')
                    pr = float
                    name_competitor, created = dictionaries_models.CompetitorModel.objects.get_or_create(
                        competitor_name =  v[4]
                    )
                    #print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',  name_competitor, 'name_competitor =', v[4])
                    season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name=v[5]) 
                    if season_usage:
                        season_usage = season_usage[0]
                    else:
                        season_usage = None 
                    if coma:
                        pr = float(v[0].replace(',', '.'))
                    models.CompetitorSiteModel.objects.update_or_create(
                        site = 'onliner.by',
                        #tyre = tyre,
                        currency = dictionaries_models.Currency.objects.get(currency='BYN'),
                        price = pr,
                        date_period = datetime.datetime.today(),
                        #developer = v[4],
                        developer = name_competitor,
                        tyresize_competitor = v[1],
                        name_competitor = v[2], 
                        parametres_competitor = v[3],
                        season = season_usage
                        #tyre_to_compare = models.ComparativeAnalysisTyresModel.objects.get
                    )                                                                                                                                                                                                         
        ##### END OF ONLINER PARSING

        # 2 ###### ПАРСИНГ АВТОСЕТЬ:
        avtoset_good_num = 0
        # 1) Легковые шины
        url = 'https://autoset.by/tires/'       
        webdriverr = webdriver.Chrome()
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')   
        products_lt = soup.find_all('section', class_='container-block product__wrap specprice')

        for data_got in products_lt:
            tyre_title_lt = str(data_got.find('div', class_='brand').text).replace('\\n', '') 
            tyre_title_lt = re.sub('\r?\n', '', tyre_title_lt)
            tyre_model_lt = str(data_got.find('a', class_='model link_blue').text.replace('\\n', ''))  
            tyre_model_lt = re.sub('\r?\n', '', tyre_model_lt)
            tyre_size_lt = str(data_got.find('a', class_='size-val link_hov').text.replace(' ', '').replace(',', '.'))
            tyre_index_lt = str(data_got.find('span', class_='index-val').text) 
            tyre_season_lt = str(data_got.find('span', class_='val').text) 
            #print(tyre_title_lt, tyre_size_lt, tyre_index_lt, tyre_model_lt)
            tyre_rub_price_lt = str(data_got.find('span', class_='full').text.replace(' ', '')) 
            tyre_coins_price_lt = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
            tyre_price_lt = float(tyre_rub_price_lt + '.' + tyre_coins_price_lt)
            #print(tyre_price_lt)
            goods_dict_avtoset[tyre_size_lt, avtoset_good_num] = tyre_title_lt, tyre_model_lt, tyre_index_lt, tyre_price_lt, tyre_season_lt
            avtoset_good_num += 1

        # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
        #1. получаем количество страниц:
        pages = soup.find('div', class_='pagination-block__pages-wrap')        
        urls_get = []
        links = pages.find_all('a', class_='pagination-block__page') 
        for link in links:
            pageNum = int(link.text) if link.text.isdigit() else None
            if pageNum != None:
                urls_get.append(pageNum)
    
        #2. получаем данные со всех страниц:                         
        #for slug in range(1, urls_get[-1]):                             # мое добавление специально для АВТОСЕТЬ   # c 1 по 2 станицы
        for slug in range(1, 2):
            #newUrl = url.replace('', f'/?PAGEN_1={slug}')       #https://autoset.by/tires/?PAGEN_1=3
            newUrl = url + f'?PAGEN_1={slug}'       #https://autoset.by/tires/?PAGEN_1=3
            webdriverr.get(newUrl)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_lt = soup.find_all('section', class_='container-block product__wrap specprice')

            for data_got in products_lt:
                tyre_title_lt = str(data_got.find('div', class_='brand').text).replace('\\n', '')
                tyre_title_lt = re.sub('\r?\n', '', tyre_title_lt)
                tyre_model_lt = str(data_got.find('a', class_='model link_blue').text.replace('\\n', ''))  
                tyre_model_lt = re.sub('\r?\n', '', tyre_model_lt)
                tyre_size_lt = str(data_got.find('a', class_='size-val link_hov').text.replace(' ', '').replace(',', '.'))
                tyre_index_lt = str(data_got.find('span', class_='index-val').text) 
                tyre_season_lt = str(data_got.find('span', class_='val').text) 
                #print(tyre_title_lt, tyre_size_lt, tyre_index_lt, tyre_model_lt)
                tyre_rub_price_lt = str(data_got.find('span', class_='full').text.replace(' ', '')) 
                tyre_coins_price_lt = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
                tyre_price_lt = float(tyre_rub_price_lt + '.' + tyre_coins_price_lt)
                #print(tyre_price_lt)
                goods_dict_avtoset[tyre_size_lt, avtoset_good_num] = tyre_title_lt, tyre_model_lt, tyre_index_lt, tyre_price_lt, tyre_season_lt
                avtoset_good_num += 1

        # 2) Грузовые шины
        url = 'https://autoset.by/trucks-tires/'
        webdriverr = webdriver.Chrome()
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')   
        products_t = soup.find_all('section', class_='container-block product__wrap')
           
        for data_got in products_t:
            tyre_title_t = str(data_got.find('div', class_='brand').text).replace('\\n', '')
            tyre_title_t = re.sub('\r?\n', '', tyre_title_t)
            tyre_model_t = str(data_got.find('a', class_='model link_blue').text.replace('\\n', ''))  
            tyre_size_t = str(data_got.find('a', class_='size-val link_hov').text.replace(' ', '').replace(',', '.'))
            tyre_index_t = str(data_got.find('span', class_='index-val').text) 
            #print(tyre_title_t, tyre_size_t, tyre_index_t, tyre_model_t)
            tyre_rub_price_t = str(data_got.find('span', class_='full').text.replace(' ', '')) 
            tyre_coins_price_t = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
            tyre_price_t = float(tyre_rub_price_t + '.' + tyre_coins_price_t)
            #print(tyre_price_t)
            goods_dict_avtoset[tyre_size_t, avtoset_good_num] = tyre_title_t, tyre_model_t, tyre_index_t, tyre_price_t 
            avtoset_good_num += 1    

        # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
        #1. получаем количество страниц:
        pages = soup.find('div', class_='pagination-block__pages-wrap')        
        urls_get = []
        links = pages.find_all('a', class_='pagination-block__page') 
        for link in links:
            pageNum = int(link.text) if link.text.isdigit() else None
            if pageNum != None:
                urls_get.append(pageNum)
    
        #2. получаем данные со всех страниц:                         
        #for slug in range(1, urls_get[-1]):                             # мое добавление специально для АВТОСЕТЬ   # c 1 по 2 станицы
        for slug in range(1, 2):
            newUrl = url + f'?PAGEN_1={slug}'       #https://autoset.by/trucks-tires/?PAGEN_1=2
            webdriverr.get(newUrl)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_lt = soup.find_all('section', class_='container-block product__wrap specprice')   

            for data_got in products_t:
                tyre_title_t = str(data_got.find('div', class_='brand').text).replace('\\n', '')
                tyre_title_t = re.sub('\r?\n', '', tyre_title_t)
                tyre_model_t = str(data_got.find('a', class_='model link_blue').text.replace('\\n', ''))  
                tyre_size_t = str(data_got.find('a', class_='size-val link_hov').text.replace(' ', '').replace(',', '.'))
                tyre_index_t = str(data_got.find('span', class_='index-val').text) 
                tyre_rub_price_t = str(data_got.find('span', class_='full').text.replace(' ', '')) 
                tyre_coins_price_t = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
                tyre_price_t = float(tyre_rub_price_t + '.' + tyre_coins_price_t)
                goods_dict_avtoset[tyre_size_t, avtoset_good_num] = tyre_title_t, tyre_model_t, tyre_index_t, tyre_price_t 
                avtoset_good_num += 1 

        # 3) Грузовые индустриальные спец. шины
        url = 'https://autoset.by/industrial-tires/'
        webdriverr = webdriver.Chrome()
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')   
        products_ts = soup.find_all('section', class_='container-block product__wrap')
        
        for data_got in products_ts:
            tyre_title_ts = str(data_got.find('div', class_='brand').text).replace('\\n', '')
            tyre_title_ts = re.sub('\r?\n', '', tyre_title_ts)
            tyre_model_ts = str(data_got.find('a', class_='model link_blue').text).replace('\n', '')  
            tyre_size_ts = str(data_got.find('a', class_='size-val link_hov').text.replace(' ', '').replace(',', '.'))
            tyre_index_ts = str(data_got.find('span', class_='index-val').text) 
            #print(tyre_title_ts, tyre_size_ts, tyre_index_ts, tyre_model_ts)
            tyre_rub_price_ts = str(data_got.find('span', class_='full').text.replace(' ', '')) 
            tyre_coins_price_ts = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
            tyre_price_ts = float(tyre_rub_price_ts + '.' + tyre_coins_price_ts)
            #print(tyre_price_ts)
            goods_dict_avtoset[tyre_size_ts, avtoset_good_num] = tyre_title_ts, tyre_model_ts, tyre_index_ts, tyre_price_ts 

       # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
        #1. получаем количество страниц:
        pages = soup.find('div', class_='pagination-block__pages-wrap')        
        urls_get = []
        links = pages.find_all('a', class_='pagination-block__page') 
        for link in links:
            pageNum = int(link.text) if link.text.isdigit() else None
            if pageNum != None:
                urls_get.append(pageNum)
    
        #2. получаем данные со всех страниц:                         
        #for slug in range(1, urls_get[-1]):                             # мое добавление специально для АВТОСЕТЬ   # c 1 по 2 станицы
        for slug in range(1, 2):
            newUrl = url + f'?PAGEN_1={slug}'       #https://autoset.by/industrial-tires/?PAGEN_1=2
            webdriverr.get(newUrl)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_lt = soup.find_all('section', class_='container-block product__wrap specprice')

            for data_got in products_ts:
                tyre_title_ts = str(data_got.find('div', class_='brand').text).replace('\\n', '')
                tyre_title_ts = re.sub('\r?\n', '', tyre_title_ts)
                tyre_model_ts = str(data_got.find('a', class_='model link_blue').text).replace('\n', '')  
                tyre_size_ts = str(data_got.find('a', class_='size-val link_hov').text.replace(' ', '').replace(',', '.'))
                tyre_index_ts = str(data_got.find('span', class_='index-val').text) 
                #print(tyre_title_ts, tyre_size_ts, tyre_index_ts, tyre_model_ts)
                tyre_rub_price_ts = str(data_got.find('span', class_='full').text.replace(' ', '')) 
                tyre_coins_price_ts = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
                tyre_price_ts = float(tyre_rub_price_ts + '.' + tyre_coins_price_ts)
                #print(tyre_price_ts)
                goods_dict_avtoset[tyre_size_ts, avtoset_good_num] = tyre_title_ts, tyre_model_ts, tyre_index_ts, tyre_price_ts 

        # 4) Сельскохозяйственные шины
        url = 'https://autoset.by/agricultural-tires/'
        webdriverr = webdriver.Chrome()
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')   
        products_agro = soup.find_all('section', class_='container-block product__wrap')
        
        for data_got in products_agro:
            tyre_title_agro = str(data_got.find('div', class_='brand').text).replace('\\n', '')
            tyre_title_agro = re.sub('\r?\n', '', tyre_title_agro)
            tyre_model_agro = str(data_got.find('a', class_='model link_blue').text)
            tyre_model_agro = tyre_model_agro.replace("\n","")
            tyre_size_agro = str(data_got.find('a', class_='size-val link_hov').text.replace(' ', '').replace(',', '.'))
            tyre_index_agro = str(data_got.find('span', class_='index-val').text) 
            #print(tyre_title_agro, tyre_size_agro, tyre_index_agro, tyre_model_agro, len(tyre_model_agro))
            tyre_rub_price_agro = str(data_got.find('span', class_='full').text.replace(' ', '')) 
            tyre_coins_price_agro = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
            tyre_price_agro = float(tyre_rub_price_agro + '.' + tyre_coins_price_agro)
            #print(tyre_price_agro)
            goods_dict_avtoset[tyre_size_agro, avtoset_good_num] = tyre_title_agro, tyre_model_agro, tyre_index_agro, tyre_price_agro 

       # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
        #1. получаем количество страниц:
        pages = soup.find('div', class_='pagination-block__pages-wrap')        
        urls_get = []
        links = pages.find_all('a', class_='pagination-block__page') 
        for link in links:
            pageNum = int(link.text) if link.text.isdigit() else None
            if pageNum != None:
                urls_get.append(pageNum)
    
        #2. получаем данные со всех страниц:                         
        #for slug in range(1, urls_get[-1]):                             # мое добавление специально для АВТОСЕТЬ   # c 1 по 2 станицы
        for slug in range(1, 2):
            newUrl = url + f'?PAGEN_1={slug}'       #https://autoset.by/agricultural-tires/?PAGEN_1=2
            webdriverr.get(newUrl)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_lt = soup.find_all('section', class_='container-block product__wrap specprice')

            for data_got in products_agro:
                tyre_title_agro = str(data_got.find('div', class_='brand').text).replace('\\n', '')
                tyre_title_agro = re.sub('\r?\n', '', tyre_title_agro)
                tyre_model_agro = str(data_got.find('a', class_='model link_blue').text)
                tyre_model_agro = tyre_model_agro.replace("\n","")
                tyre_size_agro = str(data_got.find('a', class_='size-val link_hov').text.replace(' ', '').replace(',', '.'))
                tyre_index_agro = str(data_got.find('span', class_='index-val').text) 
                tyre_rub_price_agro = str(data_got.find('span', class_='full').text.replace(' ', '')) 
                tyre_coins_price_agro = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
                tyre_price_agro = float(tyre_rub_price_agro + '.' + tyre_coins_price_agro)
                goods_dict_avtoset[tyre_size_agro, avtoset_good_num] = tyre_title_agro, tyre_model_agro, tyre_index_agro, tyre_price_agro 

        #print(goods_dict_avtoset, len(goods_dict_avtoset.keys()))     # СЛОВАРЬ ключи = типоразмер, номер в словаре, данные = производитель, модель, индексы, цена

        #for k, v in goods_dict_avtoset.items():
        #    print(k, v)                             #('175/70R14', 34): ('Росава', 'Snowgard', '84T', 112.99, 'Зимняя')

        # формируем отдельный список ПРОИЗВОДИТЕЛИ:
        avtoset_companies_list = []  # список компаний-производителей Avtoset
        for v in goods_dict_avtoset.values():
            if v[0] and v[0].isdigit() is False:
                avtoset_companies_list.append(v[0])
        avtoset_companies_list = list(set(avtoset_companies_list))  
        #print(avtoset_companies_list, 'avtoset_companies_list')

        chosen_by_company_dict = {}
        for k, v in goods_dict_avtoset.items():
            if v[0] and v[0] in avtoset_companies_list:                 # СЕЙЧАС ВЫДАЕТ ВСЕХ ПРОИЗВОДИТЕЛЕЙ  ВСЕЮ ПРОДУКЦИЮ или подкинутых пользователем
                chosen_by_company_dict[k] = v
        #print('chosen_by_company_dict', chosen_by_company_dict)

        # сопоставление с БД  и запись в БД конкурентов (Автосеть):
        tyres_in_bd = tyres_models.Tyre.objects.all()
        for tyre in tyres_in_bd:
            for k, v in chosen_by_company_dict.items():
                #print(k,v)
                if tyre.tyre_size.tyre_size == k[0]:
                    #print('TTTT', k)                                                                                            #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
                    #('235/75R17,5', 90) ('Triangle', 'TR689A', '143/141J', 560.18)                                # Cordiant Polar SL 205/55R16 94T ('165,00', '205/55R16', 'Cordiant Polar SL', '94T', 'Cordiant')
                    coma = v[0].find(',')           
                    pr = float
                    name_competitor, created = dictionaries_models.CompetitorModel.objects.get_or_create(
                        competitor_name =  v[0]
                    )
                    #print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',  name_competitor, 'name_competitor =', v[0])
                    if v[4]:
                        season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name=v[4]) 
                    if season_usage:
                        season_usage = season_usage[0]
                    else:
                        season_usage = None 
                    if coma:
                        pr = float(str(v[3]).replace(',', '.'))
                    models.CompetitorSiteModel.objects.update_or_create(
                        site = 'autoset.by',
                        currency = dictionaries_models.Currency.objects.get(currency='BYN'),
                        price = pr,
                        date_period = datetime.datetime.today(),
                        developer = name_competitor,
                        tyresize_competitor = k[0],                                        
                        name_competitor = v[1], 
                        parametres_competitor = v[2],
                        season = season_usage
                        #tyre_to_compare = models.ComparativeAnalysisTyresModel.objects.get
                    )                                                                                                                                                                                                         
        ###### END OF АВТОСЕТЬ PARSING

        # 2 ###### ПАРСИНГ BAGORIA:
        all_seasons = 'allseason'
        snow = 'winterColor'
        summer = 'summer'
        bagoria_good_num = 0
        # 1) Легковые шины
        url = 'https://bagoria.by/legkovye-shiny/'       
        webdriverr = webdriver.Chrome()
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')   
        products_lt = soup.find_all('div', class_='accordion-manufacturers__main_item')

        bagoria_good_num = 0
        for data_got in products_lt:
            tyre_title_lt = str(data_got.find('h6', class_='manufacturer').text).replace('\n', '').replace(' ', '')
            tyre_model_lt = str(data_got.find('div', class_='model').text).replace('\n', '').replace(' ', '')   
            tyre_size_lt = str(data_got.find('div', class_='size').text.replace(' ', '').replace('\n', ''))
            tyre_index_lt = str(data_got.find('p', class_='index').text) 
            tyre_season_lt = str(data_got.find('div', class_='accordion-manufacturers__main_icons')) 
            if all_seasons in tyre_season_lt:
              tyre_season_lt  = 'всесезонные'
            elif snow in tyre_season_lt:
              tyre_season_lt  = 'зимние'
            elif summer in tyre_season_lt:
              tyre_season_lt  = 'летние'
        #    tyre_rub_price_lt = str(data_got.find('span', class_='full').text.replace(' ', '')) 
        #    tyre_coins_price_lt = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
        #    tyre_price_lt = float(tyre_rub_price_lt + '.' + tyre_coins_price_lt)
            goods_dict_bagoria[tyre_size_lt, bagoria_good_num] = tyre_title_lt, tyre_model_lt, tyre_index_lt, #tyre_price_lt, tyre_season_lt
            bagoria_good_num += 1

        # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
        #1. получаем количество страниц:
        pages = soup.find('ul', class_='pagination')        
        urls_get = []
        links = pages.find_all('a', class_='pagination__link')         # <li class="pagination__item"><a class="pagination__link" href="/legkovye-shiny/?nav=page-262">262</a></li>
        for link in links:
            if link.text:
                pageNum = link.text
                if pageNum.isdigit():
                    urls_get.append(int(pageNum))
        urls_get = max(urls_get)
        #print(urls_get, 'pages --pages ')
    
        #2. получаем данные со всех страниц:                         
        #for slug in range(1, urls_get[-1]):                             # мое добавление специально для АВТОСЕТЬ   # c 1 по 2 станицы
        for slug in range(1, 2):
            #newUrl = url.replace('', f'/?PAGEN_1={slug}')       #https://bagoria.by/legkovye-shiny/?PAGEN_1=3
            newUrl = url + f'?nav=page-{slug}'       #https://bagoria.by/legkovye-shiny/?nav=page-9
            webdriverr.get(newUrl)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_lt = soup.find_all('div', class_='accordion-manufacturers__main_item')

            for data_got in products_lt:
                tyre_title_lt = str(data_got.find('h6', class_='manufacturer').text).replace('\n', '').replace(' ', '')
                tyre_model_lt = str(data_got.find('div', class_='model').text).replace('\n', '').replace(' ', '')   
                tyre_size_lt = str(data_got.find('div', class_='size').text.replace(' ', '').replace('\n', ''))
                tyre_index_lt = str(data_got.find('p', class_='index').text) 
                tyre_season_lt = str(data_got.find('div', class_='accordion-manufacturers__main_icons')) 
                if all_seasons in tyre_season_lt:
                  tyre_season_lt  = 'всесезонные'
                elif snow in tyre_season_lt:
                  tyre_season_lt  = 'зимние'
                elif summer in tyre_season_lt:
                  tyre_season_lt  = 'летние'
            #    tyre_rub_price_lt = str(data_got.find('span', class_='full').text.replace(' ', '')) 
            #    tyre_coins_price_lt = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
            #    tyre_price_lt = float(tyre_rub_price_lt + '.' + tyre_coins_price_lt)
                goods_dict_bagoria[tyre_size_lt, bagoria_good_num] = tyre_title_lt, tyre_model_lt, tyre_index_lt, #tyre_price_lt, tyre_season_lt
                bagoria_good_num += 1
        #print(goods_dict_bagoria, 'goods_dict_bagoria')

        # 2) Грузовые шины
        url = 'https://bagoria.by/gruzovye-shiny/'
        webdriverr = webdriver.Chrome()
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')   
        products_t = soup.find_all('div', class_='accordion-manufacturers__main_item')
           
        for data_got in products_t:
            tyre_title_t = str(data_got.find('h6', class_='manufacturer').text).replace('\n', '').replace(' ', '').lstrip().rstrip()
            tyre_model_t = str(data_got.find('div', class_='model').text).replace('\n', '').replace(' ', '')   
            tyre_size_t = str(data_got.find('div', class_='size').text.replace(' ', '').replace('\n', '').replace(',', '.'))
            tyre_index_t = str(data_got.find('p', class_='index').text).replace('\n', '').replace(' ', '')         
            tyre_param_t = str(data_got.find('div', class_='accordion-manufacturers__main_layering').text).replace('\n', '').replace(' ', '')  
            tyre_ax_t = str(data_got.find('div', class_='accordion-manufacturers__main_applicability').text).replace('\n', '').replace(' ', '') 
            tyre_price_t = str(data_got.find('span', class_='accordion-manufacturers__main_price').text.replace(' ', '').replace('р.', '').replace(',', '.').replace(' ', '').lstrip().rstrip())     
            #print(tyre_title_t, tyre_size_t, tyre_model_t, tyre_index_t, tyre_ax_t, tyre_param_t, tyre_price_t)
            goods_dict_bagoria[tyre_size_t, bagoria_good_num] = tyre_title_t, tyre_model_t, tyre_index_t, tyre_param_t, tyre_price_t, tyre_ax_t
            bagoria_good_num += 1    

        # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:

        #1. получаем количество страниц:
        pages = soup.find('ul', class_='pagination')        
        urls_get = []
        links = pages.find_all('a', class_='pagination__link')         
        for link in links:
            if link.text:
                pageNum = link.text
                if pageNum.isdigit():
                    urls_get.append(int(pageNum))
        urls_get = max(urls_get)

        #2. получаем данные со всех страниц:                         
        #for slug in range(1, urls_get[-1]):                             # мое добавление специально для АВТОСЕТЬ   # c 1 по 2 станицы
        for slug in range(1, 2):
            newUrl = url + f'?nav=page-{slug}'       #https://bagoria.by/gruzovye-shiny/?nav=page-9
            webdriverr.get(newUrl)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_t = soup.find_all('div', class_='accordion-manufacturers__main_item')  

            for data_got in products_t:
                tyre_title_t = str(data_got.find('h6', class_='manufacturer').text).replace('\n', '').replace(' ', '').lstrip().rstrip()
                tyre_model_t = str(data_got.find('div', class_='model').text).replace('\n', '').replace(' ', '')   
                tyre_size_t = str(data_got.find('div', class_='size').text.replace(' ', '').replace('\n', '').replace(',', '.'))
                tyre_index_t = str(data_got.find('p', class_='index').text).replace('\n', '').replace(' ', '')         
                tyre_param_t = str(data_got.find('div', class_='accordion-manufacturers__main_layering').text).replace('\n', '').replace(' ', '')  
                tyre_ax_t = str(data_got.find('div', class_='accordion-manufacturers__main_applicability').text).replace('\n', '').replace(' ', '') 
                tyre_price_t = str(data_got.find('span', class_='accordion-manufacturers__main_price').text.replace(' ', '').replace('р.', '').replace(',', '.').replace(' ', '').lstrip().rstrip())     
                goods_dict_bagoria[tyre_size_t, bagoria_good_num] = tyre_title_t, tyre_model_t, tyre_index_t, tyre_param_t, tyre_price_t, tyre_ax_t
                bagoria_good_num += 1  
        
        # 3) Грузовые индустриальные спец. шины
        url = 'https://bagoria.by/industr-shiny/'
        webdriverr = webdriver.Chrome()
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')   
        products_ts = soup.find_all('div', class_='accordion-manufacturers__main_item')
        
        for data_got in products_ts:
            tyre_title_ts = str(data_got.find('h6', class_='manufacturer').text).replace('\n', '').replace(' ', '').lstrip().rstrip()
            tyre_model_ts = str(data_got.find('div', class_='model').text).replace('\n', '').replace(' ', '')   
            tyre_size_ts = str(data_got.find('div', class_='size').text.replace(' ', '').replace('\n', '').replace(',', '.'))
            tyre_index_ts = str(data_got.find('p', class_='index').text).replace('\n', '').replace(' ', '')         
            tyre_param_ts = str(data_got.find('div', class_='accordion-manufacturers__main_layering').text).replace('\n', '').replace(' ', '')  
            tyre_price_ts = str(data_got.find('span', class_='accordion-manufacturers__main_price').text.replace(' ', '').replace('р.', '').replace(',', '.').replace(' ', '').lstrip().rstrip())     
            goods_dict_bagoria[tyre_size_ts, bagoria_good_num] = tyre_title_ts, tyre_model_ts, tyre_index_ts, tyre_param_ts, tyre_price_ts
            bagoria_good_num += 1   
        #print('goods_dict_bagoria11', goods_dict_bagoria)

       # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
        #1. получаем количество страниц:
        pages = soup.find('ul', class_='pagination')        
        urls_get = []
        links = pages.find_all('a', class_='pagination__link')         
        for link in links:
            if link.text:
                pageNum = link.text
                if pageNum.isdigit():
                    urls_get.append(int(pageNum))
        urls_get = max(urls_get)
    
        #2. получаем данные со всех страниц:                         
        #for slug in range(1, urls_get[-1]):                             # мое добавление специально для АВТОСЕТЬ   # c 1 по 2 станицы
        for slug in range(1, 2):
            newUrl = url + f'?PAGEN_1={slug}'       #https://bagoria.by/industr-shiny/
            webdriverr.get(newUrl)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_ts = soup.find_all('div', class_='accordion-manufacturers__main_item')

            for data_got in products_ts:
                tyre_title_ts = str(data_got.find('h6', class_='manufacturer').text).replace('\n', '').replace(' ', '').lstrip().rstrip()
                tyre_model_ts = str(data_got.find('div', class_='model').text).replace('\n', '').replace(' ', '')   
                tyre_size_ts = str(data_got.find('div', class_='size').text.replace(' ', '').replace('\n', '').replace(',', '.'))
                tyre_index_ts = str(data_got.find('p', class_='index').text).replace('\n', '').replace(' ', '')         
                tyre_param_ts = str(data_got.find('div', class_='accordion-manufacturers__main_layering').text).replace('\n', '').replace(' ', '')  
                tyre_price_ts = str(data_got.find('span', class_='accordion-manufacturers__main_price').text.replace(' ', '').replace('р.', '').replace(',', '.').replace(' ', '').lstrip().rstrip())     
                goods_dict_bagoria[tyre_size_ts, bagoria_good_num] = tyre_title_ts, tyre_model_ts, tyre_index_ts, tyre_param_ts, tyre_price_ts
                bagoria_good_num += 1   

        # 4) Сельскохозяйственные шины
        url = 'https://bagoria.by/selhoz-shiny/'
        webdriverr = webdriver.Chrome()
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')   
        products_agro = soup.find_all('div', class_='accordion-manufacturers__main_item')
        
        for data_got in products_agro:
            tyre_title_agro = str(data_got.find('h6', class_='manufacturer').text).replace('\n', '').replace(' ', '').lstrip().rstrip()
            tyre_model_agro = str(data_got.find('div', class_='model').text).replace('\n', '').replace(' ', '')   
            tyre_size_agro = str(data_got.find('div', class_='size').text.replace(' ', '').replace('\n', '').replace(',', '.'))
            tyre_index_agro = str(data_got.find('p', class_='index').text).replace('\n', '').replace(' ', '')         
            tyre_param_agro = str(data_got.find('div', class_='accordion-manufacturers__main_layering').text).replace('\n', '').replace(' ', '')  
            tyre_price_agro = str(data_got.find('span', class_='accordion-manufacturers__main_price').text.replace(' ', '').replace('р.', '').replace(',', '.').replace(' ', '').lstrip().rstrip())     
            goods_dict_bagoria[tyre_size_agro, bagoria_good_num] = tyre_title_agro, tyre_model_agro, tyre_index_agro, tyre_param_agro, tyre_price_agro
            bagoria_good_num += 1 
        #print('goods_dict_bagoria', goods_dict_bagoria)

       # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
        #1. получаем количество страниц:
        pages = soup.find('ul', class_='pagination')        
        urls_get = []
        links = pages.find_all('a', class_='pagination__link')         
        for link in links:
            if link.text:
                pageNum = link.text
                if pageNum.isdigit():
                    urls_get.append(int(pageNum))
        urls_get = max(urls_get)
    
        #2. получаем данные со всех страниц:                         
        #for slug in range(1, urls_get[-1]):                             # мое добавление специально для АВТОСЕТЬ   # c 1 по 2 станицы
        for slug in range(1, 2):
            newUrl = url + f'?PAGEN_1={slug}'       #https://bagoria.by/selhoz-shiny/
            webdriverr.get(newUrl)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_agro = soup.find_all('div', class_='accordion-manufacturers__main_item')

            for data_got in products_agro:
                tyre_title_agro = str(data_got.find('h6', class_='manufacturer').text).replace('\n', '').replace(' ', '').lstrip().rstrip()
                tyre_model_agro = str(data_got.find('div', class_='model').text).replace('\n', '').replace(' ', '')   
                tyre_size_agro = str(data_got.find('div', class_='size').text.replace(' ', '').replace('\n', '').replace(',', '.'))
                tyre_index_agro = str(data_got.find('p', class_='index').text).replace('\n', '').replace(' ', '')         
                tyre_param_agro = str(data_got.find('div', class_='accordion-manufacturers__main_layering').text).replace('\n', '').replace(' ', '')  
                tyre_price_agro = str(data_got.find('span', class_='accordion-manufacturers__main_price').text.replace(' ', '').replace('р.', '').replace(',', '.').replace(' ', '').lstrip().rstrip())     
                goods_dict_bagoria[tyre_size_agro, bagoria_good_num] = tyre_title_agro, tyre_model_agro, tyre_index_agro, tyre_param_agro, tyre_price_agro
                bagoria_good_num += 1 

        #print(goods_dict_bagoria, len(goods_dict_bagoria.keys()))     # СЛОВАРЬ ключи = типоразмер, номер в словаре, данные = производитель, модель, индексы, цена
        #for k, v in goods_dict_bagoria.items():
        #   print(k, v)                             #('12,4-32', 599): ('OZKA', 'KNK50', '125A6TT', 'нс08', '902.64')

        # формируем отдельный список ПРОИЗВОДИТЕЛИ:
        bagoria_companies_list = []  # список компаний-производителей Bagoria
        for v in goods_dict_bagoria.values():
            if v[0] and v[0].isdigit() is False:
                bagoria_companies_list.append(v[0])
        bagoria_companies_list = list(set(bagoria_companies_list))  
        #print(bagoria_companies_list, 'bagoria_companies_list')

        chosen_by_company_dict = {}
        for k, v in goods_dict_bagoria.items():
            if v[0] and v[0] in bagoria_companies_list:                 # СЕЙЧАС ВЫДАЕТ ВСЕХ ПРОИЗВОДИТЕЛЕЙ  ВСЕЮ ПРОДУКЦИЮ или подкинутых пользователем
                chosen_by_company_dict[k] = v
        #print('chosen_by_company_dict', chosen_by_company_dict)

        # сопоставление с БД  и запись в БД конкурентов (Bagoria):
        tyres_in_bd = tyres_models.Tyre.objects.all()
        for tyre in tyres_in_bd:
            for k, v in chosen_by_company_dict.items():
                #print(k, 'GGG', v, 'GGG', len(v))
                if tyre.tyre_size.tyre_size == k[0]:
                    #print('TTTT', k)                                                                                            #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
                    #('12,4-32', 599): ('OZKA', 'KNK50', '125A6TT', 'нс08', '902.64')
                    coma = v[0].find(',')           
                    pr = None
                    name_competitor, created = dictionaries_models.CompetitorModel.objects.get_or_create(
                        competitor_name =  v[0]
                    )
                    #print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',  name_competitor, 'name_competitor =', v[0])
    #                if v[5]:
    #                    season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name=v[4]) 
    #                if season_usage:
    #                    season_usage = season_usage[0]
    #                else:
    #                    season_usage = None 
                    if coma and len(v) > 3:  #len(v[4]) == 5 :
                        pr = float(str(v[4]).replace(',', '.'))
                    models.CompetitorSiteModel.objects.update_or_create(
                        site = 'bagoria.by',
                        currency = dictionaries_models.Currency.objects.get(currency='BYN'),
                        price = pr,
                        date_period = datetime.datetime.today(),
                        developer = name_competitor,
                        tyresize_competitor = k[0],                                               
                        name_competitor = v[1], 
                        parametres_competitor = v[2],                      
                        #season = season_usage
                        #tyre_to_compare = models.ComparativeAnalysisTyresModel.objects.get
                    )                                                                                                                                                                                                         
        ###### END OF BAGORIA PARSING

        return comparative_analysis_table

    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        obj = context.get('object')
        list_of_tyre_comparative_objects = obj.comparative_table.all()

        ## 1 фильтр конкурентов Onliner:
        all_competitors = models.CompetitorSiteModel.objects.filter(site='onliner.by')
            # 1.1 ФИЛЬТР по дате
        #  all_competitors = models.CompetitorSiteModel.objects.filter(date_period=datetime.date(2022, 11, 22))       # по дате 
            # 1.2 ФИЛЬТР список производителей :
        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        onliner_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
            object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
            object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?

            list_of_matched_competitors = []
            if models.ONLINER_COMPETITORS:
                for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.ONLINER_COMPETITORS):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                        print("На пол шишечки", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                        #onliner_competitors_dict[object_unit.tyre] = competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price
                        list_of_matched_competitors.append(competitor)
                onliner_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
            else:
                for competitor in all_competitors[0 : 3]:                                                                                                           ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                        #print("На пол шишечки", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                        #onliner_competitors_dict[object_unit.tyre] = competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price
                        list_of_matched_competitors.append(competitor)
                onliner_competitors_dict1[object_unit.tyre] = list_of_matched_competitors

        ######  НАДО СФОРМИРОВАТЬ СЛОВАРЬ С НЕСКОЛЬКИМИ КОНКУРЕНТАМИя 05.12.2022
        models.ONLINER_COMPETITORS_DICTIONARY1 = onliner_competitors_dict1  
        #object_unit.onliner_competitor_on_date1() 

        # ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ ONLINER: 
        onliner_max_lengh_list = []
        for object_unit in list_of_tyre_comparative_objects:
            obj_num = len(object_unit.onliner_competitor_on_date1())
            onliner_max_lengh_list.append(obj_num)
        onliner_max_lengh_header = max(onliner_max_lengh_list)

        models.ONLINER_HEADER_NUMBER = onliner_max_lengh_header

        obj.onliner_heders_value()
        #object_unit.onliner_competitor_price_on_date1()
        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects
        print('ONLINER', context['list_of_tyre_comparative_objects'])



        ## 1 фильтр конкурентов Автосеть:
        all_competitors = models.CompetitorSiteModel.objects.filter(site='autoset.by')
        #print(all_competitors , 'all_competitors ')
            # 1.1 ФИЛЬТР по дате
        #  all_competitors = models.CompetitorSiteModel.objects.filter(date_period=datetime.date(2022, 11, 22))       # по дате 
            # 1.2 ФИЛЬТР список производителей :
        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        avtoset_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
            object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
            object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            if models.AVTOSET_COMPETITORS:
                for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.AVTOSET_COMPETITORS):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                        print("На пол шишечки", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                        #onliner_competitors_dict[object_unit.tyre] = competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price
                        list_of_matched_competitors.append(competitor)
                avtoset_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
            else:
                for competitor in all_competitors[0 : 3]:                                                                                                           ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                        #print("На пол шишечки", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                        list_of_matched_competitors.append(competitor)
                avtoset_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
        #print('avtoset_competitors_dict1', avtoset_competitors_dict1)

       ######  НАДО СФОРМИРОВАТЬ СЛОВАРЬ С НЕСКОЛЬКИМИ КОНКУРЕНТАМИя 05.12.2022
        models.AVTOSET_COMPETITORS_DICTIONARY1 = avtoset_competitors_dict1  
        object_unit.avtoset_competitor_on_date1() 

       ## ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ AVTOSET: 
        avtoset_max_lengh_list = []
        for object_unit in list_of_tyre_comparative_objects:
            obj_num = len(object_unit.avtoset_competitor_on_date1())
            avtoset_max_lengh_list.append(obj_num)
        avtoset_max_lengh_header = max(avtoset_max_lengh_list)

        models.AVTOSET_HEADER_NUMBER = avtoset_max_lengh_header
        # print('models.AVTOSET_HEADER_NUMBER ====+++==', models.AVTOSET_COMPETITORS_NAMES_FILTER )

        obj.avtoset_heders_value()
        #object_unit.onliner_competitor_price_on_date1()
        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects
        print('avtoset', context['list_of_tyre_comparative_objects'])
        ###### END OF AVTOSET

        ## 1 фильтр конкурентов BAGORIA:
        all_competitors = models.CompetitorSiteModel.objects.filter(site='bagoria.by')
        #print(all_competitors , 'all_competitors ')
    #        # 1.1 ФИЛЬТР по дате
    #    #  all_competitors = models.CompetitorSiteModel.objects.filter(date_period=datetime.date(2022, 11, 22))       # по дате 
    #        # 1.2 ФИЛЬТР список производителей :
    #    # выбор по производителю:                               
    #    # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        bagoria_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
            object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
            object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            if models.BAGORIA_COMPETITORS:
                for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.BAGORIA_COMPETITORS):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                        #print("На пол шишечки", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                        #onliner_competitors_dict[object_unit.tyre] = competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price
                        list_of_matched_competitors.append(competitor)
                bagoria_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
            else:
                for competitor in all_competitors[0 : 3]:                                                                                                           ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                        #print("На пол шишечки", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                        list_of_matched_competitors.append(competitor)
                bagoria_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
        #print('bagoria_competitors_dict1', bagoria_competitors_dict1)

       ######  НАДО СФОРМИРОВАТЬ СЛОВАРЬ С НЕСКОЛЬКИМИ КОНКУРЕНТАМИя 05.12.2022
            models.BAGORIA_COMPETITORS_DICTIONARY1 = bagoria_competitors_dict1  
            object_unit.bagoria_competitor_on_date1() 

       ## ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ BAGORIA: 
        bagoria_max_lengh_list = []
        for object_unit in list_of_tyre_comparative_objects:
            obj_num = len(object_unit.bagoria_competitor_on_date1())
            bagoria_max_lengh_list.append(obj_num)
        bagoria_max_lengh_header = max(bagoria_max_lengh_list)

        models.BAGORIA_HEADER_NUMBER = bagoria_max_lengh_header
        # print('models.BAGORIA_HEADER_NUMBER ====+++==', models.BAGORIA_COMPETITORS_NAMES_FILTER)

        obj.bagoria_heders_value()
        #object_unit.bagoria_competitor_price_on_date1()
        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects
        print('bagoria', context['list_of_tyre_comparative_objects'])
        ###### END OF BAGORIA



        ##################
        ##################
        ##Работа с интефейсом:
        list_of_all_competitors_template = []
        all_competitors_in_base = dictionaries_models.CompetitorModel.objects.all()
        for t in all_competitors_in_base:
            list_of_all_competitors_template.append(t.competitor_name)
        context['onliner_competitors'] = list(set(list_of_all_competitors_template))
        ###

        ####### Onliner фильтр для темплейта
        #print('models.ONLINER_COMPETITORS_NAMES_FILTER', models.ONLINER_COMPETITORS_NAMES_FILTER)           ###### ТАК здесь продолжим
        filter_form = forms.FilterForm()
        #filter_form.fields["competitors"].queryset = dictionaries_models.CompetitorModel.objects.filter(competitor_name__in=list(set(models.ONLINER_COMPETITORS_NAMES_FILTER))).values_list("competitor_name", flat=True)
        filter_form.fields["competitors"].queryset =  dictionaries_models.CompetitorModel.objects.filter(competitor_name__in=list(set(models.ONLINER_COMPETITORS_NAMES_FILTER)) and list(set(models.AVTOSET_COMPETITORS_NAMES_FILTER))).values_list("competitor_name", flat=True)
        context['onliner_filter_form'] = filter_form
        print('!!!!', context)
        #######


        return context
class ComparativeAnalysisTableModelUpdateView(View):

    def post(self, request):
        #print(request.POST, 'TTT')

        ## 1 работа с периодами:
        #start_period, end_period = '', ''
        #periods_list = []
        #for key, value in request.POST.items():
        #    if key == 'start_period' and value is not '':
        #        start_period = value
        #        periods_list.append(start_period)
        #    elif key == 'end_period' and value is not '':
        #        end_period = value
        #        periods_list.append(end_period)
        ##print(start_period, '||', end_period, 'RAKAKA', periods_list)
#
        ## 2-й рабочий вариант  (для некоьких групп)
        #tyre_groups_list = request.POST.getlist('tyre_groups')
#
        ## 3 работа с типоразмерами:
        #tyre_sizes_list = []
        #tyre_sizes_list = request.POST.getlist('tyre_sizes')
#
        ## 4 работа с моделями
        #tyre_models_list = []
        #tyre_models_list = request.POST.getlist('tyre_models')

        # 5 работа с производителями-конкурентами
        onliner_competitors_list = []
        onliner_competitors_list = request.POST.getlist('onliner_competitor')
        onliner_competitors_list = request.POST.getlist('competitors')
        #print('onliner_competitors_list', onliner_competitors_list)
#
        #if not periods_list:
        #    #print('EMPTY periods_list')
        #    pass
        #else:
        #    models.PERIOD_UPDATE_SALES = periods_list            # передаем в глобальныую данные и перезапускаем страницу
#
        #if not tyre_groups_list:
        #    #print('EMPTY tyre_groups_list')
        #    pass
        #else:
        #    models.TYRE_GROUP_NAMES = tyre_groups_list 
        #    #print(models.TYRE_GROUP_NAMES, 'models.TYRE_GROUP_NAMES', 'ITOGO') 
#
        #if not tyre_sizes_list:
        #    #print('EMPTY tyre_sizes_list')
        #    pass
        #else:
        #    models.TYRE_GROUP_SIZES = tyre_sizes_list  
#
        #if not tyre_models_list:
        #    #print('EMPTY tyre_sizes_list')
        #    pass
        #else:
        #    models.TYRE_GROUP_MODELS = tyre_models_list

        if not onliner_competitors_list:
            #print('onliner_competitors_list')
            pass
        #elif len(onliner_competitors_list) > 3:
        #    raise 'JHHJJHJHGGHFGFG'
        else:
            models.ONLINER_COMPETITORS = onliner_competitors_list
        return HttpResponseRedirect(reverse_lazy('prices:comparative_prices'))


