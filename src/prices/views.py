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

                    values = price_cleaned, tyresize, product_name, tyre_param, company_name 
                    goods_dict[tyre_name_cleaned] = values
        #for k, v in goods_dict.items():
        #    print(k, v)
        #print(goods_dict.items())

        # формируем отдельный список ПРОИЗВОДИТЕЛИ:
        onliner_companies_list = []  # список компаний-производителей Oliner
        for v in goods_dict.values():
            if v[4] and v[4].isdigit() is False:
                onliner_companies_list.append(v[4])
        onliner_companies_list = list(set(onliner_companies_list))    

        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые модели шин для работы в таблице:
        if models.ONLINER_COMPETITORS:
            onliner_companies_list = models.ONLINER_COMPETITORS

        chosen_by_company_dict = {}
        for k, v in goods_dict.items():
            if v[4] and v[4] in onliner_companies_list:                 # СЕЙЧАС ВЫДАЕТ ВСЕХ ПРОИЗВОДИТЕЛЕЙ  ВСЕЮ ПРОДУКЦИЮ или подкинутых пользователем
                chosen_by_company_dict[k] = v
        #print('chosen_by_company_dict', chosen_by_company_dict)

        # сопоставление с БД  и запись в БД конкурентов (Onliner):
        tyres_in_bd = tyres_models.Tyre.objects.all()
        for tyre in tyres_in_bd:
            for k, v in chosen_by_company_dict.items():
                if tyre.tyre_size.tyre_size == v[1]:
                    #print('TTTT', k)                                                                                            #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
                    #Cordiant Polar SL 205/55R16 94T ('165,00', '205/55R16', 'Cordiant Polar SL', '94T', 'Cordiant')
                    coma = v[0].find(',')
                    pr = float
                    if coma:
                        pr = float(v[0].replace(',', '.'))
                    models.CompetitorSiteModel.objects.update_or_create(
                        site = 'onliner.by',
                        #tyre = tyre,
                        currency = dictionaries_models.Currency.objects.get(currency='BYN'),
                        price = pr,
                        date_period = datetime.datetime.today(),
                        developer = v[4],
                        tyresize_competitor = v[1],
                        name_competitor = v[2],
                        parametres_competitor = v[3]
                    ) 
        ##### END OF ONLINER PARSING
        return comparative_analysis_table

    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        obj = context.get('object')
        list_of_tyre_comparative_objects = obj.comparative_table.all()


        # выбор по производителю:                               
        # ФИЛЬТР 4  - задаваемые модели шин для работы в таблице:
        if models.ONLINER_COMPETITORS:
            onliner_companies_list = models.ONLINER_COMPETITORS

        chosen_by_company_dict = {}
        for k, v in goods_dict.items():
            if v[4] and v[4] in onliner_companies_list:                 # СЕЙЧАС ВЫДАЕТ ВСЕХ ПРОИЗВОДИТЕЛЕЙ  ВСЕЮ ПРОДУКЦИЮ или подкинутых пользователем
                chosen_by_company_dict[k] = v
        #print('chosen_by_company_dict', chosen_by_company_dict)







        ## 1 фильтр конкурентов Onliner:
        all_competitors = models.CompetitorSiteModel.objects.all()
            # 1.1 ФИЛЬТР по дате
        #  all_competitors = models.CompetitorSiteModel.objects.filter(date_period=datetime.date(2022, 11, 22))       # по дате 
            # 1.2 ФИЛЬТР список производителей :
        onliner_companies_list = []
        for t in all_competitors:
            onliner_companies_list.append(t.developer)
        onliner_companies_list = list(set(onliner_companies_list))
        #print(onliner_companies_list[0:3], 'onliner_companies_list[0:3]', onliner_companies_list)

        ###################################################################################################         ВВОД ПОЛЬЗОВАТЕЛЕМ КОЛИЧЕСТВА ПРОИЗВОДИТЕЛЕЙ:
        ##############nuber_of_chosen_competitors_input_user = int
        ##############if nuber_of_chosen_competitors_input_user:
        ##############    nuber_of_chosen_competitors_input_user = 3                                                                  # по производителю (НАПРИМЕР, ПО 3 ПЕРВЫЕ В СПИСКЕ ПРОИЗВОДИТЕЛЕЙ 
        ##############    all_competitors = models.CompetitorSiteModel.objects.filter(developer__in=onliner_companies_list[0:nuber_of_chosen_competitors_input_user])      # по производителю (НАПРИМЕР, ПО 3 ПЕРВЫЕ В СПИСКЕ ПРОИЗВОДИТЕЛЕЙ )
        ##############else:
        ##############    all_competitors = models.CompetitorSiteModel.objects.all()
        ###################################################################################################

        #for t in all_competitors:
        #    print(t.developer, t.tyresize_competitor, t.price, 'YYYTTTTTTTT')
        ##

        onliner_competitors_dict1 = {}

        for object_unit in list_of_tyre_comparative_objects:
            object_unit.planned_profitabilit = object_unit.planned_profitability()
            object_unit.direct_cost_varianc = object_unit.direct_cost_variance()

            list_of_matched_competitors = []
            for competitor in all_competitors:
                if object_unit.tyre.tyre_size.tyre_size == competitor.tyresize_competitor:
                    #print("На пол шишечки", competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price,)
                    #onliner_competitors_dict[object_unit.tyre] = competitor.tyresize_competitor, competitor.name_competitor, competitor.parametres_competitor, competitor.price

                    list_of_matched_competitors.append(competitor)
            onliner_competitors_dict1[object_unit.tyre] = list_of_matched_competitors

        #print('!!!!', onliner_competitors_dict1)
        # ПОЛУЧАЕМ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО КОНКУРЕННЫХ ШИН ДЛЯ ПЕРЕДАЧИ ЧИСЛА В МОДЕЛЬ для ОТРИСОВКИ ЗАГОЛОВКОВ СТОЛБЦОВ ONLINER: 
        onliner_max_lengh_list = []
        for value in onliner_competitors_dict1.values():
            lengh = len(value)
            onliner_max_lengh_list.append(lengh)
        onliner_max_lengh_header = max(onliner_max_lengh_list)
        #print('max_competitors_tyres', onliner_max_lengh_header)
        #for k, v in onliner_competitors_dict1.items():
        #    print(k, v)

                                                                        ######  НАДО СФОРМИРОВАТЬ СЛОВАРЬ С НЕСКОЛЬКИМИ КОНКУРЕНТАМИя 05.12.2022
        #models.ONLINER_COMPETITORS_DICTIONARY = onliner_competitors_dict  
        models.ONLINER_COMPETITORS_DICTIONARY1 = onliner_competitors_dict1  
        models.ONLINER_HEADER_NUMBER = onliner_max_lengh_header
        #object_unit.onliner_competitor_on_date()
        #object_unit.onliner_competitor_price_on_date()
        #object_unit.price_902_onliner_deflection()

        object_unit.onliner_competitor_on_date1()
        obj.onliner_heders_value()
        #object_unit.onliner_competitor_price_on_date1()
        context['list_of_tyre_comparative_objects'] = list_of_tyre_comparative_objects

        ##Работа с интефейсом:
        list_of_all_competitors_template = []
        for t in all_competitors:
            list_of_all_competitors_template.append(t.developer)
        context['onliner_competitors'] = list_of_all_competitors_template
        ###

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
        print('onliner_competitors_list', onliner_competitors_list)
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
        else:
            models.ONLINER_COMPETITORS = onliner_competitors_list


        return HttpResponseRedirect(reverse_lazy('prices:comparative_prices'))
