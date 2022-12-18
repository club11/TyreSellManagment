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

                    values = price_cleaned, tyresize, product_name, tyre_param, company_name, season, studded 
                    goods_dict[tyre_name_cleaned] = values
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
                    #print('TTTT', k)                                                                                            #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
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
       ###### ЗДЕСЬ СВЯЗЫВАЕМ СПАРСЕННЫЕ ОБЕКТЫ КОНКУРЕНТОВ К ОБЪЕКТАМИ ШИН В БАЗЕ МОДЕЛИ ШИНЫ СРАВНЕНИЕ                        ! ВАЖНО - привязка моделей в бд к моделям спарсенным с сайта по критериям
       #  1 -Я ВЕРСИЯ _ ПРОСТО ПО ТИПОРАЗМЕРУ ВСЕ:        
        #for objject in models.CompetitorSiteModel.objects.all():
        #    price_tyre_obj = models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=objject.tyresize_competitor)
        #    for n in list(price_tyre_obj):
        #        objject.tyre_to_compare.add(n) 

       #  2 -Я ВЕРСИЯ ПО ТИПОРАЗМЕРУ, ИНДЕКСАМ, СЕЗОННОСТИ:
        #for objject in models.CompetitorSiteModel.objects.all():
            #if objject.season:
            #    print('objject.tyre__added_features__season_usage', objject.season.season_usage_name)
            #price_tyre_obj = models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=objject.tyresize_competitor)
            #for n in list(price_tyre_obj): 
            ## 2) совмещаем конкурентов с шинами в базе по сезонности:
            #    competior_is_found = False
            #    if n.tyre.added_features.all():
            #        tyre_in_base_season = n.tyre.added_features.all()[0].season_usage 
            #        tyre_in_base_index = n.tyre.added_features.all()[0].indexes_list
            #        if objject.season:
            #            if tyre_in_base_season.season_usage_name == objject.season.season_usage_name and tyre_in_base_index == objject.parametres_competitor:       # 1)  1. совмещаем конкурентов с шинами в базе по сезонности  и индексам:
            #                objject.tyre_to_compare.add(n)
            #                print('МЯКОТКА МЯКОТКА МЯКОТКА МЯКОТКА')
            #                continue                        
            ###            if tyre_in_base_season.season_usage_name == objject.season.season_usage_name:                                                               # 2) 2. если нет, то совмещаем конкурентов с шинами в базе по сезонности
            ###                objject.tyre_to_compare.add(n)
            ###                continue
            #            if tyre_in_base_index == objject.parametres_competitor:                                                                                     # 3) 3. если нет, то  совмещаем конкурентов с шинами в базе по индексам:
            #                objject.tyre_to_compare.add(n)
            #                continue
            #        competior_is_found = True
            #    if competior_is_found == False:
            #        objject.tyre_to_compare.add(n)                                                                                                                  # 4) если нет, то совмещаем конкурентов с шинами в базе просто потипоразмерно
                                                                                                                                                                                                         
        ##### END OF ONLINER PARSING
        return comparative_analysis_table

    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        obj = context.get('object')
        list_of_tyre_comparative_objects = obj.comparative_table.all()

        ## 1 фильтр конкурентов Onliner:
        all_competitors = models.CompetitorSiteModel.objects.all()
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
                        #print("На пол шишечки", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
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

        ##Работа с интефейсом:
        #list_of_all_competitors_template = []
        #for t in all_competitors:
        #    list_of_all_competitors_template.append(t.developer.competitor_name)
        #context['onliner_competitors'] = list(set(list_of_all_competitors_template))
        list_of_all_competitors_template = []
        all_competitors_in_base = dictionaries_models.CompetitorModel.objects.all()
        for t in all_competitors_in_base:
            list_of_all_competitors_template.append(t.competitor_name)
        context['onliner_competitors'] = list(set(list_of_all_competitors_template))
        ###

        filter_form = forms.FilterForm
        context['filter_form'] = filter_form

        return context


class ComparativeAnalysisTableModelUpdateView(View):

    def post(self, request):
        print(request.POST, 'TTT')

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


