<<<<<<< HEAD
version https://git-lfs.github.com/spec/v1
oid sha256:cf0173908fb8080e29e01e4c2d9aff9402108523617c383709797e1bb53c08ee
size 551889
=======
### for if __name__ == "__main__": ========= for TEST_SCRIPT
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "proj.settings"
import django
django.setup()
### END for if __name__ == "__main__": ========= for TEST_SCRIPT


from django.shortcuts import render
from prices import models
from tyres import models as tyres_models
from django.views.generic import DetailView, View, TemplateView
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
#from webdriver_manager.chrome import ChromeDriverManager
#from django.db.models import Min

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
    chromeOptions1.add_argument("--disable-dev-shm-usage")
    chromeOptions1.add_argument('--headless=old')
    #chromeOptions1.add_argument("--headless") 
    #chromeOptions1.add_argument("--disable-extensions") 
    #chromeOptions1.add_argument("disable-infobars")
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
        if pages:
            links = pages.find_all('a', class_='catalog-pagination__pages-link')
            for link in links:
                pageNum = int(link.text) #if link.text.isdigit() else None
                print('pageNum', pageNum)
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
    try:
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
    except:
        pass                                                                                                                                                                                               
    ###### END OF BAGORIA PARSING
                               

def russia_sites_parsing():

            chromeOptions1 = webdriver.ChromeOptions() 
            chromeOptions1.add_argument("--no-sandbox") 
            chromeOptions1.add_argument("--disable-setuid-sandbox") 
            chromeOptions1.add_argument("--disable-dev-shm-usage");
            chromeOptions1.add_argument("--headless") 
            chromeOptions1.add_argument("--disable-extensions") 
            #chromeOptions1.add_argument("disable-infobars")
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
            #parsing_script.belarus_sites_parsing()
            pass
 
        return comparative_analysis_table

    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        obj = context.get('object')

        # ДЛЯ ПОЛУЧЕНИЯ ВАЛЮТЫ ПО КУРСУ НБ РБ НА ДАТУ       
        curr_value = None
        currency = None
        shown_date = None
        if models.CURRENCY_ON_DATE is False:                         # запускаем получение курса валют с НБ РБ только раз за день
            try:
                cu, cu_val, sh_date = my_tags.currency_on_date()
                if datetime.datetime.today().strftime("%Y-%m-%d") == sh_date:       # если на сегодняшнюю дату результат получен - то более не запрашивать
                    currency, curr_value, shown_date = cu, cu_val, sh_date
                    models.CURRENCY_IS_CLEANED = currency, curr_value, shown_date   # записываем полученные значения
                    models.CURRENCY_ON_DATE = True
            except:
                currency, curr_value, shown_date = my_tags.currency_on_date()     # если что -то пошло не так - берем данные с сайта  
                models.CURRENCY_IS_CLEANED = currency, curr_value, shown_date
                models.CURRENCY_ON_DATE = True  
        if models.CURRENCY_DATE_GOT_FROM_USER:                              # если пользователь вводит данные (получить курс на определенную дату): #
            if models.CURRENCY_DATE_GOT_FROM_USER_CLEANED:                  # если только что получал данные на эту дату - то не надо запускать фунцкию - взять что уже собрано
                try:
                    currency_already, curr_value_already, shown_date_already = models.CURRENCY_DATE_GOT_FROM_USER_CLEANED
                    if shown_date_already == models.CURRENCY_DATE_GOT_FROM_USER:
                       currency_already, curr_value_already, shown_date_already = models.CURRENCY_DATE_GOT_FROM_USER_CLEANED 
                    else:
                        currency, curr_value, shown_date = my_tags.currency_on_date()
                        models.CURRENCY_DATE_GOT_FROM_USER_CLEANED = currency, curr_value, shown_date
                except:
                    currency, curr_value, shown_date = my_tags.currency_on_date()
                    models.CURRENCY_DATE_GOT_FROM_USER_CLEANED = currency, curr_value, shown_date
                if shown_date_already == models.CURRENCY_DATE_GOT_FROM_USER:
                   currency, curr_value, shown_date = currency_already, curr_value_already, shown_date_already
            else:                                                           # если ничего - тогда обращаемся к функции:
                currency, curr_value, shown_date = my_tags.currency_on_date()
                models.CURRENCY_DATE_GOT_FROM_USER_CLEANED = currency, curr_value, shown_date

        
#        models.CURRENCY_VALUE_RUB = curr_value / 100
        models.CURRENCY_VALUE_USD = curr_value 
        # END ДЛЯ ПОЛУЧЕНИЯ ВАЛЮТЫ ПО КУРСУ НБ РБ НА ДАТУ


        #### 0 подбор шин с их данными по минималкам для отображения в таблице на определенный период (не конкуренты , а именно собственная продукция)
        # ОПРЕДЕЛЕНИЕ ДАТЫ: 
        if not models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and not models.COMPETITORS_DATE_FROM_USER_ON_FILTER:           #ЕСЛИ ПОЛЬЗОВАТЕЛЬ НЕ ВЫБИРАЛ НИ НАЧ НИ КОНЕЧ ДАТЫ
            today_is = datetime.date.today()                                                                # автоматически ставит дату на неделю назад
            week_ago_date = today_is - datetime.timedelta(days=7)
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START = [week_ago_date.strftime('%Y-%m-%d')]
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER = [today_is.strftime('%Y-%m-%d')]
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START_IS_NOT_CHOSEN = True 
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_IS_NOT_CHOSEN = True  
        #    print("НЕ ВЫСТАВЛЕНЫ  НАЧ И КОН ДАТЫ")




        if not models.COMPETITORS_DATE_FROM_USER_ON_FILTER:  
        # 00.1  выборка всех имеющихся периодов с минималками:
            competitors_exist_all_dates = models.CompetitorSiteModel.objects.all().dates('date_period', 'day') # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ВСЕ ДАТЫ ДОСТУПНЫЕ ВООБЩЕ ВСЕХ КОНКУРЕТОВ все даты доступные вообще всех конкурентов
            competitors_exist_all_dates_last_date_latest_date = max(competitors_exist_all_dates)  # КОНКУРЕНТЫ ПО СТОСТОЯНИЮ НА ДАТУ
            context['table_current_date_for_header'] = competitors_exist_all_dates_last_date_latest_date.strftime("%d.%m.%Y")
    #        print('***** no date from user')
        else:
            # для поиска по собственной продукции с ходом в шаг = месяц       
            date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()                 # ['2023-01-23']
            competitors_exist_all_dates_last_date_latest_date = date_filter    # КОНКУРЕНТЫ ПО СТОСТОЯНИЮ НА ДАТУ
            context['table_current_date_for_header'] = competitors_exist_all_dates_last_date_latest_date.strftime("%d.%m.%Y")
    #        print('***** date from user')

        ################
        ################
        get_all_dates_year_month = obj.comparative_table.dates('sale_data', 'month')
        if get_all_dates_year_month:
            #oldest_date = min(get_all_dates_year_month)
            latesr_date = max(get_all_dates_year_month)
            year_to_look = latesr_date.year
            month_to_look = latesr_date.month
        else:
            year_to_look = datetime.datetime.today().year
            month_to_look = datetime.datetime.today().month
            #print('oldest_date', oldest_date)
        ################
        ################
        ####

        # ФИЛЬТР ПО СОБСТВЕННОЙ ПРОДУКЦИИ: 
        table_lookup_only_with_competitors = models.ComparativeAnalysisTyresModel.objects.filter(price_tyre_to_compare__isnull=False).distinct() ## ОБРАБАТЫВАЕМ ТОЛЬКО ТЕ У КОТОРЫХ ЕСТЬ СПАРСЕННЫЕ КОНКУРЕНТЫ ПО РАЗМЕРУ (БЕЗ ПРИВЯЗКИ К ПАРАМЕТРАМБ ИХ ФИЛЬТРУЕМ ПОЗЖЕ)
        table_lookup_only_with_competitors_all_parsed = table_lookup_only_with_competitors
        #for kk in table_lookup_only_with_competitors_all_parsed:
        #    print('kk', kk.tyre.tyre_size.tyre_size)

        # 1. ПРОДУКЦИЯ

        production_filter_search_flag = False
        # если пользовательищет через поисковик:
        if models.SEARCH_USER_REQUEST:
            user_requested_data = models.SEARCH_USER_REQUEST  
            search_result = obj.comparative_table.filter(Q(tyre__tyre_model__model__in=user_requested_data, tyre__tyre_size__tyre_size__in=user_requested_data) | Q(tyre__tyre_model__model__in=user_requested_data) | Q(tyre__tyre_size__tyre_size__in=user_requested_data))    
            search_result_id = list(search_result.values_list('id', flat=True))
            if search_result_id:
            #    print('+search_result_id', search_result_id)
                list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(id__in=search_result_id).filter(sale_data__year=year_to_look, sale_data__month=month_to_look)    #только продукция с конкурентами и только одна продукция (модель)
                search_result_id_is_true = True
            else:
                models.SEARCH_USER_REQUEST is False
                list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
                search_result_id_is_true = False


        elif models.SELF_PRODUCTION:                                                  # если пользователем введены (выбраны) шины:
            production_filter_search_flag = True        # значит один вид отбора уже произведен, значит дофильтровывать в группах (если надо) будем уже его
            id_list = []
            for n in models.SELF_PRODUCTION:
                if n.isdigit():                                 
                    comparativeanalisystyre_object_id = int(n)
                    id_list.append(comparativeanalisystyre_object_id)
            list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(id__in=id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look)    #только продукция с конкурентами  
#    list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look)     # проверенный но МЕДЛЕННЫЙ вариант - берем все объекты на посл дату и работаем по ним       
        else:       # если ничего не выбрано:
            # ## ДОРАБОТАНО _ ПРИ ОТСУТСТВИИ ВЫБОРА ПРОДУКЦИИ
            try:
                list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
                for obj in table_lookup_only_with_competitors_all_parsed.order_by('tyre__tyre_size__tyre_size'):
                    if list_of_tyre_comparative_objects: 
                        if obj == list_of_tyre_comparative_objects[0]:
    ##                        print('IFIFIFIFF')
                            obj_pk = list_of_tyre_comparative_objects[0].pk
                            list_of_tyre_comparative_objects = list_of_tyre_comparative_objects.filter(id=obj_pk)   # ЕСЛИ НИЧЕГО НЕ ВЫБРАНО _ ВЗЯТЬ ПЕРВЫЙ оббъект 
    ##                        print('!!!!GGGG! = ', list_of_tyre_comparative_objects) 
                            break
            except:  
                list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look)     # проверенный но МЕДЛЕННЫЙ вариант - берем все объекты на посл дату и работаем по ним
           ## END ДОРАБОТАНО _ ПРИ ОТСУТСТВИИ ВЫБОРА ПРОДУКЦИИ 
       
                #list_of_tyre_comparative_objects = obj.comparative_table.all().filter(sale_data__year=year_to_look, sale_data__month=month_to_look)
            #    print('!!!!!------! = ', list_of_tyre_comparative_objects)  # <QuerySet [<ComparativeAnalysisTyresModel: ComparativeAnalysisTyresModel object (512)>, <ComparativeAnalysisTyresModel: ComparativeAnalysisTyresModel object (513)>,
            # 
        #print('$$$', list_of_tyre_comparative_objects)                                      
        
        # 2. ГРУППЫ
        # ФИЛЬТР ПО ГРУППАМ ШИН:
        if production_filter_search_flag is False:          # значит, отбор по продукции не проводился - ищем из всего (это первый этап фильтрации)
            if models.TYRE_GROUPS:                                                  # если пользователем введены (выбраны) шины:
                group_id_list = []
                for n in models.TYRE_GROUPS:
                    if n.isdigit():                                 
                        gr_id = int(n)
                        group_id_list.append(gr_id)
                #existing_val_check = obj.comparative_table.all().filter(tyre__tyre_group__id__in=group_id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
                existing_val_check = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look) #только продукция с конкурентами
                if existing_val_check:
                    #list_of_tyre_comparative_objects = obj.comparative_table.all().filter(tyre__tyre_group__id__in=group_id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look)
                    list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(tyre__tyre_group__id__in=group_id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look)  #только продукция с конкурентами 
                    #print('list_of_tyre_comparative_objects', 'JJ1', list_of_tyre_comparative_objects) 
                else:  
                    #print('АШЫПКА!!!')
                    pass
            elif models.TYRE_GROUPS_ALL:
                #group_id_list = dictionaries_models.TyreGroupModel.objects.values_list('id', flat=True)                        ####### !!!  это ПРАВИЛЬНЫЙ ВАРИАНТ ВЫБОРА ВСЕХ ГРУУПП ШИН, НО ТАК КАК НЕ У ВСЕХ ШИН ПРОПИСАНА ГРУППА _ ТО ПРИДЕТСЯ ПРОСТО ВСЕ ШИНЫ В ПОБОР
                #list_of_tyre_comparative_objects = obj.comparative_table.all().filter(tyre__tyre_group__id__in=group_id_list)  ####### !!!  это ПРАВИЛЬНЫЙ ВАРИАНТ ВЫБОРА ВСЕХ ГРУУПП ШИН, НО ТАК КАК НЕ У ВСЕХ ШИН ПРОПИСАНА ГРУППА _ ТО ПРИДЕТСЯ ПРОСТО ВСЕ ШИНЫ В ПОБОР
                #list_of_tyre_comparative_objects = obj.comparative_table.all().filter(sale_data__year=year_to_look, sale_data__month=month_to_look)  
                list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look)     #####!!!!! ТОЛЬКО ОБЪЕКТЫ С КОНКУРЕНТАМИ                                             ####### !!!  ПРОСТО ВСЕ ШИНЫ В ПОБОР
        if production_filter_search_flag is True:          # значит, отбор по продукции проводился  - ищем из всего (это второй этап фильтрации)
            if models.TYRE_GROUPS:                                                  # если пользователем введены (выбраны) шины:
                group_id_list = []
                for n in models.TYRE_GROUPS:
                    if n.isdigit():                                 
                        gr_id = int(n)
                        group_id_list.append(gr_id)
                existing_val_check = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look) #только продукция с конкурентами
                if existing_val_check:
                    list_of_tyre_comparative_objects = list_of_tyre_comparative_objects.filter(tyre__tyre_group__id__in=group_id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look)  #только продукция с конкурентами 
                else:  
                    #print('АШЫПКА!!!')
                    pass
            elif models.TYRE_GROUPS_ALL:
                list_of_tyre_comparative_objects = list_of_tyre_comparative_objects.filter(sale_data__year=year_to_look, sale_data__month=month_to_look)     #####!!!!! ТОЛЬКО ОБЪЕКТЫ С КОНКУРЕНТАМИ                                             ####### !!!  ПРОСТО ВСЕ ШИНЫ В ПОБОР            


        list_of_tyre_comparative_objects_is_empty = False       # ПРОВЕРКА_ ЕСЛИ НИЧЕГО НЕ НАЙДЕНО - ставим флаг
        #print('НУ И ЧТО У НАС ТУТ???', list_of_tyre_comparative_objects_is_empty)
        if not list_of_tyre_comparative_objects: # если значений нет (отсутствуют моделели с конкурентами):
            #print('А У НАС ТУТ ПЛОТИТЬ НЕ ХОЧУТ')
            list_of_tyre_comparative_objects_is_empty = True


    #    print('!@#!@!@@' , list_of_tyre_comparative_objects)

        #3. ПО БРЕНДАМ ОТБОР БУДЕТ ДАЛЕЕ

        #0.1 подготовить последнюю доступгую дату с конкурентами:
        #last_availible_date = models.CompetitorSiteModel.objects.dates('date_period', "day").last()  
        #last_availible_date = competitors_exist_all_dates_last_date_latest_date
        last_availible_date_today = datetime.datetime.today()
        ## 1 фильтр конкурентов Onliner:
        all_competitors = models.CompetitorSiteModel.objects.filter(site='onliner.by', tyre_to_compare__in=list_of_tyre_comparative_objects)

            # 1.2 ФИЛЬТР список производителей :
        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        onliner_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
            object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
            object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            try:
                if models.ONLINER_COMPETITORS:    
                    #print('models.ONLINER_COMPETITORS', models.ONLINER_COMPETITORS)   
                    #print('1.')
                    # работа с датами для конкурентов
                    if models.COMPETITORS_DATE_FROM_USER_ON_FILTER or models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                            date_filter_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], "%Y-%m-%d").date()
                        else:
                            date_filter_start =  models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.ONLINER_COMPETITORS, site='onliner.by').earliest('date_period').date_period
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                            date_filter_end = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                        else:
                            date_filter_end =  models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.ONLINER_COMPETITORS, site='onliner.by').latest('date_period').date_period
                        got_the_list = models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.ONLINER_COMPETITORS, site='onliner.by').filter(date_period__range=[date_filter_start, date_filter_end])

                    else:
                        #print('1.2 ВЫБРАН БРЕНД И НЕ ВВЕДЕНА ДАТА')
                        got_the_list = models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.ONLINER_COMPETITORS, site='onliner.by')                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    # end работа с датами '

                    brand_name_subbrands_list = []
                    develop_name_list = []    
                    list_to_delete_rarely_parsed = []    #для удаления реже спаршеных моделей внутри одного бренда(производителя)
                    for competitor in got_the_list:
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            # доп проверка на сезонность:
                            try:
                                for get_season in object_unit.tyre.added_features.all():
                                    get_season_is_is = get_season.season_usage.season_usage_name
                                if get_season_is_is == competitor.season.season_usage_name:
                                    #print('||', competitor.name_competitor)
                                    list_of_matched_competitors.append(competitor)
                                    brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                                    develop_name_list.append((competitor.developer, competitor.name_competitor))                
                            except:     #если сезонности нет:
                                list_of_matched_competitors.append(competitor) 
                                brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                                develop_name_list.append((competitor.developer, competitor.name_competitor))  
                    brand_name_subbrands_list_final = list(set(brand_name_subbrands_list))
                    develop_name_list = list(set(develop_name_list))            # # пересобираем список = проверка производитель  сразными моделями
                    develop_name_list_only_comp = []
                    for commm_namme in develop_name_list:
                        develop_name_list_only_comp.append(commm_namme[0])
                    develop_name_list = develop_name_list_only_comp   
                    list_of_developers_which_brands_more_than_one = []
                    for comp_brand_name in develop_name_list:
                        if develop_name_list.count(comp_brand_name) > 1: # если наименование производителя более одногораза - значит есть неск брендов у него, надо взять наиб спарсенный
                            list_of_developers_which_brands_more_than_one.append(comp_brand_name)

                    list_of_developers_which_brands_more_than_one = list(set(list_of_developers_which_brands_more_than_one))
                    # если у производителя несколко моделей в типоразмере:
                    if list_of_developers_which_brands_more_than_one:                                                             # [<CompetitorModel: Cordiant>, <CompetitorModel: Continental>,
                #        # 1) сформировать бренды у данного прозводителя
                #        # 2) сравнить какой более часто спаршен
                #        # 3) убрать менее спаршенные компетиторы из общего списка (onliner_competitors_dict1)
                        for develoooper in list_of_developers_which_brands_more_than_one:                                       #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                            list_to_delete_cometitors_to_compare = [] #СПИСОК COMPETITORS ДЛЯ УДАЛЕНИЯ ИЗ ОБЩЕГО - сперва сравнить длинну моделей в бренде
                            for comp_brand_model in brand_name_subbrands_list_final:       # ['Cordiant Comfort 2', Continental ContiPremiumContact ]
                                brand_in_develoooper_dict = {}       
                                brand_in_develoooper_list = []
                                for subbrand_model_competitor in list_of_matched_competitors:
                                #    print('EEE', subbrand_model_competitor.developer, '|', develoooper, '|', subbrand_model_competitor.name_competitor, '|', comp_brand_model)
                                    if subbrand_model_competitor.developer == develoooper and subbrand_model_competitor.name_competitor == comp_brand_model:
                                        brand_in_develoooper_list.append(subbrand_model_competitor)
                                if brand_in_develoooper_list:                       #[<CompetitorModel: Cordiant>, <CompetitorModel: Continental>,
                                #    brand_in_develoooper_dict[comp_brand_model, develoooper] = brand_in_develoooper_list     #{'Cordiant Road Runner': [<CompetitorSiteModel: CompetitorSiteModel object (10966)>,
                                    brand_in_develoooper_dict = { comp_brand_model : brand_in_develoooper_list, develoooper : develoooper }
                                #    print('++--++', brand_in_develoooper_dict.items())
                                try:
                                    if brand_in_develoooper_dict[develoooper] == develoooper:                           # СВЕРКА ЧАСТОТЫ ПАРСИНГА МОДЕЛЕЙ ДАННОГО ПРОИЗВОДИТЕЛЯ, ВЫБОРКА НАИМю СПАРСЕННЫХ _ ИХ УБРАТЬ ИХ ОБЩЕГО ПЕРЕЧНЯ  list_of_matched_competitors                         
                                        #print(comp_brand_model, 'LLLL111TTTT', brand_in_develoooper_dict[develoooper], 'PP22',  develoooper)
                                        len_comparison_got = len(brand_in_develoooper_dict[comp_brand_model])
                                        #print('len_comparison_got', len_comparison_got)
                                        #compare_to_delete = len_comparison_got
                                        compare_to_delete = len_comparison_got, brand_in_develoooper_dict[comp_brand_model]
                                        list_to_delete_cometitors_to_compare.append(compare_to_delete)
                                        #brand_in_develoooper_dict_new[comp_brand_model] = brand_in_develoooper_dict[comp_brand_model]
                                except:
                                    pass
                            list_to_delete_cometitors_to_compare = sorted(list_to_delete_cometitors_to_compare, key=lambda x: x[0])     ## !!!! ОТСОРТИРОВАНЫ ПО ЧАСТОТЕ ПАРСИНГА каждого бренда(модели) внутри ДАННОГО ПРОИЗВОДИТЕЛЯ (т.е производитель Cordiant - но у него бренды Comfort 3, Winter Sport2  и т.д)
                            #print('!!', list_to_delete_cometitors_to_compare)
                            list_to_delete_cometitors_to_compare = list_to_delete_cometitors_to_compare[:-1]    ## Competitorы на удаление из перечня
                            list_to_delete_cometitors_to_compare_with_no_ind_len = []
                            for ind_len, copet_list in list_to_delete_cometitors_to_compare:                    # убираем индексы длины (количества спасенных)
                                list_to_delete_cometitors_to_compare_with_no_ind_len.append(copet_list)
                            #print('Э сюда на111111' , list_to_delete_cometitors_to_compare_with_no_ind_len)
                        #    print('===========')
                            final_list_to_delete_competitors_in_brand = []                                      # финальный список - очищенный от листов - все непопулярные competitors производителя в одном списке
                            for list_val in list_to_delete_cometitors_to_compare_with_no_ind_len:
                                for item in list_val:
                                    final_list_to_delete_competitors_in_brand.append(item)
                            final_list_to_delete_competitors_in_brand = list(set(final_list_to_delete_competitors_in_brand)) 
                            #print('Э сюда на', final_list_to_delete_competitors_in_brand)

                            list_to_delete_rarely_parsed.extend(final_list_to_delete_competitors_in_brand)          # формируем единый список на удаление
                            #print('list_to_delete_cometitors', list_to_delete_cometitors_to_compare)
                            # убираем непопулярных (реже спашенных модели данного бренда, исключая их из списка общего - останутся лишь производители с одной моделью (у тех производ, у которых было несколько моделей- останется лишь самый спашенный наиболее)):
                        #print('DELETE', list_to_delete_rarely_parsed)
                        for compet_to_delete in list_to_delete_rarely_parsed:
                            list_of_matched_competitors.remove(compet_to_delete)
                        onliner_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                    # если у каждого производителя по одной модели:
                    else:
                        ## подсчет каких моделей(суббренда) конкурента больше есть для данной модели:
                        ##print('brand_name_subbrands_list_final', brand_name_subbrands_list_final)
                        #comp_brand_model_dict = {}
                        #for comp_brand_model in brand_name_subbrands_list_final:
                        #    comp_brand_model_list = []
                        #    for subbrand_model_competitor in list_of_matched_competitors:
                        #        if subbrand_model_competitor.name_competitor == comp_brand_model:
                        #            comp_brand_model_list.append(subbrand_model_competitor)
                        ##    print('1', comp_brand_model)
                        #    comp_brand_model_dict[comp_brand_model] = comp_brand_model_list
                        #if len(comp_brand_model_dict.items()) > 1:      #если есть несколько моделей у данного бренда: берем самую спаршенную:
                        #    keu = None
                        #    v_len = 0
                        #    for k, v in comp_brand_model_dict.items():
                        #        #print(k, 'MMM', len(v))
                        #        if len(v) > v_len:
                        #            keu_index = k
                        #            v_len = len(v)
                        #    #print(keu_index, 'ABBA', v_len)
                        #    list_of_matched_competitors_with_one_brand_model = comp_brand_model_dict[keu_index]
                        #    #print('BBBBBB===1', list_of_matched_competitors_with_one_brand_model)
                        #if len(comp_brand_model_dict.items()) == 1:
                        #    list_of_matched_competitors_with_one_brand_model = list(comp_brand_model_dict.values())[0]
                        #    #print('BBBBBB===2', list_of_matched_competitors_with_one_brand_model)
                        #if len(comp_brand_model_dict.items()) < 1:
                        #    list_of_matched_competitors_with_one_brand_model = []
                        #    print('BBBBBB===3', list_of_matched_competitors_with_one_brand_model)
                        #list_of_matched_competitors = list_of_matched_competitors_with_one_brand_model
                        onliner_competitors_dict1[object_unit.tyre] = list_of_matched_competitors

                else:
                    # работа с датами без конкурентов (вся продукция)

                    if models.COMPETITORS_DATE_FROM_USER_ON_FILTER or models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                            date_filter_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], "%Y-%m-%d").date()
                        else:
                            date_filter_start =  all_competitors.earliest('date_period').date_period
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                            date_filter_end = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                        else:
                            date_filter_end =  all_competitors.latest('date_period').date_period
                        got_the_list = all_competitors.filter(date_period__range=[date_filter_start, date_filter_end])
                                                  
                    else:
                        #print('2.3 НЕ ВЫБРАН БРЕНД И НЕ ВВЕДЕНА ДАТА')
                        got_the_list = all_competitors 
                        # end работа с датами      

                    brand_name_subbrands_list = []
                    list_to_delete_rarely_parsed = []    #для удаления реже спаршеных моделей внутри одного бренда(производителя)
                    for competitor in got_the_list:
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            # доп проверка на сезонность:
                            try:
                                for get_season in object_unit.tyre.added_features.all():
                                    get_season_is_is = get_season.season_usage.season_usage_name
                                if get_season_is_is == competitor.season.season_usage_name:
                                #    print('||', competitor.name_competitor)
                                    list_of_matched_competitors.append(competitor)
                                    brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде

                            except:     #если сезонности нет:
                                list_of_matched_competitors.append(competitor) 
                                brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                    brand_name_subbrands_list_final = list(set(brand_name_subbrands_list))
                #print('111list_of_matched_competitors', list_of_matched_competitors)
                    #print('22222brand_name_subbrands_list_final', brand_name_subbrands_list_final)

                    # доп проверка - так все бренды- у них м.б. по несколько моделей - проверить -есть ли у бреда несколько моделей -взять с наибольшей частотой паринга:
                    list_of_developers_which_brands_more_than_one_for_checking = []
                    for comp_brand in list_of_matched_competitors:
                        list_of_developers_which_brands_more_than_one_for_checking.append((comp_brand.developer, comp_brand.name_competitor))  
                        #print('comp_brand', comp_brand.developer)

                    list_of_developers_which_brands_more_than_one_for_checking = list(set(list_of_developers_which_brands_more_than_one_for_checking))            # # пересобираем список = проверка производитель  сразными моделями
                    develop_name_list_only_comp = []
                    for commm_namme in list_of_developers_which_brands_more_than_one_for_checking:
                        develop_name_list_only_comp.append(commm_namme[0])
                    list_of_developers_which_brands_more_than_one_for_checking = develop_name_list_only_comp   

                    list_of_developers_which_brands_more_than_one = []
                    for comp_brand_name in list_of_developers_which_brands_more_than_one_for_checking:
                        if list_of_developers_which_brands_more_than_one_for_checking.count(comp_brand_name) > 1: # если наименование производителя более одногораза - значит есть неск брендов у него, надо взять наиб спарсенный
                            list_of_developers_which_brands_more_than_one.append(comp_brand_name)
                    list_of_developers_which_brands_more_than_one = list(set(list_of_developers_which_brands_more_than_one))
                    #print('ISS list_of_developers_which_brands_more_than_one', list_of_developers_which_brands_more_than_one)   #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                    if list_of_developers_which_brands_more_than_one:                                                             #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                #        # 1) сформировать бренды у данного прозводителя
                #        # 2) сравнить какой более часто спаршен
                #        # 3) убрать менее спаршенные компетиторы из общего списка (onliner_competitors_dict1)
                        for develoooper in list_of_developers_which_brands_more_than_one:                                       #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                            list_to_delete_cometitors_to_compare = [] #СПИСОК COMPETITORS ДЛЯ УДАЛЕНИЯ ИЗ ОБЩЕГО - сперва сравнить длинну моделей в бренде
                            for comp_brand_model in brand_name_subbrands_list_final:       # ['Cordiant Comfort 2', Continental ContiPremiumContact ]
                                brand_in_develoooper_dict = {}       
                                brand_in_develoooper_list = []
                                for subbrand_model_competitor in list_of_matched_competitors:
                                #    print('EEE', subbrand_model_competitor.developer, '|', develoooper, '|', subbrand_model_competitor.name_competitor, '|', comp_brand_model)
                                    if subbrand_model_competitor.developer == develoooper and subbrand_model_competitor.name_competitor == comp_brand_model:
                                        brand_in_develoooper_list.append(subbrand_model_competitor)
                                if brand_in_develoooper_list:
                                #    brand_in_develoooper_dict[comp_brand_model, develoooper] = brand_in_develoooper_list     #{'Cordiant Road Runner': [<CompetitorSiteModel: CompetitorSiteModel object (10966)>,
                                    brand_in_develoooper_dict = { comp_brand_model : brand_in_develoooper_list, develoooper : develoooper }
                                    #print('++--++', brand_in_develoooper_dict.keys())
                                try:
                                    if brand_in_develoooper_dict[develoooper] == develoooper:                           # СВЕРКА ЧАСТОТЫ ПАРСИНГА МОДЕЛЕЙ ДАННОГО ПРОИЗВОДИТЕЛЯ, ВЫБОРКА НАИМю СПАРСЕННЫХ _ ИХ УБРАТЬ ИХ ОБЩЕГО ПЕРЕЧНЯ  list_of_matched_competitors                         
                                        #print(comp_brand_model, 'LLLL111TTTT', brand_in_develoooper_dict[develoooper], 'PP22',  develoooper)
                                        len_comparison_got = len(brand_in_develoooper_dict[comp_brand_model])
                                        #compare_to_delete = len_comparison_got
                                        compare_to_delete = len_comparison_got, brand_in_develoooper_dict[comp_brand_model]
                                        list_to_delete_cometitors_to_compare.append(compare_to_delete)
                                        #brand_in_develoooper_dict_new[comp_brand_model] = brand_in_develoooper_dict[comp_brand_model]
                                except:
                                    pass
                            list_to_delete_cometitors_to_compare = sorted(list_to_delete_cometitors_to_compare, key=lambda x: x[0])     ## !!!! ОТСОРТИРОВАНЫ ПО ЧАСТОТЕ ПАРСИНГА каждого бренда(модели) внутри ДАННОГО ПРОИЗВОДИТЕЛЯ (т.е производитель Cordiant - но у него бренды Comfort 3, Winter Sport2  и т.д)
                            list_to_delete_cometitors_to_compare = list_to_delete_cometitors_to_compare[:-1]    ## Competitorы на удаление из перечня
                            list_to_delete_cometitors_to_compare_with_no_ind_len = []
                            for ind_len, copet_list in list_to_delete_cometitors_to_compare:                    # убираем индексы длины (количества спасенных)
                                list_to_delete_cometitors_to_compare_with_no_ind_len.append(copet_list)
                            #print('Э сюда на111111' , list_to_delete_cometitors_to_compare_with_no_ind_len)

                            final_list_to_delete_competitors_in_brand = []                                      # финальный список - очищенный от листов - все непопулярные competitors производителя в одном списке
                            for list_val in list_to_delete_cometitors_to_compare_with_no_ind_len:
                                for item in list_val:
                                    final_list_to_delete_competitors_in_brand.append(item)
                            final_list_to_delete_competitors_in_brand = list(set(final_list_to_delete_competitors_in_brand)) 
                            #print('Э сюда на', final_list_to_delete_competitors_in_brand)

                            list_to_delete_rarely_parsed.extend(final_list_to_delete_competitors_in_brand)          # формируем единый список на удаление
                            #print('list_to_delete_cometitors', list_to_delete_cometitors_to_compare)
                            # убираем непопулярных (реже спашенных модели данного бренда, исключая их из списка общего - останутся лишь производители с одной моделью (у тех производ, у которых было несколько моделей- останется лишь самый спашенный наиболее)):
                        #print('DELETE', list_to_delete_rarely_parsed)
                        for compet_to_delete in list_to_delete_rarely_parsed:
                            list_of_matched_competitors.remove(compet_to_delete)
                        onliner_competitors_dict1[object_unit.tyre] = list_of_matched_competitors

                    else:       # если у каждого бренда-производителя по одной модели:

                        onliner_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
            except:
                pass

        models.ONLINER_COMPETITORS_DICTIONARY1 = onliner_competitors_dict1 

        #print('models.ONLINER_COMPETITORS_DICTIONARY1', models.ONLINER_COMPETITORS_DICTIONARY1)
        #for k, v in models.ONLINER_COMPETITORS_DICTIONARY1.items():
        #    for n in v:
        #        print('+-=-+= ASS', n.developer)
        # END ONLINER

        ## 2 фильтр конкурентов Автосеть:

        all_competitors = models.CompetitorSiteModel.objects.filter(site='autoset.by', tyre_to_compare__in=list_of_tyre_comparative_objects)

            # 1.2 ФИЛЬТР список производителей :
        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        avtoset_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
            object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
            object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            try:
                if models.AVTOSET_COMPETITORS:
                    #print('models.AVTOSET_COMPETITORS', models.AVTOSET_COMPETITORS)   
                    #print('1.')
                    # работа с датами для конкурентов
                    if models.COMPETITORS_DATE_FROM_USER_ON_FILTER or models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                            date_filter_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], "%Y-%m-%d").date()
                        else:
                            date_filter_start =  models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.AVTOSET_COMPETITORS, site='autoset.by').earliest('date_period').date_period
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                            date_filter_end = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                        else:
                            date_filter_end =  models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.AVTOSET_COMPETITORS, site='autoset.by').latest('date_period').date_period
                        got_the_list = models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.AVTOSET_COMPETITORS, site='autoset.by').filter(date_period__range=[date_filter_start, date_filter_end])
                    #    print('BAGORIA', date_filter_start, '-', date_filter_end)
                    else:
                        #print('1.2 ВЫБРАН БРЕНД И НЕ ВВЕДЕНА ДАТА')
                        got_the_list = models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.AVTOSET_COMPETITORS, site='autoset.by')                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    # end работа с датами '


                    brand_name_subbrands_list = []
                    develop_name_list = []    
                    list_to_delete_rarely_parsed = []    #для удаления реже спаршеных моделей внутри одного бренда(производителя)
                    for competitor in got_the_list:
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            # доп проверка на сезонность:
                            try:
                                for get_season in object_unit.tyre.added_features.all():
                                    get_season_is_is = get_season.season_usage.season_usage_name
                                if get_season_is_is == competitor.season.season_usage_name:
                                    #print('||', competitor.name_competitor)
                                    list_of_matched_competitors.append(competitor)
                                    brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                                    develop_name_list.append((competitor.developer, competitor.name_competitor))                
                            except:     #если сезонности нет:
                                list_of_matched_competitors.append(competitor) 
                                brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                                develop_name_list.append((competitor.developer, competitor.name_competitor))  
                    brand_name_subbrands_list_final = list(set(brand_name_subbrands_list))
                    develop_name_list = list(set(develop_name_list))            # # пересобираем список = проверка производитель  сразными моделями
                    develop_name_list_only_comp = []
                    for commm_namme in develop_name_list:
                        develop_name_list_only_comp.append(commm_namme[0])
                    develop_name_list = develop_name_list_only_comp   
                    list_of_developers_which_brands_more_than_one = []
                    for comp_brand_name in develop_name_list:
                        if develop_name_list.count(comp_brand_name) > 1: # если наименование производителя более одногораза - значит есть неск брендов у него, надо взять наиб спарсенный
                            list_of_developers_which_brands_more_than_one.append(comp_brand_name)

                    list_of_developers_which_brands_more_than_one = list(set(list_of_developers_which_brands_more_than_one))
                    # если у производителя несколко моделей в типоразмере:
                    if list_of_developers_which_brands_more_than_one:                                                             # [<CompetitorModel: Cordiant>, <CompetitorModel: Continental>,
                #        # 1) сформировать бренды у данного прозводителя
                #        # 2) сравнить какой более часто спаршен
                #        # 3) убрать менее спаршенные компетиторы из общего списка (onliner_competitors_dict1)
                        for develoooper in list_of_developers_which_brands_more_than_one:                                       #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                            list_to_delete_cometitors_to_compare = [] #СПИСОК COMPETITORS ДЛЯ УДАЛЕНИЯ ИЗ ОБЩЕГО - сперва сравнить длинну моделей в бренде
                            for comp_brand_model in brand_name_subbrands_list_final:       # ['Cordiant Comfort 2', Continental ContiPremiumContact ]
                                brand_in_develoooper_dict = {}       
                                brand_in_develoooper_list = []
                                for subbrand_model_competitor in list_of_matched_competitors:
                                #    print('EEE', subbrand_model_competitor.developer, '|', develoooper, '|', subbrand_model_competitor.name_competitor, '|', comp_brand_model)
                                    if subbrand_model_competitor.developer == develoooper and subbrand_model_competitor.name_competitor == comp_brand_model:
                                        brand_in_develoooper_list.append(subbrand_model_competitor)
                                if brand_in_develoooper_list:                       #[<CompetitorModel: Cordiant>, <CompetitorModel: Continental>,
                                #    brand_in_develoooper_dict[comp_brand_model, develoooper] = brand_in_develoooper_list     #{'Cordiant Road Runner': [<CompetitorSiteModel: CompetitorSiteModel object (10966)>,
                                    brand_in_develoooper_dict = { comp_brand_model : brand_in_develoooper_list, develoooper : develoooper }
                                #    print('++--++', brand_in_develoooper_dict.items())
                                try:
                                    if brand_in_develoooper_dict[develoooper] == develoooper:                           # СВЕРКА ЧАСТОТЫ ПАРСИНГА МОДЕЛЕЙ ДАННОГО ПРОИЗВОДИТЕЛЯ, ВЫБОРКА НАИМю СПАРСЕННЫХ _ ИХ УБРАТЬ ИХ ОБЩЕГО ПЕРЕЧНЯ  list_of_matched_competitors                         
                                        #print(comp_brand_model, 'LLLL111TTTT', brand_in_develoooper_dict[develoooper], 'PP22',  develoooper)
                                        len_comparison_got = len(brand_in_develoooper_dict[comp_brand_model])
                                        #print('len_comparison_got', len_comparison_got)
                                        #compare_to_delete = len_comparison_got
                                        compare_to_delete = len_comparison_got, brand_in_develoooper_dict[comp_brand_model]
                                        list_to_delete_cometitors_to_compare.append(compare_to_delete)
                                        #brand_in_develoooper_dict_new[comp_brand_model] = brand_in_develoooper_dict[comp_brand_model]
                                except:
                                    pass
                            list_to_delete_cometitors_to_compare = sorted(list_to_delete_cometitors_to_compare, key=lambda x: x[0])     ## !!!! ОТСОРТИРОВАНЫ ПО ЧАСТОТЕ ПАРСИНГА каждого бренда(модели) внутри ДАННОГО ПРОИЗВОДИТЕЛЯ (т.е производитель Cordiant - но у него бренды Comfort 3, Winter Sport2  и т.д)
                            #print('!!', list_to_delete_cometitors_to_compare)
                            list_to_delete_cometitors_to_compare = list_to_delete_cometitors_to_compare[:-1]    ## Competitorы на удаление из перечня
                            list_to_delete_cometitors_to_compare_with_no_ind_len = []
                            for ind_len, copet_list in list_to_delete_cometitors_to_compare:                    # убираем индексы длины (количества спасенных)
                                list_to_delete_cometitors_to_compare_with_no_ind_len.append(copet_list)
                            #print('Э сюда на111111' , list_to_delete_cometitors_to_compare_with_no_ind_len)
                            #print('===========')
                            final_list_to_delete_competitors_in_brand = []                                      # финальный список - очищенный от листов - все непопулярные competitors производителя в одном списке
                            for list_val in list_to_delete_cometitors_to_compare_with_no_ind_len:
                                for item in list_val:
                                    final_list_to_delete_competitors_in_brand.append(item)
                            final_list_to_delete_competitors_in_brand = list(set(final_list_to_delete_competitors_in_brand)) 
                            #print('Э сюда на', final_list_to_delete_competitors_in_brand)
                            list_to_delete_rarely_parsed.extend(final_list_to_delete_competitors_in_brand)          # формируем единый список на удаление
                            #print('list_to_delete_cometitors', list_to_delete_cometitors_to_compare)
                            # убираем непопулярных (реже спашенных модели данного бренда, исключая их из списка общего - останутся лишь производители с одной моделью (у тех производ, у которых было несколько моделей- останется лишь самый спашенный наиболее)):
                        #print('DELETE', list_to_delete_rarely_parsed)
                        for compet_to_delete in list_to_delete_rarely_parsed:
                            list_of_matched_competitors.remove(compet_to_delete)
                        avtoset_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                    # если у каждого производителя по одной модели:
                    else:

                        avtoset_competitors_dict1[object_unit.tyre] = list_of_matched_competitors

                else:
                    # работа с датами без конкурентов (вся продукция)

                    if models.COMPETITORS_DATE_FROM_USER_ON_FILTER or models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                            date_filter_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], "%Y-%m-%d").date()
                        else:
                            date_filter_start =  all_competitors.earliest('date_period').date_period
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                            date_filter_end = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                        else:
                            date_filter_end =  all_competitors.latest('date_period').date_period
                        got_the_list = all_competitors.filter(date_period__range=[date_filter_start, date_filter_end])
                                                  
                    else:
                        #print('2.3 НЕ ВЫБРАН БРЕНД И НЕ ВВЕДЕНА ДАТА')
                        got_the_list = all_competitors 
                        # end работа с датами       

                    #print('2.4 БРЕНД НЕ ВЫБРАН')                                                                                                         ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ    

                    brand_name_subbrands_list = []
                    list_to_delete_rarely_parsed = []    #для удаления реже спаршеных моделей внутри одного бренда(производителя)
                    for competitor in got_the_list:
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            # доп проверка на сезонность:
                            try:
                                for get_season in object_unit.tyre.added_features.all():
                                    get_season_is_is = get_season.season_usage.season_usage_name
                                if get_season_is_is == competitor.season.season_usage_name:
                                #    print('||', competitor.name_competitor)
                                    list_of_matched_competitors.append(competitor)
                                    brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде

                            except:     #если сезонности нет:
                                list_of_matched_competitors.append(competitor) 
                                brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                    brand_name_subbrands_list_final = list(set(brand_name_subbrands_list))
                #print('111list_of_matched_competitors', list_of_matched_competitors)
                    #print('22222brand_name_subbrands_list_final', brand_name_subbrands_list_final)

                    # доп проверка - так все бренды- у них м.б. по несколько моделей - проверить -есть ли у бреда несколько моделей -взять с наибольшей частотой паринга:
                    list_of_developers_which_brands_more_than_one_for_checking = []
                    for comp_brand in list_of_matched_competitors:
                        list_of_developers_which_brands_more_than_one_for_checking.append((comp_brand.developer, comp_brand.name_competitor))  
                        #print('comp_brand', comp_brand.developer)

                    list_of_developers_which_brands_more_than_one_for_checking = list(set(list_of_developers_which_brands_more_than_one_for_checking))            # # пересобираем список = проверка производитель  сразными моделями
                    develop_name_list_only_comp = []
                    for commm_namme in list_of_developers_which_brands_more_than_one_for_checking:
                        develop_name_list_only_comp.append(commm_namme[0])
                    list_of_developers_which_brands_more_than_one_for_checking = develop_name_list_only_comp   

                    list_of_developers_which_brands_more_than_one = []
                    for comp_brand_name in list_of_developers_which_brands_more_than_one_for_checking:
                        if list_of_developers_which_brands_more_than_one_for_checking.count(comp_brand_name) > 1: # если наименование производителя более одногораза - значит есть неск брендов у него, надо взять наиб спарсенный
                            list_of_developers_which_brands_more_than_one.append(comp_brand_name)
                    list_of_developers_which_brands_more_than_one = list(set(list_of_developers_which_brands_more_than_one))
                    #print('ISS list_of_developers_which_brands_more_than_one', list_of_developers_which_brands_more_than_one)   #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                    if list_of_developers_which_brands_more_than_one:                                                             #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                #        # 1) сформировать бренды у данного прозводителя
                #        # 2) сравнить какой более часто спаршен
                #        # 3) убрать менее спаршенные компетиторы из общего списка (avtoset_competitors_dict1)
                        for develoooper in list_of_developers_which_brands_more_than_one:                                       #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                            list_to_delete_cometitors_to_compare = [] #СПИСОК COMPETITORS ДЛЯ УДАЛЕНИЯ ИЗ ОБЩЕГО - сперва сравнить длинну моделей в бренде
                            for comp_brand_model in brand_name_subbrands_list_final:       # ['Cordiant Comfort 2', Continental ContiPremiumContact ]
                                brand_in_develoooper_dict = {}       
                                brand_in_develoooper_list = []
                                for subbrand_model_competitor in list_of_matched_competitors:
                                #    print('EEE', subbrand_model_competitor.developer, '|', develoooper, '|', subbrand_model_competitor.name_competitor, '|', comp_brand_model)
                                    if subbrand_model_competitor.developer == develoooper and subbrand_model_competitor.name_competitor == comp_brand_model:
                                        brand_in_develoooper_list.append(subbrand_model_competitor)
                                if brand_in_develoooper_list:
                                #    brand_in_develoooper_dict[comp_brand_model, develoooper] = brand_in_develoooper_list     #{'Cordiant Road Runner': [<CompetitorSiteModel: CompetitorSiteModel object (10966)>,
                                    brand_in_develoooper_dict = { comp_brand_model : brand_in_develoooper_list, develoooper : develoooper }
                                    #print('++--++', brand_in_develoooper_dict.keys())
                                try:
                                    if brand_in_develoooper_dict[develoooper] == develoooper:                           # СВЕРКА ЧАСТОТЫ ПАРСИНГА МОДЕЛЕЙ ДАННОГО ПРОИЗВОДИТЕЛЯ, ВЫБОРКА НАИМю СПАРСЕННЫХ _ ИХ УБРАТЬ ИХ ОБЩЕГО ПЕРЕЧНЯ  list_of_matched_competitors                         
                                        #print(comp_brand_model, 'LLLL111TTTT', brand_in_develoooper_dict[develoooper], 'PP22',  develoooper)
                                        len_comparison_got = len(brand_in_develoooper_dict[comp_brand_model])
                                        #compare_to_delete = len_comparison_got
                                        compare_to_delete = len_comparison_got, brand_in_develoooper_dict[comp_brand_model]
                                        list_to_delete_cometitors_to_compare.append(compare_to_delete)
                                        #brand_in_develoooper_dict_new[comp_brand_model] = brand_in_develoooper_dict[comp_brand_model]
                                except:
                                    pass
                            list_to_delete_cometitors_to_compare = sorted(list_to_delete_cometitors_to_compare, key=lambda x: x[0])     ## !!!! ОТСОРТИРОВАНЫ ПО ЧАСТОТЕ ПАРСИНГА каждого бренда(модели) внутри ДАННОГО ПРОИЗВОДИТЕЛЯ (т.е производитель Cordiant - но у него бренды Comfort 3, Winter Sport2  и т.д)
                            list_to_delete_cometitors_to_compare = list_to_delete_cometitors_to_compare[:-1]    ## Competitorы на удаление из перечня
                            list_to_delete_cometitors_to_compare_with_no_ind_len = []
                            for ind_len, copet_list in list_to_delete_cometitors_to_compare:                    # убираем индексы длины (количества спасенных)
                                list_to_delete_cometitors_to_compare_with_no_ind_len.append(copet_list)
                            #print('Э сюда на111111' , list_to_delete_cometitors_to_compare_with_no_ind_len)                 
                            final_list_to_delete_competitors_in_brand = []                                      # финальный список - очищенный от листов - все непопулярные competitors производителя в одном списке
                            for list_val in list_to_delete_cometitors_to_compare_with_no_ind_len:
                                for item in list_val:
                                    final_list_to_delete_competitors_in_brand.append(item)
                            final_list_to_delete_competitors_in_brand = list(set(final_list_to_delete_competitors_in_brand)) 
                            #print('Э сюда на', final_list_to_delete_competitors_in_brand)
                            list_to_delete_rarely_parsed.extend(final_list_to_delete_competitors_in_brand)          # формируем единый список на удаление
                            #print('list_to_delete_cometitors', list_to_delete_cometitors_to_compare)
                            # убираем непопулярных (реже спашенных модели данного бренда, исключая их из списка общего - останутся лишь производители с одной моделью (у тех производ, у которых было несколько моделей- останется лишь самый спашенный наиболее)):
                        #print('DELETE', list_to_delete_rarely_parsed)
                        for compet_to_delete in list_to_delete_rarely_parsed:
                            list_of_matched_competitors.remove(compet_to_delete)
                        avtoset_competitors_dict1[object_unit.tyre] = list_of_matched_competitors           
                    else:       # если у каждого бренда-производителя по одной модели:
                        avtoset_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
            except:
                    pass

        models.AVTOSET_COMPETITORS_DICTIONARY1 = avtoset_competitors_dict1  
        #object_unit.avtoset_competitor_on_date1() 

        ###### END OF AVTOSET

        ## 3 фильтр конкурентов BAGORIA:

        all_competitors = models.CompetitorSiteModel.objects.filter(site='bagoria.by', tyre_to_compare__in=list_of_tyre_comparative_objects)

            # 1.2 ФИЛЬТР список производителей :
        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        bagoria_competitors_dict1  = {}
        for object_unit in list_of_tyre_comparative_objects:
            object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
            object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            try:
                if models.BAGORIA_COMPETITORS: 
                    #print('models.BAGORIA_COMPETITORS', models.BAGORIA_COMPETITORS)   
                    #print('1.ВЫБРАН БРЕНД И ВВЕДЕНА ДАТА - BAGORIA')
                    # работа с датами для конкурентов
                    if models.COMPETITORS_DATE_FROM_USER_ON_FILTER or models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                            date_filter_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], "%Y-%m-%d").date()
                        else:
                            date_filter_start =  models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.BAGORIA_COMPETITORS, site='bagoria.by').earliest('date_period').date_period
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                            date_filter_end = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                        else:
                            date_filter_end =  models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.BAGORIA_COMPETITORS, site='bagoria.by').latest('date_period').date_period
                        got_the_list = models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.BAGORIA_COMPETITORS, site='bagoria.by').filter(date_period__range=[date_filter_start, date_filter_end])
                        print('date_filter_start', date_filter_start, '===', 'date_filter_end', date_filter_end)
                    else:
                        print('1.2 ВЫБРАН БРЕНД И НЕ ВВЕДЕНА ДАТА  - BAGORIA')
                        got_the_list = models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.BAGORIA_COMPETITORS, site='bagoria.by')                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    # end работа с датами '

                    brand_name_subbrands_list = []
                    develop_name_list = []    
                    list_to_delete_rarely_parsed = []    #для удаления реже спаршеных моделей внутри одного бренда(производителя)
                    for competitor in got_the_list:
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            # доп проверка на сезонность:
                            try:
                                for get_season in object_unit.tyre.added_features.all():
                                    get_season_is_is = get_season.season_usage.season_usage_name
                                if get_season_is_is == competitor.season.season_usage_name:
                                    #print('||', competitor.name_competitor)
                                    list_of_matched_competitors.append(competitor)
                                    brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                                    develop_name_list.append((competitor.developer, competitor.name_competitor))                
                            except:     #если сезонности нет:
                                list_of_matched_competitors.append(competitor) 
                                brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                                develop_name_list.append((competitor.developer, competitor.name_competitor))  
                    brand_name_subbrands_list_final = list(set(brand_name_subbrands_list))
                    develop_name_list = list(set(develop_name_list))            # # пересобираем список = проверка производитель  сразными моделями
                    develop_name_list_only_comp = []
                    for commm_namme in develop_name_list:
                        develop_name_list_only_comp.append(commm_namme[0])
                    develop_name_list = develop_name_list_only_comp   
                    list_of_developers_which_brands_more_than_one = []
                    for comp_brand_name in develop_name_list:
                        if develop_name_list.count(comp_brand_name) > 1: # если наименование производителя более одногораза - значит есть неск брендов у него, надо взять наиб спарсенный
                            list_of_developers_which_brands_more_than_one.append(comp_brand_name)

######################                    for subbrand_model_competitor in list_of_matched_competitors:
######################                        print('PPPOOOPPPP', subbrand_model_competitor.developer, '|', subbrand_model_competitor.name_competitor, '|', subbrand_model_competitor.date_period)

                    list_of_developers_which_brands_more_than_one = list(set(list_of_developers_which_brands_more_than_one))
                    # если у производителя несколко моделей в типоразмере:
                    if list_of_developers_which_brands_more_than_one:                                                             # [<CompetitorModel: Cordiant>, <CompetitorModel: Continental>,
                #        # 1) сформировать бренды у данного прозводителя
                #        # 2) сравнить какой более часто спаршен
                #        # 3) убрать менее спаршенные компетиторы из общего списка (onliner_competitors_dict1)
                        for develoooper in list_of_developers_which_brands_more_than_one:                                       #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                            list_to_delete_cometitors_to_compare = [] #СПИСОК COMPETITORS ДЛЯ УДАЛЕНИЯ ИЗ ОБЩЕГО - сперва сравнить длинну моделей в бренде
                            for comp_brand_model in brand_name_subbrands_list_final:       # ['Cordiant Comfort 2', Continental ContiPremiumContact ]
                                brand_in_develoooper_dict = {}       
                                brand_in_develoooper_list = []
                                for subbrand_model_competitor in list_of_matched_competitors:
                            #        print('EEE', subbrand_model_competitor.developer, '|', develoooper, '|', subbrand_model_competitor.name_competitor, '|', comp_brand_model, '|', subbrand_model_competitor.date_period)
                                    if subbrand_model_competitor.developer == develoooper and subbrand_model_competitor.name_competitor == comp_brand_model:
                                        brand_in_develoooper_list.append(subbrand_model_competitor)
                                if brand_in_develoooper_list:                       #[<CompetitorModel: Cordiant>, <CompetitorModel: Continental>,
                                #    brand_in_develoooper_dict[comp_brand_model, develoooper] = brand_in_develoooper_list     #{'Cordiant Road Runner': [<CompetitorSiteModel: CompetitorSiteModel object (10966)>,
                                    brand_in_develoooper_dict = { comp_brand_model : brand_in_develoooper_list, develoooper : develoooper }
                                #    print('++--++', brand_in_develoooper_dict.items())
                                try:
                                    if brand_in_develoooper_dict[develoooper] == develoooper:                           # СВЕРКА ЧАСТОТЫ ПАРСИНГА МОДЕЛЕЙ ДАННОГО ПРОИЗВОДИТЕЛЯ, ВЫБОРКА НАИМю СПАРСЕННЫХ _ ИХ УБРАТЬ ИХ ОБЩЕГО ПЕРЕЧНЯ  list_of_matched_competitors                         
                                        #print(comp_brand_model, 'LLLL111TTTT', brand_in_develoooper_dict[develoooper], 'PP22',  develoooper)
                                        len_comparison_got = len(brand_in_develoooper_dict[comp_brand_model])
                                        #print('len_comparison_got', len_comparison_got)
                                        #compare_to_delete = len_comparison_got
                                        compare_to_delete = len_comparison_got, brand_in_develoooper_dict[comp_brand_model]
                                        list_to_delete_cometitors_to_compare.append(compare_to_delete)
                                        #brand_in_develoooper_dict_new[comp_brand_model] = brand_in_develoooper_dict[comp_brand_model]
                                except:
                                    pass
                            list_to_delete_cometitors_to_compare = sorted(list_to_delete_cometitors_to_compare, key=lambda x: x[0])     ## !!!! ОТСОРТИРОВАНЫ ПО ЧАСТОТЕ ПАРСИНГА каждого бренда(модели) внутри ДАННОГО ПРОИЗВОДИТЕЛЯ (т.е производитель Cordiant - но у него бренды Comfort 3, Winter Sport2  и т.д)
                            #print('!!', list_to_delete_cometitors_to_compare)
                            list_to_delete_cometitors_to_compare = list_to_delete_cometitors_to_compare[:-1]    ## Competitorы на удаление из перечня
                            list_to_delete_cometitors_to_compare_with_no_ind_len = []
                            for ind_len, copet_list in list_to_delete_cometitors_to_compare:                    # убираем индексы длины (количества спасенных)
                                list_to_delete_cometitors_to_compare_with_no_ind_len.append(copet_list)
                            #print('Э сюда на111111' , list_to_delete_cometitors_to_compare_with_no_ind_len)
                            #print('===========')
                            final_list_to_delete_competitors_in_brand = []                                      # финальный список - очищенный от листов - все непопулярные competitors производителя в одном списке
                            for list_val in list_to_delete_cometitors_to_compare_with_no_ind_len:
                                for item in list_val:
                                    final_list_to_delete_competitors_in_brand.append(item)
                            final_list_to_delete_competitors_in_brand = list(set(final_list_to_delete_competitors_in_brand)) 
                            #print('Э сюда на', final_list_to_delete_competitors_in_brand)
                            list_to_delete_rarely_parsed.extend(final_list_to_delete_competitors_in_brand)          # формируем единый список на удаление
                            #print('list_to_delete_cometitors', list_to_delete_cometitors_to_compare)
                            # убираем непопулярных (реже спашенных модели данного бренда, исключая их из списка общего - останутся лишь производители с одной моделью (у тех производ, у которых было несколько моделей- останется лишь самый спашенный наиболее)):
                        #print('DELETE', list_to_delete_rarely_parsed)
                        for compet_to_delete in list_to_delete_rarely_parsed:
                            list_of_matched_competitors.remove(compet_to_delete)
                        bagoria_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                    # если у каждого производителя по одной модели:
                    else:

                        bagoria_competitors_dict1[object_unit.tyre] = list_of_matched_competitors

                else:
                    # 2.1 работа с датами без конкурентов (вся продукция)
                    #print('2.1 НЕ ВЫБРАН БРЕНД И ВВЕДЕНА ДАТА  - BAGORIA')
                    if models.COMPETITORS_DATE_FROM_USER_ON_FILTER or models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                            date_filter_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], "%Y-%m-%d").date()
                        else:
                            date_filter_start =  all_competitors.earliest('date_period').date_period
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                            date_filter_end = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                        else:
                            date_filter_end =  all_competitors.latest('date_period').date_period
                        got_the_list = all_competitors.filter(date_period__range=[date_filter_start, date_filter_end])
                                                  
                    else:
                        #print('2.2 НЕ ВЫБРАН БРЕНД И НЕ ВВЕДЕНА ДАТА  - BAGORIA')
                        got_the_list = all_competitors 
                        # end работа с датами       
                                                                                                       ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ    

                    brand_name_subbrands_list = []
                    list_to_delete_rarely_parsed = []    #для удаления реже спаршеных моделей внутри одного бренда(производителя)
                    for competitor in got_the_list:
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            # доп проверка на сезонность:
                            try:
                                for get_season in object_unit.tyre.added_features.all():
                                    get_season_is_is = get_season.season_usage.season_usage_name
                                if get_season_is_is == competitor.season.season_usage_name:
                                #    print('||', competitor.name_competitor)
                                    list_of_matched_competitors.append(competitor)
                                    brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде

                            except:     #если сезонности нет:
                                list_of_matched_competitors.append(competitor) 
                                brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                    brand_name_subbrands_list_final = list(set(brand_name_subbrands_list))
                #print('111list_of_matched_competitors', list_of_matched_competitors)
                    #print('22222brand_name_subbrands_list_final', brand_name_subbrands_list_final)

                    # доп проверка - так все бренды- у них м.б. по несколько моделей - проверить -есть ли у бреда несколько моделей -взять с наибольшей частотой паринга:
                    list_of_developers_which_brands_more_than_one_for_checking = []
                    for comp_brand in list_of_matched_competitors:
                        list_of_developers_which_brands_more_than_one_for_checking.append((comp_brand.developer, comp_brand.name_competitor))  
                        #print('comp_brand', comp_brand.developer)

                    list_of_developers_which_brands_more_than_one_for_checking = list(set(list_of_developers_which_brands_more_than_one_for_checking))            # # пересобираем список = проверка производитель  сразными моделями
                    develop_name_list_only_comp = []
                    for commm_namme in list_of_developers_which_brands_more_than_one_for_checking:
                        develop_name_list_only_comp.append(commm_namme[0])
                    list_of_developers_which_brands_more_than_one_for_checking = develop_name_list_only_comp   

                    list_of_developers_which_brands_more_than_one = []
                    for comp_brand_name in list_of_developers_which_brands_more_than_one_for_checking:
                        if list_of_developers_which_brands_more_than_one_for_checking.count(comp_brand_name) > 1: # если наименование производителя более одногораза - значит есть неск брендов у него, надо взять наиб спарсенный
                            list_of_developers_which_brands_more_than_one.append(comp_brand_name)
                    list_of_developers_which_brands_more_than_one = list(set(list_of_developers_which_brands_more_than_one))
                    #print('ISS list_of_developers_which_brands_more_than_one', list_of_developers_which_brands_more_than_one)   #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                    if list_of_developers_which_brands_more_than_one:                                                             #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                #        # 1) сформировать бренды у данного прозводителя
                #        # 2) сравнить какой более часто спаршен
                #        # 3) убрать менее спаршенные компетиторы из общего списка (bagoria_competitors_dict1)
                        for develoooper in list_of_developers_which_brands_more_than_one:                                       #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                            list_to_delete_cometitors_to_compare = [] #СПИСОК COMPETITORS ДЛЯ УДАЛЕНИЯ ИЗ ОБЩЕГО - сперва сравнить длинну моделей в бренде
                            for comp_brand_model in brand_name_subbrands_list_final:       # ['Cordiant Comfort 2', Continental ContiPremiumContact ]
                                brand_in_develoooper_dict = {}       
                                brand_in_develoooper_list = []
                                for subbrand_model_competitor in list_of_matched_competitors:
                                #    print('EEE', subbrand_model_competitor.developer, '|', develoooper, '|', subbrand_model_competitor.name_competitor, '|', comp_brand_model)
                                    if subbrand_model_competitor.developer == develoooper and subbrand_model_competitor.name_competitor == comp_brand_model:
                                        brand_in_develoooper_list.append(subbrand_model_competitor)
                                if brand_in_develoooper_list:
                                #    brand_in_develoooper_dict[comp_brand_model, develoooper] = brand_in_develoooper_list     #{'Cordiant Road Runner': [<CompetitorSiteModel: CompetitorSiteModel object (10966)>,
                                    brand_in_develoooper_dict = { comp_brand_model : brand_in_develoooper_list, develoooper : develoooper }
                                    #print('++--++', brand_in_develoooper_dict.keys())
                                try:
                                    if brand_in_develoooper_dict[develoooper] == develoooper:                           # СВЕРКА ЧАСТОТЫ ПАРСИНГА МОДЕЛЕЙ ДАННОГО ПРОИЗВОДИТЕЛЯ, ВЫБОРКА НАИМю СПАРСЕННЫХ _ ИХ УБРАТЬ ИХ ОБЩЕГО ПЕРЕЧНЯ  list_of_matched_competitors                         
                                        #print(comp_brand_model, 'LLLL111TTTT', brand_in_develoooper_dict[develoooper], 'PP22',  develoooper)
                                        len_comparison_got = len(brand_in_develoooper_dict[comp_brand_model])
                                        #compare_to_delete = len_comparison_got
                                        compare_to_delete = len_comparison_got, brand_in_develoooper_dict[comp_brand_model]
                                        list_to_delete_cometitors_to_compare.append(compare_to_delete)
                                        #brand_in_develoooper_dict_new[comp_brand_model] = brand_in_develoooper_dict[comp_brand_model]
                                except:
                                    pass
                            list_to_delete_cometitors_to_compare = sorted(list_to_delete_cometitors_to_compare, key=lambda x: x[0])     ## !!!! ОТСОРТИРОВАНЫ ПО ЧАСТОТЕ ПАРСИНГА каждого бренда(модели) внутри ДАННОГО ПРОИЗВОДИТЕЛЯ (т.е производитель Cordiant - но у него бренды Comfort 3, Winter Sport2  и т.д)
                            list_to_delete_cometitors_to_compare = list_to_delete_cometitors_to_compare[:-1]    ## Competitorы на удаление из перечня
                            list_to_delete_cometitors_to_compare_with_no_ind_len = []
                            for ind_len, copet_list in list_to_delete_cometitors_to_compare:                    # убираем индексы длины (количества спасенных)
                                list_to_delete_cometitors_to_compare_with_no_ind_len.append(copet_list)
                            #print('Э сюда на111111' , list_to_delete_cometitors_to_compare_with_no_ind_len)                 
                            final_list_to_delete_competitors_in_brand = []                                      # финальный список - очищенный от листов - все непопулярные competitors производителя в одном списке
                            for list_val in list_to_delete_cometitors_to_compare_with_no_ind_len:
                                for item in list_val:
                                    final_list_to_delete_competitors_in_brand.append(item)
                            final_list_to_delete_competitors_in_brand = list(set(final_list_to_delete_competitors_in_brand)) 
                            #print('Э сюда на', final_list_to_delete_competitors_in_brand)
                            list_to_delete_rarely_parsed.extend(final_list_to_delete_competitors_in_brand)          # формируем единый список на удаление
                            #print('list_to_delete_cometitors', list_to_delete_cometitors_to_compare)
                            # убираем непопулярных (реже спашенных модели данного бренда, исключая их из списка общего - останутся лишь производители с одной моделью (у тех производ, у которых было несколько моделей- останется лишь самый спашенный наиболее)):
                        #print('DELETE', list_to_delete_rarely_parsed)
                        for compet_to_delete in list_to_delete_rarely_parsed:
                            list_of_matched_competitors.remove(compet_to_delete)
                        bagoria_competitors_dict1 [object_unit.tyre] = list_of_matched_competitors           
                    else:       # если у каждого бренда-производителя по одной модели:
                        bagoria_competitors_dict1 [object_unit.tyre] = list_of_matched_competitors
            except:
        #        print('3. EXCEPTION  - BAGORIA')
                pass

        models.BAGORIA_COMPETITORS_DICTIONARY1 = bagoria_competitors_dict1

        ####### END!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ИЗМЕНЕНИЯ В СЛОВАРЕ - ОСТАВЛЯЕМ ЕСЛИ ЕТЬ НЕСК ШИН ОДНОГО ПРОИЗВОДИТ - ОСТАВИТ С НАИМ ЦЕНОЙ:
        ###### END OF BAGORIA

#       ## 2 фильтр конкурентов CHEMCURIER:
        try:
            # 1.1 ФИЛЬТР по дате (БЕРЕТСЯ ПОСЛЕДНИЙ ПЕРИОД В ОТЧЕТЕ ХИМКУРЬЕР) # НО - МОЖНО И СДЕЛАТЬ ЗА ПЕРИОД - В MODELS ЕСТЬ РАСЧЕТ НА ПЕРИОДЫ - НУЖНО ТОЛЬКО ЗДЕЬ УБРАТЬ НА ПОСЛ ДАТУ И ЗАДАТЬ ПЕРИОД ОТБОРА
            last_fate_availible_chem = models.ChemCurierTyresModel.objects.latest('data_month_chem').data_month_chem
        #    print('!!!!!!!!!', last_fate_availible_chem, type(last_fate_availible_chem))
            all_competitors_chem = models.ChemCurierTyresModel.objects.filter(data_month_chem=last_fate_availible_chem)     # по дате 
        #    print('last_fate_availible_chem', last_fate_availible_chem, 'all_competitors', all_competitors_chem)
#           # 1.2 ФИЛЬТР список производителей:
            # 1.2.1 - как вариант - выбор из тех производителей - кого ввел пользователь

            list_brands_to_check = []       # набиваем перечень рендов- кого выбрал пользователь
            if models.BAGORIA_COMPETITORS:
                list_brands_to_check.extend(models.BAGORIA_COMPETITORS)   
            if models.AVTOSET_COMPETITORS:
                list_brands_to_check.extend(models.AVTOSET_COMPETITORS) 
            if models.ONLINER_COMPETITORS:
                  list_brands_to_check.extend(models.ONLINER_COMPETITORS)

            chemcurier_competitors_dict1 = {}
            if list_brands_to_check:       # если бренды выбранные есть - искать по ним:                    !!!!!!!! вариант - отбора как обычно делаем
                all_competitors_chem = all_competitors_chem.filter(producer_chem__in=list_brands_to_check)        # поиск на посл дату в химкурьере по указанным брендам
            else:
                pass                                                                                    # поиск на посл дату в химкурьере 
            for object_unit in list_of_tyre_comparative_objects:
                list_of_matched_competitors = []
                for competitor in all_competitors_chem:  
                    for t_gr in object_unit.tyre.tyre_group.all():
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyre_size_chem and t_gr == competitor.group_chem and competitor.average_price_in_usd is not None:         # сверка по типоразмеру и группе шин не пустые
                            list_of_matched_competitors.append(competitor)
                chemcurier_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
       #    #####  НАДО СФОРМИРОВАТЬ СЛОВАРЬ С НЕСКОЛЬКИМИ КОНКУРЕНТАМИя 05.12.2022
            models.CHEMCURIER_COMPETITORS_DICTIONARY1 = chemcurier_competitors_dict1  
            #print('models.CHEMCURIER_COMPETITORS_DICTIONARY1 ==', models.CHEMCURIER_COMPETITORS_DICTIONARY1)
            #for tt in models.CHEMCURIER_COMPETITORS_DICTIONARY1.values():
            #    for n in tt:
            #        print(n.producer_chem, n.data_month_chem)
        except:
            pass
        ###### END OF CHEMCURIER

        ##################
        ##################
        ##Работа с интефейсом:
        #list_of_all_competitors_template = []
        #all_competitors_in_base = dictionaries_models.CompetitorModel.objects.all()
        #for t in all_competitors_in_base:
        #    list_of_all_competitors_template.append(t.competitor_name)
        #context['onliner_competitors'] = list(set(list_of_all_competitors_template))
        #####

        ######## !!!! ПЕРЕСБОРКА ИТОГОВОГО ПЕРЕЧНЯ ОБЪЕКТОВ ДЛЯ ВЫВОДА НА СТРАНИЦУ (только объекты с отфильтрованными конкурентами only):
        #print('list_of_tyre_comparative_objects =====================1 =', len(list_of_tyre_comparative_objects ), list_of_tyre_comparative_objects)

        bagor_lengh_list = []
        avtoset_lengh_list = []
        onliner_lengh_list = []

        #for YYY in list_of_tyre_comparative_objects:
        #    print('000===000', YYY) 
        
        #print('models.ONLINER_COMPETITORS_NAMES_FILTER_IDS ', models.ONLINER_COMPETITORS_NAMES_FILTER_IDS)
        list_of_tyre_comparative_objects_ids = []
        #final_list_of_objects_for_template = []
        final_list_of_objects_for_template = models.ComparativeAnalysisTyresModel.objects.none()
        #print('TTTTTTTTT=====2 list_of_tyre_comparative_objects LEN IS', len(list_of_tyre_comparative_objects),  list_of_tyre_comparative_objects)
        for tt in list_of_tyre_comparative_objects:
        #    print('tt', tt.tyre.tyre_model.model, tt.tyre.tyre_size.tyre_size, tt.sale_data, tt.id, tt) 
            tt.onliner_competitor_on_date1()
            tt.avtoset_competitor_on_date1()
            tt.bagoria_competitor_on_date1()
            onl_result = tt.onliner_table_header()
            avt_result = tt.avtoset_table_header()
            bag_result = tt.bagoria_table_header()
            #for yyy in bag_result:
            #    print(yyy)
            chem_result = tt.chemcurier_competitor_on_date1()
            proverka = [('', '', ''), ('', '', ''), ('', '', '')] 
            proverka_chem = ('', '', '')
            if onl_result != proverka or avt_result != proverka or bag_result != proverka or chem_result != proverka_chem:
                list_of_tyre_comparative_objects_ids.append(tt.pk)  
            else:
                pass 
            final_list_of_objects_for_template = models.ComparativeAnalysisTyresModel.objects.filter(pk__in=list_of_tyre_comparative_objects_ids).order_by('tyre')  
            #print('ЭЭЭЭЭ=', final_list_of_objects_for_template)
            if bag_result:
                bagor_curr_lengh = len(bag_result)
                bagor_lengh_list.append(bagor_curr_lengh)

            if avt_result:
                avtoset_curr_lengh = len(avt_result)
                avtoset_lengh_list.append(avtoset_curr_lengh)

            if onl_result:
                onliner_curr_lengh = len(onl_result)
                onliner_lengh_list.append(onliner_curr_lengh)
            ##### ДОПОЛЛНИТЕЛЬНО К ПЕРЕСБОРКЕ - Т.К. УБРАНА ГАЛОЧКА "ВСЯ ПРОДУКЦИЯ" - ВЫБИРАЕТСЯ АВТОМАТОМ 1-й ИЗ ОБРАБОТАННЫХ ЭЛЕМЕНТОВ ДЛЯ ВЫВОДА:
            if models.SELF_PRODUCTION_FIRST is True and final_list_of_objects_for_template.exists():
            #    print('WTF?')
                break   # обрываем цикл - берем только первого
            if models.DEF_GET is True:
            #    print('=====2')
                models.DEF_GET = False
                break   # обрываем цикл - берем только первого

            ##### ДОПОЛЛНИТЕЛЬНО К ПЕРЕСБОРКЕ - Т.К. УБРАНА ГАЛОЧКА "ВСЯ ПРОДУКЦИЯ" - ВЫБИРАЕТСЯ АВТОМАТОМ 1-й ИЗ ОБРАБОТАННЫХ ЭЛЕМЕНТОВ ДЛЯ ВЫВОДА

        list_of_tyre_comparative_objects = final_list_of_objects_for_template                       # !!  список СomparativeAnalysisTyresModel  у которых отфильтрованы конкуренты
        #print('list_of_tyre_comparative_objects_ids', list_of_tyre_comparative_objects_ids)         # !!  список СomparativeAnalysisTyresModel id у которых отфильтрованы конкуренты
        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects.order_by('tyre__tyre_size__tyre_size')

        #for ttt in list_of_tyre_comparative_objects: ### ( list_of_tyre_comparative_objects из ПЕРЕСБОРКА ИТОГОВОГО ПЕРЕЧНЯ)
        #    print('111===111', YYY)         

        ########END !!!!! ПЕРЕСБОРКА ИТОГОВОГО ПЕРЕЧНЯ

    #### ЗАГОЛОЛОВКИ ТАБЛИЦЫ:
        ## ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ BAGORIA: 
        if bagor_lengh_list: 
            if models.COMPET_PER_SITE:
                bagoria_max_lengh_header = models.COMPET_PER_SITE                                      
            elif bagor_lengh_list[0] > 3:        
                bagoria_max_lengh_header = 2                            # Количество колонок (обрезает до первых 3)
            else:
                bagoria_max_lengh_header = max(bagor_lengh_list)
        else:
            bagoria_max_lengh_header = 0

        models.BAGORIA_HEADER_NUMBER = bagoria_max_lengh_header
        # print('models.BAGORIA_HEADER_NUMBER ====+++==', models.BAGORIA_COMPETITORS_NAMES_FILTER)

#        print('obj. ===', obj)
        obj = context.get('object')                 ## ДОРАБОТАНО _ ПРИ ОТСУТСТВИИ ВЫБОРА ПРОДУКЦИИ
        obj.bagoria_heders_value()
        #print('obj.bagoria_heders_value()', obj.bagoria_heders_value())
        obj.bagoria_heders_lengt() 
        ## END ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ BAGORIA:          
        ## ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ AVTOSET: 
        if avtoset_lengh_list:
        #    print('avtoset_lengh_list--------------', avtoset_lengh_list)
            if models.COMPET_PER_SITE:
                avtoset_max_lengh_header = models.COMPET_PER_SITE
            elif avtoset_lengh_list[0] > 3:                                # Количество колонок (обрезает до первых 3) 
                avtoset_max_lengh_header = 2
            else:
                avtoset_max_lengh_header = max(avtoset_lengh_list)
        else:
            avtoset_max_lengh_header = 0
        #print('avtoset_max_lengh_header+++++++++++', avtoset_max_lengh_header, 'avtoset_lengh_list', avtoset_lengh_list, 'models.COMPET_PER_SITE', models.COMPET_PER_SITE)
        models.AVTOSET_HEADER_NUMBER = avtoset_max_lengh_header
        #print('models.AVTOSET_HEADER_NUMBER ====+++==', models.AVTOSET_COMPETITORS_NAMES_FILTER )
        #print('models.AVTOSET_HEADER_NUMBER ====+++==', models.AVTOSET_HEADER_NUMBER)
        obj.avtoset_heders_value()
        obj.avtoset_heders_lengt()         
        ##END ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ AVTOSET: 
        # ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ ONLINER: 

        if onliner_lengh_list:
            if models.COMPET_PER_SITE:
                onliner_max_lengh_header = models.COMPET_PER_SITE
            elif onliner_lengh_list[0] > 3:
                onliner_max_lengh_header = 2                        # Количество колонок (обрезает до первых 3)
            else:
                onliner_max_lengh_header = max(onliner_lengh_list)
        else:
            onliner_max_lengh_header = 0
            
        models.ONLINER_HEADER_NUMBER = onliner_max_lengh_header


        obj.onliner_heders_value()
        obj.onliner_heders_lengt()
        #END ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ ONLINER: 
       ## ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ CHEMCURIER: 
        chemcurier_max_lengh_header = 1                                 # chemcurier будет лишь один столбец
        models.CHEMCURIER_HEADER_NUMBER = chemcurier_max_lengh_header
        # print('models.CHEMCURIER_HEADER_NUMBER ====+++==', models.CHEMCURIER_HEADER_NUMBER)
        obj.chemcurier_heders_value()
        obj.chemcurier_heders_lengt()
       ##END ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ CHEMCURIER: 
    #### END ЗАГОЛОЛОВКИ ТАБЛИЦЫ   


        ####### Формы для фильтров темплейта:
        #print('models.ONLINER_COMPETITORS_NAMES_FILTER', models.ONLINER_COMPETITORS_NAMES_FILTER)           ###### ТАК здесь продолжим
        # если применен фильтр:
        # 1) выбрать производителя:
        #filter_form = forms.FilterForm()
        #context['producer_filter_form'] = filter_form                                           
        #context['producer_filter_form'].queryset = dictionaries_models.CompetitorModel.objects.filter(competitor_name__in=list(set(models.ONLINER_COMPETITORS_NAMES_FILTER)) and list(set(models.AVTOSET_COMPETITORS_NAMES_FILTER) and list(set(models.BAGORIA_COMPETITORS_NAMES_FILTER)))
        #and list(set(models.BAGORIA_COMPETITORS_NAMES_FILTER))).values_list("competitor_name", flat=True)

        ### фильтр ПРОРИСОВКА по брендам для темплейт отрисовка чекбоксов:
        brand_names_check_status_list = []
        brand_names = list(dictionaries_models.CompetitorModel.objects.filter(developer_competitor__site__in=['onliner.by', 'bagoria.by', 'autoset.by']).distinct().values_list("competitor_name", flat=True).order_by('competitor_name'))
        if models.PRODUCER_FILTER_BRAND_LIST_CHECKED_ON:        # если пользовательвыбирал бренды производителей (checked)
            for namee in brand_names:
                if namee in models.PRODUCER_FILTER_BRAND_LIST_CHECKED_ON:
                    name_and_status = namee, 'checked'
                    brand_names_check_status_list.append(name_and_status)
                    context['producer_filter_brand_list_checked__only_3_cheapest_chosen_bage'] = None
                else:
                    name_and_status = namee, ''
                    brand_names_check_status_list.append(name_and_status)

        else:
            for namee in brand_names:
                name_and_status = namee, ''
                brand_names_check_status_list.append(name_and_status)
                context['producer_filter_brand_list_checked__only_3_cheapest_chosen_bage'] = 'бренд не выбран (автоматически предоставлены данные о всех брендах)'
######        print('brand_names_check_status_list1111', brand_names_check_status_list)

        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_IS_NOT_CHOSEN is True:
            context['end_date_is_not_chosen_bage'] = 'конечная дата не выбрана (дата выставлена автоматически)'
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START_IS_NOT_CHOSEN is True:
            context['start_date_is_not_chosen_bage'] = 'начальная дата не выбрана (дата выставлена автоматически)'



        context['producer_filter_brand_list'] = brand_names_check_status_list
        context['producer_filter_brand_list_checked_bage'] = models.PRODUCER_FILTER_BRAND_LIST_CHECKED_ON        # для вплывающей подсказки - значек с выбранными позициями брендов       # для вплывающей подсказки - значек с выбранными позициями брендов
        #context['producer_filter_brand_list'] = list(dictionaries_models.CompetitorModel.objects.filter(developer_competitor__site__in=['onliner.by', 'bagoria.by', 'autoset.by']).distinct().values_list("competitor_name", flat=True).order_by('competitor_name'))
        
        context['producer_filter_all'] = dictionaries_models.CompetitorModel.objects.all()
        ## END фильтр по брендам для темплейт отрисовка чекбоксов

        # 2) выбрать продукцию:
        ### Отдельная сборка списка всех объеков с конкурентами для меню:
        ##if not models.SELF_PRODUCTION:
        models.FOR_MENU_OBJECTS_LIST = final_list_of_objects_for_template              # постоянный список объектов для отображения в меню
        in_base_tyres_check_status_list = []
        in_base_tyres_check_status_list_checked_bage = []
        #for obj in models.FOR_MENU_OBJECTS_LIST:       old version  
        for obj in table_lookup_only_with_competitors_all_parsed.order_by('tyre__tyre_size__tyre_size'):           # берем для меню вообще все, для кого хоть когда-либо что-то парсилось хоть раз
            if models.SELF_PRODUCTION_ALL:
                objj_and_status = obj, ''
            elif str(obj.id) in models.SELF_PRODUCTION:
                objj_and_status = obj, 'checked'
                in_base_tyres_check_status_list_checked_bage.append(obj)
            else: 
#                if obj == list_of_tyre_comparative_objects[0]:    # т.к. в template закоменчен выбор всей продукции - то автоматом ставим галочку на первой в списке и выводим ее:
#                    #print('zloy pinguin')
#                    objj_and_status = obj, 'checked'
#                    if models.SELF_PRODUCTION_FIRST is True:
#                        context['no_chosen_production_checked_bage'] = f'продукция не выбрана (автоматически представлены данные по {obj.tyre.tyre_size.tyre_size} {obj.tyre.tyre_model.model})' 
#                else:    
#                    objj_and_status = obj, ''

                if list_of_tyre_comparative_objects:                                                       
                    if obj == list_of_tyre_comparative_objects[0]:    # т.к. в template закоменчен выбор всей продукции - то автоматом ставим галочку на первой в списке и выводим ее:
                        #print('zloy pinguin')
                        objj_and_status = obj, 'checked'
                        if models.SELF_PRODUCTION_FIRST is True:
                            if models.SEARCH_USER_REQUEST and search_result_id_is_true:                  # если поиск продукции был через ПОИСК
                                in_base_tyres_check_status_list_checked_bage.append(obj)
                                context['in_base_tyres_list_checked_bage'] = in_base_tyres_check_status_list_checked_bage
                            else:
                                context['no_chosen_production_checked_bage'] = f'продукция не выбрана (автоматически представлены данные по {obj.tyre.tyre_size.tyre_size} {obj.tyre.tyre_model.model})' 
                    else:
                        objj_and_status = obj, ''
                else:    
                    objj_and_status = obj, ''
                    #if obj == list_of_tyre_comparative_objects[0]:
                    #    context['no_chosen_production_checked_bage'] = f'продукция не выбрана (автоматически представлены данные по {obj.tyre.tyre_size.tyre_size} {obj.tyre.tyre_model.model})'

            in_base_tyres_check_status_list.append(objj_and_status)

        if models.SELF_PRODUCTION:
            context['in_base_tyres_list_checked_bage'] = in_base_tyres_check_status_list_checked_bage    # для вплывающей подсказки - значек с выбранными позициями типоразмеров
        context['in_base_tyres'] = in_base_tyres_check_status_list
         ### END Отдельная сборка списка всех объеков с конкурентами для меню

        #######  
        # 3) выбрать группу шин:
        tyr_groups = dictionaries_models.TyreGroupModel.objects.all()
        tyr_groups_check_status_list = []
        tyr_groups_check_status_list_checked_bage = []
        for tyr_gr in tyr_groups:
            #print('tyr_gr.id', tyr_gr.id)
            if models.TYRE_GROUPS_ALL:
                tyr_gr_and_status = tyr_gr, ''
            #if str(tyr_gr.id) in models.TYRE_GROUPS:    
            elif str(tyr_gr.id) in models.TYRE_GROUPS:
                tyr_gr_and_status = tyr_gr, 'checked'
                tyr_groups_check_status_list_checked_bage.append(tyr_gr)
            else:
                tyr_gr_and_status = tyr_gr, ''
            tyr_groups_check_status_list.append(tyr_gr_and_status)
        ##print('tyr_groups', tyr_groups)
        context['in_base_tyres_by_group_checked_bage'] = tyr_groups_check_status_list_checked_bage
        context['in_base_tyres_by_group'] = tyr_groups_check_status_list
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
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
            context['chosen_date_start'] = models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0]

        #### СБРОС ДАННЫХ _ ОЧИСТКА ПРИ ОБНОВЛЕНИИ СТРАНИЦЫ:
        #models.TYRE_GROUPS = []     
        #models.TYRE_GROUPS_ALL = [] 
        #models.SELF_PRODUCTION = []
        #models.SELF_PRODUCTION_ALL = []  
        #models.ONLINER_COMPETITORS = [] 
        #models.AVTOSET_COMPETITORS = []
        #models.BAGORIA_COMPETITORS = []
        #models.CHEMCURIER_COMPETITORS = []
        #models.SEARCH_USER_REQUEST = []
        #models.COMPETITORS_DATE_FROM_USER_ON_FILTER = []

        # пагинация самодельная:
        current_pagination_value = models.PAGINATION_VAL
        if current_pagination_value is None:
            current_pagination_value = 10
        pagination_form = forms.PaginationInputForm(initial={'pagination_data': current_pagination_value})
        context['pagination_val_per_form'] = pagination_form        
        #context['current_pagination_value'] = current_pagination_value        
        posts = context['list_of_tyre_comparative_objects']
        #print('1!!!!', len(posts))
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
        #print('!!!!!!!!!!!!!!!0', self.request.GET, self.request.GET.urlencode())
        # END # пагинация самодельная


        # количество выводимых конкурентов на для сайтов:
        current_compet_per_site_value = models.COMPET_PER_SITE
        if current_compet_per_site_value is None:
            current_compet_per_site_value = 2
        compet_per_site_form = forms.CompetitoPerSiteInputForm(initial={'competitor_pagination_data': current_compet_per_site_value})
        context['compet_per_site_form'] = compet_per_site_form
        # END количество выводимых конкурентов на для сайтов:


        currency_input_form = forms.CurrencyDateInputForm()
        context['currency_input_form'] = currency_input_form

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

        #print('ONLINER_COMPETITORS_NAMES_FILTER', models.ONLINER_COMPETITORS_NAMES_FILTER)
        


        #############   ТЕСТОВАЯ ШТУКА ДЛЯ ГРАФИКОВ PANDAS  
        # 0. Получаем объекты и их реально офильтрованные по параметрам конкуренты:
        #print('ONLINER_COMPETITORS_NAMES_FILTER_IDS', models.ONLINER_COMPETITORS_NAMES_FILTER_IDS) # ключ - id объета ComparativeAnalysisTyresModel, згначения - список id отфильтрованных конкурентов CompetitorSiteModel

        edyniy_slovar_dict_dlja_pandas_chart_graphic = {}               ##### И.С.Х.О.Д.Н.И.К. Д.Л.Я. О.Т.Р.И.С.О.В.К.И. Г.Р.А.Ф.И.К.А. !!!WARNING IMPORTANT
        spisok_competitors_filtered = []

        #print('list_keys', list_keys) #
        #print('list_of_tyre_comparative_objects ====!',  list_of_tyre_comparative_objects_ids,) #'list_of_tyre_comparative_objects TRUE', list_of_tyre_comparative_objects)      

        #print('1 list_of_tyre_comparative_objects_ids', list_of_tyre_comparative_objects_ids)

        for tyre_for_chart_need_all_checked_competitors in list_of_tyre_comparative_objects_ids:
            competitors_ids1 = models.ONLINER_COMPETITORS_NAMES_FILTER_IDS.get(tyre_for_chart_need_all_checked_competitors)
            if competitors_ids1 is None:
                competitors_ids1 = []
            competitors_ids2 = models.AVTOSET_COMPETITORS_NAMES_FILTER_IDS.get(tyre_for_chart_need_all_checked_competitors)
            if competitors_ids2 is None:
                competitors_ids2 = []              
            competitors_ids3 = models.BAGORIA_COMPETITORS_NAMES_FILTER_IDS.get(tyre_for_chart_need_all_checked_competitors)
            if competitors_ids3 is None:
                competitors_ids3 = []
            #for nnit in competitors_ids3:
            #   GICK = models.CompetitorSiteModel.objects.get(id=nnit)
            #   print('GICK', GICK.developer, GICK.date_period) 
            spisok_competitors_filtered = competitors_ids1 + competitors_ids2 + competitors_ids3
            edyniy_slovar_dict_dlja_pandas_chart_graphic[tyre_for_chart_need_all_checked_competitors] = spisok_competitors_filtered   #### !!!!!!!!!!!!!!!!!!!!!! СЛОВАРЬ ДЛЯ ГРАФИКА
        #print('edyniy_slovar_dict_dlja_pandas_chart_graphic == HH', edyniy_slovar_dict_dlja_pandas_chart_graphic)

        #for n, nv in edyniy_slovar_dict_dlja_pandas_chart_graphic.items():      
        #    for t in nv:
        #        ss = models.CompetitorSiteModel.objects.get(id=t)
        #        print('==++==', ss.date_period, ss.developer, ss.price,  'Takim')


        ### ЭТАП ПРОВЕРКИ СЛОВАРЯ НА НАЛИЧИЕ ПРОДУКЦИИ РАЗНЫХ ТИПОРАЗМЕРОВ - ЕСЛИ РАЗНЫЕ ТИПОРАЗМЕРЫ - БЕРЕМ ПЕРВЫЙ (И ВСЕ ОДИНАКОВЫЕ С НИМ МОДЕЛИ), ОТСЕИВАЕМ ПРОДУКЦИЮ С ИНЫМ ТИПОРАЗМЕРОМ   
        if not edyniy_slovar_dict_dlja_pandas_chart_graphic:         # если словарь пуст
            pass
        else:                                                        # если словарь не пуст    
            #print('edyniy_slovar_dict_dlja_pandas_chart_graphic.keys() = 1',edyniy_slovar_dict_dlja_pandas_chart_graphic.keys())
            #print('edyniy_slovar_dict_dlja_pandas_chart_graphic.items() = 1',edyniy_slovar_dict_dlja_pandas_chart_graphic.items())
            prod_id_with_same_tyresize_as_the_first_one_list = []
            for prod_id in edyniy_slovar_dict_dlja_pandas_chart_graphic.keys():                     
                production_tyresizes = models.ComparativeAnalysisTyresModel.objects.get(id=prod_id)
                production_tyresizes = production_tyresizes.tyre.tyre_size.tyre_size
                prod_id_and_production_tyresize = prod_id, production_tyresizes
                prod_id_with_same_tyresize_as_the_first_one_list.append(prod_id_and_production_tyresize)        # получаем id и их типоразмер
            #    print('SSUPER_KEY', prod_id, production_tyresizes)
            first_prod_id_tyr_size = prod_id_with_same_tyresize_as_the_first_one_list[0]    # сравним полученное с первым типоразмером
            #print('first_prod_id_tyr_size', first_prod_id_tyr_size)
            id_with_same_tyre_size_as_first_one_list = []
            for d_tyrr_size in prod_id_with_same_tyresize_as_the_first_one_list:
                if d_tyrr_size[1] == first_prod_id_tyr_size[1]:                                 # если одинаковый типоразмер с первым - берем продукцию
                    id_with_same_tyre_size_as_first_one_list.append(d_tyrr_size[0])
            #print('id_with_same_tyre_size_as_first_one_list = IS =', id_with_same_tyre_size_as_first_one_list)
            temorary_id_with_same_tyre_size_as_first_one_dict ={}
            for same_tyr_size_id in id_with_same_tyre_size_as_first_one_list:
                temorary_id_with_same_tyre_size_as_first_one_dict[same_tyr_size_id] = edyniy_slovar_dict_dlja_pandas_chart_graphic.get(same_tyr_size_id)
            #print('temorary_id_with_same_tyre_size_as_first_one_dict.keys() = 2', temorary_id_with_same_tyre_size_as_first_one_dict.keys())
            #print('temorary_id_with_same_tyre_size_as_first_one_dict.items() = 2', temorary_id_with_same_tyre_size_as_first_one_dict.items())

            ## !!! ПЕРЕПИСЫВАНИЕ СЛОВАРЯ = ТОЛЬКО ПРОДУКЦИЯ ОДНОГО ТИПОРАЗМЕРА:
            edyniy_slovar_dict_dlja_pandas_chart_graphic = temorary_id_with_same_tyre_size_as_first_one_dict
            ## END !!! ПЕРЕПИСЫВАНИЕ СЛОВАРЯ = ТОЛЬКО ПРОДУКЦИЯ ОДНОГО ТИПОРАЗМЕРА:

        ### END ЭТАП ПРОВЕРКИ СЛОВАРЯ НА НАЛИЧИЕ ПРОДУКЦИИ РАЗНЫХ ТИПОРАЗМЕРОВ - ЕСЛИ РАЗНЫЕ ТИПОРАЗМЕРЫ - БЕРЕМ ПЕРВЫЙ (И ВСЕ ОДИНАКОВЫЕ С НИМ МОДЕЛИ), ОТСЕИВАЕМ ПРОДУКЦИЮ С ИНЫМ ТИПОРАЗМЕРОМ  


        # НА ПРИМЕРЕ ОДНОГО ОБЪЕКТА: 
        #### ФИЛЬТРАЦИЯ ДАННЫХ ПО ЗАПРОСУ ПОЛЬЗОВАТЕЛЯ:
        # 1. проверка, какие данные введены пользователем:
        # 1.1 каких конкурентов ввел/не ввел пользователь:
        #listt_prodduccers = models.ONLINER_COMPETITORS # ['Yokohama', 'LingLong', 'Viatti', 'Michelin']  #  # или models.AVTOSET_COMPETITORS или models.BAGORIA_COMPETITORS - они одинаковые
        #if listt_prodduccers:
        #    filter_producer = listt_prodduccers
        #else:
        #    filter_producer = []
        #    for n in dictionaries_models.CompetitorModel.objects.values_list('competitor_name'): 
        #      n = str(n).replace("('", '').replace("',)", '')
        #      filter_producer.append(n) 
        ##print('filter_producer', filter_producer)
        no_data_on_date = False             # отсутствуют данные типоразмеры с конкурентами
        filter_producer = []
        all_filtered_competitors_ids = list(edyniy_slovar_dict_dlja_pandas_chart_graphic.values())
        filtered_competitors_ids_list = []
        for xxy in all_filtered_competitors_ids:
            filtered_competitors_ids_list += xxy
        filtered_competitors_ids_list = list(set(filtered_competitors_ids_list))        # получим только фильтрованные компетиторы
        listt_prodduccers = models.CompetitorSiteModel.objects.filter(id__in=filtered_competitors_ids_list)
        for n in listt_prodduccers:
              n = n.developer.competitor_name
              n = str(n).replace("('", '').replace("',)", '')
              filter_producer.append(n)    
        #=print('filter_producer', filter_producer)         

        # 1.2 какие сайты ввел/не ввел пользователь:
        filter_sites = ['onliner.by', 'bagoria.by', 'autoset.by'] # по дефолту показать этих

        list_off_sizes_to_compare = []                                            # если есть типоразмер - роботаем по нему (шина одна или неск шин одного размера)
#!!!        for tyr_sizze in list_of_tyre_comparative_objects:
#!!!            list_off_sizes_to_compare.append(tyr_sizze.tyre.tyre_size.tyre_size)
        for tyr_sizze in edyniy_slovar_dict_dlja_pandas_chart_graphic.keys():
            production_tyresizes1 = models.ComparativeAnalysisTyresModel.objects.get(id=tyr_sizze)
            production_tyresizes1 = production_tyresizes1.tyre.tyre_size.tyre_size
            list_off_sizes_to_compare.append(production_tyresizes1)
        list_off_sizes_to_compare = set(list_off_sizes_to_compare)  
    #    print('list_off_sizes_to_compare HUSH HUSH HUSH', list_off_sizes_to_compare)
        chart_title = ''
        if len(list_off_sizes_to_compare) == 1:                                     # если есть типоразмер - роботаем по нему (шина одна или неск шин одного размера)     
            object_units = list_of_tyre_comparative_objects.filter(tyre__tyre_size__tyre_size=list(list_off_sizes_to_compare)[0])
            chart_title = object_units[0].tyre.tyre_size.tyre_size
        else:                                                                       # если не 1 типоразмер ИЛИ нет никаких ?? ХМ baby, check this out!
            #print('ГАЛЯ, У НАС ОТМЕНА!!!', type(list_of_tyre_comparative_objects), list_of_tyre_comparative_objects)
            if list_of_tyre_comparative_objects_is_empty is True:                        
                list_of_tyre_comparative_objects = models.ComparativeAnalysisTyresModel.objects.none()    # создать пустой queryset
            #print('GGGGG', list_of_tyre_comparative_objects)            # <QuerySet []> not list []
            if not list_of_tyre_comparative_objects.exists():           #### если объектов с конкурентом на дату нет - для рисовки пустой таблички:
                no_data_on_date = True
                object_units  = [None]
                chart_title = '- нет данных'
            else:
                object_units = list_of_tyre_comparative_objects.filter(tyre__tyre_size__tyre_size=list(list_off_sizes_to_compare)[0])


        # дополнительно даем имена чекбоксам сайтов для графика фильтра: 
        check_box_num = 0    
        for site_name in filter_sites:
            check_box_num += 1
            context[f'site_name'] = site_name, check_box_num

        context['object_unit'] = object_units
        context['filter_producer'] = filter_producer
        context['sites_filter_chart'] = filter_sites
        context['chart_title'] = chart_title


        #### ЕСЛИ модель/типоразмер и 1 ИЛИ несколько объктов ШИН:
        list_of_sites = []                                                                          #(ТИП-2 график по сайтам)            
        list_of_competitors_set = set()
        list_of_competitors = []
        list_start_dates = []
        list_last_dates = []
        #for object_unit in object_units:
        #    for comp in object_unit.price_tyre_to_compare.filter(site__in=filter_sites).filter(developer__competitor_name__in=filter_producer):        ## !!!! 2 ФИЛЬТР ПО САЙТАМ  и КОНКУРЕНТАМ
        #        #print('COMP', comp)  
        #        list_of_sites.append(comp.site)                                                                     #0 получаем наименования всех сайтоыдля легенды таблицы (ТИП-2 график по сайтам)   
        #        list_of_competitors.append(comp.developer.competitor_name)                                          #1 получаем наименования всех конкурентов для легенды таблицы                                               
        #    start_date = object_unit.price_tyre_to_compare.earliest('date_period').date_period                      #2.1 получаем начальную дату из всех конкурентов
        #    last_date = object_unit.price_tyre_to_compare.latest('date_period').date_period                         #2.2 получаем конечную дату из всех конкурентов
        #    list_of_competitors_set = set(list_of_competitors)                                                      #3. получаем список всех имен компаний-производителей (конкурентов)
        #    list_start_dates.append(start_date)
        #    list_last_dates.append(last_date)

        for keys, values in edyniy_slovar_dict_dlja_pandas_chart_graphic.items():
            list_of_competts = models.CompetitorSiteModel.objects.filter(pk__in=values)
            for ccomp in list_of_competts:
                list_of_sites.append(ccomp.site)                                                                    #0 получаем наименования всех сайтов для легенды таблицы (ТИП-2 график по сайтам)
                list_of_competitors.append(ccomp.developer.competitor_name)                                         #1 получаем наименования всех конкурентов для легенды таблицы   
            ooobj = models.ComparativeAnalysisTyresModel.objects.get(id=keys)
            start_date = ooobj.price_tyre_to_compare.earliest('date_period').date_period                      #2.1 получаем начальную дату из всех конкурентов  !ПЕРЕПИСАТЬ НА ВВОДИМЫЕ ПОЛЬЩОВАТЕЛЕМ
            #last_date = ooobj.price_tyre_to_compare.latest('date_period').date_period                         #2.2 получаем конечную дату из всех конкурентов   !ПЕРЕПИСАТЬ НА ВВОДИМЫЕ ПОЛЬЩОВАТЕЛЕМ           
            last_date = competitors_exist_all_dates_last_date_latest_date
            list_of_competitors_set = set(list_of_competitors)   
            list_start_dates.append(start_date)
            list_last_dates.append(last_date)

        if no_data_on_date is True:     # если отсутствуют данные типоразмеры с конкурентами
        #    print('models.COMPETITORS_DATE_FROM_USER_ON_FILTERRR', models.COMPETITORS_DATE_FROM_USER_ON_FILTER)
            if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
                chossen_day = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], '%Y-%m-%d').date()
            else:
                chossen_day = datetime.datetime.today()
            list_start_dates.append(chossen_day)
            list_last_dates.append(chossen_day)

        #    min_date = min(list_start_dates)
        #    max_date = max(list_last_dates)

            min_date = min(list_start_dates)                    
            if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                chossen_day_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], '%Y-%m-%d').date()
                min_date = chossen_day_start           
                                                                      
            max_date = max(list_last_dates)  # здесьб д.б. просто данные от пользователя какой день

        else:               # на все остальные случаи - если обект / конкуренты есть на дату:
            if models.ONLY_ON_CURRENT_DATE is True and models.COMPETITORS_DATE_FROM_USER_ON_FILTER:         # если нужно выводить график только на выбранную дату (стои галочка):
                chossen_day = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], '%Y-%m-%d').date()
                list_start_dates.append(chossen_day)
                list_last_dates.append(chossen_day)
            #    min_date = min(list_start_dates)                                                                        # здесьб д.б. просто данные от пользователя какой день
            #    max_date = max(list_last_dates)                  
            #else:
            min_date = min(list_start_dates)                                                                        # здесьб д.б. просто данные от пользователя какой день
            
            if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                #print('!!!!models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START', models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START)
                chossen_day_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], '%Y-%m-%d').date()
                min_date = chossen_day_start           
            
            max_date = max(list_last_dates)                                                                         # здесьб д.б. просто данные от пользователя какой день
        
        all_days_in_period = pd.date_range(start=min_date, end=max_date).date 
        #print('all_days_in_period', all_days_in_period)
        list_of_sites = set(list_of_sites)                                                                  #(ТИП-2 график по сайтам) 
        #print('list_of_sites', list_of_sites)                                                               #(ТИП-2 график по сайтам) 
       
       # СОБИРАЕМ ПРЕДВАРИТЕЛЬНЫЙ СПИСОК С ИМЕЮЩИМИСЯ ДАННЫМИ и искуственными пробелами NONE:
                                                         # если нужно получить усредненное значение



        # ПРОВЕРКА - НУЖЕН ГРАФИК ПО ПРОИЗВОДИТЕЛЯМ ЛИБО ПО ПЛОЩАДКАМ:
        if models.GOOGLECHART_MARKETPLACE_ON is False:      # ЕСЛИ НЕ СТОИТ ГАЛОЧКА ПО ПЛОЩАДКАМ - ФОРМИРУЕМ ГРАФИК ПО ПРОИЗВОДИТЕЛЯМ:
            context['marketplace_on_checked'] = ''
            competit_on_current_date_assembled = []                        ###### В ДАННЫЙ СПИСОК И ФОРМИРУЮТСЯ ДАННЫЕ (ВАЖНО-затем работа по этом списку без обращений к объектам)

            new_result_for_comp_dict = {}
 
        ####################    for date_day in all_days_in_period: 
        ####################        for comp_name in list_of_competitors_set:
        ####################            #print('comp_name', comp_name)
        ####################            list_valuess = []
        ####################            for object_unit in object_units:            # "ИЗБЫТОЧНО _ ПРОВЕРКА ДЛЯ ВСЕХ существующих ComparativeAnalysisTyresModel
####################
        ####################                valuess = None
        ####################                site_comp_obj_dict = {}
        ####################                for comp_obj in object_unit.price_tyre_to_compare.all().filter(site__in=filter_sites, developer__competitor_name__in=filter_producer): 
        ####################                    site_comp_obj_dict[comp_obj.site] = comp_obj.site, None, 0 
        ####################                for comp_obj in object_unit.price_tyre_to_compare.all().filter(site__in=filter_sites, developer__competitor_name__in=filter_producer):        ## !!!! 2 ФИЛЬТР ПО САЙТАМ  и КОНКУРЕНТАМ
        ####################                #for comp_obj in object_unit.price_tyre_to_compare.all().filter(site__in=filter_sites):                                           ## !!!! 2 ФИЛЬТР ПО САЙТАМ 
        ####################                #for comp_obj in object_unit.price_tyre_to_compare.all():
        ####################                    #print(comp_name, comp_obj.date_period.strftime("%d.%m.%Y"), comp_obj.price, comp_obj.site) 
        ####################                    if comp_obj in object_unit.price_tyre_to_compare.filter(developer__competitor_name=comp_name, date_period=date_day): 
        ####################                        valuess = comp_name, comp_obj.date_period.strftime("%Y-%m-%d"), comp_obj.price, comp_obj.site
        ####################                        valuess = list(valuess)
        ####################                    else:
        ####################                        valuess = comp_name, date_day.strftime("%Y-%m-%d"), None, comp_obj.site
        ####################                        valuess = list(valuess)
        ####################                    ####site_val_on_date_for_developer = None, None
        ####################                    ####if valuess[2]:
        ####################                    ####    site_val_on_date_for_developer = valuess[3], valuess[2]
        ####################                    ####    list_valuess.append(site_val_on_date_for_developer) 
        ####################                    #print('valuess', valuess)
####################
        ####################                    # формируем словри:
        ####################                    if site_comp_obj_dict.get(valuess[3]): 
        ####################                        #print('XOXOXOXOXO', site_comp_obj_dict) 
        ####################                        current_dict_val = site_comp_obj_dict.get(valuess[3])[1]
        ####################                        dict_site = site_comp_obj_dict.get(valuess[3])[0]
        ####################                        dict_devider = site_comp_obj_dict.get(valuess[3])[2]
        ####################                        if valuess[2]:
        ####################                            if current_dict_val is None:
        ####################                                current_dict_val = valuess[2]
        ####################                                #site_comp_obj_dict.get(valuess[3])[1] = current_dict_val
        ####################                                site_comp_obj_dict[valuess[3]] = dict_site, current_dict_val, dict_devider
        ####################                            else:
        ####################                                current_dict_val = valuess[2]
        ####################                                #print('current_dict_val1', current_dict_val)
        ####################                                site_comp_obj_dict[valuess[3]] = dict_site, current_dict_val, current_dict_val
        ####################                                current_devider = site_comp_obj_dict.get(valuess[3])[2]
        ####################                                #print('current_devider', current_devider)
        ####################                                current_devider += 1
        ####################                                site_comp_obj_dict[valuess[3]] = dict_site, current_dict_val, dict_devider
        ####################                    new_result_for_comp_dict[comp_name, date_day.strftime("%Y-%m-%d"), comp_obj.site] = list(site_comp_obj_dict[valuess[3]])        # словарь с скомпанованными данными
####################
        #####################print('all_days_in_period', all_days_in_period)                ## готовые параметры для подготовки списков в отрисовку
        #####################print('list_of_sites', list_of_sites)                          ## готовые параметры для подготовки списков в отрисовку
        ####################for k, v in new_result_for_comp_dict.items():     ### !!!!!!!!!!!!!!! 
        ####################    print('==',k, v)

        #for n, nv in edyniy_slovar_dict_dlja_pandas_chart_graphic.items():      
        #    for t in nv:
        ##        ss = models.CompetitorSiteModel.objects.get(id=t)
        #        print('==++==', ss.date_period, ss.developer, ss.price,  'Takim ')

        ### ###### ####### ###########

        if models.GOOGLECHART_MARKETPLACE_ON is False:      # ЕСЛИ НЕ СТОИТ ГАЛОЧКА ПО ПЛОЩАДКАМ - ФОРМИРУЕМ ГРАФИК ПО ПРОИЗВОДИТЕЛЯМ: 
            context['marketplace_on_checked'] = ''
            competit_on_current_date_assembled = []                        ###### В ДАННЫЙ СПИСОК И ФОРМИРУЮТСЯ ДАННЫЕ (ВАЖНО-затем работа по этом списку без обращений к объектам)

            new_result_for_comp_dict = {}

            prices_of_competitors_one_name_producer_dict = {}
            for date_day in all_days_in_period:                                                              
                for object_unit_id, comp_obj_ss_id in edyniy_slovar_dict_dlja_pandas_chart_graphic.items():
                    #print('object_unit_id', object_unit_id, 'comp_obj_ss_id', comp_obj_ss_id)
                    object_unit = models.ComparativeAnalysisTyresModel.objects.get(id=object_unit_id)
                    list_of_competts = models.CompetitorSiteModel.objects.filter(pk__in=comp_obj_ss_id)
                    list_of_competts_name_competitor = list_of_competts.values_list('name_competitor')
                    #print('list_of_competts_name_competitor OT', list_of_competts_name_competitor)
                    # 1. БЛОК ДОРИСОВКИ NULL (ИЛИ 0) ЗНАЧЕНИЙ В ДАТЫ ЕСЛИ ЕСТЬ ХОТЬ ОДНА ДАТА С ТАКИМ ПРОИЗВОДИТЕЛЕМ НА САЙТЕ - сохдание нулевых значений в даты, в которых не получены данные
                    
                    # ТЕКУЩЕЕ РЕШЕНИЕ = БЕРЕМ ВСЕ ЗНАЧЕНИЯ КОНКУРЕНТОВ ПРОИЗВОДИТЕЛЯ С ТАКИМ ИМЕНЕМ И ОСТАВЛЯЕИ МЕНЬШЕЕ
                    #for comp_obj in object_unit.price_tyre_to_compare.all().filter(site__in=filter_sites, developer__competitor_name__in=filter_producer):    # WARNING !!!!!!!!!!!!!!## С.Т.АРЫЙ ВАРИАНТ - РИСОВАТЬ КОНКУРЕНТОВ НА САЙТЕ ДАННОГО ПРОИЗВОДИТЕЛЯ
                    for comp_obj in object_unit.price_tyre_to_compare.all().filter(site__in=filter_sites, developer__competitor_name__in=filter_producer, name_competitor__in=list_of_competts_name_competitor):      # WARNING !!!!!!!!!!!!!!## Н.О.В.Ы.Й. ВАРИАНТ - РИСОВАТЬ КОНКУРЕНТОВ НА САЙТЕ ДАННОГО ПРОИЗВОДИТЕЛЯ ИМЕННО ДАННОЙ МОДЕЛИ
                    
                        #print('comp_obj ==', comp_obj.name_competitor)
                        for comp_name in list_of_competitors_set: 
                           
                            keys_list = comp_name, comp_obj.date_period.strftime("%Y-%m-%d"), comp_obj.site
                            default_values = comp_obj.site, 'null', comp_name                                          #### !!!! null - если нет значения
                            #default_values = comp_obj.site, 0, comp_name                                               #### !!!! null - если нет значения
                            prices_of_competitors_one_name_producer_dict.setdefault(keys_list, default_values)
                            if comp_obj.developer.competitor_name == comp_name:
                                current_val_exist = prices_of_competitors_one_name_producer_dict.get(keys_list)  # если уже существует такая позиция добавим цену в список и возьмем наименьшую для данного производителя     
                                if current_val_exist == default_values:
                                    current_val = comp_obj.price 
                                    prices_of_competitors_one_name_producer_dict[keys_list] = comp_obj.site, current_val, comp_obj.developer.competitor_name
                                else:
                                    cur_site, current_val, cur_comp_name = current_val_exist
                                    min_price = min(current_val, comp_obj.price)
                                    prices_of_competitors_one_name_producer_dict[keys_list] = cur_site, min_price, cur_comp_name
                        # 2. БЛОК ЗАЧИТСКА ОТ ИЗЛИШНЕ ДОРИСОВАННЫХ СОЗДАННЫХ В БЛОКЕ 1 ПУСТЫХ САЙТ/ПРОИЗВОДИТЕЛЬ БЕЗ ЗНАЧЕНИЙ             
            # дополнительно проверяем на наличие созданных пустышек сайт/производитель - если на всем пероде значений нет ни одного - значит, создана пустышка - ее убрать: 
            for ssitte in list_of_sites:
                for compp in list_of_competitors_set:
                    val_exist_data_is_true = True
                    dict_indexes_of_keys_with_no_data_id_list = []
                    for date_day in all_days_in_period:
                        kkey = compp, date_day.strftime("%Y-%m-%d"), ssitte
                        got_value = prices_of_competitors_one_name_producer_dict.get(kkey)
                        if got_value:
                            if got_value[1] != 'null': # если есть хоть одно значение - значит создан не пустой клон сайт/производитель , а реальный - закончить проверку данного производиттеля на сайте
                                dict_indexes_of_keys_with_no_data_id_list = []
                                break
                            else:   
                                dict_indexes_of_keys_with_no_data_id_list.append(kkey)
                                #print(kkey, 'got_value', got_value)
                                val_exist_data_is_true = False

                    #print(dict_indexes_of_keys_with_no_data_id_list, len(dict_indexes_of_keys_with_no_data_id_list))            
                    if val_exist_data_is_true == False:
                        # удаляем созданные пустышки:
                        for kkey in dict_indexes_of_keys_with_no_data_id_list:
                            prices_of_competitors_one_name_producer_dict.pop(kkey)
                    #print('=======')
               
        new_result_for_comp_dict = prices_of_competitors_one_name_producer_dict  

        #for n, nv in prices_of_competitors_one_name_producer_dict.items():      # == приводим в неулюжий вид такого типа: ('WestLake', '2023-08-05', 'bagoria.by') ['bagoria.by', 188.48, 0]
        #    print(n, '==++==', nv, 'Takim neschasnym')
            ### ###### ####### ############  
                   
        # 3. БЛОК + ДОПОЛНИТЕЛЬНАЯ ДОРИСОВКА ДАННЫХ УЖЕ НА ВЕСЬ ПЕРИОД _ ЧТОБЫ ПЕРЕДАТЬ В ТЕМПЛАЙТ ОДИНАКОВОЕ ЧИСЛО ДАННЫХ ПО КАЖДОМУ ПРОИЗВОДИТЕЛЮ НА САЙТАХ 
        ############ !!!! ПРОВЕРКА ДОСТАВЛЕНИЕ ДАННЫХ                   Д.О.Р.И.С.О.В.К.А.  Д.А.Н.Н.Ы.Х   WARNING!!!!
        # 1) дата с наибольшим количеством данных
        list_of_inputed_dates = [] 
        list_of_inputed_dates_set = set()
        list_of_inputed_producers = []
        list_of_inputed_producers_set = set()
        list_of_inputed_sites = []
        list_of_inputed_sites_set = set()
        for kkkeyy in prices_of_competitors_one_name_producer_dict.keys(): 
            if kkkeyy[1] in list_of_inputed_dates:
                pass   
            else:
                list_of_inputed_dates.append(kkkeyy[1])
            list_of_inputed_producers.append(kkkeyy[0])
            list_of_inputed_sites.append(kkkeyy[2]) 
        list_of_inputed_dates_set = list_of_inputed_dates
        #print('list_of_inputed_dates_set!', list_of_inputed_dates_set)                                     # list_of_inputed_dates_set!
        list_of_inputed_producers_set = set(list_of_inputed_producers)
        list_of_inputed_sites_set = set(list_of_inputed_sites)
        #print('list_of_inputed_dates_set', list_of_inputed_dates_set)
        #print('list_of_inputed_producers_set', list_of_inputed_producers_set)
        #print('list_of_inputed_sites_set', list_of_inputed_sites_set)
        list_of_existing_prod_in_sites = []     # проверка - был ли производитель на сайте/ на одном- нескольких
        for kkkeeeyy in prices_of_competitors_one_name_producer_dict:
            ppproodducer, sssiitttteee = kkkeeeyy[0], kkkeeeyy[2]
            pr_si = ppproodducer, sssiitttteee
            list_of_existing_prod_in_sites.append(pr_si)
        list_of_existing_prod_in_sites = list(set(list_of_existing_prod_in_sites))

        ##
        list_of_inputed_dates_set_sorted = []     # 1) додабвление (достраивание данных из соседних - из предыдущего дня) если в какое то число не спарсено
        for str_data in list_of_inputed_dates_set:
            some_data = datetime.datetime.strptime(str_data, '%Y-%m-%d').date()
            list_of_inputed_dates_set_sorted.append(some_data)
        #mmmin = min(list_of_inputed_dates_set_sorted)
        #mmmax = max(list_of_inputed_dates_set_sorted)
        
        try:
            if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                from_iser_start_date = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], '%Y-%m-%d').date()
                mmmin = from_iser_start_date
            else:
                mmmin = min(all_days_in_period)                                 ## возьмем отсчет из древнейшей даты в базе вообще НЕОЧЕВИДНОЕ
                mmmax = max(all_days_in_period)
            if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                from_iser_end_date = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], '%Y-%m-%d').date()
                mmmax = from_iser_end_date
            else:
                mmmin = min(all_days_in_period)                                 ## возьмем отсчет из древнейшей даты в базе вообще НЕОЧЕВИДНОЕ
                mmmax = max(all_days_in_period)
        except:
            mmmin = datetime.datetime.today()
            mmmax = datetime.datetime.today()
        datelist_d_pandas_range = pd.date_range(mmmin, mmmax)
        list_of_dates_with_no_exceptions = []
        for ddatta in datelist_d_pandas_range:
            str_date = ddatta.strftime('%Y-%m-%d')
            list_of_dates_with_no_exceptions.append(str_date)
        ##    
        list_of_inputed_dates_set = list_of_dates_with_no_exceptions            # теперь список дат без выпадающих дат
        #print('list_of_inputed_dates_set', list_of_inputed_dates_set)

        prices_of_competitors_one_name_producer_dict_temporary_with_missing_data = {}
        for date_iz_spiska in list_of_inputed_dates_set:                                        # 2) додабвление 0 в другие дни если нет  данных, но в какое то число хоть раз был конкурент на данном сайте
            for producer_iz_spiska in list_of_inputed_producers_set:
                for site_iz_spiska in list_of_inputed_sites_set:
                    prod_in_site_existed_check = producer_iz_spiska, site_iz_spiska
                    if prod_in_site_existed_check in list_of_existing_prod_in_sites:            # если производитель и сайтодновременно есть в списке(т.е. производитель именно был хоть в какую то дату взят с данного сайта)
                        what_to_look = producer_iz_spiska, date_iz_spiska, site_iz_spiska
                        #print(date_iz_spiska, type(date_iz_spiska), '||', prod_in_site_existed_check)
                        get_data = prices_of_competitors_one_name_producer_dict.get(what_to_look)
                        #print(date_iz_spiska,  '||', prod_in_site_existed_check,   '|==|',  get_data)
                        if get_data:
                            #print(date_iz_spiska,  '||', prod_in_site_existed_check,   '|==|',  get_data)
                            prices_of_competitors_one_name_producer_dict_temporary_with_missing_data[producer_iz_spiska, date_iz_spiska, site_iz_spiska] = get_data
                        else:
                            null_data = site_iz_spiska, 'null', producer_iz_spiska                              ##### !!!! null - если нет значения
                            #null_data = site_iz_spiska, 0, producer_iz_spiska                                  ##### !!!! 0 - если нет значения                        
                            prices_of_competitors_one_name_producer_dict_temporary_with_missing_data[producer_iz_spiska, date_iz_spiska, site_iz_spiska] = null_data 

        # подменяем исходный словарик на словарик с доставленными нулевыми  значениями:
        new_result_for_comp_dict = prices_of_competitors_one_name_producer_dict_temporary_with_missing_data


            ##### УДАЛЕНИЕ ДУБЛЯЖЕЙ_ПРИЗРАКОВ на параллельных сайтах С NULL НА ВСЕМ ОТРЕЗКЕ:
    ##    try:    
        sites_titles_list = []       # список сайтов для проверки
        producer_titles_list = []
        for hhh, oooo in new_result_for_comp_dict.items():
        #    print('hhh, oooo ', hhh, '||', hhh[0], hhh[2], '||', oooo, '||', oooo[1] )
            sites_titles_list.append(hhh[2]), producer_titles_list.append(hhh[0])
        sites_titles_list = list(set(sites_titles_list))
        producer_titles_list = list(set(producer_titles_list))
        #print('sites_titles_list', sites_titles_list, 'producer_titles_list', producer_titles_list)
        # посчитать количество (длину) в словаре:
        some_counter = 0
        one_site_name = None
        one_vrand_name = None 
        if producer_titles_list and sites_titles_list: 
            one_site_name = sites_titles_list[0]     
            one_vrand_name = producer_titles_list[0]  
            for key in new_result_for_comp_dict.keys():
                if key[0] == one_vrand_name and key[2] == one_site_name:
                    #print('OPOPOPO', key)
                    some_counter += 1
    #    print('some_counter is', some_counter)
        #end  посчитать количество (длину) в словаре:           
        # ищем призраки:
        ghost_comp_site_with_only_null_to_delete_from_dict = []     #! список кортежей (Бренд, Сайт) с одними null для удаления как призрак
        for producer_title in producer_titles_list:  
            for sites_title in sites_titles_list:
                null_counter = 0    # расчет количества нулевых значений у сайт-производителя в словаре
                potential_to_delete = []        #набиваем нулевыми данного производителя на данном сайте - если их количество равно длине всего периода (some_counter is) - помечаем их на удаление внося в ghost_comp_site_with_only_null_to_delete_from_dict
                for key, val in new_result_for_comp_dict.items():   
                    if key[0] == producer_title and key[2] == sites_title:   
                        if val[1] == 'null':
                            null_counter += 1
                            potential_to_delete.append(key)
                        #    print('null_counter', null_counter, '-----', 'val[1]', val[1], key[0], key[2])
                        if null_counter == some_counter:      # если количество null значений у всех позиций сайт-производителя в словаре - он пустой призрак
                        #    print('777')
                            #ghost_comp_site_with_only_null_to_delete_from_dict.append((key[0], key[2])) # Cordiant bagoria.by
                            ghost_comp_site_with_only_null_to_delete_from_dict.extend(potential_to_delete) 
                #print('=================')
        #END ищем призраки
    #    for key, val in new_result_for_comp_dict.items():
    #        print('ASS', key, val)
        #for bbrand_ghost_site_ghost in ghost_comp_site_with_only_null_to_delete_from_dict:
        #    print('JOPA', bbrand_ghost_site_ghost)

        # удаление призраков из словаря (пересоздание словаря):
        new_result_for_comp_dict_temporary_keys_to_delete_list = []
        for key, val in new_result_for_comp_dict.items():
            for bbrand_ghost_site_ghost in ghost_comp_site_with_only_null_to_delete_from_dict: 
                #if key[0] == bbrand_ghost_site_ghost[0] and key[2] == bbrand_ghost_site_ghost[1]:
                if key == bbrand_ghost_site_ghost:
                #    print('key[0]', key[0], 'bbrand_ghost_site_ghost[0]', bbrand_ghost_site_ghost[0], 'key[2]', key[2], 'bbrand_ghost_site_ghost[1]', bbrand_ghost_site_ghost[1])
                #    print('key', key, 'val', val)
                    #print("ШОККОНТЕНТ")
                    new_result_for_comp_dict_temporary_keys_to_delete_list.append(key)
        for key_to_delete in new_result_for_comp_dict_temporary_keys_to_delete_list:
            new_result_for_comp_dict.pop(key_to_delete)
        #print('УДАЧА, ИСПААААНЦЫ! ==================================================')
    #    for a, b in new_result_for_comp_dict.items():
    #        print('==', a, b)
        #END удаление призраков из словаря:
    ##    except:
    ##        pass
                   
            ##### END УДАЛЕНИЕ ДУБЛЯЖЕЙ_ПРИЗРАКОВ на параллельных сайтах С NULL НА ВСЕМ ОТРЕЗКЕ:

    
        ############ END !!!! ПРОВЕРКА ДОСТАВЛЕНИЕ ДАННЫХ 

        #print('all_days_in_period', all_days_in_period)

        if models.WEIGHTED_AVERAGE_ON == False:                             # ЕСЛИ НЕ НУЖНО ВЫВОДИТЬ СРЕДНЕВЗВЕШЕННОЕ
            context['weighted_average_checked'] = ''
            list_for_formating = []
            position_couner = None          # понадобится для определени номера позиции с значением цены в словаре для заполнения пустых None в дальнейшем  
            for ddate in all_days_in_period:
            #    print('==========', ddate)
                small_list_for_formating = []
                for k, v in new_result_for_comp_dict.items():     ### !!!!!!              
                    if ddate.strftime("%Y-%m-%d") == k[1]:
                        #if v[1]:
                        put_data = k[0], k[1], v[1], v[0]             # [['JONWICK', '2023-04-05', None,  # 'onliner.by']   ['SAMURAI', '2023-04-19', 750.0, # 'kolesa-darom.ru']]
                        put_data = list(put_data)
                        position_couner = put_data.index(v[1])
                        small_list_for_formating.append(put_data)
            #    print('=======', small_list_for_formating)
                list_for_formating.append(small_list_for_formating)
            ##print('list_for_formating1', list_for_formating)
        else:                             # ЕСЛИ НУЖНО ВЫВОДИТЬ СРЕДНЕВЗВЕШЕННОЕ
            context['weighted_average_checked'] = 'checked'
            list_for_formating = []
            position_couner = None          ## понадобится для определени номера позиции с значением цены в словаре для заполнения пустых None в дальнейшем     
            for ddate in all_days_in_period: 
                small_list_for_formating = []    
                for compet in list_of_competitors_set:                 # УСРЕДНЕННОЕ ПО ПРОИЗВОДИТЕЛЮ !!!!!!!!!!!!!!!!!!!  
                    #print('MENTOR!')    
                    devvider = 0                                           # УСРЕДНЕННОЕ ПО ПРОИЗВОДИТЕЛЮ !!!!!!!!!!!!!!!!!!!   
                    weighted_average_val = 0                               # УСРЕДНЕННОЕ ПО ПРОИЗВОДИТЕЛЮ !!!!!!!!!!!!!!!!!!
                    list_of_sites = []
                    for k, v in new_result_for_comp_dict.items():     ### !!!!!!          
                        if ddate.strftime("%Y-%m-%d") == k[1] and compet == k[0]:
                            devvider += 1 
                            #print('v[1]', v[1], 'VZO', v, 'KTO', k)
                            perman_val = 0
                            if v[1] is None or v[1] == 'null':
                               perman_val = 0 
                            else:
                                perman_val = v[1]
                            #print('weighted_average_val', weighted_average_val, 'devvider', devvider)
                            list_of_sites.append(v[0])
                            weighted_average_val += perman_val
                            put_data = k[0], k[1], weighted_average_val, f'средневзвешенная по сайтам: {list_of_sites}'            # [['JONWICK', '2023-04-05', None,  # 'onliner.by']   ['SAMURAI', '2023-04-19', 750.0, # 'kolesa-darom.ru']]
                            put_data = list(put_data)
                            #########print('put_data', put_data)
                            position_couner = put_data.index(weighted_average_val)
                    ##print ('put_data', put_data, 'devvider:', devvider)
                    if put_data[position_couner] and devvider:
                        put_data[position_couner] = put_data[position_couner] / devvider
                    else:
                        put_data[position_couner] = None
                    #print ('put_data', put_data, 'devvider:', devvider) 
                    small_list_for_formating.append(put_data)   
                #print('=======', small_list_for_formating)
                list_for_formating.append(small_list_for_formating)
            #print('list_for_formating2!', list_for_formating)

        ### ЕСЛИ НУЖНО ВЫВОДИТЬ ГРФАИК С ДОРИСОВАННЫМИ ЛИНИЯМИ :
        if models.FULL_LINED_CHART_ON == False:  
            context['full_lined_chart_checked'] = '' 
        else: 
            context['full_lined_chart_checked'] = 'checked' 
            context['full_lined_chart_checked_flag'] = 'true'
        ### END ЕСЛИ НУЖНО ВЫВОДИТЬ ГРФАИК С ДОРИСОВАННЫМИ ЛИНИЯМИ

        competit_on_current_date_assembled = list_for_formating ### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   
        #for n in competit_on_current_date_assembled:
        #    print('fall behind====', n)   

        ## т.к. list_for_formating и затем competit_on_current_date_assembled - создает пустые дубляжи производителя для каждого сайта ( например,['Кама', '2023-08-02', None, 'onliner.by'], ['Кама', '2023-08-02', None, 'bagoria.by'])
        ## исключим те дубляжи , по которым созданы на иных сайтах копии
        #print('!!!', list_for_formating)

        # ЕСЛИ ЗНАЧЕНИЕ + NONE - ПОИСК ДАННЫХ В ДАТАХ РАНЬШЕ И ПРИРАВНИВАНИЕ К НИМ:
        complided_data_len = 0  # проверка все ли части равны
        complided_data_len_el = None
        if competit_on_current_date_assembled:
            complided_data_len = len(competit_on_current_date_assembled[0])  
            #complided_data_len_el = len(competit_on_current_date_assembled[0][0]) - 1 
            #print('complided_data_len', complided_data_len)             # количество списков на дату
        all_parts_are_equal = False      
        for complided_data in competit_on_current_date_assembled:
            complided_data_len_got = len(complided_data)
            if complided_data_len_got == complided_data_len:
                all_parts_are_equal = True

        #competit_on_current_date_assembled = list(reversed(competit_on_current_date_assembled))       # развернуть список чтобы начинать с последней даты

        #print('len(competit_on_current_date_assembled)', len(competit_on_current_date_assembled))
        #print('competit_on_current_date_assembled', competit_on_current_date_assembled) #
        whole_list_legh = len(competit_on_current_date_assembled)
        if position_couner:
            for perr_val in competit_on_current_date_assembled:
                #print('perr_val', perr_val)                                                    #[['JONWICK', '2023-03-20', None, 'onliner.by'], ['JONWICK', '2023-03-20', None, 'kolesa-darom.ru'], ['SAMURAI', '2023-03-20', None, 'onliner.by'], ['SAMURAI', '2023-03-20', None, 'kolesa-darom.ru']]
                curr_perr_val_index = competit_on_current_date_assembled.index(perr_val)        #curr_perr_val_index 0
                #print('curr_perr_val_index',curr_perr_val_index)
                for ell in perr_val:
                    #print('ell', ell)                                                          # ell ['SAMURAI', '2023-04-20', 150.0, 'onliner.by']
                    curr_ell_val_index = perr_val.index(ell)                                    # curr_ell_val_index 3              
                    val = ell[position_couner]
                    #print('val===', val)
                    #curr_val_index = ell.index(val)                                            #здесь индекс и так нам известен = он всегда равен значению position_couner
                    if val is None:                                                             # если значение  None, поиск в впредыдущих позициях дат этого производителя
                    #    print('curr_perr_val_index!!!!',curr_perr_val_index)
                        curr_perr_val_index_none = curr_perr_val_index
                        while curr_perr_val_index_none < whole_list_legh:                           
                            get_prev_val = competit_on_current_date_assembled[curr_perr_val_index_none][curr_ell_val_index][position_couner]
                            curr_perr_val_index_none += 1
                            #print('get_prev_val', get_prev_val, 'curr_ell_val_index', curr_ell_val_index)
                            if get_prev_val:
                                val = get_prev_val
                                break
                        if val is None:     # если не найдены значения в других периодах
                        #    val = 0
                            val = 'null'
                        competit_on_current_date_assembled[curr_perr_val_index][curr_ell_val_index][position_couner] = val
                #print('perr_val', perr_val)
                

                
    #    # END ЕСЛИ ЗНАЧЕНИЕ + NONE - ПОИСК ДАННЫХ В ДАТАХ РАНЬШЕ И ПРИРАВНИВАНИЕ К НИМ                  
        #for n in competit_on_current_date_assembled:
        #    print('fall behind', n)     

        # СОБИРЕМ СЛОВАРИ ДЛЯ ПЕРЕЧАЧИ В КОНТНЕКСТ, ДАЛЕЕ В СКРИПТ:
        assembles_to_dict_data_dict = {}
        assembles_to_dict_data_dict['competitor_producer_names'] = {}
        assembles_to_dict_data_dict['dates'] = {}
        assembles_to_dict_data_dict['competitor_values'] = {}
        list_of_dates = []
        for lists_values in competit_on_current_date_assembled:
        #    print('!', lists_values,'LENGTH = ', len(lists_values))    #! [('Cordiant', None, None), ('LingLong', None, None), ('iLink', None, None), ('Michelin', '20.03.2023', 351.1), ('Arivo', None, None)] LENGTH =  
            list_of_competitor_producer_names = []
            for vall in lists_values:
                #print('vall ', vall)
                if vall[3]:                                             # если указываются данные о сайте и производителе
                    comb_name = vall[0], ' ', vall[3] 
                    comb_name = ''.join(comb_name)
                    #print('comb_name', comb_name)
                    list_of_competitor_producer_names.append(comb_name)
                else:
                    list_of_competitor_producer_names.append(vall[0])  
                #list_of_competitor_producer_names.append(vall[0])    
            for vall in lists_values:
                list_of_dates.append(vall[1])
                break
            #print(list_of_dates)
            assembles_to_dict_data_dict['competitor_producer_names'] = list_of_competitor_producer_names
            assembles_to_dict_data_dict['dates'] = list_of_dates
        

        #print('competit_on_current_date_assembled 999', competit_on_current_date_assembled)    
        list_of_competitor_values = []
        list_of_competitor_values_new_dict = {}

        if no_data_on_date is True:     # если отсутствуют данные типоразмеры с конкурентами
            #print('kogda mne temno gromko gruppu KINO', all_days_in_period)
            for date_in in all_days_in_period:
                year, month, day = int(date_in.strftime('%Y')), int(date_in.strftime('%m')), int(date_in.strftime('%d'))
                date_prepared_or_js = year, month-1, day   # СДВИГ -1 ДЛЯ ОТОБРАЖЕНИЯ В ГРАФИКЕ     #  
                list_of_competitor_values_new_dict[date_prepared_or_js] = ['null']

            context['competitor_names'] = ['']
            context['competitor_values'] = ['']

        else:
            chart_data_counter = 0                                              # подмешиваем дату строкой как  # [1,  37.8, 80.8, 41.8], -
            if assembles_to_dict_data_dict['dates']:
                number_of_periods = len(assembles_to_dict_data_dict['dates'])                         # old =number_of_periods== 5 ['20.03.2023', '20.03.2023', '20.03.2023', '20.03.2023', '20.03.2023']       
                #print('number_of_periods==', number_of_periods, assembles_to_dict_data_dict['dates'])      
                for lists_values in competit_on_current_date_assembled:
                    #print('chart_data_counter', chart_data_counter, assembles_to_dict_data_dict['dates'][chart_data_counter], '==', lists_values)
                    list_of_period_competitor_values = [] 
                #    print('::::::::', 'chart_data_counter:', chart_data_counter, '  ', assembles_to_dict_data_dict['dates'])
                    list_of_period_competitor_values.append(assembles_to_dict_data_dict['dates'][chart_data_counter])
                    list_of_period_competitor_values_new = [] 
                    date_in_str = datetime.datetime.strptime(assembles_to_dict_data_dict['dates'][chart_data_counter], '%Y-%m-%d').date()
                    year, month, day = int(date_in_str.strftime('%Y')), int(date_in_str.strftime('%m')), int(date_in_str.strftime('%d'))
                    date_prepared_or_js = year, month-1, day        # СДВИГ -1 ДЛЯ ОТОБРАЖЕНИЯ В ГРАФИКЕ     #                   
                    list_of_period_competitor_values_new.append(date_prepared_or_js)
                    if chart_data_counter < number_of_periods-1:
                        chart_data_counter += 1
                    for vall in lists_values:
                        list_of_period_competitor_values.append(vall[2])
                        list_of_period_competitor_values_new.append(vall[2])
                    #per_val = list_of_period_competitor_values[ 1 :]   
                    list_of_competitor_values.append(list_of_period_competitor_values)
                    #print('list_of_period_competitor_values_new', list_of_period_competitor_values_new)

                    list_to_tuple = list_of_period_competitor_values_new[1:]
                    list_of_competitor_values_new_dict[list_of_period_competitor_values_new[0]] = list_to_tuple

            assembles_to_dict_data_dict['competitor_values'] = list(list_of_competitor_values) 

    #        print('!  ', assembles_to_dict_data_dict['competitor_producer_names'])
            if not assembles_to_dict_data_dict['competitor_producer_names']:
                context['competitor_names'] = ['нет данных']
            else:
                context['competitor_names'] = assembles_to_dict_data_dict['competitor_producer_names']
    #            print('GGGOOODDD 1', context['competitor_names'])
            
            if not assembles_to_dict_data_dict['competitor_values']:
    #            print('EERR 1')
                context['competitor_values'] = [[' ', 'null']]
            else:
                context['competitor_values'] = assembles_to_dict_data_dict['competitor_values']
    #            print('GGGOOODDD 2', context['competitor_values'])

    #        print('context[competitor_values]', context['competitor_values'])
            #for bbb in assembles_to_dict_data_dict['competitor_values']:
            #    print('LEN GRAPHIC VAL', bbb)
            #print('context[competitor_values] ++--+-+-+-', assembles_to_dict_data_dict['competitor_values'], len(assembles_to_dict_data_dict['competitor_values']))

        
        ##### ПРОВЕРКА ЦЕЛОСТНОСТИ СПИСКОВ - ЕСЛИ ЕСТЬ ПРОПУСКИ - ДОРИСОВАТЬ:
        #for vvall in list_of_competitor_values_new_dict.values():
        #    print('vvall', vvall, len(list_of_competitor_values_new_dict.values()))
        #
        ##### END ПРОВЕРКА ЦЕЛОСТНОСТИ СПИСКОВ - ЕСЛИ ЕСТЬ ПРОПУСКИ - ДОРИСОВАТЬ
            


        if not list_of_competitor_values_new_dict:
    #        print('END 0 ===== list_of_competitor_values_new_dict', list_of_competitor_values_new_dict)
            context['list_of_competitor_values_new'] = {(' '): ['null']}
        else:            
            context['list_of_competitor_values_new'] = list_of_competitor_values_new_dict  
    #        print('GGGOOODDD 3', context['list_of_competitor_values_new'])

        #for n, k in context['list_of_competitor_values_new'].items():
        ###    #print('N',type(n), n[0], n[1:])
        #    print('DD', n, k, type(n)) # n[0], n[1])
        

        #print('context [competitor_names]', context['competitor_names'])
        #print('context[competitor_values]', context['competitor_values'])
        ###frame = pd.DataFrame(assembles_to_dict_data_dict)

        #### END  ТЕСТОВАЯ ШТУКА ДЛЯ ГРАФИКОВ PANDAS
        
        #### КРУГОВОЙ ГРАФИК КОЛИЧЕСТВО СПАРСЕННЫХ ДАННЫХ С САЙТА: PANDAS
        final_parsed_data_from_sites = []
        parsed_data_from_sites = ['Сайт', 'Количество спарсенных конкурентов']
        final_parsed_data_from_sites.append(parsed_data_from_sites)
        filter_sites = ['onliner.by', 'bagoria.by', 'autoset.by']
        final_parsed_data_from_sites_whole = 0
        date_to_look_parsed_data = datetime.datetime.now().date()
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
            date_to_look_parsed_data = models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0]
            date_to_look_parsed_data = datetime.datetime.strptime(date_to_look_parsed_data, '%Y-%m-%d').date()

        for sitess in filter_sites:
            get_data_from_site_number = len(models.CompetitorSiteModel.objects.filter(date_period=date_to_look_parsed_data).filter(site=sitess))  # .filter(site__in=filter_sites))
            final_parsed_data_from_sites_whole = final_parsed_data_from_sites_whole + get_data_from_site_number
            to_put_in_list_data = sitess, get_data_from_site_number
            to_put_in_list_data = list(to_put_in_list_data)
            final_parsed_data_from_sites.append(to_put_in_list_data)
            #print('final_parsed_data_from_sites_whole', final_parsed_data_from_sites_whole)
            
        date_to_look_parsed_data = date_to_look_parsed_data.strftime('%d.%m.%Y')
        context['final_parsed_data_from_sites_whole'] = final_parsed_data_from_sites_whole   
        context['final_parsed_data_from_sites'] = final_parsed_data_from_sites
        context['final_parsed_data_from_sites_data'] = date_to_look_parsed_data
        #### END  КРУГОВОЙ ГРАФИК КОЛИЧЕСТВО СПАРСЕННЫХ ДАННЫХ С САЙТА: PANDAS

        #### ГРАФИК КОЛИЧЕСТВО СПАРСЕННЫХ ДАННЫХ ПО БРЕНДУ С САЙТОВ: PANDAS
        all_parsed_brands_developers_queryset = dictionaries_models.CompetitorModel.objects.order_by('competitor_name').values_list('competitor_name', flat=True).distinct()        ### Фильтр уникальных!
        date_to_look_parsed_data = datetime.datetime.now().date()
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
            date_to_look_parsed_data = models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0]
            date_to_look_parsed_data = datetime.datetime.strptime(date_to_look_parsed_data, '%Y-%m-%d').date()
        list_of_parrsed_brands_sites = []
        quantity_counter = 0
        for brand in all_parsed_brands_developers_queryset: 
            num_of_parsed_brand_onliner = models.CompetitorSiteModel.objects.filter(developer__competitor_name=brand, date_period=date_to_look_parsed_data, site='onliner.by').count()
            num_of_parsed_brand_bagoria = models.CompetitorSiteModel.objects.filter(developer__competitor_name=brand, date_period=date_to_look_parsed_data, site='bagoria.by').count()
            num_of_parsed_brand_autoset = models.CompetitorSiteModel.objects.filter(developer__competitor_name=brand, date_period=date_to_look_parsed_data, site='autoset.by').count()

            total_quantity = num_of_parsed_brand_onliner + num_of_parsed_brand_bagoria + num_of_parsed_brand_autoset        # для сортировки по наибольшему кол-ву спарсенных с сайтов

            brand_quantity_per_site = brand, num_of_parsed_brand_onliner, num_of_parsed_brand_bagoria, num_of_parsed_brand_autoset, total_quantity 
            list_of_parrsed_brands_sites.append(list(brand_quantity_per_site))
            quantity_counter += 1
        list_of_parrsed_brands_sites = sorted(list_of_parrsed_brands_sites, key=itemgetter(4), reverse=True) # сортируем по наиб количеству спарсенных

        top_brands_counter_for_chart = 0
        if quantity_counter == 10 or quantity_counter > 10:               # ели брендов более 10 - то берем то 10
            top_brands_counter_for_chart = 10
        elif quantity_counter < 10 and quantity_counter > 0:
            top_brands_counter_for_chart = quantity_counter
        else:
            top_brands_counter_for_chart = 'лист без данных'
        context['top_brands_num'] = top_brands_counter_for_chart

        date_to_look_parsed_data = date_to_look_parsed_data.strftime('%d.%m.%Y')
        context['brands_from_sites_date'] = date_to_look_parsed_data
        ###for n in list_of_parrsed_brands_sites:
        ###    n.insert(5, numeration_index)
        ###    numeration_index += 1
        #list_of_parrsed_brands_sites = ','.join(str(x) for x in list_of_parrsed_brands_sites) # !!!!!!! ДРУГОЙ ВАРИАНТ ПЕРЕДАЧИ ДАННЫХ
        list_of_parrsed_brands_sites = ','.join(str(x[0:4]) for x in list_of_parrsed_brands_sites) # !!!!!!! ДРУГОЙ ВАРИАНТ ПЕРЕДАЧИ ДАННЫХ
        #print('!!!', list_of_parrsed_brands_sites)
        context['brands_from_sites'] = list_of_parrsed_brands_sites

        #### END ГРАФИК КОЛИЧЕСТВО СПАРСЕННЫХ ДАННЫХ ПО БРЕНДУ С САЙТОВ: PANDAS


        #### ГРАФИК КОЛИЧЕСТВО СПАРСЕННЫХ ДАННЫХ ПО ТИПОРАЗМЕРУ С САЙТОВ: PANDAS
    #    all_parsed_tyresizes_developers_queryset = dictionaries_models.TyreSizeModel.objects.order_by('tyre_size').values_list('tyre_size', flat=True).distinct()        ### Фильтр уникальных!
        all_parsed_tyresizes_developers_queryset = models.CompetitorSiteModel.objects.order_by('tyresize_competitor').values_list('tyresize_competitor', flat=True).distinct()        ### Фильтр уникальных!
        date_to_look_parsed_data = datetime.datetime.now().date()
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
            date_to_look_parsed_data = models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0]
            date_to_look_parsed_data = datetime.datetime.strptime(date_to_look_parsed_data, '%Y-%m-%d').date()
        list_of_parrsed_tyresize_sites = []
        quantity_counter = 0
        for ttyyrr_sizze in all_parsed_tyresizes_developers_queryset: 
            num_of_parsed_tyresize_onliner = models.CompetitorSiteModel.objects.filter(tyresize_competitor=ttyyrr_sizze, date_period=date_to_look_parsed_data, site='onliner.by').count()
            num_of_parsed_tyresize_bagoria = models.CompetitorSiteModel.objects.filter(tyresize_competitor=ttyyrr_sizze, date_period=date_to_look_parsed_data, site='bagoria.by').count()
            num_of_parsed_tyresize_autoset = models.CompetitorSiteModel.objects.filter(tyresize_competitor=ttyyrr_sizze, date_period=date_to_look_parsed_data, site='autoset.by').count()

            total_quantity = num_of_parsed_tyresize_onliner + num_of_parsed_tyresize_bagoria + num_of_parsed_tyresize_autoset        # для сортировки по наибольшему кол-ву спарсенных с сайтов

            tyresize_quantity_per_site = ttyyrr_sizze, num_of_parsed_tyresize_onliner, num_of_parsed_tyresize_bagoria, num_of_parsed_tyresize_autoset, total_quantity 
            list_of_parrsed_tyresize_sites.append(list(tyresize_quantity_per_site))
            quantity_counter += 1
        list_of_parrsed_tyresize_sites = sorted(list_of_parrsed_tyresize_sites, key=itemgetter(4), reverse=True) # сортируем по наиб количеству спарсенных

        top_tyresizes_counter_for_chart = 0
        if quantity_counter == 10 or quantity_counter > 10:               # ели типоразмеров более 10 - то берем то 10
            top_tyresizes_counter_for_chartt = 10
        elif quantity_counter < 10 and quantity_counter > 0:
            top_tyresizes_counter_for_chart = quantity_counter
        else:
            top_tyresizes_counter_for_chart = 'лист без данных'
        context['top_tyresizes_num'] = top_tyresizes_counter_for_chart

        date_to_look_parsed_data = date_to_look_parsed_data.strftime('%d.%m.%Y')
        context['tyresizes_from_sites_date'] = date_to_look_parsed_data
        list_of_parrsed_tyresize_sites = ','.join(str(x[0:4]) for x in list_of_parrsed_tyresize_sites) # !!!!!!! ДРУГОЙ ВАРИАНТ ПЕРЕДАЧИ ДАННЫХ
        context['tyresizes_from_sites'] = list_of_parrsed_tyresize_sites

        #### END ГРАФИК КОЛИЧЕСТВО СПАРСЕННЫХ ДАННЫХ ПО ТИПОРАЗМЕРУ  С САЙТОВ: PANDAS

        return context
class ComparativeAnalysisTableModelUpdateView(View):

    def post(self, request):

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
        models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START = []

        ### СБРОС СЛОВАРЕЙ
        models.ONLINER_COMPETITORS_NAMES_FILTER_IDS = {}
        models.AVTOSET_COMPETITORS_NAMES_FILTER_IDS = {}
        models.BAGORIA_COMPETITORS_NAMES_FILTER_IDS = {}
        ### END СБРОС СЛОВАРЕЙ


    #    print(request.POST, 'TTTH')
    #    print (request.POST.getlist('competitors'), 'TTTT')

        ## 1 работа с периодами:
        comparative_model_parcing_date = request.POST.getlist('parcing_date') 
        #print('comparative_model_parcing_date', comparative_model_parcing_date , type(comparative_model_parcing_date))

        if comparative_model_parcing_date and comparative_model_parcing_date != ['']:
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER = comparative_model_parcing_date
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_IS_NOT_CHOSEN = False


        comparative_model_parcing_date_start = request.POST.getlist('parcing_date_start') 
        if comparative_model_parcing_date_start and comparative_model_parcing_date_start != ['']:
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START = comparative_model_parcing_date_start
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START_IS_NOT_CHOSEN = False


        if comparative_model_parcing_date == [''] and comparative_model_parcing_date_start == ['']:
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER = [datetime.date.today().strftime('%Y-%m-%d')]      # автоматически ставит дату на сегодня
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_IS_NOT_CHOSEN = True
            
            today_is = datetime.date.today()                                                                # автоматически ставит дату на неделю назад
            week_ago_date = today_is - datetime.timedelta(days=7)
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START = [week_ago_date.strftime('%Y-%m-%d')]
            #print('models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START', models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START)
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START_IS_NOT_CHOSEN = True

        #### 1.1 ПЕРИОД ДЛЯ КУРСА ВАЛЮТ:
        chosen_date_for_currency_year = request.POST.getlist('chosen_date_for_currency_year') 
        chosen_date_for_currency_month = request.POST.getlist('chosen_date_for_currency_month') 
        chosen_date_for_currency_day = request.POST.getlist('chosen_date_for_currency_day') 
        chosen_date_for_currency = chosen_date_for_currency_year + chosen_date_for_currency_month + chosen_date_for_currency_day
        if chosen_date_for_currency:
            #print('chosen_date_for_currency1', chosen_date_for_currency)  
            chosen_date_for_currency = '-'.join(str(x) for x in chosen_date_for_currency)
        #    print('chosen_date_for_currency', chosen_date_for_currency)             # 'parcing_date': ['2023-03-14'],  chosen_date_for_currency 2022-1-30
            check_date = datetime.datetime.strptime(chosen_date_for_currency, "%Y-%m-%d").date()        #  если пользователем введена дана превышающая текущую для получения курса валют то нао скинуть на сегодня:
            if check_date > datetime.datetime.now().date():
                pass
            else:
                models.CURRENCY_DATE_GOT_FROM_USER = chosen_date_for_currency
                models.CURRENCY_ON_DATE is True
#
        # 2-й работа с группами шин:
        tyre_groups_list_all = request.POST.getlist('self_production_group_id_all')
        tyre_groups_list = request.POST.getlist('self_production_group_id')
        if tyre_groups_list_all:
            #print(tyre_groups_list_all, 'tyre_groups_list_all')
            models.TYRE_GROUPS_ALL= tyre_groups_list_all
        else:
            #print(tyre_groups_list, 'tyre_groups_list')
            models.TYRE_GROUPS = tyre_groups_list 

        ## 3 работа с собственной продукцией:
        production_tyres_list_all = request.POST.getlist('self_production_all')  
        production_tyres_list = request.POST.getlist('self_production')                      # фильтр по собственным шинам
        if production_tyres_list_all:
            models.SELF_PRODUCTION_ALL = production_tyres_list_all
            models.SELF_PRODUCTION = production_tyres_list
            # дополнительно - для вывода первого, если не выбрано ничего (# т.к. в template закоменчен выбор всей продукции - то автоматом ставим галочку на первой в списке и выводим ее):
            models.SELF_PRODUCTION_FIRST = False
        if production_tyres_list:
            models.SELF_PRODUCTION = production_tyres_list
            models.SELF_PRODUCTION_FIRST = False
        else:               # если нечего не выбрано:
            models.SELF_PRODUCTION_ALL = production_tyres_list_all
            models.SELF_PRODUCTION_FIRST = True #тип нужен будет первый элемент с конкурентом - для вывода первого, если не выбрано ничего (# т.к. в template закоменчен выбор всей продукции - то автоматом ставим галочку на первой в списке и выводим ее)


        ### ЕСЛИ ПОЛЬЗОВАТЬЕЛЬ ИЩЕТ ЧЕРЕЗ ПОИСК:
        production_tyres_list_one = request.POST.getlist('product_search')
        ##print('show me', production_tyres_list_one)
        if production_tyres_list_one:
            models.SEARCH_USER_REQUEST = production_tyres_list_one

#
        # 4 работа с производителями-конкурентами (бренды)
        all_onliner_avtoset_bagoria_chemcurier_competitors_list_all = request.POST.getlist('producers_all')
        onliner_avtoset_bagoria_chemcurier_competitors_list = request.POST.getlist('producer_filter_brand_list')                               # фильтр конкурентов
        if all_onliner_avtoset_bagoria_chemcurier_competitors_list_all:
        #if not onliner_avtoset_bagoria_chemcurier_competitors_list:
            #print('onliner_competitors_list')
            models.ONL_AVT_BAG_ALL_BRANDS_CHOSEN = all_onliner_avtoset_bagoria_chemcurier_competitors_list_all
            models.PRODUCER_FILTER_BRAND_LIST_CHECKED_ON = False
            pass
        else:
            #print('onliner_avtoset_bagoria_chemcurier_competitors_list', onliner_avtoset_bagoria_chemcurier_competitors_list)
            models.ONLINER_COMPETITORS = onliner_avtoset_bagoria_chemcurier_competitors_list
            models.AVTOSET_COMPETITORS = onliner_avtoset_bagoria_chemcurier_competitors_list
            models.BAGORIA_COMPETITORS = onliner_avtoset_bagoria_chemcurier_competitors_list
            #models.CHEMCURIER_COMPETITORS = onliner_avtoset_bagoria_chemcurier_competitors_list
            # для отрисовки галочек checkeDd  выбранной прподукции:
            producer_filter_brand_list_got = onliner_avtoset_bagoria_chemcurier_competitors_list
            #print('producer_filter_brand_list_got', producer_filter_brand_list_got)
            if producer_filter_brand_list_got:
                #print('producer_filter_brand_list_got Y', producer_filter_brand_list_got)
                models.PRODUCER_FILTER_BRAND_LIST_CHECKED_ON = producer_filter_brand_list_got
            else:
                #print('producer_filter_brand_list_got N', producer_filter_brand_list_got)
                models.PRODUCER_FILTER_BRAND_LIST_CHECKED_ON = False
            models.ONL_AVT_BAG_ALL_BRANDS_CHOSEN = False

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
            print('pagination_data_got', pagination_data_got)
            models.PAGINATION_VAL = int(request.POST.get('pagination_data'))
        else:
            pass

        # 6. 1 работа с вводимыми данными по количеству выводимых конкурентов на сайте для объекта таблице
        competitor_pagination_data_got = request.POST.get('competitor_pagination_data')  
        #print('competitor_pagination_data_got', competitor_pagination_data_got)
        if competitor_pagination_data_got:
            print('competitor_pagination_data_got', competitor_pagination_data_got)
            models.COMPET_PER_SITE = int(request.POST.get('competitor_pagination_data'))
        else:
            pass

        ## 7 работа проверкой график нужен ли по производителю/площадке
        #marketplace_on_got = request.POST.get('marketplace_on')
        #if marketplace_on_got:
        #    #print('marketplace_on_got Y', marketplace_on_got)
        #    models.GOOGLECHART_MARKETPLACE_ON = True
        #else:
        #    #print('marketplace_on_got N', marketplace_on_got)
        #    models.GOOGLECHART_MARKETPLACE_ON = False

        # 8 работа проверкой график по средневзвешенной цене на рынке/в разрезе торговых площадок
        weighted_average_got = request.POST.get('weighted_average')
        if weighted_average_got:
            #print('weighted_average_got Y', weighted_average_got)
            models.WEIGHTED_AVERAGE_ON = True
        else:
            #print('weighted_average_got N', weighted_average_got)
            models.WEIGHTED_AVERAGE_ON = False

        # 9 работа проверкой - нужен вывод графика c дорисованными линиями
        full_lined_chart_got = request.POST.get('full_lined_chart')
        if full_lined_chart_got:
            #print('full_lined_chart_got Y', full_lined_chart_got)
            models.FULL_LINED_CHART_ON = True
        else:
            #print('full_lined_chart_got N', full_lined_chart_got)
            models.FULL_LINED_CHART_ON = False

        ## 10 работа проверкой - вывод графика только на выбранную дату
        #only_on_current_date_got = request.POST.get('only_on_current_date')
        #if only_on_current_date_got:
        #    models.ONLY_ON_CURRENT_DATE = True
        #else:
        #    models.ONLY_ON_CURRENT_DATE = False



        return HttpResponseRedirect(reverse_lazy('prices:comparative_prices_bel'))

class ComparativeAnalysisTableModelDetailRussiaView(DetailView):
    model = models.ComparativeAnalysisTableModel
    template_name = 'prices/comparative_prices_russia.html'

    def get_object(self, queryset=None): 
        # get comparative_analysis_table

        comparative_analysis_table = models.ComparativeAnalysisTableModel.objects.get_or_create(market_table='belarus')[0]  

        # ПРОВЕРКА - наличие в базе спарсенных данных конкурентов на сегодня для скипа/запуска парсинга:
        today_is = datetime.datetime.now().date()
        list_of_sites = ['express-shina.ru', 'kolesa-darom.ru', 'kolesatyt.ru']
        competitors_exist = models.CompetitorSiteModel.objects.filter(site__in=list_of_sites).filter(date_period=today_is)
        if competitors_exist:
            #print('объеты спарсены, пропуск повторного парсинга')
            pass
        #### END проверки
        else:
            pass
            #russia_sites_parsing()
    
        return comparative_analysis_table
    


    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        obj = context.get('object')

        # ДЛЯ ПОЛУЧЕНИЯ ВАЛЮТЫ ПО КУРСУ НБ РБ НА ДАТУ       
        curr_value = None
        currency = None
        shown_date = None
        if models.CURRENCY_ON_DATE is False:                         # запускаем получение курса валют с НБ РБ только раз за день
            try:
                cu, cu_val, sh_date = my_tags.currency_on_date()
                if datetime.datetime.today().strftime("%Y-%m-%d") == sh_date:       # если на сегодняшнюю дату результат получен - то более не запрашивать
                    currency, curr_value, shown_date = cu, cu_val, sh_date
                    models.CURRENCY_IS_CLEANED = currency, curr_value, shown_date   # записываем полученные значения
                    models.CURRENCY_ON_DATE = True
            except:
                currency, curr_value, shown_date = my_tags.currency_on_date()     # если что -то пошло не так - берем данные с сайта  
                models.CURRENCY_IS_CLEANED = currency, curr_value, shown_date
                models.CURRENCY_ON_DATE = True  
        if models.CURRENCY_DATE_GOT_FROM_USER:                              # если пользователь вводит данные (получить курс на определенную дату): #
            if models.CURRENCY_DATE_GOT_FROM_USER_CLEANED:                  # если только что получал данные на эту дату - то не надо запускать фунцкию - взять что уже собрано
                try:
                    currency_already, curr_value_already, shown_date_already = models.CURRENCY_DATE_GOT_FROM_USER_CLEANED
                    if shown_date_already == models.CURRENCY_DATE_GOT_FROM_USER:
                       currency_already, curr_value_already, shown_date_already = models.CURRENCY_DATE_GOT_FROM_USER_CLEANED 
                    else:
                        currency, curr_value, shown_date = my_tags.currency_on_date()
                        models.CURRENCY_DATE_GOT_FROM_USER_CLEANED = currency, curr_value, shown_date
                except:
                    currency, curr_value, shown_date = my_tags.currency_on_date()
                    models.CURRENCY_DATE_GOT_FROM_USER_CLEANED = currency, curr_value, shown_date
                if shown_date_already == models.CURRENCY_DATE_GOT_FROM_USER:
                   currency, curr_value, shown_date = currency_already, curr_value_already, shown_date_already
            else:                                                           # если ничего - тогда обращаемся к функции:
                currency, curr_value, shown_date = my_tags.currency_on_date()
                models.CURRENCY_DATE_GOT_FROM_USER_CLEANED = currency, curr_value, shown_date

        
#        models.CURRENCY_VALUE_RUB = curr_value / 100
        models.CURRENCY_VALUE_USD = curr_value 
        # END ДЛЯ ПОЛУЧЕНИЯ ВАЛЮТЫ ПО КУРСУ НБ РБ НА ДАТУ


        #### 0 подбор шин с их данными по минималкам для отображения в таблице на определенный период (не конкуренты , а именно собственная продукция)
        # ОПРЕДЕЛЕНИЕ ДАТЫ: 
        if not models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and not models.COMPETITORS_DATE_FROM_USER_ON_FILTER:           #ЕСЛИ ПОЛЬЗОВАТЕЛЬ НЕ ВЫБИРАЛ НИ НАЧ НИ КОНЕЧ ДАТЫ
            today_is = datetime.date.today()                                                                # автоматически ставит дату на неделю назад
            week_ago_date = today_is - datetime.timedelta(days=7)
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START = [week_ago_date.strftime('%Y-%m-%d')]
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER = [today_is.strftime('%Y-%m-%d')]
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START_IS_NOT_CHOSEN = True 
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_IS_NOT_CHOSEN = True  
        #    print("НЕ ВЫСТАВЛЕНЫ  НАЧ И КОН ДАТЫ")

        if not models.COMPETITORS_DATE_FROM_USER_ON_FILTER:  
        # 00.1  выборка всех имеющихся периодов с минималками:
            competitors_exist_all_dates = models.CompetitorSiteModel.objects.all().dates('date_period', 'day') # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ВСЕ ДАТЫ ДОСТУПНЫЕ ВООБЩЕ ВСЕХ КОНКУРЕТОВ все даты доступные вообще всех конкурентов
            competitors_exist_all_dates_last_date_latest_date = max(competitors_exist_all_dates)  # КОНКУРЕНТЫ ПО СТОСТОЯНИЮ НА ДАТУ
            context['table_current_date_for_header'] = competitors_exist_all_dates_last_date_latest_date.strftime("%d.%m.%Y")
    #        print('***** no date from user')
        else:
            # для поиска по собственной продукции с ходом в шаг = месяц       
            date_filter = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()                 # ['2023-01-23']
            competitors_exist_all_dates_last_date_latest_date = date_filter    # КОНКУРЕНТЫ ПО СТОСТОЯНИЮ НА ДАТУ
            context['table_current_date_for_header'] = competitors_exist_all_dates_last_date_latest_date.strftime("%d.%m.%Y")
    #        print('***** date from user')

        ################
        ################
        get_all_dates_year_month = obj.comparative_table.dates('sale_data', 'month')
        if get_all_dates_year_month:
            #oldest_date = min(get_all_dates_year_month)
            latesr_date = max(get_all_dates_year_month)
            year_to_look = latesr_date.year
            month_to_look = latesr_date.month
        else:
            year_to_look = datetime.datetime.today().year
            month_to_look = datetime.datetime.today().month
            #print('oldest_date', oldest_date)
        ################
        ################
        ####

        # ФИЛЬТР ПО СОБСТВЕННОЙ ПРОДУКЦИИ: 
        table_lookup_only_with_competitors = models.ComparativeAnalysisTyresModel.objects.filter(price_tyre_to_compare__isnull=False).distinct() ## ОБРАБАТЫВАЕМ ТОЛЬКО ТЕ У КОТОРЫХ ЕСТЬ СПАРСЕННЫЕ КОНКУРЕНТЫ ПО РАЗМЕРУ (БЕЗ ПРИВЯЗКИ К ПАРАМЕТРАМБ ИХ ФИЛЬТРУЕМ ПОЗЖЕ)
        table_lookup_only_with_competitors_all_parsed = table_lookup_only_with_competitors
        #for kk in table_lookup_only_with_competitors_all_parsed:
        #    print('kk', kk.tyre.tyre_size.tyre_size)

        # 1. ПРОДУКЦИЯ

        production_filter_search_flag = False
        # если пользовательищет через поисковик:
        if models.SEARCH_USER_REQUEST:
            user_requested_data = models.SEARCH_USER_REQUEST  
            search_result = obj.comparative_table.filter(Q(tyre__tyre_model__model__in=user_requested_data, tyre__tyre_size__tyre_size__in=user_requested_data) | Q(tyre__tyre_model__model__in=user_requested_data) | Q(tyre__tyre_size__tyre_size__in=user_requested_data))    
            search_result_id = list(search_result.values_list('id', flat=True))
            if search_result_id:
            #    print('+search_result_id', search_result_id)
                list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(id__in=search_result_id).filter(sale_data__year=year_to_look, sale_data__month=month_to_look)    #только продукция с конкурентами и только одна продукция (модель)
                search_result_id_is_true = True
            else:
                models.SEARCH_USER_REQUEST is False
                list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
                search_result_id_is_true = False


        elif models.SELF_PRODUCTION:                                                  # если пользователем введены (выбраны) шины:
            production_filter_search_flag = True        # значит один вид отбора уже произведен, значит дофильтровывать в группах (если надо) будем уже его
            id_list = []
            for n in models.SELF_PRODUCTION:
                if n.isdigit():                                 
                    comparativeanalisystyre_object_id = int(n)
                    id_list.append(comparativeanalisystyre_object_id)
            list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(id__in=id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look)    #только продукция с конкурентами  
#    list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look)     # проверенный но МЕДЛЕННЫЙ вариант - берем все объекты на посл дату и работаем по ним       
        else:       # если ничего не выбрано:
            # ## ДОРАБОТАНО _ ПРИ ОТСУТСТВИИ ВЫБОРА ПРОДУКЦИИ
            try:
                list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
                for obj in table_lookup_only_with_competitors_all_parsed.order_by('tyre__tyre_size__tyre_size'):
                    if list_of_tyre_comparative_objects: 
                        if obj == list_of_tyre_comparative_objects[0]:
    ##                        print('IFIFIFIFF')
                            obj_pk = list_of_tyre_comparative_objects[0].pk
                            list_of_tyre_comparative_objects = list_of_tyre_comparative_objects.filter(id=obj_pk)   # ЕСЛИ НИЧЕГО НЕ ВЫБРАНО _ ВЗЯТЬ ПЕРВЫЙ оббъект 
    ##                        print('!!!!GGGG! = ', list_of_tyre_comparative_objects) 
                            break
            except:  
                list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look)     # проверенный но МЕДЛЕННЫЙ вариант - берем все объекты на посл дату и работаем по ним
           ## END ДОРАБОТАНО _ ПРИ ОТСУТСТВИИ ВЫБОРА ПРОДУКЦИИ                                   
        
        # 2. ГРУППЫ
        # ФИЛЬТР ПО ГРУППАМ ШИН:
        if production_filter_search_flag is False:          # значит, отбор по продукции не проводился - ищем из всего (это первый этап фильтрации)
            if models.TYRE_GROUPS:                                                  # если пользователем введены (выбраны) шины:
                group_id_list = []
                for n in models.TYRE_GROUPS:
                    if n.isdigit():                                 
                        gr_id = int(n)
                        group_id_list.append(gr_id)
                #existing_val_check = obj.comparative_table.all().filter(tyre__tyre_group__id__in=group_id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look) 
                existing_val_check = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look) #только продукция с конкурентами
                if existing_val_check:
                    #list_of_tyre_comparative_objects = obj.comparative_table.all().filter(tyre__tyre_group__id__in=group_id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look)
                    list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(tyre__tyre_group__id__in=group_id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look)  #только продукция с конкурентами 
                    #print('list_of_tyre_comparative_objects', 'JJ1', list_of_tyre_comparative_objects) 
                else:  
                    #print('АШЫПКА!!!')
                    pass
            elif models.TYRE_GROUPS_ALL:
                list_of_tyre_comparative_objects = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look)     #####!!!!! ТОЛЬКО ОБЪЕКТЫ С КОНКУРЕНТАМИ                                             ####### !!!  ПРОСТО ВСЕ ШИНЫ В ПОБОР
        if production_filter_search_flag is True:          # значит, отбор по продукции проводился  - ищем из всего (это второй этап фильтрации)
            if models.TYRE_GROUPS:                                                  # если пользователем введены (выбраны) шины:
                group_id_list = []
                for n in models.TYRE_GROUPS:
                    if n.isdigit():                                 
                        gr_id = int(n)
                        group_id_list.append(gr_id)
                existing_val_check = table_lookup_only_with_competitors.filter(sale_data__year=year_to_look, sale_data__month=month_to_look) #только продукция с конкурентами
                if existing_val_check:
                    list_of_tyre_comparative_objects = list_of_tyre_comparative_objects.filter(tyre__tyre_group__id__in=group_id_list).filter(sale_data__year=year_to_look, sale_data__month=month_to_look)  #только продукция с конкурентами 
                else:  
                    #print('АШЫПКА!!!')
                    pass
            elif models.TYRE_GROUPS_ALL:
                list_of_tyre_comparative_objects = list_of_tyre_comparative_objects.filter(sale_data__year=year_to_look, sale_data__month=month_to_look)     #####!!!!! ТОЛЬКО ОБЪЕКТЫ С КОНКУРЕНТАМИ                                             ####### !!!  ПРОСТО ВСЕ ШИНЫ В ПОБОР            


        list_of_tyre_comparative_objects_is_empty = False       # ПРОВЕРКА_ ЕСЛИ НИЧЕГО НЕ НАЙДЕНО - ставим флаг
        #print('НУ И ЧТО У НАС ТУТ???', list_of_tyre_comparative_objects_is_empty)
        if not list_of_tyre_comparative_objects: # если значений нет (отсутствуют моделели с конкурентами):
            #print('А У НАС ТУТ ПЛОТИТЬ НЕ ХОЧУТ')
            list_of_tyre_comparative_objects_is_empty = True

        #3. ПО БРЕНДАМ ОТБОР БУДЕТ ДАЛЕЕ

        #0.1 подготовить последнюю доступгую дату с конкурентами:

        last_availible_date_today = datetime.datetime.today()
        ## 1 фильтр конкурентов EXPRESS-SHINA.ru:
        all_competitors = models.CompetitorSiteModel.objects.filter(site='express-shina.ru', tyre_to_compare__in=list_of_tyre_comparative_objects)

            # 1.2 ФИЛЬТР список производителей :
        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        express_shina_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
            object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
            object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            try:
                if models.EXPRESS_SHINA_COMPETITORS:    
                    if models.COMPETITORS_DATE_FROM_USER_ON_FILTER or models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                            date_filter_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], "%Y-%m-%d").date()
                        else:
                            date_filter_start =  models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.EXPRESS_SHINA_COMPETITORS, site='express-shina.ru').earliest('date_period').date_period
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                            date_filter_end = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                        else:
                            date_filter_end =  models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.EXPRESS_SHINA_COMPETITORS, site='express-shina.ru').latest('date_period').date_period
                        got_the_list = models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.EXPRESS_SHINA_COMPETITORS, site='express-shina.ru').filter(date_period__range=[date_filter_start, date_filter_end])

                    else:
                        #print('1.2 ВЫБРАН БРЕНД И НЕ ВВЕДЕНА ДАТА')
                        got_the_list = models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.EXPRESS_SHINA_COMPETITORS, site='express-shina.ru')                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    # end работа с датами '

                    brand_name_subbrands_list = []
                    develop_name_list = []    
                    list_to_delete_rarely_parsed = []    #для удаления реже спаршеных моделей внутри одного бренда(производителя)
                    for competitor in got_the_list:
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            # доп проверка на сезонность:
                            try:
                                for get_season in object_unit.tyre.added_features.all():
                                    get_season_is_is = get_season.season_usage.season_usage_name
                                if get_season_is_is == competitor.season.season_usage_name:
                                    #print('||', competitor.name_competitor)
                                    list_of_matched_competitors.append(competitor)
                                    brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                                    develop_name_list.append((competitor.developer, competitor.name_competitor))                
                            except:     #если сезонности нет:
                                list_of_matched_competitors.append(competitor) 
                                brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                                develop_name_list.append((competitor.developer, competitor.name_competitor))  
                    brand_name_subbrands_list_final = list(set(brand_name_subbrands_list))
                    develop_name_list = list(set(develop_name_list))            # # пересобираем список = проверка производитель  сразными моделями
                    develop_name_list_only_comp = []
                    for commm_namme in develop_name_list:
                        develop_name_list_only_comp.append(commm_namme[0])
                    develop_name_list = develop_name_list_only_comp   
                    list_of_developers_which_brands_more_than_one = []
                    for comp_brand_name in develop_name_list:
                        if develop_name_list.count(comp_brand_name) > 1: # если наименование производителя более одногораза - значит есть неск брендов у него, надо взять наиб спарсенный
                            list_of_developers_which_brands_more_than_one.append(comp_brand_name)

                    list_of_developers_which_brands_more_than_one = list(set(list_of_developers_which_brands_more_than_one))
                    # если у производителя несколко моделей в типоразмере:
                    if list_of_developers_which_brands_more_than_one:                                                             # [<CompetitorModel: Cordiant>, <CompetitorModel: Continental>,
                #        # 1) сформировать бренды у данного прозводителя
                #        # 2) сравнить какой более часто спаршен
                #        # 3) убрать менее спаршенные компетиторы из общего списка (kolesa_darom_competitors_dict1)
                        for develoooper in list_of_developers_which_brands_more_than_one:                                       #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                            list_to_delete_cometitors_to_compare = [] #СПИСОК COMPETITORS ДЛЯ УДАЛЕНИЯ ИЗ ОБЩЕГО - сперва сравнить длинну моделей в бренде
                            for comp_brand_model in brand_name_subbrands_list_final:       # ['Cordiant Comfort 2', Continental ContiPremiumContact ]
                                brand_in_develoooper_dict = {}       
                                brand_in_develoooper_list = []
                                for subbrand_model_competitor in list_of_matched_competitors:
                                #    print('EEE', subbrand_model_competitor.developer, '|', develoooper, '|', subbrand_model_competitor.name_competitor, '|', comp_brand_model)
                                    if subbrand_model_competitor.developer == develoooper and subbrand_model_competitor.name_competitor == comp_brand_model:
                                        brand_in_develoooper_list.append(subbrand_model_competitor)
                                if brand_in_develoooper_list:                       #[<CompetitorModel: Cordiant>, <CompetitorModel: Continental>,
                                #    brand_in_develoooper_dict[comp_brand_model, develoooper] = brand_in_develoooper_list     #{'Cordiant Road Runner': [<CompetitorSiteModel: CompetitorSiteModel object (10966)>,
                                    brand_in_develoooper_dict = { comp_brand_model : brand_in_develoooper_list, develoooper : develoooper }
                                #    print('++--++', brand_in_develoooper_dict.items())
                                try:
                                    if brand_in_develoooper_dict[develoooper] == develoooper:                           # СВЕРКА ЧАСТОТЫ ПАРСИНГА МОДЕЛЕЙ ДАННОГО ПРОИЗВОДИТЕЛЯ, ВЫБОРКА НАИМю СПАРСЕННЫХ _ ИХ УБРАТЬ ИХ ОБЩЕГО ПЕРЕЧНЯ  list_of_matched_competitors                         
                                        #print(comp_brand_model, 'LLLL111TTTT', brand_in_develoooper_dict[develoooper], 'PP22',  develoooper)
                                        len_comparison_got = len(brand_in_develoooper_dict[comp_brand_model])
                                        #print('len_comparison_got', len_comparison_got)
                                        compare_to_delete = len_comparison_got, brand_in_develoooper_dict[comp_brand_model]
                                        list_to_delete_cometitors_to_compare.append(compare_to_delete)
                                        #brand_in_develoooper_dict_new[comp_brand_model] = brand_in_develoooper_dict[comp_brand_model]
                                except:
                                    pass
                            list_to_delete_cometitors_to_compare = sorted(list_to_delete_cometitors_to_compare, key=lambda x: x[0])     ## !!!! ОТСОРТИРОВАНЫ ПО ЧАСТОТЕ ПАРСИНГА каждого бренда(модели) внутри ДАННОГО ПРОИЗВОДИТЕЛЯ (т.е производитель Cordiant - но у него бренды Comfort 3, Winter Sport2  и т.д)
                            #print('!!', list_to_delete_cometitors_to_compare)
                            list_to_delete_cometitors_to_compare = list_to_delete_cometitors_to_compare[:-1]    ## Competitorы на удаление из перечня
                            list_to_delete_cometitors_to_compare_with_no_ind_len = []
                            for ind_len, copet_list in list_to_delete_cometitors_to_compare:                    # убираем индексы длины (количества спасенных)
                                list_to_delete_cometitors_to_compare_with_no_ind_len.append(copet_list)
                            #print('Э сюда на111111' , list_to_delete_cometitors_to_compare_with_no_ind_len)
                        #    print('===========')
                            final_list_to_delete_competitors_in_brand = []                                      # финальный список - очищенный от листов - все непопулярные competitors производителя в одном списке
                            for list_val in list_to_delete_cometitors_to_compare_with_no_ind_len:
                                for item in list_val:
                                    final_list_to_delete_competitors_in_brand.append(item)
                            final_list_to_delete_competitors_in_brand = list(set(final_list_to_delete_competitors_in_brand)) 
                            #print('Э сюда на', final_list_to_delete_competitors_in_brand)

                            list_to_delete_rarely_parsed.extend(final_list_to_delete_competitors_in_brand)          # формируем единый список на удаление
                            #print('list_to_delete_cometitors', list_to_delete_cometitors_to_compare)
                            # убираем непопулярных (реже спашенных модели данного бренда, исключая их из списка общего - останутся лишь производители с одной моделью (у тех производ, у которых было несколько моделей- останется лишь самый спашенный наиболее)):
                        #print('DELETE', list_to_delete_rarely_parsed)
                        for compet_to_delete in list_to_delete_rarely_parsed:
                            list_of_matched_competitors.remove(compet_to_delete)
                        express_shina_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                    # если у каждого производителя по одной модели:
                    else:
                        express_shina_competitors_dict1[object_unit.tyre] = list_of_matched_competitors

                else:
                    # работа с датами без конкурентов (вся продукция)

                    if models.COMPETITORS_DATE_FROM_USER_ON_FILTER or models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                            date_filter_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], "%Y-%m-%d").date()
                        else:
                            date_filter_start = all_competitors.earliest('date_period').date_period
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                            date_filter_end = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                        else:
                            date_filter_end = all_competitors.latest('date_period').date_period
                        got_the_list = all_competitors.filter(date_period__range=[date_filter_start, date_filter_end])
                                                  
                    else:
                        #print('2.3 НЕ ВЫБРАН БРЕНД И НЕ ВВЕДЕНА ДАТА')
                        got_the_list = all_competitors 
                        # end работа с датами      

                    brand_name_subbrands_list = []
                    list_to_delete_rarely_parsed = []    #для удаления реже спаршеных моделей внутри одного бренда(производителя)
                    for competitor in got_the_list:
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            # доп проверка на сезонность:
                            try:
                                for get_season in object_unit.tyre.added_features.all():
                                    get_season_is_is = get_season.season_usage.season_usage_name
                                if get_season_is_is == competitor.season.season_usage_name:
                                #    print('||', competitor.name_competitor)
                                    list_of_matched_competitors.append(competitor)
                                    brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                            except:     #если сезонности нет:
                                list_of_matched_competitors.append(competitor) 
                                brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                    brand_name_subbrands_list_final = list(set(brand_name_subbrands_list))
                #print('111list_of_matched_competitors', list_of_matched_competitors)
                    #print('22222brand_name_subbrands_list_final', brand_name_subbrands_list_final)

                    # доп проверка - так все бренды- у них м.б. по несколько моделей - проверить -есть ли у бреда несколько моделей -взять с наибольшей частотой паринга:
                    list_of_developers_which_brands_more_than_one_for_checking = []
                    for comp_brand in list_of_matched_competitors:
                        list_of_developers_which_brands_more_than_one_for_checking.append((comp_brand.developer, comp_brand.name_competitor))  
                        #print('comp_brand', comp_brand.developer)

                    list_of_developers_which_brands_more_than_one_for_checking = list(set(list_of_developers_which_brands_more_than_one_for_checking))            # # пересобираем список = проверка производитель  сразными моделями
                    develop_name_list_only_comp = []
                    for commm_namme in list_of_developers_which_brands_more_than_one_for_checking:
                        develop_name_list_only_comp.append(commm_namme[0])
                    list_of_developers_which_brands_more_than_one_for_checking = develop_name_list_only_comp   

                    list_of_developers_which_brands_more_than_one = []
                    for comp_brand_name in list_of_developers_which_brands_more_than_one_for_checking:
                        if list_of_developers_which_brands_more_than_one_for_checking.count(comp_brand_name) > 1: # если наименование производителя более одногораза - значит есть неск брендов у него, надо взять наиб спарсенный
                            list_of_developers_which_brands_more_than_one.append(comp_brand_name)
                    list_of_developers_which_brands_more_than_one = list(set(list_of_developers_which_brands_more_than_one))
                    #print('ISS list_of_developers_which_brands_more_than_one', list_of_developers_which_brands_more_than_one)   #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                    if list_of_developers_which_brands_more_than_one:                                                             #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                #        # 1) сформировать бренды у данного прозводителя
                #        # 2) сравнить какой более часто спаршен
                #        # 3) убрать менее спаршенные компетиторы из общего списка (express_shina_competitors_dict1)
                        for develoooper in list_of_developers_which_brands_more_than_one:                                       #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                            list_to_delete_cometitors_to_compare = [] #СПИСОК COMPETITORS ДЛЯ УДАЛЕНИЯ ИЗ ОБЩЕГО - сперва сравнить длинну моделей в бренде
                            for comp_brand_model in brand_name_subbrands_list_final:       # ['Cordiant Comfort 2', Continental ContiPremiumContact ]
                                brand_in_develoooper_dict = {}       
                                brand_in_develoooper_list = []
                                for subbrand_model_competitor in list_of_matched_competitors:
                                #    print('EEE', subbrand_model_competitor.developer, '|', develoooper, '|', subbrand_model_competitor.name_competitor, '|', comp_brand_model)
                                    if subbrand_model_competitor.developer == develoooper and subbrand_model_competitor.name_competitor == comp_brand_model:
                                        brand_in_develoooper_list.append(subbrand_model_competitor)
                                if brand_in_develoooper_list:
                                #    brand_in_develoooper_dict[comp_brand_model, develoooper] = brand_in_develoooper_list     #{'Cordiant Road Runner': [<CompetitorSiteModel: CompetitorSiteModel object (10966)>,
                                    brand_in_develoooper_dict = { comp_brand_model : brand_in_develoooper_list, develoooper : develoooper }
                                    #print('++--++', brand_in_develoooper_dict.keys())
                                try:
                                    if brand_in_develoooper_dict[develoooper] == develoooper:                           # СВЕРКА ЧАСТОТЫ ПАРСИНГА МОДЕЛЕЙ ДАННОГО ПРОИЗВОДИТЕЛЯ, ВЫБОРКА НАИМю СПАРСЕННЫХ _ ИХ УБРАТЬ ИХ ОБЩЕГО ПЕРЕЧНЯ  list_of_matched_competitors                         
                                        #print(comp_brand_model, 'LLLL111TTTT', brand_in_develoooper_dict[develoooper], 'PP22',  develoooper)
                                        len_comparison_got = len(brand_in_develoooper_dict[comp_brand_model])
                                        #compare_to_delete = len_comparison_got
                                        compare_to_delete = len_comparison_got, brand_in_develoooper_dict[comp_brand_model]
                                        list_to_delete_cometitors_to_compare.append(compare_to_delete)
                                        #brand_in_develoooper_dict_new[comp_brand_model] = brand_in_develoooper_dict[comp_brand_model]
                                except:
                                    pass
                            list_to_delete_cometitors_to_compare = sorted(list_to_delete_cometitors_to_compare, key=lambda x: x[0])     ## !!!! ОТСОРТИРОВАНЫ ПО ЧАСТОТЕ ПАРСИНГА каждого бренда(модели) внутри ДАННОГО ПРОИЗВОДИТЕЛЯ (т.е производитель Cordiant - но у него бренды Comfort 3, Winter Sport2  и т.д)
                            list_to_delete_cometitors_to_compare = list_to_delete_cometitors_to_compare[:-1]    ## Competitorы на удаление из перечня
                            list_to_delete_cometitors_to_compare_with_no_ind_len = []
                            for ind_len, copet_list in list_to_delete_cometitors_to_compare:                    # убираем индексы длины (количества спасенных)
                                list_to_delete_cometitors_to_compare_with_no_ind_len.append(copet_list)
                            #print('Э сюда на111111' , list_to_delete_cometitors_to_compare_with_no_ind_len)

                            final_list_to_delete_competitors_in_brand = []                                      # финальный список - очищенный от листов - все непопулярные competitors производителя в одном списке
                            for list_val in list_to_delete_cometitors_to_compare_with_no_ind_len:
                                for item in list_val:
                                    final_list_to_delete_competitors_in_brand.append(item)
                            final_list_to_delete_competitors_in_brand = list(set(final_list_to_delete_competitors_in_brand)) 
                            #print('Э сюда на', final_list_to_delete_competitors_in_brand)

                            list_to_delete_rarely_parsed.extend(final_list_to_delete_competitors_in_brand)          # формируем единый список на удаление
                            #print('list_to_delete_cometitors', list_to_delete_cometitors_to_compare)
                            # убираем непопулярных (реже спашенных модели данного бренда, исключая их из списка общего - останутся лишь производители с одной моделью (у тех производ, у которых было несколько моделей- останется лишь самый спашенный наиболее)):
                        #print('DELETE', list_to_delete_rarely_parsed)
                        for compet_to_delete in list_to_delete_rarely_parsed:
                            list_of_matched_competitors.remove(compet_to_delete)
                        express_shina_competitors_dict1[object_unit.tyre] = list_of_matched_competitors

                    else:       # если у каждого бренда-производителя по одной модели:

                        express_shina_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
            except:
                pass

        models.EXPRESS_SHINA_COMPETITORS_DICTIONARY1 = express_shina_competitors_dict1 


        ## 2 фильтр конкурентов KOLESA-DAROM.ru:
        all_competitors = models.CompetitorSiteModel.objects.filter(site='kolesa-darom.ru', tyre_to_compare__in=list_of_tyre_comparative_objects)

            # 1.2 ФИЛЬТР список производителей :
        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        kolesa_darom_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
            object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
            object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            try:
                if models.KOLESA_DAROM_COMPETITORS:
                    # работа с датами для конкурентов
                    if models.COMPETITORS_DATE_FROM_USER_ON_FILTER or models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                            date_filter_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], "%Y-%m-%d").date()
                        else:
                            date_filter_start =  models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.KOLESA_DAROM_COMPETITORS, site='kolesa-darom.ru').earliest('date_period').date_period
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                            date_filter_end = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                        else:
                            date_filter_end =  models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.KOLESA_DAROM_COMPETITORS, site='kolesa-darom.ru').latest('date_period').date_period
                        got_the_list = models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.KOLESA_DAROM_COMPETITORS, site='kolesa-darom.ru').filter(date_period__range=[date_filter_start, date_filter_end])
                    #    print('BAGORIA', date_filter_start, '-', date_filter_end)
                    else:
                        #print('1.2 ВЫБРАН БРЕНД И НЕ ВВЕДЕНА ДАТА')
                        got_the_list = models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.KOLESA_DAROM_COMPETITORS, site='kolesa-darom.ru')                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    # end работа с датами '


                    brand_name_subbrands_list = []
                    develop_name_list = []    
                    list_to_delete_rarely_parsed = []    #для удаления реже спаршеных моделей внутри одного бренда(производителя)
                    for competitor in got_the_list:
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            # доп проверка на сезонность:
                            try:
                                for get_season in object_unit.tyre.added_features.all():
                                    get_season_is_is = get_season.season_usage.season_usage_name
                                if get_season_is_is == competitor.season.season_usage_name:
                                    #print('||', competitor.name_competitor)
                                    list_of_matched_competitors.append(competitor)
                                    brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                                    develop_name_list.append((competitor.developer, competitor.name_competitor))                
                            except:     #если сезонности нет:
                                list_of_matched_competitors.append(competitor) 
                                brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                                develop_name_list.append((competitor.developer, competitor.name_competitor))  
                    brand_name_subbrands_list_final = list(set(brand_name_subbrands_list))
                    develop_name_list = list(set(develop_name_list))            # # пересобираем список = проверка производитель  сразными моделями
                    develop_name_list_only_comp = []
                    for commm_namme in develop_name_list:
                        develop_name_list_only_comp.append(commm_namme[0])
                    develop_name_list = develop_name_list_only_comp   
                    list_of_developers_which_brands_more_than_one = []
                    for comp_brand_name in develop_name_list:
                        if develop_name_list.count(comp_brand_name) > 1: # если наименование производителя более одногораза - значит есть неск брендов у него, надо взять наиб спарсенный
                            list_of_developers_which_brands_more_than_one.append(comp_brand_name)

                    list_of_developers_which_brands_more_than_one = list(set(list_of_developers_which_brands_more_than_one))
                    # если у производителя несколко моделей в типоразмере:
                    if list_of_developers_which_brands_more_than_one:                                                             # [<CompetitorModel: Cordiant>, <CompetitorModel: Continental>,
                #        # 1) сформировать бренды у данного прозводителя
                #        # 2) сравнить какой более часто спаршен
                #        # 3) убрать менее спаршенные компетиторы из общего списка (kolesa_darom_competitors_dict1)
                        for develoooper in list_of_developers_which_brands_more_than_one:                                       #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                            list_to_delete_cometitors_to_compare = [] #СПИСОК COMPETITORS ДЛЯ УДАЛЕНИЯ ИЗ ОБЩЕГО - сперва сравнить длинну моделей в бренде
                            for comp_brand_model in brand_name_subbrands_list_final:       # ['Cordiant Comfort 2', Continental ContiPremiumContact ]
                                brand_in_develoooper_dict = {}       
                                brand_in_develoooper_list = []
                                for subbrand_model_competitor in list_of_matched_competitors:
                                #    print('EEE', subbrand_model_competitor.developer, '|', develoooper, '|', subbrand_model_competitor.name_competitor, '|', comp_brand_model)
                                    if subbrand_model_competitor.developer == develoooper and subbrand_model_competitor.name_competitor == comp_brand_model:
                                        brand_in_develoooper_list.append(subbrand_model_competitor)
                                if brand_in_develoooper_list:                       #[<CompetitorModel: Cordiant>, <CompetitorModel: Continental>,
                                #    brand_in_develoooper_dict[comp_brand_model, develoooper] = brand_in_develoooper_list     #{'Cordiant Road Runner': [<CompetitorSiteModel: CompetitorSiteModel object (10966)>,
                                    brand_in_develoooper_dict = { comp_brand_model : brand_in_develoooper_list, develoooper : develoooper }
                                #    print('++--++', brand_in_develoooper_dict.items())
                                try:
                                    if brand_in_develoooper_dict[develoooper] == develoooper:                           # СВЕРКА ЧАСТОТЫ ПАРСИНГА МОДЕЛЕЙ ДАННОГО ПРОИЗВОДИТЕЛЯ, ВЫБОРКА НАИМю СПАРСЕННЫХ _ ИХ УБРАТЬ ИХ ОБЩЕГО ПЕРЕЧНЯ  list_of_matched_competitors                         
                                        #print(comp_brand_model, 'LLLL111TTTT', brand_in_develoooper_dict[develoooper], 'PP22',  develoooper)
                                        len_comparison_got = len(brand_in_develoooper_dict[comp_brand_model])
                                        #print('len_comparison_got', len_comparison_got)
                                        #compare_to_delete = len_comparison_got
                                        compare_to_delete = len_comparison_got, brand_in_develoooper_dict[comp_brand_model]
                                        list_to_delete_cometitors_to_compare.append(compare_to_delete)
                                        #brand_in_develoooper_dict_new[comp_brand_model] = brand_in_develoooper_dict[comp_brand_model]
                                except:
                                    pass
                            list_to_delete_cometitors_to_compare = sorted(list_to_delete_cometitors_to_compare, key=lambda x: x[0])     ## !!!! ОТСОРТИРОВАНЫ ПО ЧАСТОТЕ ПАРСИНГА каждого бренда(модели) внутри ДАННОГО ПРОИЗВОДИТЕЛЯ (т.е производитель Cordiant - но у него бренды Comfort 3, Winter Sport2  и т.д)
                            #print('!!', list_to_delete_cometitors_to_compare)
                            list_to_delete_cometitors_to_compare = list_to_delete_cometitors_to_compare[:-1]    ## Competitorы на удаление из перечня
                            list_to_delete_cometitors_to_compare_with_no_ind_len = []
                            for ind_len, copet_list in list_to_delete_cometitors_to_compare:                    # убираем индексы длины (количества спасенных)
                                list_to_delete_cometitors_to_compare_with_no_ind_len.append(copet_list)
                            #print('Э сюда на111111' , list_to_delete_cometitors_to_compare_with_no_ind_len)
                            #print('===========')
                            final_list_to_delete_competitors_in_brand = []                                      # финальный список - очищенный от листов - все непопулярные competitors производителя в одном списке
                            for list_val in list_to_delete_cometitors_to_compare_with_no_ind_len:
                                for item in list_val:
                                    final_list_to_delete_competitors_in_brand.append(item)
                            final_list_to_delete_competitors_in_brand = list(set(final_list_to_delete_competitors_in_brand)) 
                            #print('Э сюда на', final_list_to_delete_competitors_in_brand)
                            list_to_delete_rarely_parsed.extend(final_list_to_delete_competitors_in_brand)          # формируем единый список на удаление
                            #print('list_to_delete_cometitors', list_to_delete_cometitors_to_compare)
                            # убираем непопулярных (реже спашенных модели данного бренда, исключая их из списка общего - останутся лишь производители с одной моделью (у тех производ, у которых было несколько моделей- останется лишь самый спашенный наиболее)):
                        #print('DELETE', list_to_delete_rarely_parsed)
                        for compet_to_delete in list_to_delete_rarely_parsed:
                            list_of_matched_competitors.remove(compet_to_delete)
                        kolesa_darom_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                    # если у каждого производителя по одной модели:
                    else:

                        kolesa_darom_competitors_dict1[object_unit.tyre] = list_of_matched_competitors

                else:
                    # работа с датами без конкурентов (вся продукция)

                    if models.COMPETITORS_DATE_FROM_USER_ON_FILTER or models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                            date_filter_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], "%Y-%m-%d").date()
                        else:
                            date_filter_start =  all_competitors.earliest('date_period').date_period
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                            date_filter_end = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                        else:
                            date_filter_end =  all_competitors.latest('date_period').date_period
                        got_the_list = all_competitors.filter(date_period__range=[date_filter_start, date_filter_end])
                                                  
                    else:
                        #print('2.3 НЕ ВЫБРАН БРЕНД И НЕ ВВЕДЕНА ДАТА')
                        got_the_list = all_competitors 
                        # end работа с датами       

                    #print('2.4 БРЕНД НЕ ВЫБРАН')                                                                                                         ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ    

                    brand_name_subbrands_list = []
                    list_to_delete_rarely_parsed = []    #для удаления реже спаршеных моделей внутри одного бренда(производителя)
                    for competitor in got_the_list:
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            # доп проверка на сезонность:
                            try:
                                for get_season in object_unit.tyre.added_features.all():
                                    get_season_is_is = get_season.season_usage.season_usage_name
                                if get_season_is_is == competitor.season.season_usage_name:
                                #    print('||', competitor.name_competitor)
                                    list_of_matched_competitors.append(competitor)
                                    brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде

                            except:     #если сезонности нет:
                                list_of_matched_competitors.append(competitor) 
                                brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                    brand_name_subbrands_list_final = list(set(brand_name_subbrands_list))
                #print('111list_of_matched_competitors', list_of_matched_competitors)
                    #print('22222brand_name_subbrands_list_final', brand_name_subbrands_list_final)

                    # доп проверка - так все бренды- у них м.б. по несколько моделей - проверить -есть ли у бреда несколько моделей -взять с наибольшей частотой паринга:
                    list_of_developers_which_brands_more_than_one_for_checking = []
                    for comp_brand in list_of_matched_competitors:
                        list_of_developers_which_brands_more_than_one_for_checking.append((comp_brand.developer, comp_brand.name_competitor))  
                        #print('comp_brand', comp_brand.developer)

                    list_of_developers_which_brands_more_than_one_for_checking = list(set(list_of_developers_which_brands_more_than_one_for_checking))            # # пересобираем список = проверка производитель  сразными моделями
                    develop_name_list_only_comp = []
                    for commm_namme in list_of_developers_which_brands_more_than_one_for_checking:
                        develop_name_list_only_comp.append(commm_namme[0])
                    list_of_developers_which_brands_more_than_one_for_checking = develop_name_list_only_comp   

                    list_of_developers_which_brands_more_than_one = []
                    for comp_brand_name in list_of_developers_which_brands_more_than_one_for_checking:
                        if list_of_developers_which_brands_more_than_one_for_checking.count(comp_brand_name) > 1: # если наименование производителя более одногораза - значит есть неск брендов у него, надо взять наиб спарсенный
                            list_of_developers_which_brands_more_than_one.append(comp_brand_name)
                    list_of_developers_which_brands_more_than_one = list(set(list_of_developers_which_brands_more_than_one))
                    #print('ISS list_of_developers_which_brands_more_than_one', list_of_developers_which_brands_more_than_one)   #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                    if list_of_developers_which_brands_more_than_one:                                                             #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                #        # 1) сформировать бренды у данного прозводителя
                #        # 2) сравнить какой более часто спаршен
                #        # 3) убрать менее спаршенные компетиторы из общего списка (kolesa_darom_competitors_dict1)
                        for develoooper in list_of_developers_which_brands_more_than_one:                                       #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                            list_to_delete_cometitors_to_compare = [] #СПИСОК COMPETITORS ДЛЯ УДАЛЕНИЯ ИЗ ОБЩЕГО - сперва сравнить длинну моделей в бренде
                            for comp_brand_model in brand_name_subbrands_list_final:       # ['Cordiant Comfort 2', Continental ContiPremiumContact ]
                                brand_in_develoooper_dict = {}       
                                brand_in_develoooper_list = []
                                for subbrand_model_competitor in list_of_matched_competitors:
                                #    print('EEE', subbrand_model_competitor.developer, '|', develoooper, '|', subbrand_model_competitor.name_competitor, '|', comp_brand_model)
                                    if subbrand_model_competitor.developer == develoooper and subbrand_model_competitor.name_competitor == comp_brand_model:
                                        brand_in_develoooper_list.append(subbrand_model_competitor)
                                if brand_in_develoooper_list:
                                #    brand_in_develoooper_dict[comp_brand_model, develoooper] = brand_in_develoooper_list     #{'Cordiant Road Runner': [<CompetitorSiteModel: CompetitorSiteModel object (10966)>,
                                    brand_in_develoooper_dict = { comp_brand_model : brand_in_develoooper_list, develoooper : develoooper }
                                    #print('++--++', brand_in_develoooper_dict.keys())
                                try:
                                    if brand_in_develoooper_dict[develoooper] == develoooper:                           # СВЕРКА ЧАСТОТЫ ПАРСИНГА МОДЕЛЕЙ ДАННОГО ПРОИЗВОДИТЕЛЯ, ВЫБОРКА НАИМю СПАРСЕННЫХ _ ИХ УБРАТЬ ИХ ОБЩЕГО ПЕРЕЧНЯ  list_of_matched_competitors                         
                                        #print(comp_brand_model, 'LLLL111TTTT', brand_in_develoooper_dict[develoooper], 'PP22',  develoooper)
                                        len_comparison_got = len(brand_in_develoooper_dict[comp_brand_model])
                                        #compare_to_delete = len_comparison_got
                                        compare_to_delete = len_comparison_got, brand_in_develoooper_dict[comp_brand_model]
                                        list_to_delete_cometitors_to_compare.append(compare_to_delete)
                                        #brand_in_develoooper_dict_new[comp_brand_model] = brand_in_develoooper_dict[comp_brand_model]
                                except:
                                    pass
                            list_to_delete_cometitors_to_compare = sorted(list_to_delete_cometitors_to_compare, key=lambda x: x[0])     ## !!!! ОТСОРТИРОВАНЫ ПО ЧАСТОТЕ ПАРСИНГА каждого бренда(модели) внутри ДАННОГО ПРОИЗВОДИТЕЛЯ (т.е производитель Cordiant - но у него бренды Comfort 3, Winter Sport2  и т.д)
                            list_to_delete_cometitors_to_compare = list_to_delete_cometitors_to_compare[:-1]    ## Competitorы на удаление из перечня
                            list_to_delete_cometitors_to_compare_with_no_ind_len = []
                            for ind_len, copet_list in list_to_delete_cometitors_to_compare:                    # убираем индексы длины (количества спасенных)
                                list_to_delete_cometitors_to_compare_with_no_ind_len.append(copet_list)
                            #print('Э сюда на111111' , list_to_delete_cometitors_to_compare_with_no_ind_len)                 
                            final_list_to_delete_competitors_in_brand = []                                      # финальный список - очищенный от листов - все непопулярные competitors производителя в одном списке
                            for list_val in list_to_delete_cometitors_to_compare_with_no_ind_len:
                                for item in list_val:
                                    final_list_to_delete_competitors_in_brand.append(item)
                            final_list_to_delete_competitors_in_brand = list(set(final_list_to_delete_competitors_in_brand)) 
                            #print('Э сюда на', final_list_to_delete_competitors_in_brand)
                            list_to_delete_rarely_parsed.extend(final_list_to_delete_competitors_in_brand)          # формируем единый список на удаление
                            #print('list_to_delete_cometitors', list_to_delete_cometitors_to_compare)
                            # убираем непопулярных (реже спашенных модели данного бренда, исключая их из списка общего - останутся лишь производители с одной моделью (у тех производ, у которых было несколько моделей- останется лишь самый спашенный наиболее)):
                        #print('DELETE', list_to_delete_rarely_parsed)
                        for compet_to_delete in list_to_delete_rarely_parsed:
                            list_of_matched_competitors.remove(compet_to_delete)
                        kolesa_darom_competitors_dict1[object_unit.tyre] = list_of_matched_competitors           
                    else:       # если у каждого бренда-производителя по одной модели:
                        kolesa_darom_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
            except:
                    pass

        models.KOLESA_DAROM_COMPETITORS_DICTIONARY1 = kolesa_darom_competitors_dict1  

        ###### END OF KOLESA_DAROM

        ## 3 фильтр конкурентов KOLESATYT:

        all_competitors = models.CompetitorSiteModel.objects.filter(site='kolesatyt.ru', tyre_to_compare__in=list_of_tyre_comparative_objects)

            # 1.2 ФИЛЬТР список производителей :
        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые производители шин для работы в таблице:
        kolesatyt_competitors_dict1 = {}
        for object_unit in list_of_tyre_comparative_objects:
            object_unit.planned_profitabilit = object_unit.planned_profitability()          ######  FOR WHAT?
            object_unit.direct_cost_varianc = object_unit.direct_cost_variance()            ######  FOR WHAT?
            list_of_matched_competitors = []
            try:
                if models.KOLESATYT_COMPETITORS: 
                    # работа с датами для конкурентов
                    if models.COMPETITORS_DATE_FROM_USER_ON_FILTER or models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                            date_filter_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], "%Y-%m-%d").date()
                        else:
                            date_filter_start =  models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.KOLESATYT_COMPETITORS, site='kolesatyt.ru').earliest('date_period').date_period
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                            date_filter_end = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                        else:
                            date_filter_end =  models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.KOLESATYT_COMPETITORS, site='kolesatyt.ru').latest('date_period').date_period
                        got_the_list = models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.KOLESATYT_COMPETITORS, site='kolesatyt.ru').filter(date_period__range=[date_filter_start, date_filter_end])
                        print('date_filter_start', date_filter_start, '===', 'date_filter_end', date_filter_end)
                    else:
                        print('1.2 ВЫБРАН БРЕНД И НЕ ВВЕДЕНА ДАТА  - KOLESATYT')
                        got_the_list = models.CompetitorSiteModel.objects.filter(developer__competitor_name__in=models.KOLESATYT_COMPETITORS, site='kolesatyt.ru')                      ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ
                    # end работа с датами '

                    brand_name_subbrands_list = []
                    develop_name_list = []    
                    list_to_delete_rarely_parsed = []    #для удаления реже спаршеных моделей внутри одного бренда(производителя)
                    for competitor in got_the_list:
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            # доп проверка на сезонность:
                            try:
                                for get_season in object_unit.tyre.added_features.all():
                                    get_season_is_is = get_season.season_usage.season_usage_name
                                if get_season_is_is == competitor.season.season_usage_name:
                                    #print('||', competitor.name_competitor)
                                    list_of_matched_competitors.append(competitor)
                                    brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                                    develop_name_list.append((competitor.developer, competitor.name_competitor))                
                            except:     #если сезонности нет:
                                list_of_matched_competitors.append(competitor) 
                                brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                                develop_name_list.append((competitor.developer, competitor.name_competitor))  
                    brand_name_subbrands_list_final = list(set(brand_name_subbrands_list))
                    develop_name_list = list(set(develop_name_list))            # # пересобираем список = проверка производитель  сразными моделями
                    develop_name_list_only_comp = []
                    for commm_namme in develop_name_list:
                        develop_name_list_only_comp.append(commm_namme[0])
                    develop_name_list = develop_name_list_only_comp   
                    list_of_developers_which_brands_more_than_one = []
                    for comp_brand_name in develop_name_list:
                        if develop_name_list.count(comp_brand_name) > 1: # если наименование производителя более одногораза - значит есть неск брендов у него, надо взять наиб спарсенный
                            list_of_developers_which_brands_more_than_one.append(comp_brand_name)

######################                    for subbrand_model_competitor in list_of_matched_competitors:
######################                        print('PPPOOOPPPP', subbrand_model_competitor.developer, '|', subbrand_model_competitor.name_competitor, '|', subbrand_model_competitor.date_period)

                    list_of_developers_which_brands_more_than_one = list(set(list_of_developers_which_brands_more_than_one))
                    # если у производителя несколко моделей в типоразмере:
                    if list_of_developers_which_brands_more_than_one:                                                             # [<CompetitorModel: Cordiant>, <CompetitorModel: Continental>,
                #        # 1) сформировать бренды у данного прозводителя
                #        # 2) сравнить какой более часто спаршен
                #        # 3) убрать менее спаршенные компетиторы из общего списка (kolesatyt_competitors_dict1)
                        for develoooper in list_of_developers_which_brands_more_than_one:                                       #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                            list_to_delete_cometitors_to_compare = [] #СПИСОК COMPETITORS ДЛЯ УДАЛЕНИЯ ИЗ ОБЩЕГО - сперва сравнить длинну моделей в бренде
                            for comp_brand_model in brand_name_subbrands_list_final:       # ['Cordiant Comfort 2', Continental ContiPremiumContact ]
                                brand_in_develoooper_dict = {}       
                                brand_in_develoooper_list = []
                                for subbrand_model_competitor in list_of_matched_competitors:
                            #        print('EEE', subbrand_model_competitor.developer, '|', develoooper, '|', subbrand_model_competitor.name_competitor, '|', comp_brand_model, '|', subbrand_model_competitor.date_period)
                                    if subbrand_model_competitor.developer == develoooper and subbrand_model_competitor.name_competitor == comp_brand_model:
                                        brand_in_develoooper_list.append(subbrand_model_competitor)
                                if brand_in_develoooper_list:                       #[<CompetitorModel: Cordiant>, <CompetitorModel: Continental>,
                                #    brand_in_develoooper_dict[comp_brand_model, develoooper] = brand_in_develoooper_list     #{'Cordiant Road Runner': [<CompetitorSiteModel: CompetitorSiteModel object (10966)>,
                                    brand_in_develoooper_dict = { comp_brand_model : brand_in_develoooper_list, develoooper : develoooper }
                                #    print('++--++', brand_in_develoooper_dict.items())
                                try:
                                    if brand_in_develoooper_dict[develoooper] == develoooper:                           # СВЕРКА ЧАСТОТЫ ПАРСИНГА МОДЕЛЕЙ ДАННОГО ПРОИЗВОДИТЕЛЯ, ВЫБОРКА НАИМю СПАРСЕННЫХ _ ИХ УБРАТЬ ИХ ОБЩЕГО ПЕРЕЧНЯ  list_of_matched_competitors                         
                                        #print(comp_brand_model, 'LLLL111TTTT', brand_in_develoooper_dict[develoooper], 'PP22',  develoooper)
                                        len_comparison_got = len(brand_in_develoooper_dict[comp_brand_model])
                                        #print('len_comparison_got', len_comparison_got)
                                        #compare_to_delete = len_comparison_got
                                        compare_to_delete = len_comparison_got, brand_in_develoooper_dict[comp_brand_model]
                                        list_to_delete_cometitors_to_compare.append(compare_to_delete)
                                        #brand_in_develoooper_dict_new[comp_brand_model] = brand_in_develoooper_dict[comp_brand_model]
                                except:
                                    pass
                            list_to_delete_cometitors_to_compare = sorted(list_to_delete_cometitors_to_compare, key=lambda x: x[0])     ## !!!! ОТСОРТИРОВАНЫ ПО ЧАСТОТЕ ПАРСИНГА каждого бренда(модели) внутри ДАННОГО ПРОИЗВОДИТЕЛЯ (т.е производитель Cordiant - но у него бренды Comfort 3, Winter Sport2  и т.д)
                            #print('!!', list_to_delete_cometitors_to_compare)
                            list_to_delete_cometitors_to_compare = list_to_delete_cometitors_to_compare[:-1]    ## Competitorы на удаление из перечня
                            list_to_delete_cometitors_to_compare_with_no_ind_len = []
                            for ind_len, copet_list in list_to_delete_cometitors_to_compare:                    # убираем индексы длины (количества спасенных)
                                list_to_delete_cometitors_to_compare_with_no_ind_len.append(copet_list)
                            #print('Э сюда на111111' , list_to_delete_cometitors_to_compare_with_no_ind_len)
                            #print('===========')
                            final_list_to_delete_competitors_in_brand = []                                      # финальный список - очищенный от листов - все непопулярные competitors производителя в одном списке
                            for list_val in list_to_delete_cometitors_to_compare_with_no_ind_len:
                                for item in list_val:
                                    final_list_to_delete_competitors_in_brand.append(item)
                            final_list_to_delete_competitors_in_brand = list(set(final_list_to_delete_competitors_in_brand)) 
                            #print('Э сюда на', final_list_to_delete_competitors_in_brand)
                            list_to_delete_rarely_parsed.extend(final_list_to_delete_competitors_in_brand)          # формируем единый список на удаление
                            #print('list_to_delete_cometitors', list_to_delete_cometitors_to_compare)
                            # убираем непопулярных (реже спашенных модели данного бренда, исключая их из списка общего - останутся лишь производители с одной моделью (у тех производ, у которых было несколько моделей- останется лишь самый спашенный наиболее)):
                        #print('DELETE', list_to_delete_rarely_parsed)
                        for compet_to_delete in list_to_delete_rarely_parsed:
                            list_of_matched_competitors.remove(compet_to_delete)
                        kolesatyt_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
                    # если у каждого производителя по одной модели:
                    else:

                        kolesatyt_competitors_dict1[object_unit.tyre] = list_of_matched_competitors

                else:
                    # 2.1 работа с датами без конкурентов (вся продукция)
                    #print('2.1 НЕ ВЫБРАН БРЕНД И ВВЕДЕНА ДАТА  - BAGORIA')
                    if models.COMPETITORS_DATE_FROM_USER_ON_FILTER or models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                            date_filter_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], "%Y-%m-%d").date()
                        else:
                            date_filter_start =  all_competitors.earliest('date_period').date_period
                        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                            date_filter_end = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
                        else:
                            date_filter_end =  all_competitors.latest('date_period').date_period
                        got_the_list = all_competitors.filter(date_period__range=[date_filter_start, date_filter_end])
                                                  
                    else:
                        #print('2.2 НЕ ВЫБРАН БРЕНД И НЕ ВВЕДЕНА ДАТА  - BAGORIA')
                        got_the_list = all_competitors 
                        # end работа с датами       
                                                                                                       ####!~!!!!!!!!!!!!!!!!! ПОКАЗЫВАТЬ В TEMPLATE ФИЛЬТР ДО 3 ПРОИЗВОДИТЕЛЕЙ ПО ДЕФОЛТУ    

                    brand_name_subbrands_list = []
                    list_to_delete_rarely_parsed = []    #для удаления реже спаршеных моделей внутри одного бренда(производителя)
                    for competitor in got_the_list:
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                            # доп проверка на сезонность:
                            try:
                                for get_season in object_unit.tyre.added_features.all():
                                    get_season_is_is = get_season.season_usage.season_usage_name
                                if get_season_is_is == competitor.season.season_usage_name:
                                #    print('||', competitor.name_competitor)
                                    list_of_matched_competitors.append(competitor)
                                    brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде

                            except:     #если сезонности нет:
                                list_of_matched_competitors.append(competitor) 
                                brand_name_subbrands_list.append(competitor.name_competitor)    #формирование суббренжов(моделей) в данном бренде
                    brand_name_subbrands_list_final = list(set(brand_name_subbrands_list))
                #print('111list_of_matched_competitors', list_of_matched_competitors)
                    #print('22222brand_name_subbrands_list_final', brand_name_subbrands_list_final)

                    # доп проверка - так все бренды- у них м.б. по несколько моделей - проверить -есть ли у бреда несколько моделей -взять с наибольшей частотой паринга:
                    list_of_developers_which_brands_more_than_one_for_checking = []
                    for comp_brand in list_of_matched_competitors:
                        list_of_developers_which_brands_more_than_one_for_checking.append((comp_brand.developer, comp_brand.name_competitor))  
                        #print('comp_brand', comp_brand.developer)

                    list_of_developers_which_brands_more_than_one_for_checking = list(set(list_of_developers_which_brands_more_than_one_for_checking))            # # пересобираем список = проверка производитель  сразными моделями
                    develop_name_list_only_comp = []
                    for commm_namme in list_of_developers_which_brands_more_than_one_for_checking:
                        develop_name_list_only_comp.append(commm_namme[0])
                    list_of_developers_which_brands_more_than_one_for_checking = develop_name_list_only_comp   

                    list_of_developers_which_brands_more_than_one = []
                    for comp_brand_name in list_of_developers_which_brands_more_than_one_for_checking:
                        if list_of_developers_which_brands_more_than_one_for_checking.count(comp_brand_name) > 1: # если наименование производителя более одногораза - значит есть неск брендов у него, надо взять наиб спарсенный
                            list_of_developers_which_brands_more_than_one.append(comp_brand_name)
                    list_of_developers_which_brands_more_than_one = list(set(list_of_developers_which_brands_more_than_one))
                    #print('ISS list_of_developers_which_brands_more_than_one', list_of_developers_which_brands_more_than_one)   #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                    if list_of_developers_which_brands_more_than_one:                                                             #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                #        # 1) сформировать бренды у данного прозводителя
                #        # 2) сравнить какой более часто спаршен
                #        # 3) убрать менее спаршенные компетиторы из общего списка (kolesatyt_competitors_dict1)
                        for develoooper in list_of_developers_which_brands_more_than_one:                                       #[<CompetitorModel: Goodride>, <CompetitorModel: Matador>,
                            list_to_delete_cometitors_to_compare = [] #СПИСОК COMPETITORS ДЛЯ УДАЛЕНИЯ ИЗ ОБЩЕГО - сперва сравнить длинну моделей в бренде
                            for comp_brand_model in brand_name_subbrands_list_final:       # ['Cordiant Comfort 2', Continental ContiPremiumContact ]
                                brand_in_develoooper_dict = {}       
                                brand_in_develoooper_list = []
                                for subbrand_model_competitor in list_of_matched_competitors:
                                #    print('EEE', subbrand_model_competitor.developer, '|', develoooper, '|', subbrand_model_competitor.name_competitor, '|', comp_brand_model)
                                    if subbrand_model_competitor.developer == develoooper and subbrand_model_competitor.name_competitor == comp_brand_model:
                                        brand_in_develoooper_list.append(subbrand_model_competitor)
                                if brand_in_develoooper_list:
                                #    brand_in_develoooper_dict[comp_brand_model, develoooper] = brand_in_develoooper_list     #{'Cordiant Road Runner': [<CompetitorSiteModel: CompetitorSiteModel object (10966)>,
                                    brand_in_develoooper_dict = { comp_brand_model : brand_in_develoooper_list, develoooper : develoooper }
                                    #print('++--++', brand_in_develoooper_dict.keys())
                                try:
                                    if brand_in_develoooper_dict[develoooper] == develoooper:                           # СВЕРКА ЧАСТОТЫ ПАРСИНГА МОДЕЛЕЙ ДАННОГО ПРОИЗВОДИТЕЛЯ, ВЫБОРКА НАИМю СПАРСЕННЫХ _ ИХ УБРАТЬ ИХ ОБЩЕГО ПЕРЕЧНЯ  list_of_matched_competitors                         
                                        #print(comp_brand_model, 'LLLL111TTTT', brand_in_develoooper_dict[develoooper], 'PP22',  develoooper)
                                        len_comparison_got = len(brand_in_develoooper_dict[comp_brand_model])
                                        #compare_to_delete = len_comparison_got
                                        compare_to_delete = len_comparison_got, brand_in_develoooper_dict[comp_brand_model]
                                        list_to_delete_cometitors_to_compare.append(compare_to_delete)
                                        #brand_in_develoooper_dict_new[comp_brand_model] = brand_in_develoooper_dict[comp_brand_model]
                                except:
                                    pass
                            list_to_delete_cometitors_to_compare = sorted(list_to_delete_cometitors_to_compare, key=lambda x: x[0])     ## !!!! ОТСОРТИРОВАНЫ ПО ЧАСТОТЕ ПАРСИНГА каждого бренда(модели) внутри ДАННОГО ПРОИЗВОДИТЕЛЯ (т.е производитель Cordiant - но у него бренды Comfort 3, Winter Sport2  и т.д)
                            list_to_delete_cometitors_to_compare = list_to_delete_cometitors_to_compare[:-1]    ## Competitorы на удаление из перечня
                            list_to_delete_cometitors_to_compare_with_no_ind_len = []
                            for ind_len, copet_list in list_to_delete_cometitors_to_compare:                    # убираем индексы длины (количества спасенных)
                                list_to_delete_cometitors_to_compare_with_no_ind_len.append(copet_list)
                            #print('Э сюда на111111' , list_to_delete_cometitors_to_compare_with_no_ind_len)                 
                            final_list_to_delete_competitors_in_brand = []                                      # финальный список - очищенный от листов - все непопулярные competitors производителя в одном списке
                            for list_val in list_to_delete_cometitors_to_compare_with_no_ind_len:
                                for item in list_val:
                                    final_list_to_delete_competitors_in_brand.append(item)
                            final_list_to_delete_competitors_in_brand = list(set(final_list_to_delete_competitors_in_brand)) 
                            #print('Э сюда на', final_list_to_delete_competitors_in_brand)
                            list_to_delete_rarely_parsed.extend(final_list_to_delete_competitors_in_brand)          # формируем единый список на удаление
                            #print('list_to_delete_cometitors', list_to_delete_cometitors_to_compare)
                            # убираем непопулярных (реже спашенных модели данного бренда, исключая их из списка общего - останутся лишь производители с одной моделью (у тех производ, у которых было несколько моделей- останется лишь самый спашенный наиболее)):
                        #print('DELETE', list_to_delete_rarely_parsed)
                        for compet_to_delete in list_to_delete_rarely_parsed:
                            list_of_matched_competitors.remove(compet_to_delete)
                        kolesatyt_competitors_dict1[object_unit.tyre] = list_of_matched_competitors           
                    else:       # если у каждого бренда-производителя по одной модели:
                        kolesatyt_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
            except:
        #        print('3. EXCEPTION - KOLESATYT')
                pass

        models.KOLESATYT_COMPETITORS_DICTIONARY1 = kolesatyt_competitors_dict1

        ####### END!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ИЗМЕНЕНИЯ В СЛОВАРЕ - ОСТАВЛЯЕМ ЕСЛИ ЕТЬ НЕСК ШИН ОДНОГО ПРОИЗВОДИТ - ОСТАВИТ С НАИМ ЦЕНОЙ:
        ###### END OF KOLESATYT

#       ## 2 фильтр конкурентов CHEMCURIER:
        try:
            # 1.1 ФИЛЬТР по дате (БЕРЕТСЯ ПОСЛЕДНИЙ ПЕРИОД В ОТЧЕТЕ ХИМКУРЬЕР) # НО - МОЖНО И СДЕЛАТЬ ЗА ПЕРИОД - В MODELS ЕСТЬ РАСЧЕТ НА ПЕРИОДЫ - НУЖНО ТОЛЬКО ЗДЕЬ УБРАТЬ НА ПОСЛ ДАТУ И ЗАДАТЬ ПЕРИОД ОТБОРА
            last_fate_availible_chem = models.ChemCurierTyresModel.objects.latest('data_month_chem').data_month_chem
        #    print('!!!!!!!!!', last_fate_availible_chem, type(last_fate_availible_chem))
            all_competitors_chem = models.ChemCurierTyresModel.objects.filter(data_month_chem=last_fate_availible_chem)     # по дате 
        #    print('last_fate_availible_chem', last_fate_availible_chem, 'all_competitors', all_competitors_chem)
#           # 1.2 ФИЛЬТР список производителей:
            # 1.2.1 - как вариант - выбор из тех производителей - кого ввел пользователь

            list_brands_to_check = []       # набиваем перечень рендов- кого выбрал пользователь
            if models.EXPRESS_SHINA_COMPETITORS:
                list_brands_to_check.extend(models.EXPRESS_SHINA_COMPETITORS)   
            if models.KOLESA_DAROM_COMPETITORS:
                list_brands_to_check.extend(models.KOLESA_DAROM_COMPETITORS) 
            if models.KOLESATYT_COMPETITORS:
                  list_brands_to_check.extend(models.KOLESATYT_COMPETITORS)

            chemcurier_competitors_dict1 = {}
            if list_brands_to_check:       # если бренды выбранные есть - искать по ним:                    !!!!!!!! вариант - отбора как обычно делаем
                all_competitors_chem = all_competitors_chem.filter(producer_chem__in=list_brands_to_check)        # поиск на посл дату в химкурьере по указанным брендам
            else:
                pass                                                                                    # поиск на посл дату в химкурьере 
            for object_unit in list_of_tyre_comparative_objects:
                list_of_matched_competitors = []
                for competitor in all_competitors_chem:  
                    for t_gr in object_unit.tyre.tyre_group.all():
                        if object_unit.tyre.tyre_size.tyre_size == competitor.tyre_size_chem and t_gr == competitor.group_chem and competitor.average_price_in_usd is not None:         # сверка по типоразмеру и группе шин не пустые
                            list_of_matched_competitors.append(competitor)
                chemcurier_competitors_dict1[object_unit.tyre] = list_of_matched_competitors
       #    #####  НАДО СФОРМИРОВАТЬ СЛОВАРЬ С НЕСКОЛЬКИМИ КОНКУРЕНТАМИя 05.12.2022
            models.CHEMCURIER_COMPETITORS_DICTIONARY1 = chemcurier_competitors_dict1  
            #print('models.CHEMCURIER_COMPETITORS_DICTIONARY1 ==', models.CHEMCURIER_COMPETITORS_DICTIONARY1)
            for tt in models.CHEMCURIER_COMPETITORS_DICTIONARY1.values():
                for n in tt:
                    print(n.producer_chem, n.data_month_chem)
        except:
            pass
        ###### END OF CHEMCURIER

        ##################
        ##################
        ##Работа с интефейсом:

        ######## !!!! ПЕРЕСБОРКА ИТОГОВОГО ПЕРЕЧНЯ ОБЪЕКТОВ ДЛЯ ВЫВОДА НА СТРАНИЦУ (только объекты с отфильтрованными конкурентами only):

        express_shina_lengh_list = []
        kolesa_darom_lengh_list = []
        kolesatyt_lengh_list = []
        
        #print('models.ONLINER_COMPETITORS_NAMES_FILTER_IDS ', models.ONLINER_COMPETITORS_NAMES_FILTER_IDS)
        list_of_tyre_comparative_objects_ids = []
        #final_list_of_objects_for_template = []
        final_list_of_objects_for_template = models.ComparativeAnalysisTyresModel.objects.none()
        #print('TTTTTTTTT=====2 list_of_tyre_comparative_objects LEN IS', len(list_of_tyre_comparative_objects),  list_of_tyre_comparative_objects)
        for tt in list_of_tyre_comparative_objects:
        #    print('tt', tt.tyre.tyre_model.model, tt.tyre.tyre_size.tyre_size, tt.sale_data, tt.id, tt) 
            tt.express_shina_competitor_on_date1()
            tt.kolesatyt_competitor_on_date1()
            tt.kolesa_darom_competitor_on_date1()
            express_shina_result = tt.express_shina_table_header()
            kolesatyt_result = tt.kolesatyt_table_header()
            kolesa_darom_result = tt.kolesa_darom_table_header()
            #for yyy in bag_result:
            #    print(yyy)
            chem_result = tt.chemcurier_competitor_on_date1()
            proverka = [('', '', ''), ('', '', ''), ('', '', '')] 
            proverka_chem = ('', '', '')
            if express_shina_result != proverka or kolesatyt_result != proverka or kolesa_darom_result != proverka or chem_result != proverka_chem:
                list_of_tyre_comparative_objects_ids.append(tt.pk)  
            else:
                pass 
            final_list_of_objects_for_template = models.ComparativeAnalysisTyresModel.objects.filter(pk__in=list_of_tyre_comparative_objects_ids).order_by('tyre')  
            #print('ЭЭЭЭЭ=', final_list_of_objects_for_template)
            if express_shina_result:
                express_shina_result_curr_lengh = len(express_shina_result)
                express_shina_lengh_list.append(express_shina_result_curr_lengh)

            if kolesatyt_result:
                kolesatyt_curr_lengh = len(kolesatyt_result)
                kolesatyt_lengh_list.append(kolesatyt_curr_lengh)

            if kolesa_darom_result:
                kolesa_darom_curr_lengh = len(kolesa_darom_result)
                kolesa_darom_lengh_list.append(kolesa_darom_curr_lengh)
            ##### ДОПОЛЛНИТЕЛЬНО К ПЕРЕСБОРКЕ - Т.К. УБРАНА ГАЛОЧКА "ВСЯ ПРОДУКЦИЯ" - ВЫБИРАЕТСЯ АВТОМАТОМ 1-й ИЗ ОБРАБОТАННЫХ ЭЛЕМЕНТОВ ДЛЯ ВЫВОДА:
            if models.SELF_PRODUCTION_FIRST is True and final_list_of_objects_for_template.exists():
            #    print('WTF?')
                break   # обрываем цикл - берем только первого
            if models.DEF_GET is True:
            #    print('=====2')
                models.DEF_GET = False
                break   # обрываем цикл - берем только первого

            ##### ДОПОЛЛНИТЕЛЬНО К ПЕРЕСБОРКЕ - Т.К. УБРАНА ГАЛОЧКА "ВСЯ ПРОДУКЦИЯ" - ВЫБИРАЕТСЯ АВТОМАТОМ 1-й ИЗ ОБРАБОТАННЫХ ЭЛЕМЕНТОВ ДЛЯ ВЫВОДА

        list_of_tyre_comparative_objects = final_list_of_objects_for_template                       # !!  список СomparativeAnalysisTyresModel  у которых отфильтрованы конкуренты
        #print('list_of_tyre_comparative_objects_ids', list_of_tyre_comparative_objects_ids)         # !!  список СomparativeAnalysisTyresModel id у которых отфильтрованы конкуренты
        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects.order_by('tyre__tyre_size__tyre_size')  

        ########END !!!!! ПЕРЕСБОРКА ИТОГОВОГО ПЕРЕЧНЯ

    #### ЗАГОЛОЛОВКИ ТАБЛИЦЫ:
        ## ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ EXPRESS_SHINA: 
        if express_shina_lengh_list: 
            if models.COMPET_PER_SITE:
                express_shina_max_lengh_header = models.COMPET_PER_SITE                                      
            elif express_shina_lengh_list[0] > 3:        
                express_shina_max_lengh_header = 2                            # Количество колонок (обрезает до первых 3)
            else:
                express_shina_max_lengh_header = max(express_shina_lengh_list)
        else:
            express_shina_max_lengh_header = 0

        models.EXPRESS_SHINA_HEADER_NUMBER = express_shina_max_lengh_header

#        print('obj. ===', obj)
        obj = context.get('object')                 ## ДОРАБОТАНО _ ПРИ ОТСУТСТВИИ ВЫБОРА ПРОДУКЦИИ
        obj.express_shina_heders_value()
        #print('obj.express_shina_heders_valuee()', obj.express_shina_heders_value())
        obj.express_shina_heders_lengt() 
        ## END ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ EXPRESS_SHINA:          
        ## ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ KOLESATYT_HEADER_NUMBER: 
        if kolesatyt_lengh_list: 
        #    print('kolesatyt_lengh_list--------------', kolesatyt_lengh_list)
            if models.COMPET_PER_SITE:
                kolesatyt_max_lengh_header = models.COMPET_PER_SITE
            elif kolesatyt_lengh_list[0] > 3:                                # Количество колонок (обрезает до первых 3) 
                kolesatyt_max_lengh_header = 2
            else:
                kolesatyt_max_lengh_header = max(kolesatyt_lengh_list)
        else:
            kolesatyt_max_lengh_header = 0
        models.KOLESATYT_HEADER_NUMBER = kolesatyt_max_lengh_header

        obj.kolesatyt_heders_value()
        obj.kolesatyt_heders_lengt()         
        ##END ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ KOLESATYT: 
        # ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ KOLESA_DAROM: 

        if kolesa_darom_lengh_list:  
            if models.COMPET_PER_SITE:
                kolesa_darom_max_lengh_header = models.COMPET_PER_SITE
            elif kolesa_darom_lengh_list[0] > 3:
                kolesa_darom_max_lengh_header = 2                        # Количество колонок (обрезает до первых 3)
            else:
                kolesa_darom_max_lengh_header = max(kolesa_darom_lengh_list)
        else:
            kolesa_darom_max_lengh_header = 0
            
        models.KOLESA_DAROM_HEADER_NUMBER = kolesa_darom_max_lengh_header

        obj.kolesa_darom_heders_value()
        obj.kolesa_darom_heders_lengt()
        #END ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ KOLESA_DAROM: 
       ## ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ CHEMCURIER: 
        chemcurier_max_lengh_header = 1                                 # chemcurier будет лишь один столбец
        models.CHEMCURIER_HEADER_NUMBER = chemcurier_max_lengh_header
        # print('models.CHEMCURIER_HEADER_NUMBER ====+++==', models.CHEMCURIER_HEADER_NUMBER)
        obj.chemcurier_heders_value()
        obj.chemcurier_heders_lengt()
       ##END ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ CHEMCURIER: 
    #### END ЗАГОЛОЛОВКИ ТАБЛИЦЫ   

        ####### Формы для фильтров темплейта:
        # если применен фильтр:
        # 1) выбрать производителя:

        ### фильтр ПРОРИСОВКА по брендам для темплейт отрисовка чекбоксов:
        brand_names_check_status_list = []
        brand_names = list(dictionaries_models.CompetitorModel.objects.filter(developer_competitor__site__in=['express-shina.ru', 'kolesa-darom.ru', 'kolesatyt.ru']).distinct().values_list("competitor_name", flat=True).order_by('competitor_name'))
        if models.PRODUCER_FILTER_BRAND_LIST_CHECKED_ON:        # если пользовательвыбирал бренды производителей (checked)
            for namee in brand_names:
                if namee in models.PRODUCER_FILTER_BRAND_LIST_CHECKED_ON:
                    name_and_status = namee, 'checked'
                    brand_names_check_status_list.append(name_and_status)
                    context['producer_filter_brand_list_checked__only_3_cheapest_chosen_bage'] = None
                else:
                    name_and_status = namee, ''
                    brand_names_check_status_list.append(name_and_status)

        else:
            for namee in brand_names:
                name_and_status = namee, ''
                brand_names_check_status_list.append(name_and_status)
                context['producer_filter_brand_list_checked__only_3_cheapest_chosen_bage'] = 'бренд не выбран (автоматически предоставлены данные о всех брендах)'
######        print('brand_names_check_status_list1111', brand_names_check_status_list)

        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_IS_NOT_CHOSEN is True:
            context['end_date_is_not_chosen_bage'] = 'конечная дата не выбрана (дата выставлена автоматически)'
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START_IS_NOT_CHOSEN is True:
            context['start_date_is_not_chosen_bage'] = 'начальная дата не выбрана (дата выставлена автоматически)'


        context['producer_filter_brand_list'] = brand_names_check_status_list
        context['producer_filter_brand_list_checked_bage'] = models.PRODUCER_FILTER_BRAND_LIST_CHECKED_ON        # для вплывающей подсказки - значек с выбранными позициями брендов       # для вплывающей подсказки - значек с выбранными позициями брендов
        #context['producer_filter_brand_list'] = list(dictionaries_models.CompetitorModel.objects.filter(developer_competitor__site__in=['express-shina.ru', 'kolesa-darom.ru', 'kolesatyt.ru']).distinct().values_list("competitor_name", flat=True).order_by('competitor_name'))
        
        context['producer_filter_all'] = dictionaries_models.CompetitorModel.objects.all()
        ## END фильтр по брендам для темплейт отрисовка чекбоксов

        # 2) выбрать продукцию:
        ### Отдельная сборка списка всех объеков с конкурентами для меню:
        ##if not models.SELF_PRODUCTION:
        models.FOR_MENU_OBJECTS_LIST = final_list_of_objects_for_template              # постоянный список объектов для отображения в меню
        in_base_tyres_check_status_list = []
        in_base_tyres_check_status_list_checked_bage = []
        #for obj in models.FOR_MENU_OBJECTS_LIST:       old version  
        for obj in table_lookup_only_with_competitors_all_parsed.order_by('tyre__tyre_size__tyre_size'):           # берем для меню вообще все, для кого хоть когда-либо что-то парсилось хоть раз
            if models.SELF_PRODUCTION_ALL:
                objj_and_status = obj, ''
            elif str(obj.id) in models.SELF_PRODUCTION:
                objj_and_status = obj, 'checked'
                in_base_tyres_check_status_list_checked_bage.append(obj)
            else: 

                if list_of_tyre_comparative_objects:                                                       
                    if obj == list_of_tyre_comparative_objects[0]:    # т.к. в template закоменчен выбор всей продукции - то автоматом ставим галочку на первой в списке и выводим ее:
                        #print('zloy pinguin')
                        objj_and_status = obj, 'checked'
                        if models.SELF_PRODUCTION_FIRST is True:
                            if models.SEARCH_USER_REQUEST and search_result_id_is_true:                  # если поиск продукции был через ПОИСК
                                in_base_tyres_check_status_list_checked_bage.append(obj)
                                context['in_base_tyres_list_checked_bage'] = in_base_tyres_check_status_list_checked_bage
                            else:
                                context['no_chosen_production_checked_bage'] = f'продукция не выбрана (автоматически представлены данные по {obj.tyre.tyre_size.tyre_size} {obj.tyre.tyre_model.model})' 
                    else:
                        objj_and_status = obj, ''
                else:    
                    objj_and_status = obj, ''
                    #if obj == list_of_tyre_comparative_objects[0]:
                    #    context['no_chosen_production_checked_bage'] = f'продукция не выбрана (автоматически представлены данные по {obj.tyre.tyre_size.tyre_size} {obj.tyre.tyre_model.model})'

            in_base_tyres_check_status_list.append(objj_and_status)

        if models.SELF_PRODUCTION:
            context['in_base_tyres_list_checked_bage'] = in_base_tyres_check_status_list_checked_bage    # для вплывающей подсказки - значек с выбранными позициями типоразмеров
        context['in_base_tyres'] = in_base_tyres_check_status_list
         ### END Отдельная сборка списка всех объеков с конкурентами для меню

        #######  
        # 3) выбрать группу шин:
        tyr_groups = dictionaries_models.TyreGroupModel.objects.all()
        tyr_groups_check_status_list = []
        tyr_groups_check_status_list_checked_bage = []
        for tyr_gr in tyr_groups:
            #print('tyr_gr.id', tyr_gr.id)
            if models.TYRE_GROUPS_ALL:
                tyr_gr_and_status = tyr_gr, ''
            #if str(tyr_gr.id) in models.TYRE_GROUPS:    
            elif str(tyr_gr.id) in models.TYRE_GROUPS:
                tyr_gr_and_status = tyr_gr, 'checked'
                tyr_groups_check_status_list_checked_bage.append(tyr_gr)
            else:
                tyr_gr_and_status = tyr_gr, ''
            tyr_groups_check_status_list.append(tyr_gr_and_status)
        ##print('tyr_groups', tyr_groups)
        context['in_base_tyres_by_group_checked_bage'] = tyr_groups_check_status_list_checked_bage
        context['in_base_tyres_by_group'] = tyr_groups_check_status_list
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
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START:
            context['chosen_date_start'] = models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0]

        # пагинация самодельная:
        current_pagination_value = models.PAGINATION_VAL
        if current_pagination_value is None:
            current_pagination_value = 10
        pagination_form = forms.PaginationInputForm(initial={'pagination_data': current_pagination_value})
        context['pagination_val_per_form'] = pagination_form        
        #context['current_pagination_value'] = current_pagination_value        
        posts = context['list_of_tyre_comparative_objects']
        #print('1!!!!', len(posts))
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
        #print('!!!!!!!!!!!!!!!0', self.request.GET, self.request.GET.urlencode())
        # END # пагинация самодельная

        # количество выводимых конкурентов на для сайтов:
        current_compet_per_site_value = models.COMPET_PER_SITE
        if current_compet_per_site_value is None:
            current_compet_per_site_value = 2
        compet_per_site_form = forms.CompetitoPerSiteInputForm(initial={'competitor_pagination_data': current_compet_per_site_value})
        context['compet_per_site_form'] = compet_per_site_form
        # END количество выводимых конкурентов на для сайтов:

        currency_input_form = forms.CurrencyDateInputForm()
        context['currency_input_form'] = currency_input_form

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
        # 0. Получаем объекты и их реально офильтрованные по параметрам конкуренты:
        #print('ONLINER_COMPETITORS_NAMES_FILTER_IDS', models.ONLINER_COMPETITORS_NAMES_FILTER_IDS) # ключ - id объета ComparativeAnalysisTyresModel, згначения - список id отфильтрованных конкурентов CompetitorSiteModel

        edyniy_slovar_dict_dlja_pandas_chart_graphic = {}               ##### И.С.Х.О.Д.Н.И.К. Д.Л.Я. О.Т.Р.И.С.О.В.К.И. Г.Р.А.Ф.И.К.А. !!!WARNING IMPORTANT
        spisok_competitors_filtered = []

        for tyre_for_chart_need_all_checked_competitors in list_of_tyre_comparative_objects_ids:
            competitors_ids1 = models.ONLINER_COMPETITORS_NAMES_FILTER_IDS.get(tyre_for_chart_need_all_checked_competitors)
            if competitors_ids1 is None:
                competitors_ids1 = []
            competitors_ids2 = models.AVTOSET_COMPETITORS_NAMES_FILTER_IDS.get(tyre_for_chart_need_all_checked_competitors)
            if competitors_ids2 is None:
                competitors_ids2 = []              
            competitors_ids3 = models.BAGORIA_COMPETITORS_NAMES_FILTER_IDS.get(tyre_for_chart_need_all_checked_competitors)
            if competitors_ids3 is None:
                competitors_ids3 = []
            #for nnit in competitors_ids3:
            #   GICK = models.CompetitorSiteModel.objects.get(id=nnit)
            #   print('GICK', GICK.developer, GICK.date_period) 
            spisok_competitors_filtered = competitors_ids1 + competitors_ids2 + competitors_ids3
            edyniy_slovar_dict_dlja_pandas_chart_graphic[tyre_for_chart_need_all_checked_competitors] = spisok_competitors_filtered   #### !!!!!!!!!!!!!!!!!!!!!! СЛОВАРЬ ДЛЯ ГРАФИКА
        #print('edyniy_slovar_dict_dlja_pandas_chart_graphic == HH', edyniy_slovar_dict_dlja_pandas_chart_graphic)

        ### ЭТАП ПРОВЕРКИ СЛОВАРЯ НА НАЛИЧИЕ ПРОДУКЦИИ РАЗНЫХ ТИПОРАЗМЕРОВ - ЕСЛИ РАЗНЫЕ ТИПОРАЗМЕРЫ - БЕРЕМ ПЕРВЫЙ (И ВСЕ ОДИНАКОВЫЕ С НИМ МОДЕЛИ), ОТСЕИВАЕМ ПРОДУКЦИЮ С ИНЫМ ТИПОРАЗМЕРОМ   
        if not edyniy_slovar_dict_dlja_pandas_chart_graphic:         # если словарь пуст
            pass
        else:                                                        # если словарь не пуст    
            #print('edyniy_slovar_dict_dlja_pandas_chart_graphic.keys() = 1',edyniy_slovar_dict_dlja_pandas_chart_graphic.keys())
            #print('edyniy_slovar_dict_dlja_pandas_chart_graphic.items() = 1',edyniy_slovar_dict_dlja_pandas_chart_graphic.items())
            prod_id_with_same_tyresize_as_the_first_one_list = []
            for prod_id in edyniy_slovar_dict_dlja_pandas_chart_graphic.keys():                     
                production_tyresizes = models.ComparativeAnalysisTyresModel.objects.get(id=prod_id)
                production_tyresizes = production_tyresizes.tyre.tyre_size.tyre_size
                prod_id_and_production_tyresize = prod_id, production_tyresizes
                prod_id_with_same_tyresize_as_the_first_one_list.append(prod_id_and_production_tyresize)        # получаем id и их типоразмер
            #    print('SSUPER_KEY', prod_id, production_tyresizes)
            first_prod_id_tyr_size = prod_id_with_same_tyresize_as_the_first_one_list[0]    # сравним полученное с первым типоразмером
            #print('first_prod_id_tyr_size', first_prod_id_tyr_size)
            id_with_same_tyre_size_as_first_one_list = []
            for d_tyrr_size in prod_id_with_same_tyresize_as_the_first_one_list:
                if d_tyrr_size[1] == first_prod_id_tyr_size[1]:                                 # если одинаковый типоразмер с первым - берем продукцию
                    id_with_same_tyre_size_as_first_one_list.append(d_tyrr_size[0])
            #print('id_with_same_tyre_size_as_first_one_list = IS =', id_with_same_tyre_size_as_first_one_list)
            temorary_id_with_same_tyre_size_as_first_one_dict ={}
            for same_tyr_size_id in id_with_same_tyre_size_as_first_one_list:
                temorary_id_with_same_tyre_size_as_first_one_dict[same_tyr_size_id] = edyniy_slovar_dict_dlja_pandas_chart_graphic.get(same_tyr_size_id)
            #print('temorary_id_with_same_tyre_size_as_first_one_dict.keys() = 2', temorary_id_with_same_tyre_size_as_first_one_dict.keys())
            #print('temorary_id_with_same_tyre_size_as_first_one_dict.items() = 2', temorary_id_with_same_tyre_size_as_first_one_dict.items())

            ## !!! ПЕРЕПИСЫВАНИЕ СЛОВАРЯ = ТОЛЬКО ПРОДУКЦИЯ ОДНОГО ТИПОРАЗМЕРА:
            edyniy_slovar_dict_dlja_pandas_chart_graphic = temorary_id_with_same_tyre_size_as_first_one_dict
            ## END !!! ПЕРЕПИСЫВАНИЕ СЛОВАРЯ = ТОЛЬКО ПРОДУКЦИЯ ОДНОГО ТИПОРАЗМЕРА:

        ### END ЭТАП ПРОВЕРКИ СЛОВАРЯ НА НАЛИЧИЕ ПРОДУКЦИИ РАЗНЫХ ТИПОРАЗМЕРОВ - ЕСЛИ РАЗНЫЕ ТИПОРАЗМЕРЫ - БЕРЕМ ПЕРВЫЙ (И ВСЕ ОДИНАКОВЫЕ С НИМ МОДЕЛИ), ОТСЕИВАЕМ ПРОДУКЦИЮ С ИНЫМ ТИПОРАЗМЕРОМ  


        # НА ПРИМЕРЕ ОДНОГО ОБЪЕКТА: 
        #### ФИЛЬТРАЦИЯ ДАННЫХ ПО ЗАПРОСУ ПОЛЬЗОВАТЕЛЯ:
        # 1. проверка, какие данные введены пользователем:
        # 1.1 каких конкурентов ввел/не ввел пользователь:

        no_data_on_date = False             # отсутствуют данные типоразмеры с конкурентами
        filter_producer = []
        all_filtered_competitors_ids = list(edyniy_slovar_dict_dlja_pandas_chart_graphic.values())
        filtered_competitors_ids_list = []
        for xxy in all_filtered_competitors_ids:
            filtered_competitors_ids_list += xxy
        filtered_competitors_ids_list = list(set(filtered_competitors_ids_list))        # получим только фильтрованные компетиторы
        listt_prodduccers = models.CompetitorSiteModel.objects.filter(id__in=filtered_competitors_ids_list)
        for n in listt_prodduccers:
              n = n.developer.competitor_name
              n = str(n).replace("('", '').replace("',)", '')
              filter_producer.append(n)    
        #=print('filter_producer', filter_producer)         

        # 1.2 какие сайты ввел/не ввел пользователь:
        filter_sites = ['express-shina.ru', 'kolesa-darom.ru', 'kolesatyt.ru'] # #  ['express-shina.ru']     # по дефолту показать этих

        list_off_sizes_to_compare = []                                            # если есть типоразмер - роботаем по нему (шина одна или неск шин одного размера)

        for tyr_sizze in edyniy_slovar_dict_dlja_pandas_chart_graphic.keys():
            production_tyresizes1 = models.ComparativeAnalysisTyresModel.objects.get(id=tyr_sizze)
            production_tyresizes1 = production_tyresizes1.tyre.tyre_size.tyre_size
            list_off_sizes_to_compare.append(production_tyresizes1)
        list_off_sizes_to_compare = set(list_off_sizes_to_compare)  
    #    print('list_off_sizes_to_compare HUSH HUSH HUSH', list_off_sizes_to_compare)
        chart_title = ''
        if len(list_off_sizes_to_compare) == 1:                                     # если есть типоразмер - роботаем по нему (шина одна или неск шин одного размера)     
            object_units = list_of_tyre_comparative_objects.filter(tyre__tyre_size__tyre_size=list(list_off_sizes_to_compare)[0])
            chart_title = object_units[0].tyre.tyre_size.tyre_size
        else:                                                                       # если не 1 типоразмер ИЛИ нет никаких ?? ХМ baby, check this out!
            #print('ГАЛЯ, У НАС ОТМЕНА!!!', type(list_of_tyre_comparative_objects), list_of_tyre_comparative_objects)
            if list_of_tyre_comparative_objects_is_empty is True:                        
                list_of_tyre_comparative_objects = models.ComparativeAnalysisTyresModel.objects.none()    # создать пустой queryset
            #print('GGGGG', list_of_tyre_comparative_objects)            # <QuerySet []> not list []
            if not list_of_tyre_comparative_objects.exists():           #### если объектов с конкурентом на дату нет - для рисовки пустой таблички:
                no_data_on_date = True
                object_units  = [None]
                chart_title = '- нет данных'
            else:
                object_units = list_of_tyre_comparative_objects.filter(tyre__tyre_size__tyre_size=list(list_off_sizes_to_compare)[0])

        # дополнительно даем имена чекбоксам сайтов для графика фильтра: 
        check_box_num = 0    
        for site_name in filter_sites:
            check_box_num += 1
            context[f'site_name'] = site_name, check_box_num

        context['object_unit'] = object_units
        context['filter_producer'] = filter_producer
        context['sites_filter_chart'] = filter_sites
        context['chart_title'] = chart_title

        #### ЕСЛИ модель/типоразмер и 1 ИЛИ несколько объктов ШИН:
        list_of_sites = []                                                                          #(ТИП-2 график по сайтам)            
        list_of_competitors_set = set()
        list_of_competitors = []
        list_start_dates = []
        list_last_dates = []

        for keys, values in edyniy_slovar_dict_dlja_pandas_chart_graphic.items():
            list_of_competts = models.CompetitorSiteModel.objects.filter(pk__in=values)
            for ccomp in list_of_competts:
                list_of_sites.append(ccomp.site)                                                                    #0 получаем наименования всех сайтов для легенды таблицы (ТИП-2 график по сайтам)
                list_of_competitors.append(ccomp.developer.competitor_name)                                         #1 получаем наименования всех конкурентов для легенды таблицы   
            ooobj = models.ComparativeAnalysisTyresModel.objects.get(id=keys)
            start_date = ooobj.price_tyre_to_compare.earliest('date_period').date_period                      #2.1 получаем начальную дату из всех конкурентов  !ПЕРЕПИСАТЬ НА ВВОДИМЫЕ ПОЛЬЩОВАТЕЛЕМ
            #last_date = ooobj.price_tyre_to_compare.latest('date_period').date_period                         #2.2 получаем конечную дату из всех конкурентов   !ПЕРЕПИСАТЬ НА ВВОДИМЫЕ ПОЛЬЩОВАТЕЛЕМ           
            last_date = competitors_exist_all_dates_last_date_latest_date
            list_of_competitors_set = set(list_of_competitors)   
            list_start_dates.append(start_date)
            list_last_dates.append(last_date)

        if no_data_on_date is True:     # если отсутствуют данные типоразмеры с конкурентами
        #    print('models.COMPETITORS_DATE_FROM_USER_ON_FILTERRR', models.COMPETITORS_DATE_FROM_USER_ON_FILTER)
            if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
                chossen_day = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], '%Y-%m-%d').date()
            else:
                chossen_day = datetime.datetime.today()
            list_start_dates.append(chossen_day)
            list_last_dates.append(chossen_day)

        #    min_date = min(list_start_dates)
        #    max_date = max(list_last_dates)

            min_date = min(list_start_dates)                    
            if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                chossen_day_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], '%Y-%m-%d').date()
                min_date = chossen_day_start           
                                                                      
            max_date = max(list_last_dates)  # здесьб д.б. просто данные от пользователя какой день

        else:               # на все остальные случаи - если обект / конкуренты есть на дату:
            if models.ONLY_ON_CURRENT_DATE is True and models.COMPETITORS_DATE_FROM_USER_ON_FILTER:         # если нужно выводить график только на выбранную дату (стои галочка):
                chossen_day = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], '%Y-%m-%d').date()
                list_start_dates.append(chossen_day)
                list_last_dates.append(chossen_day)
            #    min_date = min(list_start_dates)                                                                        # здесьб д.б. просто данные от пользователя какой день
            #    max_date = max(list_last_dates)                  
            #else:
            min_date = min(list_start_dates)                                                                        # здесьб д.б. просто данные от пользователя какой день
            
            if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                #print('!!!!models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START', models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START)
                chossen_day_start = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], '%Y-%m-%d').date()
                min_date = chossen_day_start           
            
            max_date = max(list_last_dates)                                                                         # здесьб д.б. просто данные от пользователя какой день
        
        all_days_in_period = pd.date_range(start=min_date, end=max_date).date 
        #print('all_days_in_period', all_days_in_period)
        list_of_sites = set(list_of_sites)                                                                  #(ТИП-2 график по сайтам) 
        #print('list_of_sites', list_of_sites)                                                               #(ТИП-2 график по сайтам) 
       
       # СОБИРАЕМ ПРЕДВАРИТЕЛЬНЫЙ СПИСОК С ИМЕЮЩИМИСЯ ДАННЫМИ и искуственными пробелами NONE:
                                                         # если нужно получить усредненное значение

        # ПРОВЕРКА - НУЖЕН ГРАФИК ПО ПРОИЗВОДИТЕЛЯМ ЛИБО ПО ПЛОЩАДКАМ:
        if models.GOOGLECHART_MARKETPLACE_ON is False:      # ЕСЛИ НЕ СТОИТ ГАЛОЧКА ПО ПЛОЩАДКАМ - ФОРМИРУЕМ ГРАФИК ПО ПРОИЗВОДИТЕЛЯМ:
            context['marketplace_on_checked'] = ''
            competit_on_current_date_assembled = []                        ###### В ДАННЫЙ СПИСОК И ФОРМИРУЮТСЯ ДАННЫЕ (ВАЖНО-затем работа по этом списку без обращений к объектам)

            new_result_for_comp_dict = {}
 
        if models.GOOGLECHART_MARKETPLACE_ON is False:      # ЕСЛИ НЕ СТОИТ ГАЛОЧКА ПО ПЛОЩАДКАМ - ФОРМИРУЕМ ГРАФИК ПО ПРОИЗВОДИТЕЛЯМ: 
            context['marketplace_on_checked'] = ''
            competit_on_current_date_assembled = []                        ###### В ДАННЫЙ СПИСОК И ФОРМИРУЮТСЯ ДАННЫЕ (ВАЖНО-затем работа по этом списку без обращений к объектам)

            new_result_for_comp_dict = {}

            prices_of_competitors_one_name_producer_dict = {}
            for date_day in all_days_in_period:                                                              
                for object_unit_id, comp_obj_ss_id in edyniy_slovar_dict_dlja_pandas_chart_graphic.items():
                    #print('object_unit_id', object_unit_id, 'comp_obj_ss_id', comp_obj_ss_id)
                    object_unit = models.ComparativeAnalysisTyresModel.objects.get(id=object_unit_id)
                    list_of_competts = models.CompetitorSiteModel.objects.filter(pk__in=comp_obj_ss_id)
                    list_of_competts_name_competitor = list_of_competts.values_list('name_competitor')
                    #print('list_of_competts_name_competitor OT', list_of_competts_name_competitor)
                    # 1. БЛОК ДОРИСОВКИ NULL (ИЛИ 0) ЗНАЧЕНИЙ В ДАТЫ ЕСЛИ ЕСТЬ ХОТЬ ОДНА ДАТА С ТАКИМ ПРОИЗВОДИТЕЛЕМ НА САЙТЕ - сохдание нулевых значений в даты, в которых не получены данные
                    
                    # ТЕКУЩЕЕ РЕШЕНИЕ = БЕРЕМ ВСЕ ЗНАЧЕНИЯ КОНКУРЕНТОВ ПРОИЗВОДИТЕЛЯ С ТАКИМ ИМЕНЕМ И ОСТАВЛЯЕИ МЕНЬШЕЕ
                    #for comp_obj in object_unit.price_tyre_to_compare.all().filter(site__in=filter_sites, developer__competitor_name__in=filter_producer):    # WARNING !!!!!!!!!!!!!!## С.Т.АРЫЙ ВАРИАНТ - РИСОВАТЬ КОНКУРЕНТОВ НА САЙТЕ ДАННОГО ПРОИЗВОДИТЕЛЯ
                    for comp_obj in object_unit.price_tyre_to_compare.all().filter(site__in=filter_sites, developer__competitor_name__in=filter_producer, name_competitor__in=list_of_competts_name_competitor):      # WARNING !!!!!!!!!!!!!!## Н.О.В.Ы.Й. ВАРИАНТ - РИСОВАТЬ КОНКУРЕНТОВ НА САЙТЕ ДАННОГО ПРОИЗВОДИТЕЛЯ ИМЕННО ДАННОЙ МОДЕЛИ
                    
                        #print('comp_obj ==', comp_obj.name_competitor)
                        for comp_name in list_of_competitors_set: 
                           
                            keys_list = comp_name, comp_obj.date_period.strftime("%Y-%m-%d"), comp_obj.site
                            default_values = comp_obj.site, 'null', comp_name                                          #### !!!! null - если нет значения
                            #default_values = comp_obj.site, 0, comp_name                                               #### !!!! null - если нет значения
                            prices_of_competitors_one_name_producer_dict.setdefault(keys_list, default_values)
                            if comp_obj.developer.competitor_name == comp_name:
                                current_val_exist = prices_of_competitors_one_name_producer_dict.get(keys_list)  # если уже существует такая позиция добавим цену в список и возьмем наименьшую для данного производителя     
                                if current_val_exist == default_values:
                                    current_val = comp_obj.price 
                                    prices_of_competitors_one_name_producer_dict[keys_list] = comp_obj.site, current_val, comp_obj.developer.competitor_name
                                else:
                                    cur_site, current_val, cur_comp_name = current_val_exist
                                    min_price = min(current_val, comp_obj.price)
                                    prices_of_competitors_one_name_producer_dict[keys_list] = cur_site, min_price, cur_comp_name
                        # 2. БЛОК ЗАЧИТСКА ОТ ИЗЛИШНЕ ДОРИСОВАННЫХ СОЗДАННЫХ В БЛОКЕ 1 ПУСТЫХ САЙТ/ПРОИЗВОДИТЕЛЬ БЕЗ ЗНАЧЕНИЙ             
            # дополнительно проверяем на наличие созданных пустышек сайт/производитель - если на всем пероде значений нет ни одного - значит, создана пустышка - ее убрать: 
            for ssitte in list_of_sites:
                for compp in list_of_competitors_set:
                    val_exist_data_is_true = True
                    dict_indexes_of_keys_with_no_data_id_list = []
                    for date_day in all_days_in_period:
                        kkey = compp, date_day.strftime("%Y-%m-%d"), ssitte
                        got_value = prices_of_competitors_one_name_producer_dict.get(kkey)
                        if got_value:
                            if got_value[1] != 'null': # если есть хоть одно значение - значит создан не пустой клон сайт/производитель , а реальный - закончить проверку данного производиттеля на сайте
                                dict_indexes_of_keys_with_no_data_id_list = []
                                break
                            else:   
                                dict_indexes_of_keys_with_no_data_id_list.append(kkey)
                                #print(kkey, 'got_value', got_value)
                                val_exist_data_is_true = False

                    #print(dict_indexes_of_keys_with_no_data_id_list, len(dict_indexes_of_keys_with_no_data_id_list))            
                    if val_exist_data_is_true == False:
                        # удаляем созданные пустышки:
                        for kkey in dict_indexes_of_keys_with_no_data_id_list:
                            prices_of_competitors_one_name_producer_dict.pop(kkey)
                    #print('=======')
               
        new_result_for_comp_dict = prices_of_competitors_one_name_producer_dict  

        #for n, nv in prices_of_competitors_one_name_producer_dict.items():      # == приводим в неулюжий вид такого типа: ('WestLake', '2023-08-05', 'express-shina.ru') ['express-shina.ru', 188.48, 0]
        #    print(n, '==++==', nv, 'Takim neschasnym')
            ### ###### ####### ############  
                   
        # 3. БЛОК + ДОПОЛНИТЕЛЬНАЯ ДОРИСОВКА ДАННЫХ УЖЕ НА ВЕСЬ ПЕРИОД _ ЧТОБЫ ПЕРЕДАТЬ В ТЕМПЛАЙТ ОДИНАКОВОЕ ЧИСЛО ДАННЫХ ПО КАЖДОМУ ПРОИЗВОДИТЕЛЮ НА САЙТАХ 
        ############ !!!! ПРОВЕРКА ДОСТАВЛЕНИЕ ДАННЫХ                   Д.О.Р.И.С.О.В.К.А.  Д.А.Н.Н.Ы.Х   WARNING!!!!
        # 1) дата с наибольшим количеством данных
        list_of_inputed_dates = [] 
        list_of_inputed_dates_set = set()
        list_of_inputed_producers = []
        list_of_inputed_producers_set = set()
        list_of_inputed_sites = []
        list_of_inputed_sites_set = set()
        for kkkeyy in prices_of_competitors_one_name_producer_dict.keys(): 
            if kkkeyy[1] in list_of_inputed_dates:
                pass   
            else:
                list_of_inputed_dates.append(kkkeyy[1])
            list_of_inputed_producers.append(kkkeyy[0])
            list_of_inputed_sites.append(kkkeyy[2]) 
        list_of_inputed_dates_set = list_of_inputed_dates
        #print('list_of_inputed_dates_set!', list_of_inputed_dates_set)                                     # list_of_inputed_dates_set!
        list_of_inputed_producers_set = set(list_of_inputed_producers)
        list_of_inputed_sites_set = set(list_of_inputed_sites)

        list_of_existing_prod_in_sites = []     # проверка - был ли производитель на сайте/ на одном- нескольких
        for kkkeeeyy in prices_of_competitors_one_name_producer_dict:
            ppproodducer, sssiitttteee = kkkeeeyy[0], kkkeeeyy[2]
            pr_si = ppproodducer, sssiitttteee
            list_of_existing_prod_in_sites.append(pr_si)
        list_of_existing_prod_in_sites = list(set(list_of_existing_prod_in_sites))

        ##
        list_of_inputed_dates_set_sorted = []     # 1) додабвление (достраивание данных из соседних - из предыдущего дня) если в какое то число не спарсено
        for str_data in list_of_inputed_dates_set:
            some_data = datetime.datetime.strptime(str_data, '%Y-%m-%d').date()
            list_of_inputed_dates_set_sorted.append(some_data)
        
        try:
            if models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START and models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START != ['']:
                from_iser_start_date = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START[0], '%Y-%m-%d').date()
                mmmin = from_iser_start_date
            else:
                mmmin = min(all_days_in_period)                                 ## возьмем отсчет из древнейшей даты в базе вообще НЕОЧЕВИДНОЕ
                mmmax = max(all_days_in_period)
            if models.COMPETITORS_DATE_FROM_USER_ON_FILTER and models.COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                from_iser_end_date = datetime.datetime.strptime(models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0], '%Y-%m-%d').date()
                mmmax = from_iser_end_date
            else:
                mmmin = min(all_days_in_period)                                 ## возьмем отсчет из древнейшей даты в базе вообще НЕОЧЕВИДНОЕ
                mmmax = max(all_days_in_period)
        except:
            mmmin = datetime.datetime.today()
            mmmax = datetime.datetime.today()
        datelist_d_pandas_range = pd.date_range(mmmin, mmmax)
        list_of_dates_with_no_exceptions = []
        for ddatta in datelist_d_pandas_range:
            str_date = ddatta.strftime('%Y-%m-%d')
            list_of_dates_with_no_exceptions.append(str_date)
        ##    
        list_of_inputed_dates_set = list_of_dates_with_no_exceptions            # теперь список дат без выпадающих дат
        #print('list_of_inputed_dates_set', list_of_inputed_dates_set)

        prices_of_competitors_one_name_producer_dict_temporary_with_missing_data = {}
        for date_iz_spiska in list_of_inputed_dates_set:                                        # 2) додабвление 0 в другие дни если нет  данных, но в какое то число хоть раз был конкурент на данном сайте
            for producer_iz_spiska in list_of_inputed_producers_set:
                for site_iz_spiska in list_of_inputed_sites_set:
                    prod_in_site_existed_check = producer_iz_spiska, site_iz_spiska
                    if prod_in_site_existed_check in list_of_existing_prod_in_sites:            # если производитель и сайтодновременно есть в списке(т.е. производитель именно был хоть в какую то дату взят с данного сайта)
                        what_to_look = producer_iz_spiska, date_iz_spiska, site_iz_spiska
                        #print(date_iz_spiska, type(date_iz_spiska), '||', prod_in_site_existed_check)
                        get_data = prices_of_competitors_one_name_producer_dict.get(what_to_look)
                        #print(date_iz_spiska,  '||', prod_in_site_existed_check,   '|==|',  get_data)
                        if get_data:
                            #print(date_iz_spiska,  '||', prod_in_site_existed_check,   '|==|',  get_data)
                            prices_of_competitors_one_name_producer_dict_temporary_with_missing_data[producer_iz_spiska, date_iz_spiska, site_iz_spiska] = get_data
                        else:
                            null_data = site_iz_spiska, 'null', producer_iz_spiska                              ##### !!!! null - если нет значения
                            #null_data = site_iz_spiska, 0, producer_iz_spiska                                  ##### !!!! 0 - если нет значения                        
                            prices_of_competitors_one_name_producer_dict_temporary_with_missing_data[producer_iz_spiska, date_iz_spiska, site_iz_spiska] = null_data 

        # подменяем исходный словарик на словарик с доставленными нулевыми  значениями:
        new_result_for_comp_dict = prices_of_competitors_one_name_producer_dict_temporary_with_missing_data


            ##### УДАЛЕНИЕ ДУБЛЯЖЕЙ_ПРИЗРАКОВ на параллельных сайтах С NULL НА ВСЕМ ОТРЕЗКЕ:
    ##    try:    
        sites_titles_list = []       # список сайтов для проверки
        producer_titles_list = []
        for hhh, oooo in new_result_for_comp_dict.items():
        #    print('hhh, oooo ', hhh, '||', hhh[0], hhh[2], '||', oooo, '||', oooo[1] )
            sites_titles_list.append(hhh[2]), producer_titles_list.append(hhh[0])
        sites_titles_list = list(set(sites_titles_list))
        producer_titles_list = list(set(producer_titles_list))
        #print('sites_titles_list', sites_titles_list, 'producer_titles_list', producer_titles_list)
        # посчитать количество (длину) в словаре:
        some_counter = 0
        one_site_name = None
        one_vrand_name = None 
        if producer_titles_list and sites_titles_list: 
            one_site_name = sites_titles_list[0]     
            one_vrand_name = producer_titles_list[0]  
            for key in new_result_for_comp_dict.keys():
                if key[0] == one_vrand_name and key[2] == one_site_name:
                    #print('OPOPOPO', key)
                    some_counter += 1
    #    print('some_counter is', some_counter)
        #end  посчитать количество (длину) в словаре:           
        # ищем призраки:
        ghost_comp_site_with_only_null_to_delete_from_dict = []     #! список кортежей (Бренд, Сайт) с одними null для удаления как призрак
        for producer_title in producer_titles_list:  
            for sites_title in sites_titles_list:
                null_counter = 0    # расчет количества нулевых значений у сайт-производителя в словаре
                potential_to_delete = []        #набиваем нулевыми данного производителя на данном сайте - если их количество равно длине всего периода (some_counter is) - помечаем их на удаление внося в ghost_comp_site_with_only_null_to_delete_from_dict
                for key, val in new_result_for_comp_dict.items():   
                    if key[0] == producer_title and key[2] == sites_title:   
                        if val[1] == 'null':
                            null_counter += 1
                            potential_to_delete.append(key)
                        #    print('null_counter', null_counter, '-----', 'val[1]', val[1], key[0], key[2])
                        if null_counter == some_counter:      # если количество null значений у всех позиций сайт-производителя в словаре - он пустой призрак
                        #    print('777')
                            #ghost_comp_site_with_only_null_to_delete_from_dict.append((key[0], key[2])) # Cordiant express-shina.ru
                            ghost_comp_site_with_only_null_to_delete_from_dict.extend(potential_to_delete) 

        # удаление призраков из словаря (пересоздание словаря):
        new_result_for_comp_dict_temporary_keys_to_delete_list = []
        for key, val in new_result_for_comp_dict.items():
            for bbrand_ghost_site_ghost in ghost_comp_site_with_only_null_to_delete_from_dict: 
                #if key[0] == bbrand_ghost_site_ghost[0] and key[2] == bbrand_ghost_site_ghost[1]:
                if key == bbrand_ghost_site_ghost:
                #    print('key[0]', key[0], 'bbrand_ghost_site_ghost[0]', bbrand_ghost_site_ghost[0], 'key[2]', key[2], 'bbrand_ghost_site_ghost[1]', bbrand_ghost_site_ghost[1])
                #    print('key', key, 'val', val)
                    #print("ШОККОНТЕНТ")
                    new_result_for_comp_dict_temporary_keys_to_delete_list.append(key)
        for key_to_delete in new_result_for_comp_dict_temporary_keys_to_delete_list:
            new_result_for_comp_dict.pop(key_to_delete)           
            ##### END УДАЛЕНИЕ ДУБЛЯЖЕЙ_ПРИЗРАКОВ на параллельных сайтах С NULL НА ВСЕМ ОТРЕЗКЕ:

        ############ END !!!! ПРОВЕРКА ДОСТАВЛЕНИЕ ДАННЫХ 

        #print('all_days_in_period', all_days_in_period)

        if models.WEIGHTED_AVERAGE_ON == False:                             # ЕСЛИ НЕ НУЖНО ВЫВОДИТЬ СРЕДНЕВЗВЕШЕННОЕ
            context['weighted_average_checked'] = ''
            list_for_formating = []
            position_couner = None          # понадобится для определени номера позиции с значением цены в словаре для заполнения пустых None в дальнейшем  
            for ddate in all_days_in_period:
            #    print('==========', ddate)
                small_list_for_formating = []
                for k, v in new_result_for_comp_dict.items():     ### !!!!!!              
                    if ddate.strftime("%Y-%m-%d") == k[1]:
                        #if v[1]:
                        put_data = k[0], k[1], v[1], v[0]             # [['JONWICK', '2023-04-05', None,  # 'express-shina.ru',]   ['SAMURAI', '2023-04-19', 750.0, # 'kolesa-darom.ru']]
                        put_data = list(put_data)
                        position_couner = put_data.index(v[1])
                        small_list_for_formating.append(put_data)
            #    print('=======', small_list_for_formating)
                list_for_formating.append(small_list_for_formating)
            ##print('list_for_formating1', list_for_formating)
        else:                             # ЕСЛИ НУЖНО ВЫВОДИТЬ СРЕДНЕВЗВЕШЕННОЕ
            context['weighted_average_checked'] = 'checked'
            list_for_formating = []
            position_couner = None          ## понадобится для определени номера позиции с значением цены в словаре для заполнения пустых None в дальнейшем     
            for ddate in all_days_in_period: 
                small_list_for_formating = []    
                for compet in list_of_competitors_set:                 # УСРЕДНЕННОЕ ПО ПРОИЗВОДИТЕЛЮ !!!!!!!!!!!!!!!!!!!  
                    #print('MENTOR!')    
                    devvider = 0                                           # УСРЕДНЕННОЕ ПО ПРОИЗВОДИТЕЛЮ !!!!!!!!!!!!!!!!!!!   
                    weighted_average_val = 0                               # УСРЕДНЕННОЕ ПО ПРОИЗВОДИТЕЛЮ !!!!!!!!!!!!!!!!!!
                    list_of_sites = []
                    for k, v in new_result_for_comp_dict.items():     ### !!!!!!          
                        if ddate.strftime("%Y-%m-%d") == k[1] and compet == k[0]:
                            devvider += 1 
                            #print('v[1]', v[1], 'VZO', v, 'KTO', k)
                            perman_val = 0
                            if v[1] is None or v[1] == 'null':
                               perman_val = 0 
                            else:
                                perman_val = v[1]
                            #print('weighted_average_val', weighted_average_val, 'devvider', devvider)
                            list_of_sites.append(v[0])
                            weighted_average_val += perman_val
                            put_data = k[0], k[1], weighted_average_val, f'средневзвешенная по сайтам: {list_of_sites}'            # [['JONWICK', '2023-04-05', None,  # 'express-shina.ru']   ['SAMURAI', '2023-04-19', 750.0, # 'kolesa-darom.ru']]
                            put_data = list(put_data)
                            #########print('put_data', put_data)
                            position_couner = put_data.index(weighted_average_val)
                    ##print ('put_data', put_data, 'devvider:', devvider)
                    if put_data[position_couner] and devvider:
                        put_data[position_couner] = put_data[position_couner] / devvider
                    else:
                        put_data[position_couner] = None
                    #print ('put_data', put_data, 'devvider:', devvider) 
                    small_list_for_formating.append(put_data)   
                #print('=======', small_list_for_formating)
                list_for_formating.append(small_list_for_formating)
            #print('list_for_formating2!', list_for_formating)

        ### ЕСЛИ НУЖНО ВЫВОДИТЬ ГРФАИК С ДОРИСОВАННЫМИ ЛИНИЯМИ :
        if models.FULL_LINED_CHART_ON == False:  
            context['full_lined_chart_checked'] = '' 
        else: 
            context['full_lined_chart_checked'] = 'checked' 
            context['full_lined_chart_checked_flag'] = 'true'
        ### END ЕСЛИ НУЖНО ВЫВОДИТЬ ГРФАИК С ДОРИСОВАННЫМИ ЛИНИЯМИ

        competit_on_current_date_assembled = list_for_formating ### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   
        #for n in competit_on_current_date_assembled:
        #    print('fall behind====', n)   

        ## т.к. list_for_formating и затем competit_on_current_date_assembled - создает пустые дубляжи производителя для каждого сайта ( например,['Кама', '2023-08-02', None, 'express-shina.ru'], ['Кама', '2023-08-02', None, 'express-shina.ru'])
        ## исключим те дубляжи , по которым созданы на иных сайтах копии
        #print('!!!', list_for_formating)

        # ЕСЛИ ЗНАЧЕНИЕ + NONE - ПОИСК ДАННЫХ В ДАТАХ РАНЬШЕ И ПРИРАВНИВАНИЕ К НИМ:
        complided_data_len = 0  # проверка все ли части равны
        complided_data_len_el = None
        if competit_on_current_date_assembled:
            complided_data_len = len(competit_on_current_date_assembled[0])  
            #complided_data_len_el = len(competit_on_current_date_assembled[0][0]) - 1 
            #print('complided_data_len', complided_data_len)             # количество списков на дату
        all_parts_are_equal = False      
        for complided_data in competit_on_current_date_assembled:
            complided_data_len_got = len(complided_data)
            if complided_data_len_got == complided_data_len:
                all_parts_are_equal = True

        #competit_on_current_date_assembled = list(reversed(competit_on_current_date_assembled))       # развернуть список чтобы начинать с последней даты

        #print('len(competit_on_current_date_assembled)', len(competit_on_current_date_assembled))
        #print('competit_on_current_date_assembled', competit_on_current_date_assembled) #
        whole_list_legh = len(competit_on_current_date_assembled)
        if position_couner:
            for perr_val in competit_on_current_date_assembled:
                #print('perr_val', perr_val)                                                    #[['JONWICK', '2023-03-20', None, 'express-shina.ru'], ['JONWICK', '2023-03-20', None, 'kolesa-darom.ru'], ['SAMURAI', '2023-03-20', None, 'kolesa_darom.ru'], ['SAMURAI', '2023-03-20', None, 'kolesa-darom.ru']]
                curr_perr_val_index = competit_on_current_date_assembled.index(perr_val)        #curr_perr_val_index 0
                #print('curr_perr_val_index',curr_perr_val_index)
                for ell in perr_val:
                    #print('ell', ell)                                                          # ell ['SAMURAI', '2023-04-20', 150.0, 'express-shina.ru']
                    curr_ell_val_index = perr_val.index(ell)                                    # curr_ell_val_index 3              
                    val = ell[position_couner]
                    #print('val===', val)
                    #curr_val_index = ell.index(val)                                            #здесь индекс и так нам известен = он всегда равен значению position_couner
                    if val is None:                                                             # если значение  None, поиск в впредыдущих позициях дат этого производителя
                    #    print('curr_perr_val_index!!!!',curr_perr_val_index)
                        curr_perr_val_index_none = curr_perr_val_index
                        while curr_perr_val_index_none < whole_list_legh:                           
                            get_prev_val = competit_on_current_date_assembled[curr_perr_val_index_none][curr_ell_val_index][position_couner]
                            curr_perr_val_index_none += 1
                            #print('get_prev_val', get_prev_val, 'curr_ell_val_index', curr_ell_val_index)
                            if get_prev_val:
                                val = get_prev_val
                                break
                        if val is None:     # если не найдены значения в других периодах
                        #    val = 0
                            val = 'null'
                        competit_on_current_date_assembled[curr_perr_val_index][curr_ell_val_index][position_couner] = val
                #print('perr_val', perr_val)
                

                
    #    # END ЕСЛИ ЗНАЧЕНИЕ + NONE - ПОИСК ДАННЫХ В ДАТАХ РАНЬШЕ И ПРИРАВНИВАНИЕ К НИМ                  
        #for n in competit_on_current_date_assembled:
        #    print('fall behind', n)     

        # СОБИРЕМ СЛОВАРИ ДЛЯ ПЕРЕЧАЧИ В КОНТНЕКСТ, ДАЛЕЕ В СКРИПТ:
        assembles_to_dict_data_dict = {}
        assembles_to_dict_data_dict['competitor_producer_names'] = {}
        assembles_to_dict_data_dict['dates'] = {}
        assembles_to_dict_data_dict['competitor_values'] = {}
        list_of_dates = []
        for lists_values in competit_on_current_date_assembled:
        #    print('!', lists_values,'LENGTH = ', len(lists_values))    #! [('Cordiant', None, None), ('LingLong', None, None), ('iLink', None, None), ('Michelin', '20.03.2023', 351.1), ('Arivo', None, None)] LENGTH =  
            list_of_competitor_producer_names = []
            for vall in lists_values:
                #print('vall ', vall)
                if vall[3]:                                             # если указываются данные о сайте и производителе
                    comb_name = vall[0], ' ', vall[3] 
                    comb_name = ''.join(comb_name)
                    #print('comb_name', comb_name)
                    list_of_competitor_producer_names.append(comb_name)
                else:
                    list_of_competitor_producer_names.append(vall[0])  
                #list_of_competitor_producer_names.append(vall[0])    
            for vall in lists_values:
                list_of_dates.append(vall[1])
                break
            #print(list_of_dates)
            assembles_to_dict_data_dict['competitor_producer_names'] = list_of_competitor_producer_names
            assembles_to_dict_data_dict['dates'] = list_of_dates
        

        #print('competit_on_current_date_assembled 999', competit_on_current_date_assembled)    
        list_of_competitor_values = []
        list_of_competitor_values_new_dict = {}

        if no_data_on_date is True:     # если отсутствуют данные типоразмеры с конкурентами
            #print('kogda mne temno gromko gruppu KINO', all_days_in_period)
            for date_in in all_days_in_period:
                year, month, day = int(date_in.strftime('%Y')), int(date_in.strftime('%m')), int(date_in.strftime('%d'))
                date_prepared_or_js = year, month-1, day   # СДВИГ -1 ДЛЯ ОТОБРАЖЕНИЯ В ГРАФИКЕ     #  
                list_of_competitor_values_new_dict[date_prepared_or_js] = ['null']

            context['competitor_names'] = ['']
            context['competitor_values'] = ['']

        else:
            chart_data_counter = 0                                              # подмешиваем дату строкой как  # [1,  37.8, 80.8, 41.8], -
            if assembles_to_dict_data_dict['dates']:
                number_of_periods = len(assembles_to_dict_data_dict['dates'])                         # old =number_of_periods== 5 ['20.03.2023', '20.03.2023', '20.03.2023', '20.03.2023', '20.03.2023']       
                #print('number_of_periods==', number_of_periods, assembles_to_dict_data_dict['dates'])      
                for lists_values in competit_on_current_date_assembled:
                    #print('chart_data_counter', chart_data_counter, assembles_to_dict_data_dict['dates'][chart_data_counter], '==', lists_values)
                    list_of_period_competitor_values = [] 
                #    print('::::::::', 'chart_data_counter:', chart_data_counter, '  ', assembles_to_dict_data_dict['dates'])
                    list_of_period_competitor_values.append(assembles_to_dict_data_dict['dates'][chart_data_counter])
                    list_of_period_competitor_values_new = [] 
                    date_in_str = datetime.datetime.strptime(assembles_to_dict_data_dict['dates'][chart_data_counter], '%Y-%m-%d').date()
                    year, month, day = int(date_in_str.strftime('%Y')), int(date_in_str.strftime('%m')), int(date_in_str.strftime('%d'))
                    date_prepared_or_js = year, month-1, day        # СДВИГ -1 ДЛЯ ОТОБРАЖЕНИЯ В ГРАФИКЕ     #                   
                    list_of_period_competitor_values_new.append(date_prepared_or_js)
                    if chart_data_counter < number_of_periods-1:
                        chart_data_counter += 1
                    for vall in lists_values:
                        list_of_period_competitor_values.append(vall[2])
                        list_of_period_competitor_values_new.append(vall[2])
                    #per_val = list_of_period_competitor_values[ 1 :]   
                    list_of_competitor_values.append(list_of_period_competitor_values)
                    #print('list_of_period_competitor_values_new', list_of_period_competitor_values_new)

                    list_to_tuple = list_of_period_competitor_values_new[1:]
                    list_of_competitor_values_new_dict[list_of_period_competitor_values_new[0]] = list_to_tuple

            assembles_to_dict_data_dict['competitor_values'] = list(list_of_competitor_values) 

    #        print('!  ', assembles_to_dict_data_dict['competitor_producer_names'])
            if not assembles_to_dict_data_dict['competitor_producer_names']:
                context['competitor_names'] = ['нет данных']
            else:
                context['competitor_names'] = assembles_to_dict_data_dict['competitor_producer_names']
    #            print('GGGOOODDD 1', context['competitor_names'])
            
            if not assembles_to_dict_data_dict['competitor_values']:
    #            print('EERR 1')
                context['competitor_values'] = [[' ', 'null']]
            else:
                context['competitor_values'] = assembles_to_dict_data_dict['competitor_values']
    #            print('GGGOOODDD 2', context['competitor_values'])

        if not list_of_competitor_values_new_dict:
    #        print('END 0 ===== list_of_competitor_values_new_dict', list_of_competitor_values_new_dict)
            context['list_of_competitor_values_new'] = {(' '): ['null']}
        else:            
            context['list_of_competitor_values_new'] = list_of_competitor_values_new_dict  
    #        print('GGGOOODDD 3', context['list_of_competitor_values_new'])

        #### END  ТЕСТОВАЯ ШТУКА ДЛЯ ГРАФИКОВ PANDAS
        
        #### КРУГОВОЙ ГРАФИК КОЛИЧЕСТВО СПАРСЕННЫХ ДАННЫХ С САЙТА: PANDAS
        final_parsed_data_from_sites = []
        parsed_data_from_sites = ['Сайт', 'Количество спарсенных конкурентов']
        final_parsed_data_from_sites.append(parsed_data_from_sites)
        filter_sites = ['express-shina.ru', 'kolesa-darom.ru', 'kolesatyt.ru']
        final_parsed_data_from_sites_whole = 0
        date_to_look_parsed_data = datetime.datetime.now().date()
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
            date_to_look_parsed_data = models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0]
            date_to_look_parsed_data = datetime.datetime.strptime(date_to_look_parsed_data, '%Y-%m-%d').date()

        for sitess in filter_sites:
            get_data_from_site_number = len(models.CompetitorSiteModel.objects.filter(date_period=date_to_look_parsed_data).filter(site=sitess))  # .filter(site__in=filter_sites))
            final_parsed_data_from_sites_whole = final_parsed_data_from_sites_whole + get_data_from_site_number
            to_put_in_list_data = sitess, get_data_from_site_number
            to_put_in_list_data = list(to_put_in_list_data)
            final_parsed_data_from_sites.append(to_put_in_list_data)
            #print('final_parsed_data_from_sites_whole', final_parsed_data_from_sites_whole)
            
        date_to_look_parsed_data = date_to_look_parsed_data.strftime('%d.%m.%Y')
        context['final_parsed_data_from_sites_whole'] = final_parsed_data_from_sites_whole   
        context['final_parsed_data_from_sites'] = final_parsed_data_from_sites
        context['final_parsed_data_from_sites_data'] = date_to_look_parsed_data
        #### END  КРУГОВОЙ ГРАФИК КОЛИЧЕСТВО СПАРСЕННЫХ ДАННЫХ С САЙТА: PANDAS

        #### ГРАФИК КОЛИЧЕСТВО СПАРСЕННЫХ ДАННЫХ ПО БРЕНДУ С САЙТОВ: PANDAS
        all_parsed_brands_developers_queryset = dictionaries_models.CompetitorModel.objects.order_by('competitor_name').values_list('competitor_name', flat=True).distinct()        ### Фильтр уникальных!
        date_to_look_parsed_data = datetime.datetime.now().date()
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
            date_to_look_parsed_data = models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0]
            date_to_look_parsed_data = datetime.datetime.strptime(date_to_look_parsed_data, '%Y-%m-%d').date()
        list_of_parrsed_brands_sites = []
        quantity_counter = 0
        for brand in all_parsed_brands_developers_queryset: 
            num_of_parsed_brand_express_shina = models.CompetitorSiteModel.objects.filter(developer__competitor_name=brand, date_period=date_to_look_parsed_data, site='express-shina.ru').count()
            num_of_parsed_brand_kolesa_darom = models.CompetitorSiteModel.objects.filter(developer__competitor_name=brand, date_period=date_to_look_parsed_data, site='kolesa-darom.ru').count()
            num_of_parsed_brand_kolesatyt = models.CompetitorSiteModel.objects.filter(developer__competitor_name=brand, date_period=date_to_look_parsed_data, site='kolesatyt.ru').count()

            total_quantity = num_of_parsed_brand_express_shina + num_of_parsed_brand_kolesa_darom + num_of_parsed_brand_kolesatyt        # для сортировки по наибольшему кол-ву спарсенных с сайтов

            brand_quantity_per_site = brand, num_of_parsed_brand_express_shina, num_of_parsed_brand_kolesa_darom, num_of_parsed_brand_kolesatyt, total_quantity 
            list_of_parrsed_brands_sites.append(list(brand_quantity_per_site))
            quantity_counter += 1
        list_of_parrsed_brands_sites = sorted(list_of_parrsed_brands_sites, key=itemgetter(4), reverse=True) # сортируем по наиб количеству спарсенных

        top_brands_counter_for_chart = 0
        if quantity_counter == 10 or quantity_counter > 10:               # ели брендов более 10 - то берем то 10
            top_brands_counter_for_chart = 10
        elif quantity_counter < 10 and quantity_counter > 0:
            top_brands_counter_for_chart = quantity_counter
        else:
            top_brands_counter_for_chart = 'лист без данных'
        context['top_brands_num'] = top_brands_counter_for_chart

        date_to_look_parsed_data = date_to_look_parsed_data.strftime('%d.%m.%Y')
        context['brands_from_sites_date'] = date_to_look_parsed_data
        list_of_parrsed_brands_sites = ','.join(str(x[0:4]) for x in list_of_parrsed_brands_sites) # !!!!!!! ДРУГОЙ ВАРИАНТ ПЕРЕДАЧИ ДАННЫХ
        #print('!!!', list_of_parrsed_brands_sites)
        context['brands_from_sites'] = list_of_parrsed_brands_sites

        #### END ГРАФИК КОЛИЧЕСТВО СПАРСЕННЫХ ДАННЫХ ПО БРЕНДУ С САЙТОВ: PANDAS


        #### ГРАФИК КОЛИЧЕСТВО СПАРСЕННЫХ ДАННЫХ ПО ТИПОРАЗМЕРУ С САЙТОВ: PANDAS
    #    all_parsed_tyresizes_developers_queryset = dictionaries_models.TyreSizeModel.objects.order_by('tyre_size').values_list('tyre_size', flat=True).distinct()        ### Фильтр уникальных!
        all_parsed_tyresizes_developers_queryset = models.CompetitorSiteModel.objects.order_by('tyresize_competitor').values_list('tyresize_competitor', flat=True).distinct()        ### Фильтр уникальных!
        date_to_look_parsed_data = datetime.datetime.now().date()
        if models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
            date_to_look_parsed_data = models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0]
            date_to_look_parsed_data = datetime.datetime.strptime(date_to_look_parsed_data, '%Y-%m-%d').date()
        list_of_parrsed_tyresize_sites = []
        quantity_counter = 0
        for ttyyrr_sizze in all_parsed_tyresizes_developers_queryset: 
            num_of_parsed_tyresize_express_shina = models.CompetitorSiteModel.objects.filter(tyresize_competitor=ttyyrr_sizze, date_period=date_to_look_parsed_data, site='express-shina.ru').count()
            num_of_parsed_tyresize_kolesa_darom = models.CompetitorSiteModel.objects.filter(tyresize_competitor=ttyyrr_sizze, date_period=date_to_look_parsed_data, site='kolesa-darom.ru').count()
            num_of_parsed_tyresize_kolesatyt = models.CompetitorSiteModel.objects.filter(tyresize_competitor=ttyyrr_sizze, date_period=date_to_look_parsed_data, site='kolesatyt.ru').count()

            total_quantity = num_of_parsed_tyresize_express_shina + num_of_parsed_tyresize_kolesa_darom + num_of_parsed_tyresize_kolesatyt        # для сортировки по наибольшему кол-ву спарсенных с сайтов

            tyresize_quantity_per_site = ttyyrr_sizze, num_of_parsed_tyresize_express_shina, num_of_parsed_tyresize_kolesa_darom, num_of_parsed_tyresize_kolesatyt, total_quantity 
            list_of_parrsed_tyresize_sites.append(list(tyresize_quantity_per_site))
            quantity_counter += 1
        list_of_parrsed_tyresize_sites = sorted(list_of_parrsed_tyresize_sites, key=itemgetter(4), reverse=True) # сортируем по наиб количеству спарсенных

        top_tyresizes_counter_for_chart = 0
        if quantity_counter == 10 or quantity_counter > 10:               # ели типоразмеров более 10 - то берем то 10
            top_tyresizes_counter_for_chartt = 10
        elif quantity_counter < 10 and quantity_counter > 0:
            top_tyresizes_counter_for_chart = quantity_counter
        else:
            top_tyresizes_counter_for_chart = 'лист без данных'
        context['top_tyresizes_num'] = top_tyresizes_counter_for_chart

        date_to_look_parsed_data = date_to_look_parsed_data.strftime('%d.%m.%Y')
        context['tyresizes_from_sites_date'] = date_to_look_parsed_data
        list_of_parrsed_tyresize_sites = ','.join(str(x[0:4]) for x in list_of_parrsed_tyresize_sites) # !!!!!!! ДРУГОЙ ВАРИАНТ ПЕРЕДАЧИ ДАННЫХ
        context['tyresizes_from_sites'] = list_of_parrsed_tyresize_sites

        #### END ГРАФИК КОЛИЧЕСТВО СПАРСЕННЫХ ДАННЫХ ПО ТИПОРАЗМЕРУ  С САЙТОВ: PANDAS

        return context             

class ComparativeAnalysisTableModelRussiaUpdateView(View):

    def post(self, request):
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
        models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START = []

        ### СБРОС СЛОВАРЕЙ
        models.EXPRESS_SHINA_COMPETITORS_NAMES_FILTER_IDS = {}
        models.KOLESATYT_COMPETITORS_NAMES_FILTER_IDS = {}
        models.KOLESA_DAROM_COMPETITORS_NAMES_FILTER_IDS = {}
        ### END СБРОС СЛОВАРЕЙ

        ## 1 работа с периодами:
        comparative_model_parcing_date = request.POST.getlist('parcing_date') 
        #print('comparative_model_parcing_date', comparative_model_parcing_date , type(comparative_model_parcing_date))

        if comparative_model_parcing_date and comparative_model_parcing_date != ['']:
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER = comparative_model_parcing_date
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_IS_NOT_CHOSEN = False


        comparative_model_parcing_date_start = request.POST.getlist('parcing_date_start') 
        if comparative_model_parcing_date_start and comparative_model_parcing_date_start != ['']:
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START = comparative_model_parcing_date_start
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START_IS_NOT_CHOSEN = False


        if comparative_model_parcing_date == [''] and comparative_model_parcing_date_start == ['']:
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER = [datetime.date.today().strftime('%Y-%m-%d')]      # автоматически ставит дату на сегодня
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_IS_NOT_CHOSEN = True
            
            today_is = datetime.date.today()                                                                # автоматически ставит дату на неделю назад
            week_ago_date = today_is - datetime.timedelta(days=7)
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START = [week_ago_date.strftime('%Y-%m-%d')]
            models.COMPETITORS_DATE_FROM_USER_ON_FILTER_START_IS_NOT_CHOSEN = True

        #### 1.1 ПЕРИОД ДЛЯ КУРСА ВАЛЮТ:
        chosen_date_for_currency_year = request.POST.getlist('chosen_date_for_currency_year') 
        chosen_date_for_currency_month = request.POST.getlist('chosen_date_for_currency_month') 
        chosen_date_for_currency_day = request.POST.getlist('chosen_date_for_currency_day') 
        chosen_date_for_currency = chosen_date_for_currency_year + chosen_date_for_currency_month + chosen_date_for_currency_day
        if chosen_date_for_currency:
            #print('chosen_date_for_currency1', chosen_date_for_currency)  
            chosen_date_for_currency = '-'.join(str(x) for x in chosen_date_for_currency)
        #    print('chosen_date_for_currency', chosen_date_for_currency)             # 'parcing_date': ['2023-03-14'],  chosen_date_for_currency 2022-1-30
            check_date = datetime.datetime.strptime(chosen_date_for_currency, "%Y-%m-%d").date()        #  если пользователем введена дана превышающая текущую для получения курса валют то нао скинуть на сегодня:
            if check_date > datetime.datetime.now().date():
                pass
            else:
                models.CURRENCY_DATE_GOT_FROM_USER = chosen_date_for_currency
                models.CURRENCY_ON_DATE is True
#
        # 2-й работа с группами шин:
        tyre_groups_list_all = request.POST.getlist('self_production_group_id_all')
        tyre_groups_list = request.POST.getlist('self_production_group_id')
        if tyre_groups_list_all:
            #print(tyre_groups_list_all, 'tyre_groups_list_all')
            models.TYRE_GROUPS_ALL= tyre_groups_list_all
        else:
            #print(tyre_groups_list, 'tyre_groups_list')
            models.TYRE_GROUPS = tyre_groups_list 

        ## 3 работа с собственной продукцией:
        production_tyres_list_all = request.POST.getlist('self_production_all')  
        production_tyres_list = request.POST.getlist('self_production')                      # фильтр по собственным шинам
        if production_tyres_list_all:
            models.SELF_PRODUCTION_ALL = production_tyres_list_all
            models.SELF_PRODUCTION = production_tyres_list
            # дополнительно - для вывода первого, если не выбрано ничего (# т.к. в template закоменчен выбор всей продукции - то автоматом ставим галочку на первой в списке и выводим ее):
            models.SELF_PRODUCTION_FIRST = False
        if production_tyres_list:
            models.SELF_PRODUCTION = production_tyres_list
            models.SELF_PRODUCTION_FIRST = False
        else:               # если нечего не выбрано:
            models.SELF_PRODUCTION_ALL = production_tyres_list_all
            models.SELF_PRODUCTION_FIRST = True #тип нужен будет первый элемент с конкурентом - для вывода первого, если не выбрано ничего (# т.к. в template закоменчен выбор всей продукции - то автоматом ставим галочку на первой в списке и выводим ее)

        ### ЕСЛИ ПОЛЬЗОВАТЬЕЛЬ ИЩЕТ ЧЕРЕЗ ПОИСК:
        production_tyres_list_one = request.POST.getlist('product_search')
        ##print('show me', production_tyres_list_one)
        if production_tyres_list_one:
            models.SEARCH_USER_REQUEST = production_tyres_list_one

        # 4 работа с производителями-конкурентами (бренды)
        all_express_shina_kolesa_darom_kolesatyt_chemcurier_competitors_list_all = request.POST.getlist('producers_all')
        express_shina_kolesa_darom_kolesatyt_chemcurier_competitors_list = request.POST.getlist('producer_filter_brand_list')                               # фильтр конкурентов
        if all_express_shina_kolesa_darom_kolesatyt_chemcurier_competitors_list_all:
        #if not express_shina_kolesa_darom_kolesatyt_chemcurier_competitors_list:
            models.EXPRESS_SHINA_KOLESATYT_KOLESA_DAROM_ALL_BRANDS_CHOSEN = all_express_shina_kolesa_darom_kolesatyt_chemcurier_competitors_list_all
            models.PRODUCER_FILTER_BRAND_LIST_CHECKED_ON = False
            pass
        else:
            #print('express_shina_kolesa_darom_kolesatyt_chemcurier_competitors_list', express_shina_kolesa_darom_kolesatyt_chemcurier_competitors_list)
            models.EXPRESS_SHINA_COMPETITORS = express_shina_kolesa_darom_kolesatyt_chemcurier_competitors_list
            models.KOLESATYT_COMPETITORS = express_shina_kolesa_darom_kolesatyt_chemcurier_competitors_list
            models.KOLESA_DAROM_COMPETITORS = express_shina_kolesa_darom_kolesatyt_chemcurier_competitors_list
            #models.CHEMCURIER_COMPETITORS = express_shina_kolesa_darom_kolesatyt_chemcurier_competitors_list
            # для отрисовки галочек checkeDd  выбранной прподукции:
            producer_filter_brand_list_got = express_shina_kolesa_darom_kolesatyt_chemcurier_competitors_list
            #print('producer_filter_brand_list_got', producer_filter_brand_list_got)
            if producer_filter_brand_list_got:
                #print('producer_filter_brand_list_got Y', producer_filter_brand_list_got)
                models.PRODUCER_FILTER_BRAND_LIST_CHECKED_ON = producer_filter_brand_list_got
            else:
                #print('producer_filter_brand_list_got N', producer_filter_brand_list_got)
                models.PRODUCER_FILTER_BRAND_LIST_CHECKED_ON = False
            models.EXPRESS_SHINA_KOLESATYT_KOLESA_DAROM_ALL_BRANDS_CHOSEN = False

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
            #print('pagination_data_got', pagination_data_got)
            models.PAGINATION_VAL = int(request.POST.get('pagination_data'))
        else:
            pass

        # 6. 1 работа с вводимыми данными по количеству выводимых конкурентов на сайте для объекта таблице
        competitor_pagination_data_got = request.POST.get('competitor_pagination_data')  
        #print('competitor_pagination_data_got', competitor_pagination_data_got)
        if competitor_pagination_data_got:
            #print('competitor_pagination_data_got', competitor_pagination_data_got)
            models.COMPET_PER_SITE = int(request.POST.get('competitor_pagination_data'))
        else:
            pass

        # 8 работа проверкой график по средневзвешенной цене на рынке/в разрезе торговых площадок
        weighted_average_got = request.POST.get('weighted_average')
        if weighted_average_got:
            #print('weighted_average_got Y', weighted_average_got)
            models.WEIGHTED_AVERAGE_ON = True
        else:
            #print('weighted_average_got N', weighted_average_got)
            models.WEIGHTED_AVERAGE_ON = False

        # 9 работа проверкой - нужен вывод графика c дорисованными линиями
        full_lined_chart_got = request.POST.get('full_lined_chart')
        if full_lined_chart_got:
            #print('full_lined_chart_got Y', full_lined_chart_got)
            models.FULL_LINED_CHART_ON = True
        else:
            #print('full_lined_chart_got N', full_lined_chart_got)
            models.FULL_LINED_CHART_ON = False
            
        return HttpResponseRedirect(reverse_lazy('prices:comparative_prices_russia'))
    


def running_programm():

    belarus_sites_parsing()
    #russia_sites_parsing()
    print('script is running')


    return 'the programm is fullfilled'



if __name__ == "__main__":
    running_programm()

>>>>>>> new_branch
