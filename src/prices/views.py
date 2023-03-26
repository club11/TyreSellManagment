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
from django.db.models import Q

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.list import MultipleObjectMixin

from homepage.templatetags import my_tags
from . import forms as prices_forms

import pandas as pd
import matplotlib.pyplot as plt


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
        '\d{1}(\.|\,)\d{2}(([A-Za-z]|-)|[A-Za-z]-)\d{2}',
        '\d{1}[A-Za-z]-\d{2} ',
        '\d{3}[A-Za-z]\d{2}[A-Za-z]',
        '\s\d{2}([A-Za-z]|-)\d{2}(\.|\,)\d{1}', 
        '\d{2}[A-Za-z][A-Za-z]\d{2}', 
        ]
goods_dict = {}
onliner_competitors_dict = {}
goods_dict_avtoset = {}
goods_dict_bagoria = {}

goods_dict_express_shina = {}
goods_dict_kolesatyt = {}
goods_dict_kolesa_darom= {}


class ComparativeAnalysisTableModelDetailView(DetailView):
    model = models.ComparativeAnalysisTableModel
    template_name = 'prices/comparative_prices.html'

    #login_url = reverse_lazy('abc_table_xyz:abctable')
    def get_object(self, queryset=None):                
        # get comparative_analysis_table

        #comparative_analysis_table = models.ComparativeAnalysisTableModel.objects.all()[0]              # ПОКА ЧТО ПОЛУЧИМ ПРОСТО ТУПО СОЗДАННУЮ ПЕРВУЮ ТАБЛИЦУ (без филтров по датам и тд)
        comparative_analysis_table = models.ComparativeAnalysisTableModel.objects.get_or_create(market_table='belarus')[0]  

        # ПРОВЕРКА - наличие в базе спарсенных данных конкурентов на сегодня для скипа/запуска парсинга:
        today_is = datetime.datetime.now().date()
        list_of_sites = ['onliner.by', 'autoset.by', 'bagoria.by']
        competitors_exist = models.CompetitorSiteModel.objects.filter(site__in=list_of_sites).filter(date_period=today_is)
        if competitors_exist:
            #print('объеты спарсены, пропуск повторного парсинга')
            pass
        #### END проверки
        else:
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
            try:
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
                #for k, v in goods_dict.items():
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
            except:
                pass                                                                                                                                                                                                       
            ##### END OF ONLINER PARSING

            # 2 ###### ПАРСИНГ АВТОСЕТЬ:
            try:
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

           #     ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
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

           #     ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
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
            except:
                pass                                                                                                                                                                                                                   
            ###### END OF АВТОСЕТЬ PARSING

            # 2 ###### ПАРСИНГ BAGORIA:
            try:
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
                    #tyre_rub_price_lt = str(data_got.find('span', class_='full').text.replace(' ', '')) 
                    #tyre_coins_price_lt = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
                    #tyre_price_lt = float(tyre_rub_price_lt + '.' + tyre_coins_price_lt)
                    #print('tyre_price_lt', tyre_price_lt)
                    tyre_price_lt = str(data_got.find('span', class_='accordion-manufacturers__main_price').text.replace(' ', '').replace('р.', '').replace(',', '.').replace(' ', '').lstrip().rstrip())  
                    goods_dict_bagoria[tyre_size_lt, bagoria_good_num] = tyre_title_lt, tyre_model_lt, tyre_index_lt, tyre_season_lt, tyre_price_lt
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

                        #tyre_rub_price_lt = str(data_got.find('span', class_='full').text.replace(' ', '')) 
                        #tyre_coins_price_lt = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
                        #tyre_price_lt = float(tyre_rub_price_lt + '.' + tyre_coins_price_lt)
                        tyre_price_lt = str(data_got.find('span', class_='accordion-manufacturers__main_price').text.replace(' ', '').replace('р.', '').replace(',', '.').replace(' ', '').lstrip().rstrip())  
                        goods_dict_bagoria[tyre_size_lt, bagoria_good_num] = tyre_title_lt, tyre_model_lt, tyre_index_lt, tyre_season_lt, tyre_price_lt
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
       #            ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
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
       #            ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
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
                            #print('TTTT', k, 's111', v)                                                                                            #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
                            #('12,4-32', 599): ('OZKA', 'KNK50', '125A6TT', 'нс08', '902.64')
                            coma = v[0].find(',')           
                            pr = None
                            name_competitor, created = dictionaries_models.CompetitorModel.objects.get_or_create(
                                competitor_name =  v[0]
                            )
                            #print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',  name_competitor, 'name_competitor =', v[0])
    #                           if v[5]:
    #                               season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name=v[4]) 
    #                           if season_usage:
    #                               season_usage = season_usage[0]
    #                           else:
    #                               season_usage = None 
                            if coma and len(v) > 3 and v[4]:  #len(v[4]) == 5 :
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
            except:
                pass                                                                                                                                                                                                      
            ###### END OF BAGORIA PARSING

        return comparative_analysis_table

    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        obj = context.get('object')

        my_tags.currency_on_date()                  # ДЛЯ ПОЛУЧЕНИЯ ВАЛЮТЫ ПО КУРСУ НБ РБ НА ДАТУ
        currency, curr_value, shown_date = my_tags.currency_on_date()
        models.CURRENCY_VALUE_RUB = curr_value / 100


        #### 0 подбор шин с их данными по минималкам для отображения в таблице на определенный период (не конкуренты , а именно собственная продукция)Ж          
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:  
            # для поиска по собственной продукции с ходом в шаг = месяц       
            date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()                 # ['2023-01-23']
            year_to_look = date_filter.year
            month_to_look = date_filter.month
            #aRRRRR = obj.comparative_table.filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
            #print('aRRRRR', aRRRRR)
            # для поиска по кнкурентампродукции с ходом в шаг = день  
            all_competitors = models.CompetitorSiteModel.objects.filter(site='onliner.by').filter(date_period=date_filter)
        else:
        # 00.1  выборка всех имеющихся периодов с минималками:
            get_all_dates_year_month = obj.comparative_table.dates('sale_data', 'month')
            if get_all_dates_year_month:
                oldest_date = min(get_all_dates_year_month)
                latesr_date = max(get_all_dates_year_month)

                year_to_look = latesr_date.year
                month_to_look = latesr_date.month

        ####

        # ФИЛЬТР ПО СОБСТВЕННОЙ ПРОДУКЦИИ:   
        if models.SELF_PRODUCTION:                                                  # если пользователем введены (выбраны) шины:
            id_list = []
            for n in models.SELF_PRODUCTION:
                if n.isdigit():                                 
                    comparativeanalisystyre_object_id = int(n)
                    id_list.append(comparativeanalisystyre_object_id)
            list_of_tyre_comparative_objects = obj.comparative_table.all().filter(id__in=id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
            #print('list_of_tyre_comparative_objects', list_of_tyre_comparative_objects)   
        elif models.SELF_PRODUCTION_ALL:
            list_of_tyre_comparative_objects = obj.comparative_table.all().filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
        else:     
            list_of_tyre_comparative_objects = obj.comparative_table.all().filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
        # если пользовательищет через поисковик:
        if models.SEARCH_USER_REQUEST:
            user_requested_data = models.SEARCH_USER_REQUEST  
            search_result = obj.comparative_table.filter(Q(tyre__tyre_model__model__in=user_requested_data) | Q(tyre__tyre_size__tyre_size__in=user_requested_data))
            #print('search_result', search_result)
            if search_result:
                list_of_tyre_comparative_objects = search_result

        # ФИЛЬТР ПО ГРУППАМ ШИН:    
        if models.TYRE_GROUPS:                                                  # если пользователем введены (выбраны) шины:
            group_id_list = []
            for n in models.TYRE_GROUPS:
                if n.isdigit():                                 
                    gr_id = int(n)
                    group_id_list.append(gr_id)
            existing_val_check = obj.comparative_table.all().filter(tyre__tyre_group__id__in=group_id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
            if existing_val_check:
                list_of_tyre_comparative_objects = obj.comparative_table.all().filter(tyre__tyre_group__id__in=group_id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
                #print('list_of_tyre_comparative_objects', 'JJ', list_of_tyre_comparative_objects) 
            else:  
                #print('АШЫПКА!!!')
                pass
        elif models.TYRE_GROUPS_ALL:
            #group_id_list = dictionaries_models.TyreGroupModel.objects.values_list('id', flat=True)                        ####### !!!  это ПРАВИЛЬНЫЙ ВАРИАНТ ВЫБОРА ВСЕХ ГРУУПП ШИН, НО ТАК КАК НЕ У ВСЕХ ШИН ПРОПИСАНА ГРУППА _ ТО ПРИДЕТСЯ ПРОСТО ВСЕ ШИНЫ В ПОБОР
            #list_of_tyre_comparative_objects = obj.comparative_table.all().filter(tyre__tyre_group__id__in=group_id_list)  ####### !!!  это ПРАВИЛЬНЫЙ ВАРИАНТ ВЫБОРА ВСЕХ ГРУУПП ШИН, НО ТАК КАК НЕ У ВСЕХ ШИН ПРОПИСАНА ГРУППА _ ТО ПРИДЕТСЯ ПРОСТО ВСЕ ШИНЫ В ПОБОР
            list_of_tyre_comparative_objects = obj.comparative_table.all().filter(sale_data__year=year_to_look, sale_data__month=month_to_look)                                                   ####### !!!  ПРОСТО ВСЕ ШИНЫ В ПОБОР

        ## 1 фильтр конкурентов Onliner:
        # 1.1 ФИЛЬТР по дате
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:         
            date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()                 # ['2023-01-23']
            all_competitors = models.CompetitorSiteModel.objects.filter(site='onliner.by').filter(date_period=date_filter)
            #print('date_filter', date_filter,  '!!!!!!!!!!!!!!!!!!!!!!!', all_competitors)
        else:
            all_competitors = models.CompetitorSiteModel.objects.filter(site='onliner.by')     
            # 1.2 ФИЛЬТР список производителей :
        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        onliner_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
            object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
            object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?

            list_of_matched_competitors = []
            if models.ONLINER_COMPETITORS:
                if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:  
                    date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                    got_the_list = models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.ONLINER_COMPETITORS, site='onliner.by').filter(date_period=date_filter)

                    for competitor in got_the_list:                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            #print(date_filter, "На пол шишечки Onliner", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                            #onliner_competitors_dict[object_unit.tyre] = competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price
                            list_of_matched_competitors.append(competitor)
                    if len(list_of_matched_competitors) > 3:
                        onliner_competitors_dict1[object_unit.tyre] = list_of_matched_competitors[0 : 3]
                    else:
                        onliner_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                else:
                    for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.ONLINER_COMPETITORS, site='onliner.by'):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            #print("На пол шишечки Onliner", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                            #onliner_competitors_dict[object_unit.tyre] = competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price
                            list_of_matched_competitors.append(competitor)
                    if len(list_of_matched_competitors) > 3:
                        onliner_competitors_dict1[object_unit.tyre] = list_of_matched_competitors[0 : 3]
                    else:
                        onliner_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
            else:
                for competitor in all_competitors[0 : 3]:                                                                                                           ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                        #print("На пол шишечки", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                        #onliner_competitors_dict[object_unit.tyre] = competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price
                        list_of_matched_competitors.append(competitor)
                onliner_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
        #print('onliner_competitors_dict1', onliner_competitors_dict1)
        ######  НАДО СФОРМИРОВАТЬ СЛОВАРЬ С НЕСКОЛЬКИМИ КОНКУРЕНТАМИя 05.12.2022
        models.ONLINER_COMPETITORS_DICTIONARY1 = onliner_competitors_dict1  
        #object_unit.onliner_competitor_on_date1() 

        # ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ ONLINER: 
        onliner_max_lengh_list = []
        for object_unit in list_of_tyre_comparative_objects:
            obj_num = len(object_unit.onliner_competitor_on_date1())
            onliner_max_lengh_list.append(obj_num)
        #print('onliner_max_lengh_list', onliner_max_lengh_list)
        if onliner_max_lengh_list:
            onliner_max_lengh_header = max(onliner_max_lengh_list)
        else:
            onliner_max_lengh_header = 0

        models.ONLINER_HEADER_NUMBER = onliner_max_lengh_header

        obj.onliner_heders_value()
        obj.onliner_heders_lengt()
        #object_unit.onliner_competitor_price_on_date1()
        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects
        #print('ONLINER', context['list_of_tyre_comparative_objects'])
        # END ONLINER

        ## 2 фильтр конкурентов Автосеть:
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:         
            date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()                 # ['2023-01-23']
            all_competitors = models.CompetitorSiteModel.objects.filter(site='autoset.by').filter(date_period=date_filter)
        else:
            all_competitors = models.CompetitorSiteModel.objects.filter(site='autoset.by')
        #print(all_competitors , 'all_competitors ')
            # 1.2 ФИЛЬТР список производителей :
        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        avtoset_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
        #    object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
        #    object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            if models.AVTOSET_COMPETITORS:
                if models.COMPETITORS_DATE_FROM_USER_ON_FILTER: 
                    date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                    for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.AVTOSET_COMPETITORS, site='autoset.by').filter(date_period=date_filter):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            #print("На пол шишечки Автосеть", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                            #onliner_competitors_dict[object_unit.tyre] = competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price
                            list_of_matched_competitors.append(competitor)
                    #avtoset_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                    if len(list_of_matched_competitors) > 3:
                        avtoset_competitors_dict1[object_unit.tyre] = list_of_matched_competitors[0 : 3]
                    else:
                        avtoset_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                else:
                    for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.AVTOSET_COMPETITORS, site='autoset.by'):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            #print("На пол шишечки Автосеть", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                            #onliner_competitors_dict[object_unit.tyre] = competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price
                            list_of_matched_competitors.append(competitor)
                    #avtoset_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                    if len(list_of_matched_competitors) > 3:
                        avtoset_competitors_dict1[object_unit.tyre] = list_of_matched_competitors[0 : 3]
                    else:
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
        if avtoset_max_lengh_list:
            avtoset_max_lengh_header = max(avtoset_max_lengh_list)
        else:
            avtoset_max_lengh_header = 0
        #print('avtoset_max_lengh_header', avtoset_max_lengh_header)

        models.AVTOSET_HEADER_NUMBER = avtoset_max_lengh_header
        # print('models.AVTOSET_HEADER_NUMBER ====+++==', models.AVTOSET_COMPETITORS_NAMES_FILTER )

        obj.avtoset_heders_value()
        obj.avtoset_heders_lengt()
        #object_unit.onliner_competitor_price_on_date1()
        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects
        #print('avtoset', context['list_of_tyre_comparative_objects'])
        ###### END OF AVTOSET

        ## 3 фильтр конкурентов BAGORIA:
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:         
            date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()                 # ['2023-01-23']
            all_competitors = models.CompetitorSiteModel.objects.filter(site='bagoria.by').filter(date_period=date_filter)
        else:
            all_competitors = models.CompetitorSiteModel.objects.filter(site='bagoria.by')
        #print(all_competitors , 'all_competitors ')
    #        # 1.2 ФИЛЬТР список производителей :
    #    # выбор по производителю:                               
    #    # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        bagoria_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
        #    object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
        #    object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            if models.BAGORIA_COMPETITORS:
                if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
                    date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                    for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.BAGORIA_COMPETITORS, site='bagoria.by').filter(date_period=date_filter):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            #print("На пол шишечки BAGORIA", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                            #onliner_competitors_dict[object_unit.tyre] = competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price
                            list_of_matched_competitors.append(competitor)
                    #bagoria_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                    if len(list_of_matched_competitors) > 3:
                        bagoria_competitors_dict1[object_unit.tyre] = list_of_matched_competitors[0 : 3]
                    else:
                        bagoria_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                else:
                    for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.BAGORIA_COMPETITORS, site='bagoria.by'):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            #print("На пол шишечки BAGORIA", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                            #onliner_competitors_dict[object_unit.tyre] = competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price
                            list_of_matched_competitors.append(competitor)
                    #bagoria_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                    if len(list_of_matched_competitors) > 3:
                        bagoria_competitors_dict1[object_unit.tyre] = list_of_matched_competitors[0 : 3]
                    else:
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
        if bagoria_max_lengh_list:
            bagoria_max_lengh_header = max(bagoria_max_lengh_list)
        else:
            bagoria_max_lengh_header = 0

        models.BAGORIA_HEADER_NUMBER = bagoria_max_lengh_header
        # print('models.BAGORIA_HEADER_NUMBER ====+++==', models.BAGORIA_COMPETITORS_NAMES_FILTER)

        obj.bagoria_heders_value()
        obj.bagoria_heders_lengt()
        #object_unit.bagoria_competitor_price_on_date1()
        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects
        #print('bagoria', context['list_of_tyre_comparative_objects'])
        ###### END OF BAGORIA

#       ## 2 фильтр конкурентов CHEMCURIER:
        # if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:       - ЗАГОТОВКА ДЛЯ ФИЛЬТРА ПО ДАТЕ И В ХИМКУРЬЕР

        all_competitors = models.ChemCurierTyresModel.objects.all()
        #print(all_competitors , 'all_competitors ')
#            # 1.1 ФИЛЬТР по дате
#        #  all_competitors = models.CompetitorSiteModel.objects.filter(date_period=datetime.date(2022, 11, 22))       # по дате 
#            # 1.2 ФИЛЬТР список производителей :
#        # выбор по производителю:                               
#        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        chemcurier_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
#           object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
#           object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            if models.CHEMCURIER_COMPETITORS:
                for competitor in models.ChemCurierTyresModel.objects.filter(producer_chem__in=models.CHEMCURIER_COMPETITORS):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyre_size_chem:
                        #print("CHEMCURIER На пол шишечки TTT")
                        list_of_matched_competitors.append(competitor)
                chemcurier_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
            else:
                #for competitor in all_competitors[0 : 3]:  
                for competitor in all_competitors:  
                    #print(object_unit.tyre.tyre_size.tyre_size, '&&&', competitor.tyre_size_chem, 'FINSY ZALIV', competitor.tyre_size_chem.split(',')[0].replace('(', '').replace('\'', ''))                                                                                                   ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    #if object_unit.tyre.tyre_size.tyre_size == competitor.tyre_size_chem:
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyre_size_chem.split(',')[0].replace('(', '').replace('\'', ''):
                        list_of_matched_competitors.append(competitor)
            #            print('UMNYE LUDY', competitor)
            chemcurier_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
            #for mm, vv in chemcurier_competitors_dict1.items():
            #    print(mm, vv, 'HHH')
            #print('chemcurier_competitors_dict1', chemcurier_competitors_dict1)     # hemcurier_competitors_dict1 {<Tyre: Tyre object (1899)>: [], <Tyre: Tyre object (1900)>: [],

       ######  НАДО СФОРМИРОВАТЬ СЛОВАРЬ С НЕСКОЛЬКИМИ КОНКУРЕНТАМИя 05.12.2022
            models.CHEMCURIER_COMPETITORS_DICTIONARY1 = chemcurier_competitors_dict1  
            object_unit.chemcurier_competitor_on_date1()
            # CCC [('', '', ''), ('', '', ''), ('', '', '')]
            #print(object_unit.chemcurier_competitor_on_date1(), 'TTT')  

       ## ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ CHEMCURIER: 
        chemcurier_max_lengh_header = 1                                 # chemcurier будет лишь один столбец
        models.CHEMCURIER_HEADER_NUMBER = chemcurier_max_lengh_header
        # print('models.CHEMCURIER_HEADER_NUMBER ====+++==', models.CHEMCURIER_HEADER_NUMBER)

        obj.chemcurier_heders_value()
        obj.chemcurier_heders_lengt()
        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects
        ###### END OF CHEMCURIER

        ##################
        ##################
        ##Работа с интефейсом:
        #list_of_all_competitors_template = []
        #all_competitors_in_base = dictionaries_models.CompetitorModel.objects.all()
        #for t in all_competitors_in_base:
        #    list_of_all_competitors_template.append(t.competitor_name)
        #context['onliner_competitors'] = list(set(list_of_all_competitors_template))
        ####

        ####### Формы для фильтров темплейта:
        #print('models.ONLINER_COMPETITORS_NAMES_FILTER', models.ONLINER_COMPETITORS_NAMES_FILTER)           ###### ТАК здесь продолжим
        # если применен фильтр:
        # 1) выбрать производителя:
        filter_form = forms.FilterForm()
        context['producer_filter_form'] = filter_form                                           
        context['producer_filter_form'].queryset = dictionaries_models.CompetitorModel.objects.filter(competitor_name__in=list(set(models.ONLINER_COMPETITORS_NAMES_FILTER)) and list(set(models.AVTOSET_COMPETITORS_NAMES_FILTER)) 
        and list(set(models.BAGORIA_COMPETITORS_NAMES_FILTER))).values_list("competitor_name", flat=True)
        context['producer_filter_all'] = dictionaries_models.CompetitorModel.objects.all()
        #filter_form.fields["competitors"].queryset = dictionaries_models.CompetitorModel.objects.filter(competitor_name__in=list(set(models.ONLINER_COMPETITORS_NAMES_FILTER))).values_list("competitor_name", flat=True)
        # 2) выбрать продукцию:
        in_base_tyres = models.ComparativeAnalysisTyresModel.objects.all()
        context['in_base_tyres'] = in_base_tyres.order_by('-tyre')
        #######  
        # 3) выбрать группу шин:
        tyr_groups = dictionaries_models.TyreGroupModel.objects.all()
        #print('tyr_groups', tyr_groups)
        context['in_base_tyres_by_group'] = tyr_groups
        #######      
        # 
        # 4) ввод % отклонения торговой надбавки:
        deflection_form = forms.DeflectionInputForm(   initial={'deflection_data': models.DEFLECTION_VAL})
        context['deflection_form'] = deflection_form
        current_deflection_value = models.DEFLECTION_VAL
        if current_deflection_value is None:
            current_deflection_value = 0.0
        context['current_deflection_value'] = current_deflection_value

        # 5) выбранное пользователем значение даты:
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
            context['chosen_date'] = models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0]

        ### СБРОС ДАННЫХ _ ОЧИСТКА ПРИ ОБНОВЛЕНИИ СТРАНИЦЫ:
        models.TYRE_GROUPS = []     
        models.TYRE_GROUPS_ALL = [] 
        models.SELF_PRODUCTION = []
        models.SELF_PRODUCTION_ALL = []  
        models.ONLINER_COMPETITORS = [] 
        models.AVTOSET_COMPETITORS = []
        models.BAGORIA_COMPETITORS = []
        models.CHEMCURIER_COMPETITORS = []
        models.SEARCH_USER_REQUEST = []
        models.COMPETITORS_DATE_FROM_USER_ON_FILTER = []

        # пагинация самодельная:
        current_pagination_value = models.PAGINATION_VAL
        if current_pagination_value is None:
            current_pagination_value = 10
        pagination_form = forms.PaginationInputForm(initial={'pagination_data': current_pagination_value})
        context['pagination_val_per_form'] = pagination_form        
        #context['current_pagination_value'] = current_pagination_value        
        posts = context['list_of_tyre_comparative_objects']
        if 'page' in self.request.GET:
            page = self.request.GET['page']
        else:
            page = 1
        paginator = Paginator(posts, current_pagination_value)
        #print('paginator', paginator.num_pages)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        #print('posts', posts)

        context['list_of_tyre_comparative_objects'] = posts  

        currency_input_form = forms.CurrencyDateInputForm()
        context['currency_input_form'] = currency_input_form

        #currency, curr_value, shown_date = my_tags.currency_on_date()
        context['currency'] = currency
        context['curr_value'] = curr_value
        date_exist_true = None
        if shown_date:
            date_exist_true = datetime.datetime.strptime(shown_date, "%Y-%m-%d").date()
        else:
            date_exist_true = datetime.date.today()
        currency_input_form = forms.CurrencyDateInputForm()       
        currency_input_form.fields['chosen_date_for_currency'].initial = date_exist_true                        # !!! ЭТО БАЗА

        context['currency_input_form'] = currency_input_form

        ######## ДЛЯ ПЕРЕВОДА МИНИМАЛОК ИЗ РОССИЙСКОЙ ВАЛЮТЫ В БЕЛ РУБ (ДЛЯ РЫНКА БЕЛАРУСИ):

        for object_unit in list_of_tyre_comparative_objects:
           object_unit.currentpricesprice_from_currency_to_bel_rub()
           object_unit.planned_costs_from_currency_to_bel_rub()
           object_unit.semi_variable_prices_from_currency_to_bel_rub()
           object_unit.belarus902price_from_currency_to_bel_rub()
           object_unit.planned_profitability_from_currency_to_bel_rub()
           object_unit.direct_cost_variance_from_currency_to_bel_rub()
        ####### END ДЛЯ ПЕРЕВОДА МИНИМАЛОК ИЗ РОССИЙСКОЙ ВАЛЮТЫ В БЕЛ РУБ (ДЛЯ РЫНКА БЕЛАРУСИ)


        
        #############   ТЕСТОВАЯ ШТУКА ДЛЯ ГРАФИКОВ PANDAS              
        object_unit = list_of_tyre_comparative_objects.get(id=310)          # import matplotlib.pyplot as plt
        list_of_filtered_competitors_dates = [] 
        list_of_filtered_competitors_prices = []
        for comp in object_unit.price_tyre_to_compare.filter(site='onliner.by'):
            print(comp.price, comp.date_period, comp )
            list_of_filtered_competitors_dates.append(comp.date_period)
            list_of_filtered_competitors_prices.append(comp.price)
        my_series = pd.DataFrame({'dates':list_of_filtered_competitors_dates, 'prices':list_of_filtered_competitors_prices})
        plt.plot(my_series['dates'], my_series['prices'])               
        print(plt.plot(my_series['dates'], my_series['prices']))
        plt.show()
        #### END  ТЕСТОВАЯ ШТУКА ДЛЯ ГРАФИКОВ PANDAS


        return context
class ComparativeAnalysisTableModelUpdateView(View):

    def post(self, request):
        #print(request.POST, 'TTTH')
        #print (request.POST.getlist('competitors'), 'TTTT')

        ## 1 работа с периодами:
        comparative_model_parcing_date = request.POST.getlist('parcing_date') 
        #print('comparative_model_parcing_date', comparative_model_parcing_date , type(comparative_model_parcing_date))
        if comparative_model_parcing_date == ['']:
            pass
        elif comparative_model_parcing_date:
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER = comparative_model_parcing_date
            #print('{J{J{J{JJ{', comparative_model_parcing_date)
        else:
            pass

        #### 1.1 ПЕРИОД ДЛЯ КУРСА ВАЛЮТ:
        chosen_date_for_currency_year = request.POST.getlist('chosen_date_for_currency_year') 
        chosen_date_for_currency_month = request.POST.getlist('chosen_date_for_currency_month') 
        chosen_date_for_currency_day = request.POST.getlist('chosen_date_for_currency_day') 
        chosen_date_for_currency = chosen_date_for_currency_year + chosen_date_for_currency_month + chosen_date_for_currency_day
        if chosen_date_for_currency:
            #print('chosen_date_for_currency1', chosen_date_for_currency)  
            chosen_date_for_currency = '-'.join(str(x) for x in chosen_date_for_currency)
            #print('chosen_date_for_currency', chosen_date_for_currency)             # 'parcing_date': ['2023-03-14'],  chosen_date_for_currency 2022-1-30
            check_date = datetime.datetime.strptime(chosen_date_for_currency, "%Y-%m-%d").date()        #  если пользователем введена дана превышающая текущую для получения курса валют то нао скинуть на сегодня:
            if check_date > datetime.datetime.now().date():
                pass
            else:
                models.CURRENCY_DATE_GOT_FROM_USER = chosen_date_for_currency
#
        # 2-й работа с группами шин:
        tyre_groups_list_all = request.POST.getlist('self_production_group_id_all')
        tyre_groups_list = request.POST.getlist('self_production_group_id')
        if tyre_groups_list_all:
            #print(tyre_groups_list_all, 'tyre_groups_list_all')
            models.TYRE_GROUPS_ALL= tyre_groups_list_all
        else:
            #print(tyre_groups_list, 'tyre_groups_list')
            models.TYRE_GROUPS= tyre_groups_list 

        ## 3 работа с собственной продукцией:
        production_tyres_list_all = request.POST.getlist('self_production_all')  
        production_tyres_list = request.POST.getlist('self_production')                                                             # фильтр по собственным шинам
        if production_tyres_list_all:
            #print('production_tyres_list_all', production_tyres_list_all)
            models.SELF_PRODUCTION_ALL = production_tyres_list_all
        else:
            #print('production_tyres_list', production_tyres_list)
            models.SELF_PRODUCTION = production_tyres_list

        ### ЕСЛИ ПОЛЬЗОВАТЬЕЛЬ ИЩЕТ ЧЕРЕЗ ПОИСК:
        production_tyres_list_one = request.POST.getlist('product_search')
        #print('show me', production_tyres_list_one)
        if production_tyres_list_one:
            models.SEARCH_USER_REQUEST = production_tyres_list_one
#
        # 4 работа с производителями-конкурентами
        all_onliner_avtoset_bagoria_chemcurier_competitors_list_all = request.POST.getlist('producers_all')
        onliner_avtoset_bagoria_chemcurier_competitors_list = request.POST.getlist('competitors')                               # фильтр конкурентов
        if all_onliner_avtoset_bagoria_chemcurier_competitors_list_all:
        #if not onliner_avtoset_bagoria_chemcurier_competitors_list:
            #print('onliner_competitors_list')
            pass
        else:
            #print('onliner_avtoset_bagoria_chemcurier_competitors_list', onliner_avtoset_bagoria_chemcurier_competitors_list)
            models.ONLINER_COMPETITORS = onliner_avtoset_bagoria_chemcurier_competitors_list
            models.AVTOSET_COMPETITORS = onliner_avtoset_bagoria_chemcurier_competitors_list
            models.BAGORIA_COMPETITORS = onliner_avtoset_bagoria_chemcurier_competitors_list
            #models.CHEMCURIER_COMPETITORS = onliner_avtoset_bagoria_chemcurier_competitors_list


        # 5 работа с вводимыми данными по отклонению торговой надбавки
        deflection_data_got = request.POST.get('deflection_data')  
        #print('deflection_data_got', deflection_data_got)
        if deflection_data_got:
            models.DEFLECTION_VAL = float(request.POST.get('deflection_data'))
        else:
            pass

        # 6 работа с вводимыми данными по количеству выводимых объектов в таблице
        pagination_data_got = request.POST.get('pagination_data')  
        #print('pagination_data_got', pagination_data_got)
        if pagination_data_got:
            models.PAGINATION_VAL = int(request.POST.get('pagination_data'))
        else:
            pass
            
        return HttpResponseRedirect(reverse_lazy('prices:comparative_prices_bel'))

class ComparativeAnalysisTableModelDetailRussiaView(DetailView):
    model = models.ComparativeAnalysisTableModel
    template_name = 'prices/comparative_prices_russia.html'
    paginate_by = 5

    def get_object(self, queryset=None):                
        # get comparative_analysis_table
        comparative_analysis_table = models.ComparativeAnalysisTableModel.objects.get_or_create(market_table='russia')[0]

        # ПРОВЕРКА - наличие в базе спарсенных данных конкурентов на сегодня для скипа/запуска парсинга:
        today_is = datetime.datetime.now().date()
        list_of_sites = ['express-shina.ru', 'kolesa-darom.ru', 'kolesatyt.ru']
        competitors_exist = models.CompetitorSiteModel.objects.filter(site__in=list_of_sites).filter(date_period=today_is)
        if competitors_exist:
            #print('объеты спарсены, пропуск повторного парсинга')
            pass
        #### END проверки
        else:
                                                    #all_comparative_tyre_model_objects = models.ComparativeAnalysisTyresModel.objects.all()
                                                    #for ob in all_comparative_tyre_model_objects:
                                                    #    comparative_analysis_table.comparative_analysis_table.add(ob)

            # 1 ###### ПАРСИНГ express-shina:
            try:
                express_shina_good_num = 0
                # 1) парсинг грузовых шин
                url = 'https://express-shina.ru/search/gruzovyie-shinyi'       
                webdriverr = webdriver.Chrome()
                webdriverr.get(url)
                time.sleep(2)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                products = soup.find_all('div', class_='b-offer')      
                #print('products', products)


                # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
                #1. получаем количество страниц:
                pages = soup.find('div', class_='b-paging__list')        
                urls_get = []
                links = pages.find_all('a', class_='b-paging__page') 
                for link in links:
                    pageNum = int(link.text) if link.text.isdigit() else None
                    if pageNum != None:
                        urls_get.append(pageNum)

                #2. получаем данные со всех страниц:                         
                #for slug in range(1, urls_get[-1]):                             # мое добавление специально для express-shina  # c 1 по 2 станицы
                for slug in range(1, 2):
                    newUrl = url + f'?num={slug}'       #https://express-shina.ru/search/gruzovyie-shinyi?num=2
                    webdriverr.get(newUrl)
                    time.sleep(2)
                    webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)
                    soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                    products = soup.find_all('div', class_='b-offer')   

                    for data_got in products:
                        #print('data_got', data_got)
                        tyre_title = str(data_got.find('a', class_='b-offer-main__title').text.replace('Грузовая шина ', '').replace('новая', '')) 
                        #print(tyre_title)
                        if_price_exist = data_got.find('div', class_='b-offer-pay__price')
                        if if_price_exist:
                            tyre_rub_price = str(data_got.find('div', class_='b-offer-pay__price').text.replace('₽', '').replace(' ', '').replace('\xa0', ''))   
                        #print('tyre_rub_price ===', tyre_rub_price)
                        #print(tyre_title, ' ============',tyre_rub_price)
                        if tyre_title and tyre_rub_price:            # Грузовая шина Н.Камск CRG VM-201 8.25R20 130/128K универсальная 12PR новая  ============ 13870 
                            tyr_data_list = tyre_title.split(' ')
                            tyr_size_index_in_list = None
                            for some_param in tyr_data_list:        #['Н.Камск', 'НК-240', '8.25R20', '130/128K', 'универсальная', '12PR', '']
                                for n in reg_list:
                                    result = re.search(rf'(?i){n}', some_param)
                                    if result:
                                        #print(result, 'result', tyr_data_list.index(some_param))
                                        tyr_size_index_in_list = tyr_data_list.index(some_param)
                                        break
                                if some_param == '':
                                    tyr_data_list.remove(some_param)
                            len_list = len(tyr_data_list)
                            if tyr_size_index_in_list:
                                tyr_size = tyr_data_list[tyr_size_index_in_list]
                                tyr_producer = tyr_data_list[0]
                                tyr_model = ''
                                for n in range(1, tyr_size_index_in_list):
                                    tyr_model += tyr_data_list[n]
                                tyr_indexes = str
                                tyr_usabiity = str   
                                if tyr_size_index_in_list+1 < len_list or tyr_size_index_in_list+1 < len_list:
                                    tyr_indexes_is = tyr_data_list[tyr_size_index_in_list+1]
                                if tyr_indexes and tyr_indexes_is.isalpha():
                                    tyr_usabiity = tyr_indexes_is
                                else:
                                    tyr_indexes = tyr_indexes_is
                                if tyr_indexes and tyr_size_index_in_list+2 < len_list or tyr_size_index_in_list+2 < len_list:
                                    tyr_usabiity = tyr_data_list[tyr_size_index_in_list+2]
                                tyr_ply = str
                                if tyr_data_list.index(tyr_usabiity) < (len_list-1):
                                    tyr_ply = tyr_data_list[len_list-1]
                                tyr_group = 'грузовая'
                        tyre_period = str(data_got.find('ul', class_='b-offer-main__parameters').text)
                        tyr_per = ''
                        if tyre_period:
                            obrezra = tyre_period.find('Ось применения грузовой шины: ') + 29
                            tyre_period = tyre_period[obrezra:].split(' ')
                            tyre_period = tyre_period[1]
                            end_pos = tyre_period.find('Слойность')
                            if end_pos:
                                tyre_period = tyre_period[0:end_pos]
                            #print('tyre_period', tyre_period)
                            #tyr_primenjaemost = tyre_period
                        #print(tyr_size, '=tyr_size', tyr_producer, '=tyr_producer', tyr_model, '=tyr_model', tyr_indexes, '=tyr_indexes', tyr_usabiity, '=tyr_usabiity', tyr_ply, '=tyr_ply')
                        goods_dict_express_shina[tyr_size, express_shina_good_num] = tyr_producer, tyr_model, tyr_indexes, tyr_group,  tyre_rub_price, tyr_usabiity,  tyr_ply
                        express_shina_good_num += 1 

                for k, v in goods_dict_express_shina.items():
                    print(k, v, '!!!')

                # 2) парсинг легковых шин
                url = 'https://express-shina.ru/search/legkovyie-shinyi'       
                webdriverr = webdriver.Chrome()
                webdriverr.get(url)
                time.sleep(2)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                products = soup.find_all('div', class_='b-offer')      
                #print('products', products)


                # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
                #1. получаем количество страниц:
                pages = soup.find('div', class_='b-paging__list')        
                urls_get = []
                links = pages.find_all('a', class_='b-paging__page') 
                for link in links:
                    pageNum = int(link.text) if link.text.isdigit() else None
                    if pageNum != None:
                        urls_get.append(pageNum)

                #2. получаем данные со всех страниц:                         
                #for slug in range(1, urls_get[-1]):                             # мое добавление специально для express-shina  # c 1 по 2 станицы
                for slug in range(1, 2):
                    newUrl = url + f'?num={slug}'       #https://express-shina.ru/search/gruzovyie-shinyi?num=2
                    webdriverr.get(newUrl)
                    time.sleep(2)
                    webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)
                    soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                    products = soup.find_all('div', class_='b-offer')   

                    for data_got in products:
                        tyre_title = str(data_got.find('a', class_='b-offer-main__title').text.replace('новая', '').replace('Легковая шина ', ''))   
                        tyre_rub_price = str(data_got.find('div', class_='b-offer-pay__price').text.replace('₽', '').replace(' ', '').replace('\xa0', ''))   
                        if tyre_title and tyre_rub_price:            
                            tyr_data_list = tyre_title.split(' ')   #  Royal Black Royal Winter UHP 255/40 R19 100V
                            len_list = len(tyr_data_list)
                            tyr_size_index_in_list = None
                            tyr_size = str
                            tyr_indexes = str
                            if len_list > 3:
                                tyr_indexes = tyr_data_list[len_list-1]
                                tyr_size_pre = tyr_data_list[len_list-3] + tyr_data_list[len_list-2]
                                for n in reg_list:
                                    result = re.search(rf'(?i){n}', tyr_size_pre)
                                    if result:
                                        tyr_size = tyr_size_pre
                                        tyr_size_index_in_list = tyr_data_list.index(tyr_data_list[len_list-3])
                                        break
                                tyr_producer = tyr_data_list[0]
                                tyr_model = ''
                                for some_data in (1, tyr_size_index_in_list-1):
                                    tyr_model += tyr_data_list[some_data]
                                tyr_group = 'легковая'
                        tyre_period = str(data_got.find('ul', class_='b-offer-main__parameters').text.replace('Наличие шипов:', ''))
                        tyr_per = ''
                        tyr_spike = ''
                        if tyre_period:
                            obrezra = tyre_period.find('Сезон:') + 7
                            tyre_period = tyre_period[obrezra:].split(' ')
                            tyr_per = tyre_period[0]
                            tyr_spike = tyre_period[1]
                        #print(tyr_size, '=tyr_size', tyr_producer, '=tyr_producer', tyr_model, '=tyr_model', tyr_indexes, '=tyr_indexes', tyr_usabiity, '=tyr_usabiity', tyr_ply, '=tyr_ply')
                        goods_dict_express_shina[tyr_size, express_shina_good_num] = tyr_producer, tyr_model, tyr_indexes, tyr_group, tyre_rub_price, tyr_per, tyr_spike,
                        express_shina_good_num += 1 

                for k, v in goods_dict_express_shina.items():
                    print(k, v, '!!!')

                # 3) парсинг легкогрузовых шин
                url = 'https://express-shina.ru/search/legkogruzovyie-shinyi'       
                webdriverr = webdriver.Chrome()
                webdriverr.get(url)
                time.sleep(2)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                products = soup.find_all('div', class_='b-offer')      
                #print('products', products)


                # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
                #1. получаем количество страниц:
                pages = soup.find('div', class_='b-paging__list')        
                urls_get = []
                links = pages.find_all('a', class_='b-paging__page') 
                for link in links:
                    pageNum = int(link.text) if link.text.isdigit() else None
                    if pageNum != None:
                        urls_get.append(pageNum)

                #2. получаем данные со всех страниц:                         
                #for slug in range(1, urls_get[-1]):                             # мое добавление специально для express-shina  # c 1 по 2 станицы
                for slug in range(1, 2):
                    newUrl = url + f'?num={slug}'       #https://express-shina.ru/search/legkogruzovyie-shinyi?num=2
                    webdriverr.get(newUrl)
                    time.sleep(2)
                    webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)
                    soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                    products = soup.find_all('div', class_='b-offer')   

                    tyr_indexes_reg = ['\d{3}\/\d{3}[A-Za-z]',       #107/105R
                    '\d{2}[A-Za-z]\/\d{2}[A-Za-z]',
                    '\d{3}[A-Za-z]\/\d{2}[A-Za-z]',
                    '\d{2}[A-Za-z]\/\d{3}[A-Za-z]',
                    ]

                    for data_got in products:
                        tyre_title = str(data_got.find('a', class_='b-offer-main__title').text.replace('Легкогрузовая шина ', '').replace('новая', '')) 
                        tyre_rub_price = str(data_got.find('div', class_='b-offer-pay__price').text.replace('₽', '').replace(' ', '').replace('\xa0', ''))   
                        if tyre_title and tyre_rub_price:            
                            tyr_data_list = tyre_title.split(' ')   #  Royal Black Royal Winter UHP 255/40 R19 100V
                            len_list = len(tyr_data_list)
                            tyr_size = ''
                            tyr_size_index_first = ''
                            for some_data in tyr_data_list:
                                some_data_index = ''

                                for n in reg_list:
                                    some_data_index = tyr_data_list.index(some_data)
                                    if some_data_index > 1:
                                        prev_some_data = tyr_data_list[some_data_index-1]
                                        check_data = prev_some_data + some_data
                                        result = re.search(rf'{n}', check_data)
                                        if result:
                                            tyr_size = check_data
                                            tyr_size_index_first = tyr_data_list.index(prev_some_data) 
                                            tyr_size_index_last = tyr_data_list.index(some_data)
                                            break
                            tyr_producer = tyr_data_list[0]
                            tyr_model = ''
                            #print('tyr_size_index_firs ==== tyr_size_index_firs', tyr_size_index_first)

                            for some_dd in range(1, tyr_size_index_first):
                                tyr_model += tyr_data_list[some_dd] + ' '
                            tyr_group = 'легкогрузовая'

                            tyr_indexes = tyr_data_list[tyr_size_index_last+1]
                            for nn in tyr_indexes_reg:
                                result2 = re.search(rf'(?i){nn}', tyr_indexes)
                                if result2:
                                    #print('result2', result2, tyr_indexes)
                                    break
                                else:
                                    if len_list > tyr_size_index_last+2 or len_list == tyr_size_index_last+2:
                                        tyr_indexes = tyr_data_list[tyr_size_index_last+1 ] + tyr_data_list[tyr_size_index_last+2]

                        tyre_period = str(data_got.find('ul', class_='b-offer-main__parameters').text.replace('Наличие', ''))              # Сезон: ЗимаНаличие шипов: Нет
                        is_season = tyre_period.find('Сезон:')
                        is_spiky = tyre_period.find('Наличие шипов:')
                        if is_season:
                            #print('&&&')
                            if is_spiky:
                                obrezra = tyre_period.find('Сезон:') + 7
                                tyre_period1 = tyre_period[obrezra:].split(' ')
                                tyr_per = tyre_period1[0]
                                #print('tyr_per', tyr_per)
                                list_of_seasons = ['Зима', 'Лето']
                                if tyr_per in list_of_seasons:
                                    tyr_per = tyr_per 
                                else:
                                    tyr_per = ''
                            else:
                                obrezra = tyre_period.find('Сезон:') + 7
                                tyre_period1 = tyre_period[obrezra:].split(' ')
                                tyr_per = tyre_period1[0]
                                list_of_seasons = ['Зима', 'Лето']
                                if tyr_per in list_of_seasons:
                                    tyr_per = tyr_per 
                                else:
                                    tyr_per = ''  
                        if is_spiky:
                            obrezra = tyre_period.find('шипов: ') + 7
                            tyre_period2 = tyre_period[obrezra:].split(' ')
                            tyr_spike = tyre_period2[0]
                            #print('tyr_spike', tyr_spike)
                            list_of_spikes = ['Да', 'Нет']
                            if tyr_spike in list_of_spikes:
                                tyr_spike = tyr_spike
                            else:
                                tyr_spike = ''


                        #print(tyr_size, '=tyr_size', tyr_producer, '=tyr_producer', tyr_model, '=tyr_model', tyr_indexes, '=tyr_indexes', tyr_usabiity, '=tyr_usabiity', tyr_ply, '=tyr_ply')
                        goods_dict_express_shina[tyr_size, express_shina_good_num] = tyr_producer, tyr_model, tyr_indexes, tyr_group, tyre_rub_price, tyr_per, tyr_spike, 
                        express_shina_good_num += 1 

                for k, v in goods_dict_express_shina.items():
                    print(k, v, '!!!')

           #     3) парсинг спец шин
                url = 'https://express-shina.ru/search/spetcshinyi'       
                webdriverr = webdriver.Chrome()
                webdriverr.get(url)
                time.sleep(2)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                products = soup.find_all('div', class_='b-offer')      

                # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
                #1. получаем количество страниц:
                pages = soup.find('div', class_='b-paging__list')        
                urls_get = []
                links = pages.find_all('a', class_='b-paging__page') 
                for link in links:
                    pageNum = int(link.text) if link.text.isdigit() else None
                    if pageNum != None:
                        urls_get.append(pageNum)

                #2. получаем данные со всех страниц:                         
                #for slug in range(1, urls_get[-1]):                             # мое добавление специально для express-shina  # c 1 по 2 станицы
                for slug in range(1, 2):
                    newUrl = url + f'?num={slug}'       #https://express-shina.ru/search/spetcshinyi?num=4
                    webdriverr.get(newUrl)
                    time.sleep(2)
                    webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)
                    soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                    products = soup.find_all('div', class_='b-offer')   

                    tyr_indexes_reg = ['\d{3}\/\d{3}[A-Za-z]',       #107/105R
                    '\d{2}[A-Za-z]\/\d{2}[A-Za-z]',
                    '\d{3}[A-Za-z]\/\d{2}[A-Za-z]',
                    '\d{2}[A-Za-z]\/\d{3}[A-Za-z]',
                    ]

                    for data_got in products:
                        #print('data_got', data_got)
                        tyre_title = str(data_got.find('a', class_='b-offer-main__title').text.replace('Спецшина ', '').replace('новая', '')) 
                        #print(tyre_title)
                        tyre_rub_price = str(data_got.find('div', class_='b-offer-pay__price').text.replace('₽', '').replace(' ', '').replace('\xa0', ''))   
                        #print('tyre_rub_price ===', tyre_rub_price)
                        #print(tyre_title, ' ============',tyre_rub_price)
                        if tyre_title and tyre_rub_price:            # Волтайр Л-225 6R16 88/86A6 6PR  ============ 5720
                            tyr_data_list = tyre_title.split(' ')
                            tyr_size_index_in_list = None
                            for some_param in tyr_data_list:        #['Н.Камск', 'НК-240', '8.25R20', '130/128K', 'универсальная', '12PR', '']
                                for n in reg_list:
                                    result = re.search(rf'(?i){n}', some_param)
                                    if result:
                                        #print(result, 'result', tyr_data_list.index(some_param))
                                        tyr_size_index_in_list = tyr_data_list.index(some_param)
                                        break
                                if some_param == '':
                                    tyr_data_list.remove(some_param)
                            tyr_size = ''
                            tyr_producer = ''
                            tyr_group = ''
                            tyr_model = ''
                            len_list = len(tyr_data_list)
                            if tyr_size_index_in_list:
                                tyr_size = tyr_data_list[tyr_size_index_in_list]
                                tyr_producer = tyr_data_list[0] 
                                for n in range(1, tyr_size_index_in_list):
                                    tyr_model += tyr_data_list[n]
                                tyr_group = 'прочая'

                            if tyr_size_index_in_list:
                                tyr_indexes = tyr_data_list[tyr_size_index_in_list+1]
                                for nn in tyr_indexes_reg:
                                    result2 = re.search(rf'(?i){nn}', tyr_indexes)
                                    if result2:
                                        #print('result2', result2, tyr_indexes)
                                        break
                                    else:
                                        if len_list > tyr_size_index_in_list+2 or len_list == tyr_size_index_in_list+2:
                                            tyr_indexes = tyr_data_list[tyr_size_index_in_list+1] 
                            tyre_period = str(data_got.find('ul', class_='b-offer-main__parameters').text)              # Сезон: ЗимаНаличие шипов: Нет
                            if tyr_size == '':
                                pass
                            else:
                                goods_dict_express_shina[tyr_size, express_shina_good_num] = tyr_producer, tyr_model, tyr_indexes,  tyr_group,  tyre_rub_price
                            express_shina_good_num += 1 
                #for k, v in goods_dict_express_shina.items(): # СЛОВАРЬ ключи = типоразмер, номер в словаре, данные = производитель, модель, индексы, группа, цена
                #    print(k, v, '!!!')


                # формируем отдельный список ПРОИЗВОДИТЕЛИ:
                express_shina_companies_list = []  # список компаний-производителей express_shina
                for v in goods_dict_express_shina.values():
                    if v[0] and v[0].isdigit() is False:
                        express_shina_companies_list.append(v[0])
                express_shina_companies_list = list(set(express_shina_companies_list))  
                #print(express_shina_companies_list, 'express_shina_companies_list')

                chosen_by_company_dict = {}
                for k, v in goods_dict_express_shina.items():
                    if v[0] and v[0] in express_shina_companies_list:                 # СЕЙЧАС ВЫДАЕТ ВСЕХ ПРОИЗВОДИТЕЛЕЙ  ВСЕЮ ПРОДУКЦИЮ или подкинутых пользователем
                        chosen_by_company_dict[k] = v
                #print('chosen_by_company_dict', chosen_by_company_dict)

                # сопоставление с БД  и запись в БД конкурентов (express_shina):
                tyres_in_bd = tyres_models.Tyre.objects.all()
                for tyre in tyres_in_bd:
                    for k, v in chosen_by_company_dict.items():
                        #print(k, 'GGG', v, 'GGG', len(v))
                        if tyre.tyre_size.tyre_size == k[0]:
                            #print('TTTT', k)                                                                                            #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
                            coma = v[0].find(',')           
                            pr = None
                            name_competitor, created = dictionaries_models.CompetitorModel.objects.get_or_create(
                                competitor_name =  v[0]
                            )
                            #print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',  name_competitor, 'name_competitor =', v[0])
                            #if len(v) > 5 or len(v) == 5:
                            #    print(v[4])
                            #    if v[5] in ['Зима', 'Лето']:
                            #        if v[5][0] == 'Зима':
                            #            v[5][0] = 'зимние'
                            #        if v[5][0] == 'Лето':
                            #            v[5][0] = 'летние'
                            #    season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name=v[5]) 
                            #if season_usage:
                            #    season_usage = season_usage[0]
                            #else:
                            #    season_usage = None 
                            if coma and len(v) > 3:  #len(v[4]) == 5 :
                                pr = float(str(v[4]).replace(',', '.'))
                            models.CompetitorSiteModel.objects.update_or_create(
                                site = 'express-shina.ru',
                                currency = dictionaries_models.Currency.objects.get(currency='RUB'),
                                price = pr,
                                date_period = datetime.datetime.today(),
                                developer = name_competitor,
                                tyresize_competitor = k[0],                                               
                                name_competitor = v[1], 
                                parametres_competitor = v[2],                      
                                #season = season_usage
                                #tyre_to_compare = models.ComparativeAnalysisTyresModel.objects.get
                            )  
            except:
                pass                                                                                                                                                                                                       
            ###### END OF express-shina PARSING

           # 1 ###### ПАРСИНГ kolesatyt:
            try:
                kolesatyt_good_num = 0
                # 1) парсинг грузовых шин
                url = 'https://kolesatyt.ru/podbor/gruzovye-shiny/'       
                webdriverr = webdriver.Chrome()
                webdriverr.get(url)
                time.sleep(2)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                products = soup.find_all('div', class_='cat-item w-100 block-rel mob-item')      
                #print('products', products)


                # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
                #1. получаем количество страниц:
                pages = soup.find('ul', class_='pagination pagination-sm pagination-custom js-pager')        
                urls_get = []
                links = pages.find_all('a', class_='page-link')   
                for link in links:
                    pageNum = int(link.text) if link.text.isdigit() else None
                    if pageNum != None:
                        urls_get.append(pageNum)

                #2. получаем данные со всех страниц:                         
                #for slug in range(1, urls_get[-1]):                             # мое добавление специально для express-shina  # c 1 по 2 станицы
                for slug in range(1, 2):
                    newUrl = url + f'?PAGEN_1={slug}'       #https://kolesatyt.ru/podbor/gruzovye-shiny/?PAGEN_1=2
                    webdriverr.get(newUrl)
                    time.sleep(2)
                    webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)
                    soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                    products = soup.find_all('div', class_='cat-item w-100 block-rel mob-item') 

                    for data_got in products:
                        #print('data_got', data_got)
                        tyre_title = str(data_got.find('span', class_='text-uppercase').text)       #.text.replace('Легкогрузовая шина ', '').replace('новая', '')
                        #print(tyre_title)
                        tyre_rub_price = str(data_got.find('div', class_='txt-bigger w-100 price').text) #.replace('₽', '').replace(' ', '').replace('\xa0', ''))   
                        season = str(data_got.find('div', class_='catalog-item__season-icons d-flex flex-column')) # !!!!!!!!!!!!!!
                        #print('season', season)
                        brand = str(data_got.find('span', class_='catalog-item__brand').text) 
                        #print('brand', brand)
                        #print(tyre_title, ' ============',tyre_rub_price, '====', season, '======', brand)
                        if tyre_title and tyre_rub_price:            # Грузовая шина Н.Камск CRG VM-201 8.25R20 130/128K универсальная 12PR новая  ============ 13870 
                            tyr_size = tyre_title
                            tyre_rub_price = tyre_rub_price
                            got_data = brand.replace('\n', ' ').replace('\t', ' ').split(' ')
                            #print('got_data', got_data)
                            list_remaked_data_no_whites = []
                            for nn in got_data:
                                if nn == ' ' or nn == '':
                                    pass
                                else:
                                    list_remaked_data_no_whites.append(nn)
                            #print('list_remaked_data_no_whites', list_remaked_data_no_whites)
                            tyr_producer = ''
                            tyr_model = ''
                            for nnn in list_remaked_data_no_whites:
                                if list_remaked_data_no_whites.index(nnn) == 0:
                                    tyr_producer = nnn
                                else:
                                    tyr_model += nnn + ' '
                            tyr_group = 'легковые'
                        #print ('tyr_size = ', tyr_size, 'tyre_rub_price = ', tyre_rub_price, 'tyr_producer = ', tyr_producer, 'tyr_model = ', tyr_model, 'tyr_group = ', tyr_group )

                        #print(tyr_size, '=tyr_size', tyr_producer, '=tyr_producer', tyr_model, '=tyr_model', tyr_indexes, '=tyr_indexes', tyr_usabiity, '=tyr_usabiity', tyr_ply, '=tyr_ply')
                        #goods_dict_kolesatyt[tyr_size, kolesatyt_good_num] = tyr_producer, tyr_model, tyr_indexes, tyr_group,  tyre_rub_price, tyr_usabiity,  tyr_ply
                        goods_dict_kolesatyt[tyr_size, kolesatyt_good_num] = tyr_producer, tyr_model,  tyr_group,  tyre_rub_price
                        kolesatyt_good_num += 1 

                #for k, v in goods_dict_kolesatyt.items():
                #    print(k, v)


                # 2) парсинг легковых шин
                url = 'https://kolesatyt.ru/podbor/shiny/type-car/'       
                webdriverr = webdriver.Chrome()
                webdriverr.get(url)
                time.sleep(2)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                products = soup.find_all('div', class_='cat-item w-100 block-rel mob-item')      
                #print('products', products)


                # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
                #1. получаем количество страниц:
                pages = soup.find('ul', class_='pagination pagination-sm pagination-custom js-pager')        
                urls_get = []
                links = pages.find_all('a', class_='page-link')   
                for link in links:
                    pageNum = int(link.text) if link.text.isdigit() else None
                    if pageNum != None:
                        urls_get.append(pageNum)

                #2. получаем данные со всех страниц:                         
                #for slug in range(1, urls_get[-1]):                             # мое добавление специально для express-shina  # c 1 по 2 станицы
                for slug in range(1, 2):
                    newUrl = url + f'?PAGEN_1={slug}'       #https://kolesatyt.ru/podbor/gruzovye-shiny/?PAGEN_1=2
                    webdriverr.get(newUrl)
                    time.sleep(2)
                    webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)
                    soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                    products = soup.find_all('div', class_='cat-item w-100 block-rel mob-item') 

                    for data_got in products:
                        #print('data_got', data_got)
                        tyre_title = str(data_got.find('span', class_='text-uppercase').text)       #.text.replace('Легкогрузовая шина ', '').replace('новая', '')
                        #print(tyre_title)
                        tyre_rub_price = str(data_got.find('div', class_='txt-bigger w-100 price').text) #.replace('₽', '').replace(' ', '').replace('\xa0', ''))   
                        season = str(data_got.find('div', class_='catalog-item__season-icons d-flex flex-column')) # !!!!!!!!!!!!!!
                        #print('season', season)
                        brand = str(data_got.find('span', class_='catalog-item__brand').text.replace('Шина', '')) 
                        #print('brand', brand)
                        #print(tyre_title, ' ============',tyre_rub_price, '====', season, '======', brand)
                        if tyre_title and tyre_rub_price:            # Грузовая шина Н.Камск CRG VM-201 8.25R20 130/128K универсальная 12PR новая  ============ 13870 
                            tyr_size = tyre_title
                            tyre_rub_price = tyre_rub_price
                            got_data = brand.replace('\n', ' ').replace('\t', ' ').split(' ')
                            #print('got_data', got_data)
                            list_remaked_data_no_whites = []
                            for nn in got_data:
                                if nn == ' ' or nn == '':
                                    pass
                                else:
                                    list_remaked_data_no_whites.append(nn)
                            #print('list_remaked_data_no_whites', list_remaked_data_no_whites)
                            tyr_producer = ''
                            tyr_model = ''
                            for nnn in list_remaked_data_no_whites:
                                if list_remaked_data_no_whites.index(nnn) == 0:
                                    tyr_producer = nnn
                                else:
                                    tyr_model += nnn + ' '
                            tyr_group = 'грузовые'
                        #print ('tyr_size = ', tyr_size, 'tyre_rub_price = ', tyre_rub_price, 'tyr_producer = ', tyr_producer, 'tyr_model = ', tyr_model, 'tyr_group = ', tyr_group )

                        #print(tyr_size, '=tyr_size', tyr_producer, '=tyr_producer', tyr_model, '=tyr_model', tyr_indexes, '=tyr_indexes', tyr_usabiity, '=tyr_usabiity', tyr_ply, '=tyr_ply')
                        #goods_dict_kolesatyt[tyr_size, kolesatyt_good_num] = tyr_producer, tyr_model, tyr_indexes, tyr_group,  tyre_rub_price, tyr_usabiity,  tyr_ply
                        goods_dict_kolesatyt[tyr_size, kolesatyt_good_num] = tyr_producer, tyr_model,  tyr_group,  tyre_rub_price
                        kolesatyt_good_num += 1 

                #for k, v in goods_dict_kolesatyt.items():
                #    print(k, v)

                # 3) парсинг легкогрузовых шин
                url = 'https://kolesatyt.ru/podbor/shiny/type-light-truck/'       
                webdriverr = webdriver.Chrome()
                webdriverr.get(url)
                time.sleep(2)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                products = soup.find_all('div', class_='cat-item w-100 block-rel mob-item')      
                #print('products', products)


                # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
                #1. получаем количество страниц:
                pages = soup.find('ul', class_='pagination pagination-sm pagination-custom js-pager')        
                urls_get = []
                links = pages.find_all('a', class_='page-link')   
                for link in links:
                    pageNum = int(link.text) if link.text.isdigit() else None
                    if pageNum != None:
                        urls_get.append(pageNum)

                #2. получаем данные со всех страниц:                         
                #for slug in range(1, urls_get[-1]):                             # мое добавление специально для express-shina  # c 1 по 2 станицы
                for slug in range(1, 2):
                    newUrl = url + f'?PAGEN_1={slug}'       #https://kolesatyt.ru/podbor/gruzovye-shiny/?PAGEN_1=2
                    webdriverr.get(newUrl)
                    time.sleep(2)
                    webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)
                    soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                    products = soup.find_all('div', class_='cat-item w-100 block-rel mob-item') 

                    for data_got in products:
                        #print('data_got', data_got)
                        tyre_title = str(data_got.find('span', class_='text-uppercase').text)       #.text.replace('Легкогрузовая шина ', '').replace('новая', '')
                        #print(tyre_title)
                        tyre_rub_price = str(data_got.find('div', class_='txt-bigger w-100 price').text) #.replace('₽', '').replace(' ', '').replace('\xa0', ''))   
                        season = str(data_got.find('div', class_='catalog-item__season-icons d-flex flex-column')) # !!!!!!!!!!!!!!
                        #print('season', season)
                        brand = str(data_got.find('span', class_='catalog-item__brand').text.replace('Шина', '')) 
                        #print('brand', brand)
                        #print(tyre_title, ' ============',tyre_rub_price, '====', season, '======', brand)
                        if tyre_title and tyre_rub_price:            # Грузовая шина Н.Камск CRG VM-201 8.25R20 130/128K универсальная 12PR новая  ============ 13870 
                            tyr_size = tyre_title
                            tyre_rub_price = tyre_rub_price
                            got_data = brand.replace('\n', ' ').replace('\t', ' ').split(' ')
                            #print('got_data', got_data)
                            list_remaked_data_no_whites = []
                            for nn in got_data:
                                if nn == ' ' or nn == '':
                                    pass
                                else:
                                    list_remaked_data_no_whites.append(nn)
                            #print('list_remaked_data_no_whites', list_remaked_data_no_whites)
                            tyr_producer = ''
                            tyr_model = ''
                            for nnn in list_remaked_data_no_whites:
                                if list_remaked_data_no_whites.index(nnn) == 0:
                                    tyr_producer = nnn
                                else:
                                    tyr_model += nnn + ' '
                            tyr_group = 'легкогруз'
                        #print ('tyr_size = ', tyr_size, 'tyre_rub_price = ', tyre_rub_price, 'tyr_producer = ', tyr_producer, 'tyr_model = ', tyr_model, 'tyr_group = ', tyr_group )

                        #print(tyr_size, '=tyr_size', tyr_producer, '=tyr_producer', tyr_model, '=tyr_model', tyr_indexes, '=tyr_indexes', tyr_usabiity, '=tyr_usabiity', tyr_ply, '=tyr_ply')
                        #goods_dict_kolesatyt[tyr_size, kolesatyt_good_num] = tyr_producer, tyr_model, tyr_indexes, tyr_group,  tyre_rub_price, tyr_usabiity,  tyr_ply
                        goods_dict_kolesatyt[tyr_size, kolesatyt_good_num] = tyr_producer, tyr_model,  tyr_group,  tyre_rub_price
                        kolesatyt_good_num += 1 

                #for k, v in goods_dict_kolesatyt.items():           # ('295/35R23', 30) ('HANKOOK', 'Winter I*cept evo2 W320A ', 'грузовые', '65 000')
                #    print(k, v)

                # формируем отдельный список ПРОИЗВОДИТЕЛИ:
                kolesatyt_companies_list = []  # список компаний-производителей kolesatyt
                for v in goods_dict_kolesatyt.values():
                    if v[0] and v[0].isdigit() is False:
                        kolesatyt_companies_list.append(v[0])
                kolesatyt_companies_list = list(set(kolesatyt_companies_list))  
                #print(kolesatyt_companies_list, 'kolesatyt_companies_list')

                chosen_by_company_dict = {}
                for k, v in goods_dict_kolesatyt.items():
                    if v[0] and v[0] in kolesatyt_companies_list:                 # СЕЙЧАС ВЫДАЕТ ВСЕХ ПРОИЗВОДИТЕЛЕЙ  ВСЕЮ ПРОДУКЦИЮ или подкинутых пользователем
                        chosen_by_company_dict[k] = v
                #print('chosen_by_company_dict', chosen_by_company_dict)

                # сопоставление с БД  и запись в БД конкурентов (kolesatyt):
                tyres_in_bd = tyres_models.Tyre.objects.all()
                for tyre in tyres_in_bd:
                    for k, v in chosen_by_company_dict.items():
                        #print(k, 'GGG', v, 'GGG', len(v))
                        if tyre.tyre_size.tyre_size == k[0]:
                            #print('TTTT', k)                                                                                            #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
                            coma = v[3].find(',')           
                            pr = None
                            name_competitor, created = dictionaries_models.CompetitorModel.objects.get_or_create(
                                competitor_name =  v[0]
                            )
                            #print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',  name_competitor, 'name_competitor =', v[0])
                            #if len(v) > 5 or len(v) == 5:
                            #    print(v[4])
                            #    if v[5] in ['Зима', 'Лето']:
                            #        if v[5][0] == 'Зима':
                            #            v[5][0] = 'зимние'
                            #        if v[5][0] == 'Лето':
                            #            v[5][0] = 'летние'
                            #    season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name=v[5]) 
                            #if season_usage:
                            #    season_usage = season_usage[0]
                            #else:
                            #    season_usage = None 
                            if coma and len(v) > 3:  #len(v[4]) == 5 :
                                pr = float(str(v[3]).replace(',', '.').replace(' ', ''))
                            models.CompetitorSiteModel.objects.update_or_create(
                                site = 'kolesatyt.ru',
                                currency = dictionaries_models.Currency.objects.get(currency='RUB'),
                                price = pr,
                                date_period = datetime.datetime.today(),
                                developer = name_competitor,
                                tyresize_competitor = k[0],                                               
                                name_competitor = v[1], 
                                parametres_competitor = v[2],                      
                                #season = season_usage
                                #tyre_to_compare = models.ComparativeAnalysisTyresModel.objects.get
                            )  
            except:
                pass                                                                                                                                                                                                       
            ###### END OF kolesatyt

           # 1 ###### ПАРСИНГ KOLESA_DAROM:       kolesa-darom.ru     
            try:     
                kolesa_darom_good_num = 0
                # 1) парсинг легковых зимних шин
                url = 'https://www.kolesa-darom.ru/catalog/avto/shiny/zima/'       
                webdriverr = webdriver.Chrome()
                webdriverr.get(url)
                time.sleep(2)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                products = soup.find_all('div', class_='product-card__wrapper')      
                #print('products', products)

                # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
                #1. получаем количество страниц:
                pages = soup.find('ul', class_='main-section__pagination pagination')        
                urls_get = []
                links = pages.find_all('li', class_='pagination__item')   
                for link in links:
                    pageNum = int(link.text) if link.text.isdigit() else None
                    if pageNum != None:
                        urls_get.append(pageNum)#
                #2. получаем данные со всех страниц:                         
                #for slug in range(1, urls_get[-1]):                             # мое добавление специально для express-shina  # c 1 по 2 станицы
                for slug in range(1, 2):
                    newUrl = url + f'nav/page-{slug}/'       #https://www.kolesa-darom.ru/catalog/avto/shiny/zima/nav/page-2/
                    webdriverr.get(newUrl)
                    time.sleep(2)
                    webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)
                    soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                    products = soup.find_all('div', class_='product-card__wrapper')  
                    for data_got in products:
                        #print('data_got', data_got)
                        tyre_title = str(data_got.find('p', class_='product-card-properties__title').text.replace('tyre_rub_price', ' '))     
                        #print(tyre_title)
                        tyre_rub_price = str(data_got.find('button', 'product-card__button kd-btn kd-btn--small kd-btn--flex kd-btn_primary').text.replace('₽', '').replace(' ', ''))#.replace('\xa0', ''))   
                        tyr_size_data1 = str(data_got.find('ul', class_='product-card-properties__group product-card-properties__group--full-width product-card-properties__group--chips kd-chips').text) # !!!!!!!!!!!!!!
                        #print('tyre_title', tyre_title, 'tyre_rub_price', tyre_rub_price, 'tyr_size', tyr_size_data1)
                        tyr_model = ''
                        tyr_group = ''
                        tyr_season = ''
                        tyr_indexes = ''
                        tyr_size = ''
                        tyr_producer = ''
                        list_of_prod_names = ['Ling', 'Nokian', 'Royal', 'Киров']
                        if tyre_title and tyre_rub_price:            
                            tyre_title = tyre_title.split(' ')
                            t_prod_n = tyre_title[0]
                            t_index = 0
                            if t_prod_n in list_of_prod_names:
                                tyr_producer = tyre_title[0] + tyre_title[1]
                                t_index = 1
                            else:
                                tyr_producer = tyre_title[0]
                            llen = len(tyr_producer)
                            for tt in tyre_title[t_index+1 : llen]:
                                tyr_model += tt
                            tyr_size_data1 = tyr_size_data1.split(' ')
                            for kk in tyr_size_data1[0 : 3]:
                                if tyr_size_data1.index(kk) == 1:
                                    tyr_size = tyr_size + '/'                        
                                tyr_size += kk
                            tyr_size_len = len(tyr_size)
                            if tyr_size[tyr_size_len-1] == 'C':
                                tyr_group = 'легкогруз'
                            else:
                                tyr_group = 'легковые'
                            tyr_season = 'зимние'
                            for ii in reversed(tyr_size_data1[3 : ]):
                                tyr_indexes += ii
                        #goods_dict_kolesa_darom[tyr_size, kolesa_darom_good_num] = tyr_producer, tyr_model, tyr_indexes, tyr_group,  tyre_rub_price, tyr_season,  tyr_ply       #('195/60R15', 39) ('Nokian', 'Tyres7', '92T', 'легковая', '5380', 'Зима', 'Да') !!!
                        goods_dict_kolesa_darom[tyr_size, kolesa_darom_good_num] = tyr_producer, tyr_model, tyr_indexes, tyr_group, tyre_rub_price, tyr_season
                        kolesa_darom_good_num += 1 

                #for k, v in goods_dict_kolesa_darom.items():           # ('235 65 R17 ', 16) ('Goodyear', 'UltraGrip Ice Gen-1 SUV ', 'T 108  ', 'легковые', '11000', 'зимние')
                #    print(k, v)

                # 2) парсинг легковых летних шин
                url = 'https://www.kolesa-darom.ru/catalog/avto/shiny/leto/'       
                webdriverr = webdriver.Chrome()
                webdriverr.get(url)
                time.sleep(2)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                products = soup.find_all('div', class_='product-card__wrapper')      
                #print('products', products)

                # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
                #1. получаем количество страниц:
                pages = soup.find('ul', class_='main-section__pagination pagination')        
                urls_get = []
                links = pages.find_all('li', class_='pagination__item')   
                for link in links:
                    pageNum = int(link.text) if link.text.isdigit() else None
                    if pageNum != None:
                        urls_get.append(pageNum)#
                #2. получаем данные со всех страниц:                         
                #for slug in range(1, urls_get[-1]):                             # мое добавление специально для express-shina  # c 1 по 2 станицы
                for slug in range(1, 2):
                    newUrl = url + f'nav/page-{slug}/'       #https://www.kolesa-darom.ru/catalog/avto/shiny/zima/nav/page-2/
                    webdriverr.get(newUrl)
                    time.sleep(2)
                    webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)
                    soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                    products = soup.find_all('div', class_='product-card__wrapper')  
                    for data_got in products:
                        #print('data_got', data_got)
                        tyre_title = str(data_got.find('p', class_='product-card-properties__title').text.replace('tyre_rub_price', ' '))     
                        #print(tyre_title)
                        tyre_rub_price = str(data_got.find('button', 'product-card__button kd-btn kd-btn--small kd-btn--flex kd-btn_primary').text.replace('₽', '').replace(' ', ''))#.replace('\xa0', ''))   
                        tyr_size_data1 = str(data_got.find('ul', class_='product-card-properties__group product-card-properties__group--full-width product-card-properties__group--chips kd-chips').text) # !!!!!!!!!!!!!!
                        #print('tyre_title', tyre_title, 'tyre_rub_price', tyre_rub_price, 'tyr_size', tyr_size_data1)
                        tyr_model = ''
                        tyr_group = ''
                        tyr_season = ''
                        tyr_indexes = ''
                        tyr_size = ''
                        tyr_producer = ''
                        list_of_prod_names = ['Ling', 'Nokian', 'Royal', 'Киров']
                        if tyre_title and tyre_rub_price:            
                            tyre_title = tyre_title.split(' ')
                            t_prod_n = tyre_title[0]
                            t_index = 0
                            if t_prod_n in list_of_prod_names:
                                tyr_producer = tyre_title[0] + tyre_title[1]
                                t_index = 1
                            else:
                                tyr_producer = tyre_title[0]
                            llen = len(tyr_producer)
                            for tt in tyre_title[t_index+1 : llen]:
                                tyr_model += tt
                            tyr_size_data1 = tyr_size_data1.split(' ')
                            for kk in tyr_size_data1[0 : 3]:
                                if tyr_size_data1.index(kk) == 1:
                                    tyr_size = tyr_size + '/'                        
                                tyr_size += kk
                            tyr_size_len = len(tyr_size)
                            if tyr_size[tyr_size_len-1] == 'C':
                                tyr_group = 'легкогруз'
                            else:
                                tyr_group = 'легковые'
                            tyr_season = 'летние'
                            for ii in reversed(tyr_size_data1[3 : ]):
                                tyr_indexes += ii
                        #goods_dict_kolesa_darom[tyr_size, kolesa_darom_good_num] = tyr_producer, tyr_model, tyr_indexes, tyr_group,  tyre_rub_price, tyr_season,  tyr_ply       #('195/60R15', 39) ('Nokian', 'Tyres7', '92T', 'легковая', '5380', 'Зима', 'Да') !!!
                        goods_dict_kolesa_darom[tyr_size, kolesa_darom_good_num] = tyr_producer, tyr_model, tyr_indexes, tyr_group, tyre_rub_price, tyr_season
                        kolesa_darom_good_num += 1 

                #for k, v in goods_dict_kolesa_darom.items():           # ('225/65R16C', 39) ('LingLong', 'Green-MaxVAN', '112R', 'легкогруз', '6590', 'летние'
                #    print(k, v)
            except:
                pass



        # формируем отдельный список ПРОИЗВОДИТЕЛИ:
        kolesa_darom_companies_list = []  # список компаний-производителей kolesa_darom
        for v in goods_dict_kolesa_darom.values():
            if v[0] and v[0].isdigit() is False:
                kolesa_darom_companies_list.append(v[0])
        kolesa_darom_companies_list = list(set(kolesa_darom_companies_list))  
        #print(kolesa_darom_companies_list, 'kolesa_darom_companies_list')

        chosen_by_company_dict = {}
        for k, v in goods_dict_kolesa_darom.items():
            if v[0] and v[0] in kolesa_darom_companies_list:                 # СЕЙЧАС ВЫДАЕТ ВСЕХ ПРОИЗВОДИТЕЛЕЙ  ВСЕЮ ПРОДУКЦИЮ или подкинутых пользователем
                chosen_by_company_dict[k] = v
        #print('chosen_by_company_dict', chosen_by_company_dict)

        # сопоставление с БД  и запись в БД конкурентов (kolesa_darom):
        tyres_in_bd = tyres_models.Tyre.objects.all()
        for tyre in tyres_in_bd:
            for k, v in chosen_by_company_dict.items():
                #print(k, 'GGG', v, 'GGG', len(v))
                if tyre.tyre_size.tyre_size == k[0]:
                    #print('TTTT', k)                                                                                            #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
                    coma = v[4].find(',')           
                    pr = None
                    name_competitor, created = dictionaries_models.CompetitorModel.objects.get_or_create(
                        competitor_name =  v[0]
                    )
                    #print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',  name_competitor, 'name_competitor =', v[0])     # ('225/65R16C', 39) ('LingLong', 'Green-MaxVAN', '112R', 'легкогруз', '6590', 'летние')
                    #if len(v) > 5 or len(v) == 5:
                    #    print(v[4])
                    #    if v[5] in ['зимние', 'летние']:
                    #        if v[5][0] == 'зимние':
                    #            v[5][0] = 'зимние'
                    #        if v[5][0] == 'летние':
                    #            v[5][0] = 'летние'
                    #    season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name=v[5]) 
                    #if season_usage:
                    #    season_usage = season_usage[0]
                    #else:
                    #    season_usage = None 
                    if coma and len(v) > 3:  #len(v[4]) == 5 :
                        pr = float(str(v[4]).replace(',', '.').replace(' ', ''))
                    models.CompetitorSiteModel.objects.update_or_create(
                        site = 'kolesa-darom.ru',
                        currency = dictionaries_models.Currency.objects.get(currency='RUB'),
                        price = pr,
                        date_period = datetime.datetime.today(),
                        developer = name_competitor,
                        tyresize_competitor = k[0],                                               
                        name_competitor = v[1], 
                        parametres_competitor = v[2],                      
                        #season = season_usage
                        #tyre_to_compare = models.ComparativeAnalysisTyresModel.objects.get
                    )                                            

        ###### END OF KOLESA_DAROM

        return comparative_analysis_table

    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        obj = context.get('object')

        my_tags.currency_on_date()                  # ДЛЯ ПОЛУЧЕНИЯ ВАЛЮТЫ ПО КУРСУ НБ РБ НА ДАТУ

        #### 0 подбор шин с их данными по минималкам для отображения в таблице на определенный период (не конкуренты , а именно собственная продукция)Ж          
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:  
            # для поиска по собственной продукции с ходом в шаг = месяц       
            date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()                 # ['2023-01-23']
            year_to_look = date_filter.year
            month_to_look = date_filter.month
            #aRRRRR = obj.comparative_table.filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
            #print('aRRRRR', aRRRRR)
            # для поиска по кнкурентампродукции с ходом в шаг = день  
            all_competitors = models.CompetitorSiteModel.objects.filter(site='onliner.by').filter(date_period=date_filter)
        else:
        # 00.1  выборка всех имеющихся периодов с минималками:
            get_all_dates_year_month = obj.comparative_table.dates('sale_data', 'month')
            if get_all_dates_year_month:
                oldest_date = min(get_all_dates_year_month)
                latesr_date = max(get_all_dates_year_month)

                year_to_look = latesr_date.year
                month_to_look = latesr_date.month
        ####

        # ФИЛЬТР ПО СОБСТВЕННОЙ ПРОДУКЦИИ:   
        if models.SELF_PRODUCTION:                                                  # если пользователем введены (выбраны) шины:
            id_list = []
            for n in models.SELF_PRODUCTION:
                if n.isdigit():                                 
                    comparativeanalisystyre_object_id = int(n)
                    id_list.append(comparativeanalisystyre_object_id)
            list_of_tyre_comparative_objects = obj.comparative_table.all().filter(id__in=id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
            #print('list_of_tyre_comparative_objects', list_of_tyre_comparative_objects)   
        elif models.SELF_PRODUCTION_ALL:
            list_of_tyre_comparative_objects = obj.comparative_table.all().filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
        else:     
            list_of_tyre_comparative_objects = obj.comparative_table.all().filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
        # если пользовательищет через поисковик:
        if models.SEARCH_USER_REQUEST:
            user_requested_data = models.SEARCH_USER_REQUEST  
            search_result = obj.comparative_table.filter(Q(tyre__tyre_model__model__in=user_requested_data) | Q(tyre__tyre_size__tyre_size__in=user_requested_data))
            #print('search_result', search_result)
            if search_result:
                list_of_tyre_comparative_objects = search_result

        # ФИЛЬТР ПО ГРУППАМ ШИН:    
        if models.TYRE_GROUPS:                                                  # если пользователем введены (выбраны) шины:
            group_id_list = []
            for n in models.TYRE_GROUPS:
                if n.isdigit():                                 
                    gr_id = int(n)
                    group_id_list.append(gr_id)
            existing_val_check = obj.comparative_table.all().filter(tyre__tyre_group__id__in=group_id_list).filter(id__in=id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
            if existing_val_check:
                list_of_tyre_comparative_objects = obj.comparative_table.all().filter(tyre__tyre_group__id__in=group_id_list).filter(id__in=id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
                #print('list_of_tyre_comparative_objects', 'JJ', list_of_tyre_comparative_objects) 
            else:  
                #print('АШЫПКА!!!')
                pass
        elif models.TYRE_GROUPS_ALL:
            #group_id_list = dictionaries_models.TyreGroupModel.objects.values_list('id', flat=True)                        ####### !!!  это ПРАВИЛЬНЫЙ ВАРИАНТ ВЫБОРА ВСЕХ ГРУУПП ШИН, НО ТАК КАК НЕ У ВСЕХ ШИН ПРОПИСАНА ГРУППА _ ТО ПРИДЕТСЯ ПРОСТО ВСЕ ШИНЫ В ПОБОР
            #list_of_tyre_comparative_objects = obj.comparative_table.all().filter(tyre__tyre_group__id__in=group_id_list)  ####### !!!  это ПРАВИЛЬНЫЙ ВАРИАНТ ВЫБОРА ВСЕХ ГРУУПП ШИН, НО ТАК КАК НЕ У ВСЕХ ШИН ПРОПИСАНА ГРУППА _ ТО ПРИДЕТСЯ ПРОСТО ВСЕ ШИНЫ В ПОБОР
            list_of_tyre_comparative_objects = obj.comparative_table.all()                                                  ####### !!!  ПРОСТО ВСЕ ШИНЫ В ПОБОР

    #    ################# 1 фильтр конкурентов:

        ##  фильтр конкурентов EXPRESS_SHINA:
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:         
            date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()                 # ['2023-01-23']
            all_competitors = models.CompetitorSiteModel.objects.filter(site='express-shina.ru').filter(date_period=date_filter)
        else:
            all_competitors = models.CompetitorSiteModel.objects.filter(site='express-shina.ru')
        #print(all_competitors , 'all_competitors ')
            # 1.2 ФИЛЬТР список производителей :
        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        express_shina_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
    #        object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
    #        object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            if models.EXPRESS_SHINA_COMPETITORS:
                if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
                    date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                    for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.EXPRESS_SHINA_COMPETITORS, site='express-shina.ru').filter(date_period=date_filter):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            list_of_matched_competitors.append(competitor)
   ##                if len(list_of_matched_competitors) > 3:
                        express_shina_competitors_dict1[object_unit.tyre] = list_of_matched_competitors[0 : 3]
                    else:
                        express_shina_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                else:
                    for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.EXPRESS_SHINA_COMPETITORS, site='express-shina.ru'):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            list_of_matched_competitors.append(competitor)
                    if len(list_of_matched_competitors) > 3:
                        express_shina_competitors_dict1[object_unit.tyre] = list_of_matched_competitors[0 : 3]
                    else:
                        express_shina_competitors_dict1[object_unit.tyre] = list_of_matched_competitors                    
            else:
                for competitor in all_competitors[0 : 3]:                                                                                                           ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                        #print("На пол шишечки", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                        list_of_matched_competitors.append(competitor)
                express_shina_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
        #print('express_shina_competitors_dict1', express_shina_competitors_dict1)
   ##   ######  НАДО СФОРМИРОВАТЬ СЛОВАРЬ С НЕСКОЛЬКИМИ КОНКУРЕНТАМИя 05.12.2022
            models.EXPRESS_SHINA_COMPETITORS_DICTIONARY1 = express_shina_competitors_dict1  
            object_unit.express_shina_competitor_on_date1()                       ###!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   ##   ## ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ EXPRESS_SHINA: 
        express_shina_max_lengh_list = []
        for object_unit in list_of_tyre_comparative_objects:
            obj_num = len(object_unit.express_shina_competitor_on_date1() )
            express_shina_max_lengh_list.append(obj_num)
        if express_shina_max_lengh_list:
            express_shina_max_lengh_header = max(express_shina_max_lengh_list)
        else:
            express_shina_max_lengh_header = 0
        models.EXPRESS_SHINA_HEADER_NUMBER = express_shina_max_lengh_header
        #print('models.EXPRESS_SHINA_HEADER_NUMBER', models.EXPRESS_SHINA_HEADER_NUMBER)
        # print('EXPRESS_SHINA_HEADER_NUMBER ====+++==', models.EXPRESS_SHINA_HEADER_NUMBER_COMPETITORS_NAMES_FILTER)

        obj.express_shina_heders_value()
        obj.express_shina_heders_lengt()
        #object_unit.express_shina_competitor_on_date1()
        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects
        #print('bagoria', context['list_of_tyre_comparative_objects'])

        ###### END EXPRESS_SHINA


        ##  фильтр конкурентов KOLESATYT: 
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:         
            date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()                 # ['2023-01-23']
            all_competitors = models.CompetitorSiteModel.objects.filter(site='kolesatyt.ru').filter(date_period=date_filter)
        else:
            all_competitors = models.CompetitorSiteModel.objects.filter(site='kolesatyt.ru')
        #print(all_competitors , 'all_competitors ')
            # 1.2 ФИЛЬТР список производителей :
        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        kolesatyt_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
    #        object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
    #        object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            if models.KOLESATYT_COMPETITORS:
                if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
                    date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                    for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.KOLESATYT_COMPETITORS, site='kolesatyt.ru').filter(date_period=date_filter):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            list_of_matched_competitors.append(competitor)

                    if len(list_of_matched_competitors) > 3:
                        kolesatyt_competitors_dict1[object_unit.tyre] = list_of_matched_competitors[0 : 3]
                    else:
                        kolesatyt_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                else:
                    for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.EXPRESS_SHINA_COMPETITORS, site='kolesatyt.ru'):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            list_of_matched_competitors.append(competitor)
                    if len(list_of_matched_competitors) > 3:
                        kolesatyt_competitors_dict1[object_unit.tyre] = list_of_matched_competitors[0 : 3]
                    else:
                        kolesatyt_competitors_dict1[object_unit.tyre] = list_of_matched_competitors                    
            else:
                for competitor in all_competitors[0 : 3]:                                                                                                           ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                        #print("На пол шишечки", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                        list_of_matched_competitors.append(competitor)
                kolesatyt_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
        #print('kolesatyt_competitors_dict1', kolesatyt_competitors_dict1)

       ######  НАДО СФОРМИРОВАТЬ СЛОВАРЬ С НЕСКОЛЬКИМИ КОНКУРЕНТАМИя 05.12.2022
            models.KOLESATYT_COMPETITORS_DICTIONARY1 = kolesatyt_competitors_dict1 
            object_unit.kolesatyt_competitor_on_date1()                      ###!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ('175/65R15', 20) ('Pirelli', 'CinturatoP1Verde', '84H', 'легковые', '4690', 'летние')

       ## ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ KOLESATYT: 
        kolesatyt_max_lengh_list = []
        for object_unit in list_of_tyre_comparative_objects:
            obj_num = len(object_unit.kolesatyt_competitor_on_date1())
            kolesatyt_max_lengh_list.append(obj_num)
        if kolesatyt_max_lengh_list:
            kolesatyt_max_lengh_header = max(kolesatyt_max_lengh_list)
        else:
            kolesatyt_max_lengh_header = 0

        models.KOLESATYT_HEADER_NUMBER = express_shina_max_lengh_header
        #print('models.EXPRESS_SHINA_HEADER_NUMBER', models.EXPRESS_SHINA_HEADER_NUMBER)
        # print('EXPRESS_SHINA_HEADER_NUMBER ====+++==', models.EXPRESS_SHINA_HEADER_NUMBER_COMPETITORS_NAMES_FILTER)

        obj.kolesatyt_heders_value()
        obj.kolesatyt_heders_lengt()
        #object_unit.kolesatyt_competitor_on_date1()
        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects

        ###### END KOLESATYT


        ##  фильтр конкурентов KOLESA_DAROM: 
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:         
            date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()                 # ['2023-01-23']
            all_competitors = models.CompetitorSiteModel.objects.filter(site='kolesa-darom.ru').filter(date_period=date_filter)
        else:
            all_competitors = models.CompetitorSiteModel.objects.filter(site='kolesa-darom.ru')
        #print(all_competitors , 'all_competitors ')
            # 1.2 ФИЛЬТР список производителей :
        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        kolesa_darom_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
    #        object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
    #        object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            if models.KOLESA_DAROM_COMPETITORS:
                if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
                    date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                    for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.KOLESATYT_COMPETITORS, site='kolesa-darom.ru').filter(date_period=date_filter):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            list_of_matched_competitors.append(competitor)

                    if len(list_of_matched_competitors) > 3:
                        kolesa_darom_competitors_dict1[object_unit.tyre] = list_of_matched_competitors[0 : 3]
                    else:
                        kolesa_darom_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                else:
                    for competitor in models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.KOLESA_DAROM_COMPETITORS, site='kolesa-darom.ru'):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            list_of_matched_competitors.append(competitor)
                    if len(list_of_matched_competitors) > 3:
                        kolesa_darom_competitors_dict1[object_unit.tyre] = list_of_matched_competitors[0 : 3]
                    else:
                        kolesa_darom_competitors_dict1[object_unit.tyre] = list_of_matched_competitors                    
            else:
                for competitor in all_competitors[0 : 3]:                                                                                                           ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                        #print("На пол шишечки", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                        list_of_matched_competitors.append(competitor)
                kolesa_darom_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
        #print('kolesa_darom_competitors_dict1', kolesa_darom_competitors_dict1)

       ######  НАДО СФОРМИРОВАТЬ СЛОВАРЬ С НЕСКОЛЬКИМИ КОНКУРЕНТАМИя 05.12.2022
            models.KOLESA_DAROM_COMPETITORS_DICTIONARY1 = kolesa_darom_competitors_dict1 
            object_unit.kolesa_darom_competitor_on_date1()                      ###!!!!!!!!!!!!!!!!!!!!!!!!!!!!

       ## ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ KOLESA_DAROM: 
        kolesa_darom_max_lengh_list = []
        for object_unit in list_of_tyre_comparative_objects:
            obj_num = len(object_unit.kolesa_darom_competitor_on_date1())
            kolesa_darom_max_lengh_list.append(obj_num)
        if kolesa_darom_max_lengh_list:
            kolesa_darom_max_lengh_header = max(kolesa_darom_max_lengh_list)
        else:
            kolesa_darom_max_lengh_header = 0

        models.KOLESA_DAROM_HEADER_NUMBER = kolesa_darom_max_lengh_header
        #print('models.KOLESA_DAROM_HEADER_NUMBER', models.KOLESA_DAROM_HEADER_NUMBER)
        # print('KOLESA_DAROM_HEADER_NUMBER ====+++==', models.KOLESA_DAROM_HEADER_NUMBER_COMPETITORS_NAMES_FILTER)

        obj.kolesa_darom_heders_value()
        obj.kolesa_darom_heders_lengt()
        #object_unit.kolesa_darom_competitor_on_date1()

        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects

        ###### END KOLESA_DAROM

#       ## 2 фильтр конкурентов CHEMCURIER:
        # if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:       - ЗАГОТОВКА ДЛЯ ФИЛЬТРА ПО ДАТЕ И В ХИМКУРЬЕР
        all_competitors = models.ChemCurierTyresModel.objects.all()
        #print(all_competitors , 'all_competitors ')
#            # 1.1 ФИЛЬТР по дате
#        #  all_competitors = models.CompetitorSiteModel.objects.filter(date_period=datetime.date(2022, 11, 22))       # по дате 
#            # 1.2 ФИЛЬТР список производителей :
#        # выбор по производителю:                               
#        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        chemcurier_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
#           object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
#           object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            if models.CHEMCURIER_COMPETITORS:
                for competitor in models.ChemCurierTyresModel.objects.filter(producer_chem__in=models.CHEMCURIER_COMPETITORS):                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyre_size_chem:
                        #print("CHEMCURIER На пол шишечки TTT")
                        list_of_matched_competitors.append(competitor)
                chemcurier_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
            else:
                #for competitor in all_competitors[0 : 3]:  
                for competitor in all_competitors:  
                    #print(object_unit.tyre.tyre_size.tyre_size, '&&&', competitor.tyre_size_chem, 'FINSY ZALIV', competitor.tyre_size_chem.split(',')[0].replace('(', '').replace('\'', ''))                                                                                                   ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    #if object_unit.tyre.tyre_size.tyre_size == competitor.tyre_size_chem:
                    if object_unit.tyre.tyre_size.tyre_size == competitor.tyre_size_chem.split(',')[0].replace('(', '').replace('\'', ''):
                        list_of_matched_competitors.append(competitor)
            #            print('UMNYE LUDY', competitor)
            chemcurier_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
            #for mm, vv in chemcurier_competitors_dict1.items():
            #    print(mm, vv, 'HHH')
            #print('chemcurier_competitors_dict1', chemcurier_competitors_dict1)     # hemcurier_competitors_dict1 {<Tyre: Tyre object (1899)>: [], <Tyre: Tyre object (1900)>: [],
       ######  НАДО СФОРМИРОВАТЬ СЛОВАРЬ С НЕСКОЛЬКИМИ КОНКУРЕНТАМИя 05.12.2022
            models.CHEMCURIER_COMPETITORS_DICTIONARY1 = chemcurier_competitors_dict1  
            object_unit.chemcurier_competitor_on_date1()
            # CCC [('', '', ''), ('', '', ''), ('', '', '')]
            #print(object_unit.chemcurier_competitor_on_date1(), 'TTT')  
       ## ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ CHEMCURIER: 
        chemcurier_max_lengh_header = 1                                 # chemcurier будет лишь один столбец
        models.CHEMCURIER_HEADER_NUMBER = chemcurier_max_lengh_header
        # print('models.CHEMCURIER_HEADER_NUMBER ====+++==', models.CHEMCURIER_HEADER_NUMBER)
        obj.chemcurier_heders_value()
        obj.chemcurier_heders_lengt()
        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects
        ###### END OF CHEMCURIER

        # если применен фильтр:
        # 1) выбрать производителя:
        filter_form = forms.FilterRussiaForm()
        context['producer_filter_form'] = filter_form                                           
        #context['producer_filter_form'].queryset = dictionaries_models.CompetitorModel.objects.filter(competitor_name__in=list(set(models.EXPRESS_SHINA_COMPETITORS_NAMES_FILTER)) and list(set(models.KOLESATYT_COMPETITORS_NAMES_FILTER)) 
        #and list(set(models.KOLESA_DAROM_COMPETITORS_NAMES_FILTER))).filter(developer_competitor__site__in=['express-shina.ru', 'kolesatyt.ru', 'kolesa-darom.ru']).values_list("competitor_name", flat=True)

        #context['producer_filter_all'] = dictionaries_models.CompetitorModel.objects.all().filter(developer_competitor__site__in=['express-shina.ru', 'kolesatyt.ru', 'kolesa-darom.ru'])
        context['producer_filter_all'] = dictionaries_models.CompetitorModel.objects.filter(developer_competitor__site__in=['express-shina.ru', 'kolesatyt.ru', 'kolesa-darom.ru'])
        #filter_form.fields["competitors"].queryset = dictionaries_models.CompetitorModel.objects.filter(competitor_name__in=list(set(models.ONLINER_COMPETITORS_NAMES_FILTER))).values_list("competitor_name", flat=True)
        # 2) выбрать продукцию:
        in_base_tyres = models.ComparativeAnalysisTyresModel.objects.all()
        context['in_base_tyres'] = in_base_tyres.order_by('-tyre')
        #######  
        # 3) выбрать группу шин:
        tyr_groups = dictionaries_models.TyreGroupModel.objects.all()
        #print('tyr_groups', tyr_groups)
        context['in_base_tyres_by_group'] = tyr_groups
        #######      
        # 
        # 4) ввод % отклонения торговой надбавки:
        deflection_form = forms.DeflectionInputForm(initial={'deflection_data': models.DEFLECTION_VAL})
        context['deflection_form'] = deflection_form
        current_deflection_value = models.DEFLECTION_VAL
        if current_deflection_value is None:
            current_deflection_value = 0.0
        context['current_deflection_value'] = current_deflection_value

        # 5) выбранное пользователем значение даты:
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
            context['chosen_date'] = models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0]

        ### СБРОС ДАННЫХ _ ОЧИСТКА ПРИ ОБНОВЛЕНИИ СТРАНИЦЫ:
        models.TYRE_GROUPS = []     
        models.TYRE_GROUPS_ALL = [] 
        models.SELF_PRODUCTION = []
        models.SELF_PRODUCTION_ALL = []  
        models.EXPRESS_SHINA_COMPETITORS = [] 
        models.KOLESATYT_COMPETITORS = []
        models.KOLESA_DAROM_COMPETITORS = []
        models.CHEMCURIER_COMPETITORS = []
        models.SEARCH_USER_REQUEST = []
        models.COMPETITORS_DATE_FROM_USER_ON_FILTER = []
        
        # пагинация самодельная:
        current_pagination_value = models.PAGINATION_VAL
        if current_pagination_value is None:
            current_pagination_value = 10
        pagination_form = forms.PaginationInputForm(initial={'pagination_data': current_pagination_value})
        context['pagination_val_per_form'] = pagination_form        
        #context['current_pagination_value'] = current_pagination_value        

        posts = context['list_of_tyre_comparative_objects']
        if 'page' in self.request.GET:
            page = self.request.GET['page']
        else:
            page = 1
        paginator = Paginator(posts, current_pagination_value)
        #print('paginator', paginator.num_pages)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        #print('posts', posts)

        context['list_of_tyre_comparative_objects'] = posts

        currency, curr_value, shown_date = my_tags.currency_on_date()
        context['currency'] = currency
        context['curr_value'] = curr_value
        date_exist_true = None
        if shown_date:
            date_exist_true = datetime.datetime.strptime(shown_date, "%Y-%m-%d").date()
        else:
            date_exist_true = datetime.date.today()
        currency_input_form = forms.CurrencyDateInputForm()       
        currency_input_form.fields['chosen_date_for_currency'].initial = date_exist_true                        # !!! ЭТО БАЗА

        context['currency_input_form'] = currency_input_form

        return context

class ComparativeAnalysisTableModelRussiaUpdateView(View):

    def post(self, request):
        #print (request.POST.getlist('competitors'), 'TTTT')
        #print (request.POST, 'TTTT')

        ## 1 работа с периодами:
        comparative_model_parcing_date = request.POST.getlist('parcing_date') 
        #print('comparative_model_parcing_date', comparative_model_parcing_date , type(comparative_model_parcing_date))

        if comparative_model_parcing_date == ['']:
            pass
        elif comparative_model_parcing_date:
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER = comparative_model_parcing_date
            #print('{J{J{J{JJ{', comparative_model_parcing_date)
        else:
            pass

        #### 1.1 ПЕРИОД ДЛЯ КУРСА ВАЛЮТ:
        chosen_date_for_currency_year = request.POST.getlist('chosen_date_for_currency_year') 
        chosen_date_for_currency_month = request.POST.getlist('chosen_date_for_currency_month') 
        chosen_date_for_currency_day = request.POST.getlist('chosen_date_for_currency_day') 
        chosen_date_for_currency = chosen_date_for_currency_year + chosen_date_for_currency_month + chosen_date_for_currency_day
        if chosen_date_for_currency:
            #print('chosen_date_for_currency1', chosen_date_for_currency)  
            chosen_date_for_currency = '-'.join(str(x) for x in chosen_date_for_currency)
            #print('chosen_date_for_currency', chosen_date_for_currency)             # 'parcing_date': ['2023-03-14'],  chosen_date_for_currency 2022-1-30
            check_date = datetime.datetime.strptime(chosen_date_for_currency, "%Y-%m-%d").date()        #  если пользователем введена дана превышающая текущую для получения курса валют то нао скинуть на сегодня:
            if check_date > datetime.datetime.now().date():
                pass
            else:
                models.CURRENCY_DATE_GOT_FROM_USER = chosen_date_for_currency


        # 2-й работа с группами шин:
        tyre_groups_list_all = request.POST.getlist('self_production_group_id_all')
        tyre_groups_list = request.POST.getlist('self_production_group_id')
        if tyre_groups_list_all:
            #print(tyre_groups_list_all, 'tyre_groups_list_all')
            models.TYRE_GROUPS_ALL= tyre_groups_list_all
        else:
            #print(tyre_groups_list, 'tyre_groups_list')
            models.TYRE_GROUPS= tyre_groups_list 

        ## 3 работа с собственной продукцией:
        production_tyres_list_all = request.POST.getlist('self_production_all')  
        production_tyres_list = request.POST.getlist('self_production')                                                             # фильтр по собственным шинам
        if production_tyres_list_all:
            #print('production_tyres_list_all', production_tyres_list_all)
            models.SELF_PRODUCTION_ALL = production_tyres_list_all

        ### ЕСЛИ ПОЛЬЗОВАТЬЕЛЬ ИЩЕТ ЧЕРЕЗ ПОИСК:
        production_tyres_list_one = request.POST.getlist('product_search')
        #print('show me', production_tyres_list_one)
        if production_tyres_list_one:
            models.SEARCH_USER_REQUEST = production_tyres_list_one

        # 4 работа с производителями-конкурентами
        all_express_shina_kolesatyt_kolesa_darom_chemcurier_competitors_list_all = request.POST.getlist('producers_all')
        express_shina_AND_OTHERS_competitors_list = request.POST.getlist('competitors')                               # фильтр конкурентов
        if all_express_shina_kolesatyt_kolesa_darom_chemcurier_competitors_list_all:
            pass
        else:
            #print('express_shina_AND_OTHERS_competitors_list', express_shina_AND_OTHERS_competitors_list)
            models.EXPRESS_SHINA_COMPETITORS = express_shina_AND_OTHERS_competitors_list
            models.KOLESATYT_COMPETITORS = express_shina_AND_OTHERS_competitors_list
            models.KOLESA_DAROM_COMPETITORS = express_shina_AND_OTHERS_competitors_list
            models.CHEMCURIER_COMPETITORS = express_shina_AND_OTHERS_competitors_list

        # 5 работа с вводимыми данными по отклонению торговой надбавки
        deflection_data_got = request.POST.get('deflection_data')  
        #print('deflection_data_got', deflection_data_got)
        if deflection_data_got:
            models.DEFLECTION_VAL = float(request.POST.get('deflection_data'))
        else:
            pass

        # 6 работа с вводимыми данными по количеству выводимых объектов в таблице
        pagination_data_got = request.POST.get('pagination_data')  
        #print('pagination_data_got', pagination_data_got)
        if pagination_data_got:
            models.PAGINATION_VAL = int(request.POST.get('pagination_data'))
        else:
            pass
            
        return HttpResponseRedirect(reverse_lazy('prices:comparative_prices_russia'))