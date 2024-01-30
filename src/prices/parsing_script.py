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
import json

from collections import Counter
from operator import itemgetter, attrgetter

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from django.db.models import Min

import random
import itertools


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



def belarus_sites_parsing():

    # 1 ###### ПАРСИНГ Onliner:    
    chromeOptions1 = webdriver.ChromeOptions() 
    chromeOptions1.add_argument("--no-sandbox") 
    chromeOptions1.add_argument("--disable-setuid-sandbox") 
    chromeOptions1.add_argument("--disable-dev-shm-usage");
    chromeOptions1.add_argument("--disable-extensions")
    chromeOptions1.add_argument("--headless") 
    #chromeOptions1.add_argument('--ignore-certificate-errors')
    webdriverr_global = webdriver.Chrome(options=chromeOptions1)  



    #webdriverr_global = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    try:
        url = 'https://catalog.onliner.by/tires'
        #response = requests.get(url)
        #soup = BeautifulSoup(response.text,"lxml")
        ## ПОДКЛЮЧЕНИЕ БИБЛИОТЕКИ SELENIUM
        #webdriverr = webdriver.Chrome()
        #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        webdriverr = webdriverr_global
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')
        #products = soup.find_all('div', class_='schema-product__group')
        #goods_dict = {}
        #for data_got in products:
        #    tyre_name = data_got.find('div', class_='schema-product__title')
        #    price = data_got.find('div', 'schema-product__price')
        #    if tyre_name and price:
        #        text_to_delete = tyre_name.text.find('шины') + 5
        #        tyre_name_cleaned = tyre_name.text[text_to_delete :]
        #        start_str_serch = price.text.find('от') + 3
        #        end_str_search = price.text.find('р') - 1
        #        price_cleaned = price.text[start_str_serch : end_str_search]
        #        goods_dict[tyre_name_cleaned] = price_cleaned
        # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
        #1. получаем количество страниц:
        #pages = soup.find('div', class_='schema-pagination schema-pagination_visible')
        pages = soup.find('ul', class_='catalog-pagination__pages-list')
        urls = []
        #links = pages.find_all('a', class_='schema-pagination__pages-link') #
        links = pages.find_all('a', class_='catalog-pagination__pages-link')
        for link in links:
            pageNum = int(link.text) if link.text.isdigit() else None
            if pageNum != None:
                urls.append(pageNum)
        #2. получаем данные со всех страниц:
        list_to_check = ['автобусов и грузовых автомобилей', 'большегрузных автомобилей', 'строительной и дорожной техники', 'тракторов и сельскохозяйственной техники', 'микроавтобусов и легкогрузовых автомобилей']
        shins_phrase = ['шины', 'Шины']
        for slug in urls[1:1]:                               # c 1 по 2 станицы    
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
                    # проверка на лишний тект в нелегковых шинах
                    check_name_is_foud = False
                    for check_name in list_to_check:
                        if check_name in tyre_name.text:
                            phrase_len = len(check_name)
                            wha_to_delete_start = tyre_name.text.find(check_name)
                            wha_to_delete_end = tyre_name.text.find(check_name) + phrase_len
                            text_with_no_phrase = tyre_name.text[: wha_to_delete_start] + tyre_name.text[wha_to_delete_end :]
                            text_with_no_phrase = text_with_no_phrase.replace('для', '')
                            text_to_delete1text_with_no_phrase = ''
                            for sh_pr in shins_phrase:
                                    text_to_delete1text_with_no_phrase = text_with_no_phrase.replace(sh_pr, '')
                            tyre_name_cleaned = text_to_delete1text_with_no_phrase
                            tyre_name_cleaned = tyre_name_cleaned.replace('\n', '') 
                            tyre_name_cleaned_split = tyre_name_cleaned.split(' ')
                            for n in tyre_name_cleaned_split:
                                if n.isalnum() is True:
                                    company_name = n
                                    break
                            check_name_is_foud = True
                    # end проверка на лишний тект в нелегковых шинах
                    if check_name_is_foud is False:
                        text_to_delete1 = tyre_name.text.find('шины') + 5
                        tyre_name_cleaned = tyre_name.text[text_to_delete1 : ]
                        tyre_name_cleaned = tyre_name_cleaned.replace('\n', '')
                    start_str_serch = price.text.find('от') + 3
                    end_str_search = price.text.find('р') - 1
                    price_cleaned = price.text[start_str_serch : end_str_search]
                ###### дополнительные праметры ищем: 
                #for data_got in products:
                    tyre_season = data_got.find('div', class_='schema-product__description')
                    seas_list = ['летние', 'зимние', 'всесезонные']
                    studded_list = ['без шипов', 'с шипами', 'возможность ошиповки']
                    group_list_cars = ['легковых', 'внедорожников', 'минивенов', 'кроссоверов'] 
                    group_list_lt = ['микро'] # ['микроавтобусов', 'легкогрузовых']                
                    group_list_trucks = ['грузовых', 'строительной', 'большегрузных'] #['автобусов', 'грузовых автомобилей', 'строительной и дорожной', 'большегрузных автомобилей']
                    group_list_agro = ['тракторов и сельскохозяйственной']
                    tyr_group_check = False
                    tyr_seas_check = False
                    tyr_group = None
                    season = None
                    if tyre_season:
                        split_str_prepared = tyre_season.text
                        split_str = split_str_prepared.replace('\n', '').split(', ')
                        season_is = []
                        try:
                            if split_str[0] and split_str[0] in ['летние', 'зимние', 'всесезонные']:
                                season_is = split_str[0]
                        except:
                            pass
                        group_is = []
                        # для грузовых
                        try:
                            if split_str[1]:
                                group_is = split_str[1]
                                tyr_group_check is True
                        except:
                            try:
                                #if 'BEL-318' in tyre_name_cleaned:
                                #    print('split42334324', split_str[0])
                                if split_str[0]:
                                    for n in group_list_cars:
                                        if n in split_str[0]:
                                            group_is = 'легковые'
                                            break
                                    for n in group_list_lt:
                                        if n in split_str[0]:
                                            group_is = 'легкогруз'
                                    #        print('---====', group_is)
                                            break
                                    for n in group_list_trucks:
                                        if n in split_str[0]:
                                            group_is = 'грузовые'
                                            break
                                    for n in group_list_agro:
                                        if n in split_str[0]:
                                            group_is = 'с/х'
                                            break
                                tyr_group = group_is        
                                tyr_group_check = True
                            except:
                                pass
                        # END для грузовых
                        # группа для легковых
                        if tyr_group_check is False:
                            for tyr_group in group_list_cars:
                                if tyr_group in group_is:
                                    t_gr = 'легковые'
                                #    print('tyr_group 111111', tyr_group)
                                    break
                                #for tyr_group in group_list_lt:
                            tg_is_lt = False    
                            for tyr_group in group_list_lt:
                                if tyr_group in group_is:
                                    t_gr = 'легкогруз'
                                #    print('tyr_group 111222', tyr_group, '||||', group_is)
                                    tg_is_lt = True
                                    break
                            if tg_is_lt is False:
                                for tyr_group in group_list_trucks:
                                    #for tyr_group in group_list_trucks:
                                    if tyr_group in group_is:
                                        t_gr = 'грузовые'
                                #        print('tyr_group 11133', tyr_group, '||||', group_is)
                                        break
                            for tyr_group in group_list_agro:
                                #for tyr_group in group_list_agro:
                                if tyr_group in group_is:
                                    t_gr = 'с/х'
                            #        print('tyr_group 111', tyr_group)
                                    break
                            tyr_group = t_gr
                        # END группа для легковых    
                        # сезонность
                        studded_is = []                       # ШИПЫ - тут доработать
                        for s_el in seas_list:
                            if s_el in tyre_season.text:
                                season = s_el
                            #    if 'BEL-318' in tyre_name_cleaned:
                            #        print('group_is ========88888=', tyre_season.text)  
                            #        print('group_is =====================', season)  
                        # END сезонность
                        # шипы
                        for studded_el in studded_list:
                            if studded_el in tyre_season.text:
                                studded = studded_el
                        #print( season, '          ', studded)
                        t_gr = None
                        # END 
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
                            if check_name_is_foud is False:
                                company_name = product_name.split(' ')[0]
                            tyre_param = str_right_data
                    values = price_cleaned, tyresize, product_name, tyre_param, company_name, season, tyr_group, #studded 
                    #print('||', price_cleaned, tyresize, product_name, tyre_param, company_name, season, tyr_group)  # 805,00 275/70R22.5    Белшина Escortera BEL-318  Белшина летние грузовые
                    goods_dict[tyre_name_cleaned] = values                                                                      # ПОДПРАВИТЬ КЛЮЧИ _ НЕ ВСЕ ПОПАДУТ ВЕДБ
        #for k, v in goods_dict.items():
        #   print('K==', k, 'V==', v, 'KV')
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
        temp_goods_dict_list_k_names_to_delete = []
        for v in goods_dict.values():
            if v[4] and v[4] in onliner_companies_list:                 # СЕЙЧАС ВЫДАЕТ ВСЕХ ПРОИЗВОДИТЕЛЕЙ  ВСЕЮ ПРОДУКЦИЮ или подкинутых пользователем
                pass
            else:
                temp_goods_dict_list_k_names_to_delete.extend(v[4])
        for k_name in temp_goods_dict_list_k_names_to_delete:
            goods_dict.pop(k_name)
        # сопоставление с БД  и запись в БД конкурентов (Onliner):
        onliner_compet_obj_tyre_bulk_list = []
        list_tyre_sizes = []
        tyres_in_bd = tyres_models.Tyre.objects.all()
        for tyre in tyres_in_bd:
            for k, v in goods_dict.items():
                #   print(k, len(k), 'v', v)
                if tyre.tyre_size.tyre_size == v[1]:                                                                                            #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
                    # Goodyear EfficientGrip Performance 2 205/60R16 92H 50 v ('\n341,08', '205/60R16', 'Goodyear EfficientGrip Performance 2', '92H', 'Goodyear', 'летние', 'легковые')                                                                                   #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
                    coma = v[0].find(',')
                    pr = float
                    name_competitor, created = dictionaries_models.CompetitorModel.objects.get_or_create(
                        competitor_name = v[4] 
                    )
                  ##     print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH', v[6])
                    season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name=v[5]) 
                    if season_usage:
                        season_usage = season_usage[0]
                    else:
                        season_usage = None 
                    if coma:
                        no_with_coma = v[0].replace(',', '.').replace('\n', '')
                        try:
                            pr = float(no_with_coma) 
                        except:
                            pr = None
                    tyre_group_ussage = dictionaries_models.TyreGroupModel.objects.filter(tyre_group=v[6])
                    if tyre_group_ussage:
                        tyre_group_ussage = tyre_group_ussage[0]
                    else:
                        tyre_group_ussage = None 
                    if coma:
                        no_with_coma = v[0].replace(',', '.').replace('\n', '')
                        try:
                            pr = float(no_with_coma) 
                        except:
                            pr = None
                    list_tyre_sizes.append(v[1])
                    #list_comparative_analysis_tyre_objects = []
                    #for comparative_analys_tyres_model_object in models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=v[1]):
                    #    list_comparative_analysis_tyre_objects.append(comparative_analys_tyres_model_object)
                    onliner_compet_obj_tyre_bulk_list.append(models.CompetitorSiteModel(
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
                        season = season_usage,
                        group = tyre_group_ussage,
                    )        
                    )
        bulk_onl_compet = models.CompetitorSiteModel.objects.bulk_create(onliner_compet_obj_tyre_bulk_list)
        list_tyre_sizes = set(list_tyre_sizes)
        for t_szz in list_tyre_sizes:
            for obbj, comparative_analys_tyres_model_object in itertools.product(models.CompetitorSiteModel.objects.filter(tyresize_competitor=t_szz, site = 'onliner.by'), models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=t_szz)):
                    obbj.tyre_to_compare.add(comparative_analys_tyres_model_object)   
                    # OLD VERSION       
                    ####competitor_site_model = models.CompetitorSiteModel.objects.update_or_create(
                    ####    site = 'onliner.by',
                    ####    #tyre = tyre,
                    ####    currency = dictionaries_models.Currency.objects.get(currency='BYN'),
                    ####    price = pr,
                    ####    date_period = datetime.datetime.today(),
                    ####    #developer = v[4],
                    ####    developer = name_competitor,
                    ####    tyresize_competitor = v[1],
                    ####    name_competitor = v[2], 
                    ####    parametres_competitor = v[3],
                    ####    season = season_usage,
                    ####    group = tyre_group_ussage,
                    ####    #tyre_to_compare = list_comparative_analys_tyres_model_objects_to_bound_with,
                    ####)
                    ####### добавлено: привязка к ComparativeAnalysisTyresModel одинаковый типоразмер
                #   #### print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH1', competitor_site_model[0])
                    ####for comparative_analys_tyres_model_object in models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=v[1]):
                    ####    competitor_site_model[0].tyre_to_compare.add(comparative_analys_tyres_model_object)
                    #######
                # END OLD VERSION   
    except:
        pass                                                                                                                                                                                                       
    ##### END OF ONLINER PARSING
    # 2 ###### ПАРСИНГ АВТОСЕТЬ:
    try:
        avtoset_good_num = 0
        # 1) Легковые шины
        url = 'https://autoset.by/tires/'       
        #webdriverr = webdriver.Chrome()
        #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        webdriverr = webdriverr_global
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')   
        ##products_lt = soup.find_all('section', class_='container-block product__wrap')
        ### ВЕРСИЯ РАБОЧАЯ ДО ИЗМЕННЕНИЙ НА САЙТЕ
        #for data_got in products_lt:
        #    tyre_title_lt = str(data_got.find('div', class_='brand').text).replace('\\n', '').replace('БЕСПЛАТНЫЙ ШИНОМОНТАЖ', '') 
        #    tyre_title_lt = re.sub('\r?\n', '', tyre_title_lt)
        ##    tyre_model_lt = str(data_got.find('a', class_='model link_blue').text.replace('\\n', ''))  
        #    tyre_model_lt = str(data_got.find('a', class_='model').text.replace('\\n', ''))  
        #    tyre_model_lt = re.sub('\r?\n', '', tyre_model_lt)
        #    tyre_size_lt_text = str(data_got.find('a', class_='size-val link_hov'))
        #    tyre_size_lt_span_start_index = tyre_size_lt_text.find('<span>') + 6
        #    tyre_size_lt_span_end_index = tyre_size_lt_text.find('</span>')
        #    tyre_index_lt = tyre_size_lt_text[tyre_size_lt_span_start_index : tyre_size_lt_span_end_index]
        #    tyre_size_lt = str(data_got.find('a', class_='size-val link_hov').text.replace(' ', '').replace(',', '.').replace(tyre_index_lt, '').replace('\n', ''))                
        #            #    tyre_index_lt = str(data_got.find('a', class_='size-val link_hov').text) 
        #            #    tyre_index_lt = tyre_index_lt.replace(tyre_size_lt, '')
        #    tyre_season_lt = str(data_got.find('span', class_='val').text) 
        #    print(tyre_title_lt,'||', tyre_size_lt,'||', tyre_index_lt,'||', tyre_model_lt, '||', tyre_season_lt)
        #    tyre_rub_price_lt = str(data_got.find('span', class_='full').text.replace(' ', '')) 
        #    tyre_coins_price_lt = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
        #    tyre_price_lt = float(tyre_rub_price_lt + '.' + tyre_coins_price_lt)
        #    tyr_group = 'легковые'
        ##    print('=0=', tyre_title_lt,'||', tyre_size_lt,'||', tyre_index_lt,'||', tyre_model_lt, '||', tyre_season_lt, '||', tyre_price_lt, '||', tyr_group)
        #    goods_dict_avtoset[tyre_size_lt, avtoset_good_num] = tyre_title_lt, tyre_model_lt, tyre_index_lt, tyr_group, tyre_price_lt, tyre_season_lt
        #    avtoset_good_num += 1
        ### END ВЕРСИЯ РАБОЧАЯ ДО ИЗМЕННЕНИЙ НА САЙТЕ
        ##for data_got in products_lt:
        ##    tyre_title_lt = str(data_got.find('div', class_='brand').text).replace('\\n', '').replace('БЕСПЛАТНЫЙ ШИНОМОНТАЖ', '').replace('БЕСПЛАТНАЯ СПЕЦГАРАНТИЯ', '')  
        ##    tyre_title_lt = re.sub('\r?\n', '', tyre_title_lt)
        ##    tyre_model_lt = str(data_got.find('a', class_='model').text.replace('\\n', ''))  
        ##    tyre_model_lt = re.sub('\r?\n', '', tyre_model_lt)
        ##    tyre_size_lt_text = str(data_got.find('a', class_='size-val'))
        ##    tyre_size_lt_span_start_index = tyre_size_lt_text.find('<span>') + 6
        ##    tyre_size_lt_span_end_index = tyre_size_lt_text.find('</span>')
        ##    tyre_index_lt = tyre_size_lt_text[tyre_size_lt_span_start_index : tyre_size_lt_span_end_index]
        ##    tyre_size_lt = str(data_got.find('a', class_='size-val').text.replace(' ', '').replace(',', '.').replace(tyre_index_lt, '').replace('\n', ''))                
        ##    tyre_season_lt = str(data_got.find('span', class_='val').text) 
        ##    tyre_rub_price_lt = str(data_got.find('span', class_='full').text.replace(' ', '')) 
        ##    tyre_coins_price_lt = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
        ##    tyre_price_lt = float(tyre_rub_price_lt + '.' + tyre_coins_price_lt)
        ##    tyr_group = 'легковые'
        ###    print('=0=', tyre_title_lt,'||', tyre_size_lt,'||', tyre_index_lt,'||', tyre_model_lt, '||', tyre_season_lt, '||', tyre_price_lt, '||', tyr_group)
        ##    goods_dict_avtoset[tyre_size_lt, avtoset_good_num] = tyre_title_lt, tyre_model_lt, tyre_index_lt, tyr_group, tyre_price_lt, tyre_season_lt
        ##    avtoset_good_num += 1
        # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
        #1. получаем количество страниц:
        pages = soup.find('div', class_='pagination-block__pages')       
        urls_get = []
        links = pages.find_all('a', class_='pagination-block__page') #pagination-block__page
        for link in links:
            pageNum = int(link.text) if link.text.isdigit() else None
            if pageNum != None:
                urls_get.append(pageNum)
        urls_get = max(urls_get)
        #2. получаем данные со всех страниц:                         
        ####for slug in range(1, urls_get[-1]):                             # мое добавление специально для АВТОСЕТЬ   # c 1 по 2 станицы              
        for slug in urls[1:1]:                                 # c 1 по 2 станицы
        #for slug in range(0,urls_get):    
            #newUrl = url.replace('', f'/?PAGEN_1={slug}')       #https://autoset.by/tires/?PAGEN_1=3
            newUrl = url + f'?PAGEN_1={slug}'       #https://autoset.by/tires/?PAGEN_1=3
            webdriverr.get(newUrl)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_lt = soup.find_all('section', class_='container-block product__wrap')
        ##    print('products_lt', products_lt)
            for data_got in products_lt:
                tyre_title_lt = str(data_got.find('div', class_='brand').text).replace('\\n', '').replace('БЕСПЛАТНЫЙ ШИНОМОНТАЖ', '').replace('БЕСПЛАТНАЯ СПЕЦГАРАНТИЯ', '') 
                tyre_title_lt = re.sub('\r?\n', '', tyre_title_lt)
            #    print('&&&&!&!&!', tyre_title_lt)
                tyre_model_lt = str(data_got.find('a', class_='model').text.replace('\\n', ''))  
                tyre_model_lt = re.sub('\r?\n', '', tyre_model_lt)
                tyre_size_lt_text = str(data_got.find('a', class_='size-val'))
                tyre_size_lt_span_start_index = tyre_size_lt_text.find('<span>') + 6
                tyre_size_lt_span_end_index = tyre_size_lt_text.find('</span>')
                tyre_index_lt = tyre_size_lt_text[tyre_size_lt_span_start_index : tyre_size_lt_span_end_index]
                tyre_size_lt = str(data_got.find('a', class_='size-val').text.replace(' ', '').replace(',', '.').replace(tyre_index_lt, '').replace('\n', ''))                
                tyre_season_lt = str(data_got.find('span', class_='val').text) 
                tyre_rub_price_lt = str(data_got.find('span', class_='full').text.replace(' ', '')) 
                tyre_coins_price_lt = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
                tyre_price_lt = float(tyre_rub_price_lt + '.' + tyre_coins_price_lt)
                tyr_group = 'легковые'
        #        print('=0=', tyre_title_lt,'||', tyre_size_lt,'||', tyre_index_lt,'||', tyre_model_lt, '||', tyre_season_lt, '||', tyre_price_lt, '||', tyr_group)
                goods_dict_avtoset[tyre_size_lt, avtoset_good_num] = tyre_title_lt, tyre_model_lt, tyre_index_lt, tyr_group, tyre_price_lt, tyre_season_lt
                avtoset_good_num += 1
        # 2) Грузовые шины
        url = 'https://autoset.by/trucks-tires/'
        #webdriverr = webdriver.Chrome()
        #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        webdriverr = webdriverr_global
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')
        products_t = soup.find_all('section', class_='container-block product__wrap')
        #for data_got in products_t:
        #    tyre_title_t = str(data_got.find('div', class_='brand').text).replace('\\n', '')
        #    tyre_title_t = re.sub('\r?\n', '', tyre_title_t)
        #    tyre_model_t = str(data_got.find('a', class_='model').text.replace('\\n', '')) 
        #    tyre_size_t_text = str(data_got.find('a', class_='size-val'))
        #    tyre_size_t_span_start_index = tyre_size_t_text.find('<span>') + 6
        #    tyre_size_t_span_end_index = tyre_size_t_text.find('</span>')
        #    tyre_index_t = tyre_size_t_text[tyre_size_t_span_start_index : tyre_size_t_span_end_index]
        #    tyre_size_t = str(data_got.find('a', class_='size-val').text.replace(' ', '').replace(',', '.').replace(tyre_index_t, '').replace('\n', '')) 
        #    tyre_rub_price_t = str(data_got.find('span', class_='full').text.replace(' ', '')) 
        #    tyre_coins_price_t = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
        #    tyre_price_t = float(tyre_rub_price_t + '.' + tyre_coins_price_t)
        #    tyr_group = 'грузовые'
        #    #print('=1=', tyre_title_t, '||', tyre_size_t, '||', tyre_index_t, '||', tyre_model_t, '||', tyre_price_t, '||', tyr_group)
        #    goods_dict_avtoset[tyre_size_t, avtoset_good_num] = tyre_title_t, tyre_model_t, tyre_index_t, tyr_group, tyre_price_t 
        #    avtoset_good_num += 1    
        # ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
        #1. получаем количество страниц:
        pages = soup.find('div', class_='pagination-block__pages')        
        urls_get = []
        links = pages.find_all('a', class_='pagination-block__page') 
        for link in links:
            pageNum = int(link.text) if link.text.isdigit() else None
            if pageNum != None:
                urls_get.append(pageNum)            
        urls_get = max(urls_get)
        #2. получаем данные со всех страниц:                         
        #for slug in range(1, urls_get[-1]):                             # мое добавление специально для АВТОСЕТЬ   # c 1 по 2 станицы                
        for slug in range(1, 1):
        #for slug in range(0,urls_get):    
            newUrl = url + f'?PAGEN_1={slug}'       #https://autoset.by/trucks-tires/?PAGEN_1=2
            webdriverr.get(newUrl)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_t = soup.find_all('section', class_='container-block product__wrap')   
            for data_got in products_t:
                tyre_title_t = str(data_got.find('div', class_='brand').text).replace('\\n', '')
                tyre_title_t = re.sub('\r?\n', '', tyre_title_t)
                tyre_model_t = str(data_got.find('a', class_='model').text.replace('\\n', '')) 
                tyre_size_t_text = str(data_got.find('a', class_='size-val'))
                tyre_size_t_span_start_index = tyre_size_t_text.find('<span>') + 6
                tyre_size_t_span_end_index = tyre_size_t_text.find('</span>')
                tyre_index_t = tyre_size_t_text[tyre_size_t_span_start_index : tyre_size_t_span_end_index]
                tyre_size_t = str(data_got.find('a', class_='size-val').text.replace(' ', '').replace(',', '.').replace(tyre_index_t, '').replace('\n', '')) 
                tyre_rub_price_t = str(data_got.find('span', class_='full').text.replace(' ', '')) 
                tyre_coins_price_t = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
                tyre_price_t = float(tyre_rub_price_t + '.' + tyre_coins_price_t)
                tyr_group = 'грузовые'
            #    print('=1=', tyre_title_t, '||', tyre_size_t, '||', tyre_index_t, '||', tyre_model_t, '||', tyre_price_t, '||', tyr_group)
                goods_dict_avtoset[tyre_size_t, avtoset_good_num] = tyre_title_t, tyre_model_t, tyre_index_t, tyr_group, tyre_price_t 
                avtoset_good_num += 1 
        # 3) Грузовые индустриальные спец. шины
        url = 'https://autoset.by/industrial-tires/'
        #webdriverr = webdriver.Chrome()
        #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        webdriverr = webdriverr_global
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')   
        products_ts = soup.find_all('section', class_='container-block product__wrap')
        #for data_got in products_ts:
        #    tyre_title_ts = str(data_got.find('div', class_='brand').text).replace('\\n', '')
        #    tyre_title_ts = re.sub('\r?\n', '', tyre_title_ts)
        #    tyre_model_ts = str(data_got.find('a', class_='model').text).replace('\n', '')  
        #    tyre_size_ts_text = str(data_got.find('a', class_='size-val'))
        #    tyre_size_ts_span_start_index = tyre_size_ts_text.find('<span>') + 6
        #    tyre_size_ts_span_end_index = tyre_size_ts_text.find('</span>')
        #    tyre_index_ts = tyre_size_ts_text[tyre_size_ts_span_start_index : tyre_size_ts_span_end_index]
        #    tyre_size_ts = str(data_got.find('a', class_='size-val').text.replace(' ', '').replace(',', '.').replace(tyre_index_ts, '').replace('\n', ''))  
        #    tyre_rub_price_ts = str(data_got.find('span', class_='full').text.replace(' ', '')) 
        #    tyre_coins_price_ts = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
        #    tyre_price_ts = float(tyre_rub_price_ts + '.' + tyre_coins_price_ts)
        #    tyr_group = 'грузовые'
        ##    print('=0=', tyre_title_ts, '||', tyre_size_ts, '||', tyre_index_ts, '||', tyre_model_ts, '||', tyre_price_ts, '||', tyr_group)
        #    goods_dict_avtoset[tyre_size_ts, avtoset_good_num] = tyre_title_ts, tyre_model_ts, tyre_index_ts, tyr_group, tyre_price_ts
        #ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
        #1. получаем количество страниц:
        pages = soup.find('div', class_='pagination-block__pages')        
        urls_get = []
        links = pages.find_all('a', class_='pagination-block__page') 
        for link in links:
            pageNum = int(link.text) if link.text.isdigit() else None
            if pageNum != None:
                urls_get.append(pageNum)
        urls_get = max(urls_get)
        #2. получаем данные со всех страниц:                         
        #for slug in range(1, urls_get[-1]):                             # мое добавление специально для АВТОСЕТЬ   # c 1 по 2 станицы
        for slug in range(1, 1):
        #for slug in range(0,urls_get):     
            newUrl = url + f'?PAGEN_1={slug}'       #https://autoset.by/industrial-tires/?PAGEN_1=2
            webdriverr.get(newUrl)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_ts = soup.find_all('section', class_='container-block product__wrap')
            for data_got in products_ts:
                tyre_title_ts = str(data_got.find('div', class_='brand').text).replace('\\n', '')
                tyre_title_ts = re.sub('\r?\n', '', tyre_title_ts)
                tyre_model_ts = str(data_got.find('a', class_='model').text).replace('\n', '')  
                tyre_size_ts_text = str(data_got.find('a', class_='size-val'))
                tyre_size_ts_span_start_index = tyre_size_ts_text.find('<span>') + 6
                tyre_size_ts_span_end_index = tyre_size_ts_text.find('</span>')
                tyre_index_ts = tyre_size_ts_text[tyre_size_ts_span_start_index : tyre_size_ts_span_end_index]
                tyre_size_ts = str(data_got.find('a', class_='size-val').text.replace(' ', '').replace(',', '.').replace(tyre_index_ts, '').replace('\n', ''))  
                tyre_rub_price_ts = str(data_got.find('span', class_='full').text.replace(' ', '')) 
                tyre_coins_price_ts = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
                tyre_price_ts = float(tyre_rub_price_ts + '.' + tyre_coins_price_ts)
                tyr_group = 'грузовые'
            #    print('=0=', tyre_title_ts, '||', tyre_size_ts, '||', tyre_index_ts, '||', tyre_model_ts, '||', tyre_price_ts, '||', tyr_group)
                goods_dict_avtoset[tyre_size_ts, avtoset_good_num] = tyre_title_ts, tyre_model_ts, tyre_index_ts, tyr_group, tyre_price_ts
        # 4) Сельскохозяйственные шины
        url = 'https://autoset.by/agricultural-tires/'
        #webdriverr = webdriver.Chrome()
        #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        webdriverr = webdriverr_global
        webdriverr.get(url)
        time.sleep(2)
        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        soup = BeautifulSoup(webdriverr.page_source,'lxml')   
        products_agro = soup.find_all('section', class_='container-block product__wrap')
        #for data_got in products_agro:
        #    tyre_title_agro = str(data_got.find('div', class_='brand').text).replace('\\n', '')
        #    tyre_title_agro = re.sub('\r?\n', '', tyre_title_agro)
        #    tyre_model_agro = str(data_got.find('a', class_='model').text)
        #    tyre_model_agro = tyre_model_agro.replace("\n","")
        #    tyre_size_agro_text = str(data_got.find('a', class_='size-val'))
        #    tyre_size_agro_span_start_index = tyre_size_agro_text.find('<span>') + 6
        #    tyre_size_agro_span_end_index = tyre_size_agro_text.find('</span>')
        #    tyre_index_agro = tyre_size_agro_text[tyre_size_agro_span_start_index : tyre_size_agro_span_end_index]
        #    tyre_size_agro = str(data_got.find('a', class_='size-val').text.replace(' ', '').replace(',', '.').replace(tyre_index_agro, '').replace('\n', '')) 
        #    tyre_rub_price_agro = str(data_got.find('span', class_='full').text.replace(' ', '')) 
        #    tyre_coins_price_agro = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
        #    tyre_price_agro = float(tyre_rub_price_agro + '.' + tyre_coins_price_agro)
        #    tyr_group = 'с/х'
        ##    print('=7=', tyre_title_agro,'||', tyre_size_agro,'||', tyre_index_agro,'||', tyre_model_agro, '||', tyre_price_agro, '||', tyr_group)
        #    goods_dict_avtoset[tyre_size_agro, avtoset_good_num] = tyre_title_agro, tyre_model_agro, tyre_index_agro, tyr_group, tyre_price_agro 
        #ХОЖДЕНИЕ ПО ВСЕМ СТРАНИЦАМ САЙТА ПАГИНАЦИЯ:
        #1. получаем количество страниц:
        pages = soup.find('div', class_='pagination-block__pages')        
        urls_get = []
        links = pages.find_all('a', class_='pagination-block__page') 
        for link in links:
            pageNum = int(link.text) if link.text.isdigit() else None
            if pageNum != None:
                urls_get.append(pageNum)
        urls_get = max(urls_get)
        #2. получаем данные со всех страниц:                         
        for slug in range(1, 1):
        #for slug in range(0,urls_get): 
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
                tyre_model_agro = str(data_got.find('a', class_='model').text)
                tyre_model_agro = tyre_model_agro.replace("\n","")
                tyre_size_agro_text = str(data_got.find('a', class_='size-val'))
                tyre_size_agro_span_start_index = tyre_size_agro_text.find('<span>') + 6
                tyre_size_agro_span_end_index = tyre_size_agro_text.find('</span>')
                tyre_index_agro = tyre_size_agro_text[tyre_size_agro_span_start_index : tyre_size_agro_span_end_index]
                tyre_size_agro = str(data_got.find('a', class_='size-val').text.replace(' ', '').replace(',', '.').replace(tyre_index_agro, '').replace('\n', '')) 
                tyre_rub_price_agro = str(data_got.find('span', class_='full').text.replace(' ', '')) 
                tyre_coins_price_agro = str(data_got.find('span', class_='coins').text.replace(' ', '')) 
                tyre_price_agro = float(tyre_rub_price_agro + '.' + tyre_coins_price_agro)
                tyr_group = 'с/х'
            #    print('=8=', tyre_title_agro,'||', tyre_size_agro,'||', tyre_index_agro,'||', tyre_model_agro, '||', tyre_price_agro, '||', tyr_group)
                goods_dict_avtoset[tyre_size_agro, avtoset_good_num] = tyre_title_agro, tyre_model_agro, tyre_index_agro, tyr_group, tyre_price_agro 
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
        autoset_compet_obj_tyre_bulk_list = []
        list_tyre_sizes = []                                
        tyres_in_bd = tyres_models.Tyre.objects.all()
        for tyre in tyres_in_bd:
            for k, v in chosen_by_company_dict.items():
            #    print(k,v)
                if tyre.tyre_size.tyre_size == k[0]:
            #        print('TTTT', k)                                                                                            #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
                    #('235/75R17,5', 90) ('Triangle', 'TR689A', '143/141J', 560.18)                                # Cordiant Polar SL 205/ 55R16 94T ('165,00', '205/ 55R16', 'Cordiant Polar SL', '94T', 'Cordiant')
                    coma = v[0].find(',')           
                    pr = float
                    name_competitor, created = dictionaries_models.CompetitorModel.objects.get_or_create(
                        competitor_name =  v[0]
                    )
                    #print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',  name_competitor, 'name_competitor =', v[0])
                    if v[3]:
                        tyre_groupp = dictionaries_models.TyreGroupModel.objects.filter(tyre_group=v[3]) 
                    if tyre_groupp:
                        tyre_groupp = tyre_groupp[0]
                    else:
                        tyre_groupp = None                         
                #    if v[5]:
                #        season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name=v[5]) 
                #    if season_usage:
                #        season_usage = season_usage[0]
                #    else:
                #        season_usage = None 
                    try:
                        if v[5]:
                            season_usage = None
                            if v[5] == 'Зимняя шина':
                                season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name='зимние') 
                            if v[5] == 'Летняя шина': 
                                season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name='летние') 
                            if v[5] == 'Всесезонная шина':
                                season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name='всесезонные') 
                        if season_usage:
                            season_usage = season_usage[0]
                    except:
                        season_usage = None 
                    if coma:
                        pr = float(str(v[4]).replace(',', '.'))
                    list_tyre_sizes.append(k[0])
                    #list_comparative_analysis_tyre_objects = []
                    #for comparative_analys_tyres_model_object in models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=k[0]):
                    #    list_comparative_analysis_tyre_objects.append(comparative_analys_tyres_model_object)
                    autoset_compet_obj_tyre_bulk_list.append(models.CompetitorSiteModel(
                        site = 'autoset.by',
                        currency = dictionaries_models.Currency.objects.get(currency='BYN'),
                        price = pr,
                        date_period = datetime.datetime.today(),
                        developer = name_competitor,
                        tyresize_competitor = k[0],                                        
                        name_competitor = v[1], 
                        parametres_competitor = v[2],
                        season = season_usage,
                        group = tyre_groupp,
                    )    
                    )
        bulk_avtoset_compet = models.CompetitorSiteModel.objects.bulk_create(autoset_compet_obj_tyre_bulk_list)    
        list_tyre_sizes = set(list_tyre_sizes)
        for t_szz in list_tyre_sizes:
            for obbj, comparative_analys_tyres_model_object in itertools.product(models.CompetitorSiteModel.objects.filter(tyresize_competitor=t_szz, site = 'autoset.by'), models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=t_szz)):
                    obbj.tyre_to_compare.add(comparative_analys_tyres_model_object)             
                    ### OLD VERSION
                    ##competitor_site_model = models.CompetitorSiteModel.objects.update_or_create(
                    ##    site = 'autoset.by',
                    ##    currency = dictionaries_models.Currency.objects.get(currency='BYN'),
                    ##    price = pr,
                    ##    date_period = datetime.datetime.today(),
                    ##    developer = name_competitor,
                    ##    tyresize_competitor = k[0],                                        
                    ##    name_competitor = v[1], 
                    ##    parametres_competitor = v[2],
                    ##    season = season_usage,
                    ##    group = tyre_groupp,
                    ##    #tyre_to_compare = models.ComparativeAnalysisTyresModel.objects.get
                    ##)    
                    ##### добавлено: привязка к ComparativeAnalysisTyresModel одинаковый типоразмер
                    ###print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH1', competitor_site_model[0])
                    ##for comparative_analys_tyres_model_object in models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=k[0]):
                    ##    competitor_site_model[0].tyre_to_compare.add(comparative_analys_tyres_model_object)
                    #####
                    ### END OLD VERSION   
    except:
        pass                                                                                                                                                                                                                   
    ###### END OF АВТОСЕТЬ PARSING
    # 2 ###### ПАРСИНГ BAGORIA:
    def switch_between_pages_generator(start, devider, lsegk_pages_quantity,  gruz_pages_quantity,  indus_pages_quantity,  selhoz_pages_quantity): 
    #def switch_between_pages_generator(start, devider, lsegk_pages_quantity, lsegk_pages_quantity_funk, gruz_pages_quantity, gruz_pages_quantity_funk, indus_pages_quantity, indus_pages_quantity_funk, selhoz_pages_quantity, selhoz_pages_quantity_funk, bag_num): 
        # devider- на сколько частей разбить запрос на странице, чтобы к ней потом возвращаться. т.е. - если  группе 100 страниц - разделить на 4 е=например и перейти к след группе
        list_op_pages_to_to_go_through_in_group_in_every_loop = []
        while True:
            if start > devider:
                raise StopIteration                    
            lsegk_pages_quantity_pages_in_period_list = []
            pages = [0, 0]
            start_p = 0
            devided_val = int(lsegk_pages_quantity / devider)
            end_p = devided_val
            for n in range(0, devider):
                if n == devider - 1:
                    if end_p < lsegk_pages_quantity:
                       end_p = lsegk_pages_quantity
                pages = [start_p, end_p]
                lsegk_pages_quantity_pages_in_period_list.append(pages)
                start_p = end_p
                end_p += devided_val
        #    print('=============', lsegk_pages_quantity_pages_in_period_list)
            gruz_pages_quantity_pages_in_period_list = []
            pages = [0, 0]
            start_p = 0
            devided_val = int(gruz_pages_quantity / devider)
            end_p = devided_val
            for n in range(0, devider):
                if n == devider - 1:
                    if end_p < gruz_pages_quantity:
                       end_p = gruz_pages_quantity                        
                pages = [start_p, end_p]
                gruz_pages_quantity_pages_in_period_list.append(pages)
                start_p = end_p
                end_p += devided_val
        #    print('=============', gruz_pages_quantity_pages_in_period_list)
            indus_pages_quantity_pages_in_period_list = []
            pages = [0, 0]
            start_p = 0
            devided_val = int(indus_pages_quantity / devider)
            end_p = devided_val
            for n in range(0, devider):
                if n == devider - 1:
                    if end_p < indus_pages_quantity:
                       end_p = indus_pages_quantity                        
                pages = [start_p, end_p]
                indus_pages_quantity_pages_in_period_list.append(pages)
                start_p = end_p
                end_p += devided_val
        #    print('=============', indus_pages_quantity_pages_in_period_list)    
            selhoz_pages_quantity_pages_in_period_list = []
            pages = [0, 0]
            start_p = 0
            devided_val = int(selhoz_pages_quantity / devider)
            end_p = devided_val
            for n in range(0, devider):
                if n == devider - 1:
                    if end_p < selhoz_pages_quantity:
                       end_p = selhoz_pages_quantity                         
                pages = [start_p, end_p]
                selhoz_pages_quantity_pages_in_period_list.append(pages)
                start_p = end_p
                end_p += devided_val
        #    print('=============', selhoz_pages_quantity_pages_in_period_list)  
        #    lsegk_pages_quantity_funk(lsegk_pages_quantity_pages_in_period_list[start][0], lsegk_pages_quantity_pages_in_period_list[start][1], bag_num)
        #    gruz_pages_quantity_funk(gruz_pages_quantity_pages_in_period_list[start][0], gruz_pages_quantity_pages_in_period_list[start][1], bag_num)
        #    indus_pages_quantity_funk(indus_pages_quantity_pages_in_period_list[start][0], indus_pages_quantity_pages_in_period_list[start][1], bag_num)
        #    selhoz_pages_quantity_funk(selhoz_pages_quantity_pages_in_period_list[start][0], selhoz_pages_quantity_pages_in_period_list[start][1], bag_num)
            for n in range(0, devider):
                loop_pages_of_every_group = lsegk_pages_quantity_pages_in_period_list[n], gruz_pages_quantity_pages_in_period_list[n], indus_pages_quantity_pages_in_period_list[n], selhoz_pages_quantity_pages_in_period_list[n]
                list_op_pages_to_to_go_through_in_group_in_every_loop.append(loop_pages_of_every_group)
            yield list_op_pages_to_to_go_through_in_group_in_every_loop
    pages_in_legkovik = 0
    pages_in_gruzovik = 0
    pages_in_indus = 0
    pages_in_selhoz = 0
    def raw_generator_page(n, stop): #генератор сна:    
        while True:
            if n > stop:
                raise StopIteration
            yield n
            n += 1
            if n == 14:
                n = 0
    i = 4
    time_to_relax = 16
    page_curr = raw_generator_page(i, time_to_relax) 
    all_seasons = 'allseason'
    snow = 'winterColor'
    summer = 'summer'
    bagoria_good_num = 0
    # 1) Легковые шины
    ## попытка в прокси запрос
    #import requests
    #proxies = {
    #    "http": 'http://124.198.17.217', 
    #    "https": 'http://20.206.106.192'
    #}
    #session = requests.Session()
    #session.proxies.update(proxies)
    #session.get('http://example.org')
    ## END попытка в прокси запрос
    url = 'https://bagoria.by/legkovye-shiny/'       
    #webdriverr = webdriver.Chrome()
    #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    webdriverr = webdriverr_global
    webdriverr.get(url)
    soup = BeautifulSoup(webdriverr.page_source,'lxml')   
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
    pages_in_legkovik = urls_get
    def legkovik(pages_quantity_start, pages_quantity_end, bg_nm):
        bagoria_good_num = bg_nm
        url = 'https://bagoria.by/legkovye-shiny/' 
    #    for slug in range(pages_quantity_start, pages_quantity_end): 
        for slug in range(pages_quantity_start, 1):     
            #newUrl = url.replace('', f'/?PAGEN_1={slug}')       #https://bagoria.by/legkovye-shiny/?PAGEN_1=3
            newUrl = url + f'?nav=page-{slug}'       #https://bagoria.by/legkovye-shiny/?nav=page-9
            webdriverr.get(newUrl)
            val_sleep = next(page_curr)
        #    print('val_sleep =', val_sleep)
            if val_sleep == 10:
            #    print('TIME TO WAIT 1')
                time.sleep(9)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #    print('TIME TO WAIT 2')
                time.sleep(11)
            else:
                rand_val_to_wait = random.randint(5, 15)    # подождать рандомно неск секунд
                time.sleep(rand_val_to_wait)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(rand_val_to_wait)
            #    time.sleep(2)
            #    webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #    time.sleep(4)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_lt = soup.find_all('div', class_='accordion-manufacturers__main_item')
            if not products_lt:
                break
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
                tyre_price_lt = str(data_got.find('span', class_='accordion-manufacturers__main_price').text.replace(' ', '').replace('р.', '').replace(',', '.').replace(' ', '').lstrip().rstrip())  
                tyr_group = 'легковые'
                goods_dict_bagoria[tyre_size_lt, bagoria_good_num] = tyre_title_lt, tyre_model_lt, tyre_index_lt, tyr_group, tyre_price_lt, tyre_season_lt 
                bagoria_good_num += 1
        func_is_succeed = 'GoT'
        return func_is_succeed
    # 2) Грузовые шины
    url = 'https://bagoria.by/gruzovye-shiny/'
    #webdriverr = webdriver.Chrome()
    #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    webdriverr = webdriverr_global
    webdriverr.get(url)
    time.sleep(7)
    webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(12)
    soup = BeautifulSoup(webdriverr.page_source,'lxml')   
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
    pages_in_gruzovik = urls_get
    random_order_pages_list = random.sample(range(0,urls_get+1), urls_get+1)
    def gruzovik(pages_quantity_start, pages_quantity_end, bg_nm):
        bagoria_good_num = bg_nm
        url = 'https://bagoria.by/gruzovye-shiny/'
    #    for slug in range(pages_quantity_start, pages_quantity_end):   
        for slug in range(pages_quantity_start, 1):   
            newUrl = url + f'?PAGEN_1={slug}'       #https://bagoria.by/industr-shiny/
            webdriverr.get(newUrl)
            time.sleep(3)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_ts = soup.find_all('div', class_='accordion-manufacturers__main_item')
            if not products_ts:
                break                    
            for data_got in products_ts:
                tyre_title_ts = str(data_got.find('h6', class_='manufacturer').text).replace('\n', '').replace(' ', '').lstrip().rstrip()
                tyre_model_ts = str(data_got.find('div', class_='model').text).replace('\n', '').replace(' ', '')   
                tyre_size_ts = str(data_got.find('div', class_='size').text.replace(' ', '').replace('\n', '').replace(',', '.'))
                tyre_index_ts = str(data_got.find('p', class_='index').text).replace('\n', '').replace(' ', '')         
                tyre_param_ts = str(data_got.find('div', class_='accordion-manufacturers__main_layering').text).replace('\n', '').replace(' ', '')  
                tyre_price_ts = str(data_got.find('span', class_='accordion-manufacturers__main_price').text.replace(' ', '').replace('р.', '').replace(',', '.').replace(' ', '').lstrip().rstrip())     
                tyr_group = 'грузовые'
                goods_dict_bagoria[tyre_size_ts, bagoria_good_num] = tyre_title_ts, tyre_model_ts, tyre_index_ts, tyr_group, tyre_price_ts, tyre_param_ts 
            #    print('III', tyre_title_ts, tyre_model_ts, tyre_index_ts, tyr_group, tyre_price_ts, tyre_param_ts)
                bagoria_good_num += 1 
        func_is_succeed = 'GoT'
        return func_is_succeed              
    # 3) Грузовые индустриальные спец. шины
    url = 'https://bagoria.by/industr-shiny/'
    #webdriverr = webdriver.Chrome()
    #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    webdriverr = webdriverr_global
    webdriverr.get(url)
    time.sleep(8)
    webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(7)
    soup = BeautifulSoup(webdriverr.page_source,'lxml')  
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
    pages_in_indus = urls_get
    random_order_pages_list = random.sample(range(0,urls_get+1), urls_get+1) 
    def induztrial(pages_quantity_start, pages_quantity_end, bg_nm):
        url = 'https://bagoria.by/industr-shiny/'
        bagoria_good_num = bg_nm
    #    for slug in range(pages_quantity_start, pages_quantity_end): 
        for slug in range(pages_quantity_start, 1):     
            newUrl = url + f'?PAGEN_1={slug}'       #https://bagoria.by/industr-shiny/
            webdriverr.get(newUrl)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_ts = soup.find_all('div', class_='accordion-manufacturers__main_item')
            if not products_ts:
                break                     
            for data_got in products_ts:
                tyre_title_ts = str(data_got.find('h6', class_='manufacturer').text).replace('\n', '').replace(' ', '').lstrip().rstrip()
                tyre_model_ts = str(data_got.find('div', class_='model').text).replace('\n', '').replace(' ', '')   
                tyre_size_ts = str(data_got.find('div', class_='size').text.replace(' ', '').replace('\n', '').replace(',', '.'))
                tyre_index_ts = str(data_got.find('p', class_='index').text).replace('\n', '').replace(' ', '')         
                tyre_param_ts = str(data_got.find('div', class_='accordion-manufacturers__main_layering').text).replace('\n', '').replace(' ', '')  
                tyre_price_ts = str(data_got.find('span', class_='accordion-manufacturers__main_price').text.replace(' ', '').replace('р.', '').replace(',', '.').replace(' ', '').lstrip().rstrip())     
                tyr_group = 'грузовые'
                goods_dict_bagoria[tyre_size_ts, bagoria_good_num] = tyre_title_ts, tyre_model_ts, tyre_index_ts, tyr_group, tyre_price_ts, tyre_param_ts 
            #    print('III', tyre_title_ts, tyre_model_ts, tyre_index_ts, tyr_group, tyre_price_ts, tyre_param_ts)
                bagoria_good_num += 1  
        func_is_succeed = 'GoT'
        return func_is_succeed
    # 4) Сельскохозяйственные шины
    url = 'https://bagoria.by/selhoz-shiny/'
    #webdriverr = webdriver.Chrome()
    #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    webdriverr = webdriverr_global
    webdriverr.get(url)
    time.sleep(5)
    webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(7)
    soup = BeautifulSoup(webdriverr.page_source,'lxml') 
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
    pages_in_selhoz = urls_get
    random_order_pages_list = random.sample(range(0,urls_get+1), urls_get+1)
    def selhozka(pages_quantity_start, pages_quantity_end, bg_nm):
        bagoria_good_num = bg_nm
        url = 'https://bagoria.by/selhoz-shiny/'
    #    print('ISISISIISISSISS', pages_quantity_start, pages_quantity_end)
    #    for slug in range(pages_quantity_start, pages_quantity_end):
        for slug in range(pages_quantity_start, 1):
            newUrl = url + f'?PAGEN_1={slug}'       #https://bagoria.by/selhoz-shiny/
            webdriverr.get(newUrl)
            time.sleep(4)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(6)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            products_agro = soup.find_all('div', class_='accordion-manufacturers__main_item')
            if not products_agro:
                break                     
            for data_got in products_agro:
                tyre_title_agro = str(data_got.find('h6', class_='manufacturer').text).replace('\n', '').replace(' ', '').lstrip().rstrip()
                tyre_model_agro = str(data_got.find('div', class_='model').text).replace('\n', '').replace(' ', '')   
                tyre_size_agro = str(data_got.find('div', class_='size').text.replace(' ', '').replace('\n', '').replace(',', '.'))
                tyre_index_agro = str(data_got.find('p', class_='index').text).replace('\n', '').replace(' ', '')         
                tyre_param_agro = str(data_got.find('div', class_='accordion-manufacturers__main_layering').text).replace('\n', '').replace(' ', '')  
                tyre_price_agro = str(data_got.find('span', class_='accordion-manufacturers__main_price').text.replace(' ', '').replace('р.', '').replace(',', '.').replace(' ', '').lstrip().rstrip())     
                tyr_group = 'с/х'
                goods_dict_bagoria[tyre_size_agro, bagoria_good_num] = tyre_title_agro, tyre_model_agro, tyre_index_agro, tyr_group, tyre_price_agro, tyre_param_agro
    #            print('OLOLO', tyre_title_agro, tyre_model_agro, tyre_index_agro, tyr_group, tyre_price_agro, tyre_param_agro)
                bagoria_good_num += 1 
        func_is_succeed = 'GoT'
        return func_is_succeed
    # формируем отдельный список ПРОИЗВОДИТЕЛИ:
    def formirovanie_dla_zapisi(some_dict):
        goods_dict_bagoria = some_dict
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
        bagoria_compet_obj_tyre_bulk_list = [] 
        list_tyre_sizes = []
        current_stack_of_competitors_before_write_in_base = []       
        #print('chosen_by_company_dict', chosen_by_company_dict)
        # сопоставление с БД  и запись в БД конкурентов (Bagoria):
        tyres_in_bd = tyres_models.Tyre.objects.all()
        for tyre in tyres_in_bd:
            try:
                for k, v in chosen_by_company_dict.items():
                    #print(k, 'GGG', v, 'GGG', len(v))
                    if tyre.tyre_size.tyre_size == k[0]:
                    #    print('TTTT', k, 's111', v)           TTTT ('155/65R13', 431) s111 ('WestLake', 'SW618', '73T', 'зимние', 'легковые', '126.07')                                                                                  #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
                        #('13.0/65-18', 399) ('OZKA', 'KNK48', '144A8TL', 'нс16', 'с/х', '698.98')
                        coma = v[0].find(',')           
                        pr = None
                        name_competitor, created = dictionaries_models.CompetitorModel.objects.get_or_create(
                            competitor_name =  v[0]
                        )
                        if v[3]:
                            tyre_gggroup = dictionaries_models.TyreGroupModel.objects.filter(tyre_group=v[3]) 
                        #    print('!!!!!', tyre_gggroup)
                        if tyre_gggroup:
                            tyre_gggroup = tyre_gggroup[0]
                        else:
                            tyre_gggroup = None 
                        try:
                           if v[5]:
                               season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name=v[5]) 
                           if season_usage:
                               season_usage = season_usage[0]
                            #   print('season_usage', season_usage)
                        except:
                               season_usage = None 
                        if coma and len(v) > 3 and v[4]:  #len(v[4]) == 5 :
                        #    print('OOOOOOOOOOOOOOOO', v[5])
                            pr = float(str(v[4]).replace(',', '.'))
                        #list_comparative_analysis_tyre_objects = []    
                        #for comparative_analys_tyres_model_object in models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=k[0]):
                        #    list_comparative_analysis_tyre_objects.append(comparative_analys_tyres_model_object)                                    
                        list_tyre_sizes.append(k[0])
                        ## вынужденная провкерка на наличие дублеров в базе и в текущем стеке (стек перед записью в базу):
                        # 1) проверка на наличие в стеке таких же конкурентов:
                        this_tyre_is_not_in_current_stack_of_competitors_before_write_in_base = False
                        this_tyre_parameters = 'bagoria.by', pr, datetime.datetime.today().date(), k[0], v[1]
                        if this_tyre_parameters not in current_stack_of_competitors_before_write_in_base:
                            current_stack_of_competitors_before_write_in_base.append(this_tyre_parameters)
                            this_tyre_is_not_in_current_stack_of_competitors_before_write_in_base = True
                        else:
                            pass
                        #    print('this_t5654757567657657===', this_tyre_parameters)
                        #print('this_tyre_parameters', this_tyre_parameters)
                        #print('=========================')
                        # 2)  проверка на наличие подобного конкурента в базе:
                        compet_obj_with_same_param = models.CompetitorSiteModel.objects.filter(tyresize_competitor=k[0], price = pr, site = 'bagoria.by', date_period = datetime.datetime.today(), name_competitor = v[1], parametres_competitor = v[2])
                        ## END вынужденная провкерка на наличие дублеров в базе
                        if not compet_obj_with_same_param and this_tyre_is_not_in_current_stack_of_competitors_before_write_in_base is True: # если ни в базе, ни в стеке такого конкурента нет - запишем   
                            bagoria_compet_obj_tyre_bulk_list.append(models.CompetitorSiteModel(
                                site = 'bagoria.by',
                                currency = dictionaries_models.Currency.objects.get(currency='BYN'),
                                price = pr,
                                date_period = datetime.datetime.today(),
                                developer = name_competitor,
                                tyresize_competitor = k[0],                                               
                                name_competitor = v[1], 
                                parametres_competitor = v[2],
                                group = tyre_gggroup,                       
                                season = season_usage
                                #tyre_to_compare = models.ComparativeAnalysisTyresModel.objects.get
                            ) 
                            )
                        ### добавлено: привязка к ComparativeAnalysisTyresModel одинаковый типоразмер
                        #print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH1', competitor_site_model[0])
                 
                            #print(comparative_analys_tyres_model_object.tyre__tyre_size__tyre_size, '+++', competitor_site_model[0].site, competitor_site_model[0].developer.competitor_name, competitor_site_model[0].tyresize_competitor, competitor_site_model[0].price, competitor_site_model[0].developer.competitor_name)
                        ### 
            except:
                pass
        bulk_bagoria_compet = models.CompetitorSiteModel.objects.bulk_create(bagoria_compet_obj_tyre_bulk_list)
        list_tyre_sizes = set(list_tyre_sizes)
        for t_szz in list_tyre_sizes:
            for obbj, comparative_analys_tyres_model_object in itertools.product(models.CompetitorSiteModel.objects.filter(tyresize_competitor=t_szz, site = 'onliner.by'), models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=t_szz)):
                    obbj.tyre_to_compare.add(comparative_analys_tyres_model_object)                                
        return 'Zapis Got'                
    sstart = 0
    ddevider = 2######################  ВАЖНО = ключевое значение вводить здесь - на сколько разбивать запрос
    got_pages_in_loop = []
    page_switch = switch_between_pages_generator(sstart, ddevider, pages_in_legkovik, pages_in_gruzovik, pages_in_indus, pages_in_selhoz) 
    #page_switch = switch_between_pages_generator(sstart, ddevider, pages_in_legkovik, legkovik, pages_in_gruzovik, gruzovik, pages_in_indus, induztrial, pages_in_selhoz, selhozka, bagoria_good_num) 
    got_pages_in_loop = next(page_switch)
    def try_to_make_all_loops_generator(n, stop, loops): #генератор для аовторения попыток повторно- продолжить парсинг и снять дынные, если была ошибка:    
        while True:
            if n > stop or n == stop:
                raise StopIteration
            yield loops[n]
            n += 1
    start_loops = sstart
    end_loops = ddevider
    curr_loop = try_to_make_all_loops_generator(start_loops, end_loops, got_pages_in_loop) 
    ##for loop in got_pages_in_loop:
    ##   print('loop loop loop loop loop loo loop loop loo loop loop loo', loop)
    ##   legkovik(loop[0][0], loop[0][1],bagoria_good_num)
    ##   # print('legkovik', loop[0][0], loop[0][1])
    ##   gruzovik(loop[1][0], loop[1][1],bagoria_good_num) 
    ##   # print('gruzovik', loop[1][0], loop[1][1])
    ##   induztrial(loop[2][0], loop[2][1],bagoria_good_num)
    ##   # print('induztrial', loop[2][0], loop[2][1])
    ##   selhozka(loop[3][0], loop[3][1], bagoria_good_num)
    ##   # print('selhozka', loop[3][0], loop[3][1])
    ##   loop_is_successfull_is = None
    ##   loop_is_successfull_is = formirovanie_dla_zapisi(goods_dict_bagoria)
    ##   time.sleep(500)
    loop_is_not_successfull = False
    loop = None
    loop_step = 0
    #print('oop_step', loop_step)
    while loop_step < ddevider:    
        if loop_is_not_successfull is False:
           loop = next(curr_loop)
           loop_step += 1
           #print(loop_step, '-----||||-----', loop)
        else:
           pass
        #print('loop loop loop loop loop loo loop loop loo loop loop loo', loop)
        one_func_is_passed = False
        legk_got = None
        legk_got = legkovik(loop[0][0], loop[0][1],bagoria_good_num)
        #print('legk_got', legk_got)
        if not legk_got:
            one_func_is_passed = True
        # print('legkovik', loop[0][0], loop[0][1])
        gruzovik_got = None
        gruzovik_got = gruzovik(loop[1][0], loop[1][1],bagoria_good_num) 
        #print('gruzovik_got', gruzovik_got)
        if not gruzovik_got:
            one_func_is_passed = True
        # print('gruzovik', loop[1][0], loop[1][1])
        induztrial_got = None
        induztrial_got = induztrial(loop[2][0], loop[2][1],bagoria_good_num)
        #print('induztrial_got', induztrial_got)
        if not induztrial_got:
            one_func_is_passed = True
        # print('induztrial', loop[2][0], loop[2][1])
        selhozka_got = None
        selhozka_got = selhozka(loop[3][0], loop[3][1], bagoria_good_num)
        #print('selhozka_got', selhozka_got)
        if not selhozka_got:
            one_func_is_passed = True
        # print('selhozka', loop[3][0], loop[3][1])
        #loop_is_successfull_is = None
        #loop_is_successfull_is = formirovanie_dla_zapisi(goods_dict_bagoria)
        #print('loop_is_successfull_is ==============', loop_is_successfull_is)
        #if not loop_is_successfull_is or one_func_is_passed is True: # если анные не собраны либо одна из функций была прервана - повторить текущий loop
        #    loop_is_not_successfull = True
        #else:
        #    loop_is_not_successfull = False  
        ##time.sleep(500)
        if one_func_is_passed is True: # если одна из функций была прервана - повторить текущий loop
            loop_is_not_successfull = True
        else:
            loop_is_not_successfull = False   
        if loop_step == ddevider - 1:   # на поседнем прогоне - лупе сделать запись  в базу
            loop_is_successfull_is = formirovanie_dla_zapisi(goods_dict_bagoria)                                                                                                                                                                                                  
    ###### END OF BAGORIA PARSING
                               

def russia_sites_parsing():

            chromeOptions1 = webdriver.ChromeOptions() 
            chromeOptions1.add_argument("--no-sandbox") 
            chromeOptions1.add_argument("--disable-setuid-sandbox") 
            chromeOptions1.add_argument("--disable-dev-shm-usage");
            chromeOptions1.add_argument("--headless") 
            chromeOptions1.add_argument("--disable-extensions") 
            chromeOptions1.add_argument("disable-infobars")
            webdriverr_global = webdriver.Chrome(options=chromeOptions1)

            #webdriverr_global = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            # 1 ###### ПАРСИНГ express-shina:
            try:
                express_shina_good_num = 0
                # 1) парсинг грузовых шин
                url = 'https://express-shina.ru/search/gruzovyie-shinyi'       
                #webdriverr = webdriver.Chrome()
                #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                webdriverr = webdriverr_global
                webdriverr.get(url)
                time.sleep(2)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
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
                    time.sleep(3)
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
                            #print('tyre_period', tyre_period)
                            if len(tyre_period) > 1:
                                tyre_period = tyre_period[1]
                                end_pos = tyre_period.find('Слойность')
                                if end_pos:
                                    tyre_period = tyre_period[0:end_pos]
                            #print('tyre_period', tyre_period)
                            #tyr_primenjaemost = tyre_period
                        #print(tyr_size, '=tyr_size', tyr_producer, '=tyr_producer', tyr_model, '=tyr_model', tyr_indexes, '=tyr_indexes', tyr_usabiity, '=tyr_usabiity', tyr_ply, '=tyr_ply')
                        goods_dict_express_shina[tyr_size, express_shina_good_num] = tyr_producer, tyr_model, tyr_indexes, tyr_group,  tyre_rub_price, tyr_usabiity,  tyr_ply
                        express_shina_good_num += 1 
                # 2) парсинг легковых шин
                url = 'https://express-shina.ru/search/legkovyie-shinyi'       
                #webdriverr = webdriver.Chrome()
                #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                webdriverr = webdriverr_global
                webdriverr.get(url)
                time.sleep(2)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
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
        #        goods_dict_express_shina_dopolnitelno = {} 
                pages_num = urls_get[-1] 
                thousands = urls_get[-1]
                if pages_num > 1000 :
                    thousands = 1000

                #!!!!!!!!!!!
                pages_num_list = [[0, thousands],[thousands, pages_num]] 
                #pages_num_list = [[0, 1],[1, 2]]                            # CТРАНИЦЫ
                #!!!!!!!!!!!

                #for pg in pages_num_list:                                         
                #    for slug in pg:                             # мое добавление специально для express-shina  # c 1 по 2 станицы
                for slug in range(1, 2):
                        if slug == 1000:
                            time.sleep(100)

                        newUrl = url + f'?num={slug}'       #https://express-shina.ru/search/gruzovyie-shinyi?num=2
                        webdriverr.get(newUrl)
                        time.sleep(2)
                        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(3)
                        soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                        products = soup.find_all('div', class_='b-offer')   
                        for data_got in products:
                            tyre_title, tyre_rub_price = None, None
                            try:
                                tyre_title = str(data_got.find('a', class_='b-offer-main__title').text.replace('новая', '').replace('Легковая шина ', ''))   
                                tyre_rub_price = str(data_got.find('div', class_='b-offer-pay__price').text.replace('₽', '').replace(' ', '').replace('\xa0', ''))   
                            except:
                                pass
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
                                    if tyr_size_index_in_list:
                                        for some_data in (1, tyr_size_index_in_list-1):
                                            tyr_model += tyr_data_list[some_data]
                                    tyr_group = 'легковая'
                            tyre_period = str(data_got.find('ul', class_='b-offer-main__parameters').text.replace('Наличие шипов:', ''))
                            tyr_per = ''
                            tyr_spike = ''
                            if tyre_period and len(tyre_period) > 1:
                                obrezra = tyre_period.find('Сезон:') + 7
                                tyre_period = tyre_period[obrezra:].split(' ')
                                try:
                                    tyr_per = tyre_period[0]
                                except:
                                    pass
                                try:
                                    tyr_spike = tyre_period[1]
                                except:
                                    pass                            
                    ###        if slug < 1000:
                                goods_dict_express_shina[tyr_size, express_shina_good_num] = tyr_producer, tyr_model, tyr_indexes, tyr_group, tyre_rub_price, tyr_per, tyr_spike,
                    ###        else:
                    ###            goods_dict_express_shina_dopolnitelno[tyr_size, express_shina_good_num] = tyr_producer, tyr_model, tyr_indexes, tyr_group, tyre_rub_price, tyr_per, tyr_spike,
                    ###        express_shina_good_num += 1 
                ###goods_dict_express_shina_dopolnitelno.update(goods_dict_express_shina_dopolnitelno)    
                #   for k, v in goods_dict_express_shina.items():
                #       print(k, v, '!!!')
                # 3) парсинг легкогрузовых шин
                url = 'https://express-shina.ru/search/legkogruzovyie-shinyi'       
                #webdriverr = webdriver.Chrome()
                #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                webdriverr = webdriverr_global
                webdriverr.get(url)
                time.sleep(2)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
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
                    try:
                        newUrl = url + f'?num={slug}'       #https://express-shina.ru/search/legkogruzovyie-shinyi?num=2
                        webdriverr.get(newUrl)
                        time.sleep(1)
                        webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(3)
                        soup = BeautifulSoup(webdriverr.page_source,'lxml')   
                        products = soup.find_all('div', class_='b-offer')   
                        tyr_indexes_reg = ['\d{3}\/\d{3}[A-Za-z]',       #107/105R
                        '\d{2}[A-Za-z]\/\d{2}[A-Za-z]',
                        '\d{3}[A-Za-z]\/\d{2}[A-Za-z]',
                        '\d{2}[A-Za-z]\/\d{3}[A-Za-z]',
                        ]
                        for data_got in products:
                            try:
                                tyre_title = str(data_got.find('a', class_='b-offer-main__title').text.replace('Легкогрузовая шина ', '').replace('новая', '')) 
                                tyre_rub_price = str(data_got.find('div', class_='b-offer-pay__price').text.replace('₽', '').replace(' ', '').replace('\xa0', ''))   
                            except:
                                pass
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
                                        try:
                                            if len_list > tyr_size_index_last+2 or len_list == tyr_size_index_last+2:
                                                tyr_indexes = tyr_data_list[tyr_size_index_last+1 ] + tyr_data_list[tyr_size_index_last+2]
                                        except:
                                            pass
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
                    except:
                        pass
                #   for k, v in goods_dict_express_shina.items():
                #       print(k, v, '!!!')
           #        3) парсинг спец шин
                url = 'https://express-shina.ru/search/spetcshinyi'       
                #webdriverr = webdriver.Chrome()
                #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                webdriverr = webdriverr_global
                webdriverr.get(url)
                time.sleep(2)
                webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
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
                        try:
                            tyre_title = str(data_got.find('a', class_='b-offer-main__title').text.replace('Спецшина ', '').replace('новая', '')) 
                            tyre_rub_price = str(data_got.find('div', class_='b-offer-pay__price').text.replace('₽', '').replace(' ', '').replace('\xa0', ''))   
                        except:
                            pass
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
                                try:
                                    print('==-===--==', tyr_data_list, '----', tyr_size_index_in_list)
                                    tyr_indexes = tyr_data_list[tyr_size_index_in_list+1]
                                    for nn in tyr_indexes_reg:
                                        result2 = re.search(rf'(?i){nn}', tyr_indexes)
                                        if result2:
                                            #print('result2', result2, tyr_indexes)
                                            break
                                        else:
                                            if len_list > tyr_size_index_in_list+2 or len_list == tyr_size_index_in_list+2:
                                                tyr_indexes = tyr_data_list[tyr_size_index_in_list+1] 
                                except:
                                    pass
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
                express_shina_compet_obj_tyre_bulk_list = []
                list_tyre_sizes = []
                tyres_in_bd = tyres_models.Tyre.objects.all()
                for tyre in tyres_in_bd:
                    for k, v in chosen_by_company_dict.items():
                        #print(k, 'GGG', v, 'GGG', len(v))
                    #    name_competitor = None
                        if tyre.tyre_size.tyre_size == k[0]:
                            #print('TTTT', k)                                                                                            #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
                            coma = v[0].find(',')  
                            pr = None                
                            name_competitor, created = dictionaries_models.CompetitorModel.objects.get_or_create(
                                competitor_name = v[0]
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
                            list_tyre_sizes.append(k[0])
                            express_shina_compet_obj_tyre_bulk_list.append(models.CompetitorSiteModel(
                                site = 'express-shina.ru',
                                currency = dictionaries_models.Currency.objects.get(currency='RUB'),
                                price = pr,
                                date_period = datetime.datetime.today(),
                                developer = name_competitor,
                                tyresize_competitor = k[0],
                                name_competitor = v[1], 
                                parametres_competitor = v[2],
                            #    season = season_usage,
                            #    group = ,
                            )        
                            )
                bulk_express_compet = models.CompetitorSiteModel.objects.bulk_create(express_shina_compet_obj_tyre_bulk_list)
                list_tyre_sizes = set(list_tyre_sizes)
                for t_szz in list_tyre_sizes:
                    for obbj, comparative_analys_tyres_model_object in itertools.product(models.CompetitorSiteModel.objects.filter(tyresize_competitor=t_szz, site = 'express-shina.ru'), models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=t_szz)):
                            obbj.tyre_to_compare.add(comparative_analys_tyres_model_object)   
            except:
                pass   
            ##### END OF express-shina PARSING

            # 2 ###### ПАРСИНГ kolesatyt:
            try:
                kolesatyt_good_num = 0
                # 1) парсинг грузовых шин
                url = 'https://kolesatyt.ru/podbor/gruzovye-shiny/'       
                #webdriverr = webdriver.Chrome()
                #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                webdriverr = webdriverr_global
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
                #webdriverr = webdriver.Chrome()
                #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                webdriverr = webdriverr_global
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
                #webdriverr = webdriver.Chrome()
                #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                webdriverr = webdriverr_global
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
                kolesatyt_compet_obj_tyre_bulk_list = []
                list_tyre_sizes = []                
                
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

                            list_tyre_sizes.append(k[0])
                            kolesatyt_compet_obj_tyre_bulk_list.append(models.CompetitorSiteModel(
                                site = 'kolesatyt.ru',
                                currency = dictionaries_models.Currency.objects.get(currency='RUB'),
                                price = pr,
                                date_period = datetime.datetime.today(),
                                developer = name_competitor,
                                tyresize_competitor = k[0],                                        
                                name_competitor = v[1], 
                                parametres_competitor = v[2],
                            #    season = season_usage,
                            #    group = tyre_groupp,
                            )    
                            )
                kolesatyt_compet = models.CompetitorSiteModel.objects.bulk_create(kolesatyt_compet_obj_tyre_bulk_list)
    
                list_tyre_sizes = set(list_tyre_sizes)
                for t_szz in list_tyre_sizes:
                    for obbj, comparative_analys_tyres_model_object in itertools.product(models.CompetitorSiteModel.objects.filter(tyresize_competitor=t_szz, site = 'kolesatyt.ru'), models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=t_szz)):
                            obbj.tyre_to_compare.add(comparative_analys_tyres_model_object)   
            except:
                pass                                                                                                                                                                                                                   
            ###### END OF kolesatyt PARSING

            # 3 ###### ПАРСИНГ KOLESA_DAROM:
            try:     
                kolesa_darom_good_num = 0
                # 1) парсинг легковых зимних шин
                url = 'https://www.kolesa-darom.ru/catalog/avto/shiny/zima/'       
                #webdriverr = webdriver.Chrome()
                #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                webdriverr = webdriverr_global
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
                    link_is = link.text
                    link_is = re.findall(r'\d+', link_is)
                    if link_is:
                        link_is = link_is[0]
                        pageNum = int(link_is) if link_is.isdigit() else None
                        if pageNum != None:
                            urls_get.append(pageNum)#
        #        print('!!!!======++', 'urls_get', urls_get)
                #2. получаем данные со всех страниц:                         
                #for slug in range(0, urls_get[-1]):                             # мое добавление специально для express-shina  # c 1 по 2 станицы
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
                        tyre_rub_price = str(data_got.find('div', class_='product-card__button-wrap').text.replace('₽', '').replace(' ', ''))#.replace('\xa0', ''))   
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
                #webdriverr = webdriver.Chrome()
                #webdriverr = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                webdriverr = webdriverr_global
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
                    link_is = link.text
                    link_is = re.findall(r'\d+', link_is)
                    if link_is:
                        link_is = link_is[0]
                        pageNum = int(link_is) if link_is.isdigit() else None
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
                        tyre_rub_price = str(data_got.find('div', class_='product-card__button-wrap').text.replace('₽', '').replace(' ', ''))#.replace('\xa0', ''))  
                        #print(tyre_title)
                        #tyre_rub_price = str(data_got.find('button', 'product-card__button kd-btn kd-btn--small kd-btn--flex kd-btn_primary').text.replace('₽', '').replace(' ', ''))#.replace('\xa0', ''))   
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
                kolesa_darom_compet_obj_tyre_bulk_list = [] 
                list_tyre_sizes = []
                current_stack_of_competitors_before_write_in_base = []       
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
                                str_to_float = str(v[4]).replace(',', '.').replace(' ', '')
                                if str_to_float.isdigit():
                                    pr = float(str_to_float) 
                            kolesa_darom_compet_obj_tyre_bulk_list.append(models.CompetitorSiteModel(
                                site = 'kolesa-darom.ru',
                                currency = dictionaries_models.Currency.objects.get(currency='RUB'),
                                price = pr,
                                date_period = datetime.datetime.today(),
                                developer = name_competitor,
                                tyresize_competitor = k[0],                                               
                                name_competitor = v[1], 
                                parametres_competitor = v[2],
                            #    group = tyre_gggroup,                       
                            #    season = season_usage
                                #tyre_to_compare = models.ComparativeAnalysisTyresModel.objects.get
                            ) 
                            )
                bulk_kolesa_darom_compet = models.CompetitorSiteModel.objects.bulk_create(kolesa_darom_compet_obj_tyre_bulk_list)
                list_tyre_sizes = set(list_tyre_sizes)
                for t_szz in list_tyre_sizes:
                    for obbj, comparative_analys_tyres_model_object in itertools.product(models.CompetitorSiteModel.objects.filter(tyresize_competitor=t_szz, site = 'kolesa-darom.ru'), models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=t_szz)):
                            obbj.tyre_to_compare.add(comparative_analys_tyres_model_object)                
            except:
                pass
            # 3 END  ###### ПАРСИНГ KOLESA_DAROM

def running_programm():
    ###get_year  = datetime.datetime.now().year
    ###get_month  = datetime.datetime.now().month
    ###get_day  = datetime.datetime.now().day
    ###     
    ###start = datetime.datetime(get_year, get_month, get_day, 12, 30) # !!!!!!! для введения часа и мин ля запуска скрипта
    ###delta = datetime.timedelta(minutes=0)
    ###end = start + delta
    ###end_hour = end.hour
    ###end_minute = end.minute
    ###end_execution = start + datetime.timedelta(minutes=2)
    ####print('end_hour', end_hour, 'end_minute', end_minute)
    ###couple_min_checking = datetime.timedelta(minutes=1)
    ###get_current_time = datetime.datetime.now()
    ###minutes_to_start_left =  start - get_current_time 
    ###print('!!!', minutes_to_start_left)
    ###if minutes_to_start_left < couple_min_checking: # если до времени запуска скрипта осталось менее минуты - то начать
    ###    #while True:
    ###    ##    print(datetime.datetime.now())
    ###    #    current_time = datetime.datetime.now()
    ###    #    if current_time.hour == end_hour and current_time.minute == end_minute:    
    ###    #        belarus_sites_parsing()
    ###    #        break
    ###    #    elif current_time.hour == end_execution.hour and current_time.minute == end_execution.minute:  
    ###    #        break
    ###    belarus_sites_parsing()
    belarus_sites_parsing()
    pass
    return 'the programm is fullfilled'

running_programm()

