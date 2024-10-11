from django.db import models
from dictionaries import models as dictionaries_models
from tyres import models as tyres_model
from django.urls import reverse
import pandas as pd

from django.contrib.auth import get_user_model
User = get_user_model()

import datetime

ONLINER_COMPETITORS_DICTIONARY1 = {}
ONLINER_HEADER_NUMBER = int
#ONLINER UPDATEVIEW:
ONLINER_COMPETITORS = []
ONLINER_COMPETITORS_NAMES_FILTER = []
ONLINER_COMPETITORS_NAMES_FILTER_IDS = {}           # id отфильтрованных для template точно подошедших конкурентов  #НУ ХЗ -ПЕРЕДЕЛАТЬ!
ONLINER_HEADER_DICT = {}

AVTOSET_COMPETITORS = []
AVTOSET_COMPETITORS_DICTIONARY1 = {}
AVTOSET_HEADER_NUMBER = int
AVTOSET_COMPETITORS_NAMES_FILTER = []
AVTOSET_COMPETITORS_NAMES_FILTER_IDS = {}
AVTOSET_HEADER_DICT = {}

BAGORIA_COMPETITORS = []
BAGORIA_COMPETITORS_DICTIONARY1 = {}
BAGORIA_HEADER_NUMBER = int
BAGORIA_COMPETITORS_NAMES_FILTER = []
BAGORIA_COMPETITORS_NAMES_FILTER_IDS = {}
BAGORIA_HEADER_DICT = {}

CHEMCURIER_COMPETITORS = []
CHEMCURIER_COMPETITORS_DICTIONARY1 = {}
CHEMCURIER_HEADER_NUMBER = int

ONL_AVT_BAG_ALL_BRANDS_CHOSEN = None

SELF_PRODUCTION = []
SELF_PRODUCTION_ALL = []
SELF_PRODUCTION_FIRST = True
COMPETITORS_DATE_FROM_USER_ON_FILTER = []
COMPETITORS_DATE_FROM_USER_ON_FILTER_START = False
TYRE_GROUPS = []
TYRE_GROUPS_ALL=[]
COMPETITORS_DATE_FROM_USER_ON_FILTER_IS_NOT_CHOSEN = False
COMPETITORS_DATE_FROM_USER_ON_FILTER_START_IS_NOT_CHOSEN = False

DEFLECTION_VAL = None
PAGINATION_VAL = None
COMPET_PER_SITE = 2
# ______ RUS_____

EXPRESS_SHINA_COMPETITORS = []
EXPRESS_SHINA_COMPETITORS_DICTIONARY1 = {}
EXPRESS_SHINA_HEADER_NUMBER = int
EXPRESS_SHINA_COMPETITORS_NAMES_FILTER = []
EXPRESS_SHINA_COMPETITORS_NAMES_FILTER_IDS = {}
EXPRESS_SHINA_HEADER_DICT = {}

KOLESATYT_COMPETITORS = []
KOLESATYT_COMPETITORS_DICTIONARY1 = {}
KOLESATYT_HEADER_NUMBER = int
KOLESATYT_COMPETITORS_NAMES_FILTER = []
KOLESATYT_COMPETITORS_NAMES_FILTER_IDS = {}
KOLESATYT_HEADER_DICT = {}

KOLESA_DAROM_COMPETITORS = []
KOLESA_DAROM_COMPETITORS_DICTIONARY1 = {}
KOLESA_DAROM_HEADER_NUMBER = int
KOLESA_DAROM_COMPETITORS_NAMES_FILTER = []
KOLESA_DAROM_COMPETITORS_NAMES_FILTER_IDS = {}
KOLESA_DAROM_HEADER_DICT = {}

EXPRESS_SHINA_KOLESATYT_KOLESA_DAROM_ALL_BRANDS_CHOSEN = None

SEARCH_USER_REQUEST = None

CURRENCY_DATE_GOT_FROM_USER = None
CURRENCY_DATE_GOT_FROM_USER_CLEANED = None
CURRENCY_IS_CLEANED = None
CURRENCY_VALUE_RUB = None
CURRENCY_VALUE_USD = None

CURRENCY_ON_DATE = False

GOOGLECHART_MARKETPLACE_ON = False
WEIGHTED_AVERAGE_ON = False
FULL_LINED_CHART_ON = False
ONLY_ON_CURRENT_DATE = False


FOR_MENU_OBJECTS_LIST = [] # список объектов для вывода в меню (шины с конкурентами)
PRODUCER_FILTER_BRAND_LIST_CHECKED_ON = False

DEF_GET = True    # первый запуск страницы (не POST запос,а GET)

SCRIPT_IS_RUNNING = False


class PlannedCosstModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='planned_costs',
        on_delete=models.CASCADE,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='prices_currency',
        on_delete=models.CASCADE,
    )
    price = models.FloatField(
        verbose_name='плановая себестоимость',
        blank=True,
        default=0,
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True,    
    )

    def get_absolute_url(self):
        return reverse('prices:planned_cost')
    
    def __str__(self):
        return str(self.price)

class SemiVariableCosstModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='semi_variable_costs',
        on_delete=models.CASCADE,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='semi_variable_prices_currency',
        on_delete=models.CASCADE,
    )
    price = models.FloatField(
        verbose_name='прямые затраты',
        blank=True,
        default=0
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True,    
    )

    def get_absolute_url(self):
        return reverse('prices:semi_variable_planned_cost')
    
    def __str__(self):
        return str(self.price)

class Belarus902PriceModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='belarus902price',
        on_delete=models.CASCADE,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='belarus902currency',
        on_delete=models.CASCADE,
    )
    price = models.FloatField(
        verbose_name='прейскуранты №№9, 902',
        blank=True,
        default=0
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True,    
    )

    def get_absolute_url(self):
        return reverse('prices:belarus902price')
    
    def __str__(self):
        return str(self.price)

class TPSRussiaFCAModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='tpsrussiafcaprice',
        on_delete=models.CASCADE,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='tpsrussiafcacurrency',
        on_delete=models.CASCADE,
    )
    price = models.FloatField(
        verbose_name='ТПС РФ FCA',
        blank=True,
        default=0
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True,    
    )

    def get_absolute_url(self):
        return reverse('prices:tpsrussiafca')
    
    def __str__(self):
        return str(self.price)

class TPSKazFCAModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='tpskazfcaprice',
        on_delete=models.CASCADE,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='tpskazfcacurrency',
        on_delete=models.CASCADE,
    )
    price = models.FloatField(
        verbose_name='ТПС Казахстан FCA',
        blank=True,
        default=0
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True,    
    )

    def get_absolute_url(self):
        return reverse('prices:tpskazfca')
    
    def __str__(self):
        return str(self.price)

class TPSMiddleAsiaFCAModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='tpsmiddleasiafcaprice',
        on_delete=models.CASCADE,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='tpsmiddleasiafcacurrency',
        on_delete=models.CASCADE,
    )
    price = models.FloatField(
        verbose_name='ТПС Средняя Азия, Закавказье, Молдова FCA',
        blank=True,
        default=0
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True,    
    )

    def get_absolute_url(self):
        return reverse('prices:tpsmiddleasiafca')
    
    def __str__(self):
        return str(self.price)

class CurrentPricesModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='currentpricesprice',
        on_delete=models.CASCADE,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='currentpricescurrency',
        on_delete=models.CASCADE,
    )
    price = models.FloatField(
        verbose_name='Действующие цены',
        blank=True,
        default=0
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True,    
    )

    def get_absolute_url(self):
        return reverse('prices:currentprices')
    
    def __str__(self):
        return str(self.price)

class ComparativeAnalysisTableModel(models.Model):
    customer = models.ForeignKey(
        User,
        verbose_name='Таблица сравнительного анализа',
        related_name='comparative_analysis_table',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    market_table = models.CharField(
        verbose_name='рынок сбыта',
        max_length=35,
        blank=True,
        null=True
    )

    def onliner_heders_value(self):                 # для расчета количества столбцов с заголовками под данные Onliner
        #print('ONLINER_HEADER_NUMBER', ONLINER_HEADER_NUMBER)
        onliner_header_1 = 'конкурент Onliner'
        onliner_header_2 = 'цена конкурента Onliner'
        onliner_header_3 = 'отклонение цены конкурента Onliner'
        list_onliner_main_headers = []
        for header_number in range(0, ONLINER_HEADER_NUMBER):
            onliner_main_header = onliner_header_1, onliner_header_2, onliner_header_3
            list_onliner_main_headers.append(onliner_main_header)
        return list_onliner_main_headers

    def onliner_heders_lengt(self):                 # для расчета длинны столбца с заголовками под данные Avtoset
        avtoset_header_2 = 'цена конкурента Onliner'
        head_lengh = 0
        for header_number in range(0, ONLINER_HEADER_NUMBER):
            if avtoset_header_2:
                head_lengh += 3   
        return head_lengh        
        
    def avtoset_heders_value(self):                 # для расчета количества столбцов с заголовками под данные Avtoset
        #print('AVTOSET_HEADER_NUMBER', AVTOSET_HEADER_NUMBER)
        avtoset_header_1 = 'конкурент Atoset'
        avtoset_header_2 = 'цена конкурента Atoset'
        avtoset_header_3 = 'отклонение цены конкурента Atoset'
        list_avtoset_main_headers = []
        for header_number in range(0, AVTOSET_HEADER_NUMBER):
            avtoset_main_header = avtoset_header_1, avtoset_header_2, avtoset_header_3       
            list_avtoset_main_headers.append(avtoset_main_header)  
        return list_avtoset_main_headers

    def avtoset_heders_lengt(self):                 # для расчета длинны столбца с заголовками под данные Avtoset
        avtoset_header_2 = 'цена конкурента Atoset'
        head_lengh = 0
        for header_number in range(0, AVTOSET_HEADER_NUMBER):
            if avtoset_header_2:
                head_lengh += 3   
        #print(head_lengh)
        return head_lengh
        
    def bagoria_heders_value(self):                 # для расчета количества столбцов с заголовками под данные Bagoria
        #print('BAGORIA_HEADER_NUMBER', BAGORIA_HEADER_NUMBER)
        bagoria_header_1 = 'конкурент Bagoria'
        bagoria_header_2 = 'цена конкурента Bagoria'
        bagoria_header_3 = 'отклонение цены конкурента Bagoria'
        list_bagoria_main_headers = []
        for header_number in range(0, BAGORIA_HEADER_NUMBER):
            bagoria_main_header = bagoria_header_1, bagoria_header_2, bagoria_header_3
            list_bagoria_main_headers.append(bagoria_main_header)
        #print('list_bagoria_main_headers =====================kjhdkfjdsjkhj', list_bagoria_main_headers)
        return list_bagoria_main_headers

    def bagoria_heders_lengt(self):                 # для расчета длинны столбца с заголовками под данные Avtoset
        avtoset_header_2 = 'цена конкурента Bagoria'
        head_lengh = 0
        for header_number in range(0, BAGORIA_HEADER_NUMBER):
            if avtoset_header_2:
                head_lengh += 3   
        return head_lengh   

    def express_shina_heders_value(self):                 # для расчета количества столбцов с заголовками под данные express_shina
        #print('EXPRESS_SHINA_HEADER_NUMBER', EXPRESS_SHINA_HEADER_NUMBER)
        express_shina_header_1 = 'конкурент express_shina'
        express_shina_header_2 = 'цена конкурента express_shina'
        express_shina_header_3 = 'отклонение цены конкурента express_shina'
        list_express_shina_main_headers = []
        for header_number in range(0, EXPRESS_SHINA_HEADER_NUMBER):
            express_shina_main_header = express_shina_header_1, express_shina_header_2, express_shina_header_3
            list_express_shina_main_headers.append(express_shina_main_header)
        return list_express_shina_main_headers
    
    def express_shina_heders_lengt(self):                 # для расчета длинны столбца с заголовками под данные express_shina
        express_shina_header_2 = 'цена конкурента express_shina'
        head_lengh = 0
        for header_number in range(0, EXPRESS_SHINA_HEADER_NUMBER):
            if express_shina_header_2:
                head_lengh += 3   
        return head_lengh 
    
    def kolesatyt_heders_value(self):                 # для расчета количества столбцов с заголовками под данные kolesatyt
        #print('KOLESATYT_HEADER_NUMBER', KOLESATYT_HEADER_NUMBER)
        kolesatyt_header_1 = 'конкурент kolesatyt'
        kolesatyt_header_2 = 'цена конкурента kolesatyt'
        kolesatyt_header_3 = 'отклонение цены конкурента kolesatyt'
        list_kolesatyt_main_headers = []
        for header_number in range(0, KOLESATYT_HEADER_NUMBER):
            kolesatyt_main_header = kolesatyt_header_1, kolesatyt_header_2, kolesatyt_header_3
            list_kolesatyt_main_headers.append(kolesatyt_main_header)
        return list_kolesatyt_main_headers
    
    def kolesatyt_heders_lengt(self):                 # для расчета длинны столбца с заголовками под данные kolesatyt
        kolesatyt_header_2 = 'цена конкурента kolesatyt'
        head_lengh = 0
        for header_number in range(0, KOLESATYT_HEADER_NUMBER):
            if kolesatyt_header_2:
                head_lengh += 3   
        return head_lengh 
    
    def kolesa_darom_heders_value(self):                 # для расчета количества столбцов с заголовками под данные kolesa_darom
        #print('KOLESA_DAROM_HEADER_NUMBER', KOLESA_DAROM_HEADER_NUMBER)
        kolesa_darom_header_1 = 'конкурент kolesa_darom'
        kolesa_darom_header_2 = 'цена конкурента kolesa_darom'
        kolesa_darom_header_3 = 'отклонение цены конкурента kolesa_darom'
        list_kolesa_darom_main_headers = []
        for header_number in range(0, KOLESA_DAROM_HEADER_NUMBER):
            kolesa_darom_main_header = kolesa_darom_header_1, kolesa_darom_header_2, kolesa_darom_header_3
            list_kolesa_darom_main_headers.append(kolesa_darom_main_header)
        return list_kolesa_darom_main_headers

    def kolesa_darom_heders_lengt(self):                 # для расчета длинны столбца с заголовками под данные kolesa_darom
        kolesa_darom_header_2 = 'цена конкурента kolesa_darom'
        head_lengh = 0
        for header_number in range(0, KOLESA_DAROM_HEADER_NUMBER):
            if kolesa_darom_header_2:
                head_lengh += 3   
        return head_lengh 

    def chemcurier_heders_value(self):                 # для расчета количества столбцов с заголовками под данные Chemcurier
        #print('CHEMCURIER_HEADER_NUMBER', CHEMCURIER_HEADER_NUMBER)
        chemcurier_header_1 = 'конкурент Chemcurier'
        chemcurier_header_2 = 'цена конкурента Chemcurier, USD'
        chemcurier_header_3 = 'цена конкурента Chemcurier, BYN'
        chemcurier_header_4 = 'отклонение цены конкурента Chemcurier'
        chemcurier_header_5 = 'посл.период отчета в Chemcurier'
        list_chemcurier_main_headers = []
        for header_number in range(0, CHEMCURIER_HEADER_NUMBER):
            chemcurier_main_header = chemcurier_header_1, chemcurier_header_2, chemcurier_header_3, chemcurier_header_4, chemcurier_header_5
            list_chemcurier_main_headers.append(chemcurier_main_header)
        #print('list_chemcurier_main_headers =====================kjhdkfjdsjkhj', list_chemcurier_main_headers)
        return list_chemcurier_main_headers

    def chemcurier_heders_lengt(self):                 # для расчета длинны столбца с заголовками под данные Avtoset
        chemcurier_header_2 = 'цена конкурента Chemcurier'
        head_lengh = 0
        for header_number in range(0, CHEMCURIER_HEADER_NUMBER):
            if chemcurier_header_2:
                head_lengh += 5   
        return head_lengh   

#____RUS____

    def express_shina_heders_value(self):                 # для расчета количества столбцов с заголовками под данные EXPRESS_SHINA
        #print('EXPRESS_SHINA_HEADER_NUMBER', EXPRESS_SHINA_HEADER_NUMBER)
        express_shina_header_1 = 'конкурент EXPRESS_SHINA'
        express_shina_header_2 = 'цена конкурента EXPRESS_SHINA'
        express_shina_header_3 = 'отклонение цены конкурента EXPRESS_SHINA'
        list_express_shina__main_headers = []
        for header_number in range(0, EXPRESS_SHINA_HEADER_NUMBER):
            express_shina_main_header = express_shina_header_1, express_shina_header_2, express_shina_header_3
            list_express_shina__main_headers.append(express_shina_main_header)
        #print('list_express_shina_main_headers =====================kjhdkfjdsjkhj', list_express_shina__main_headers)
        return list_express_shina__main_headers

    def express_shina_heders_lengt(self):                 # для расчета длинны столбца с заголовками под данные EXPRESS_SHINA
        express_shina_2 = 'цена конкурента EXPRESS_SHINA'
        head_lengh = 0
        for header_number in range(0, EXPRESS_SHINA_HEADER_NUMBER):
            if express_shina_2:
                head_lengh += 3   
        return head_lengh   

    def kolesatyt_heders_value(self):                 # для расчета количества столбцов с заголовками под данные KOLESATYT
        #print('KOLESATYT_HEADER_NUMBER', KOLESATYT_HEADER_NUMBER)
        kolesatyt_header_1 = 'конкурент KOLESATYT'
        kolesatyt_header_2 = 'цена конкурента KOLESATYT'
        kolesatyt_header_3 = 'отклонение цены конкурента KOLESATYT'
        list_kolesatyt__main_headers = []
        for header_number in range(0, KOLESATYT_HEADER_NUMBER):
            kolesatyt_main_header = kolesatyt_header_1, kolesatyt_header_2, kolesatyt_header_3
            list_kolesatyt__main_headers.append(kolesatyt_main_header)
        #print('list_kolesatyt_main_headers =====================kjhdkfjdsjkhj', list_kolesatyt__main_headers)
        return list_kolesatyt__main_headers

    def kolesatyt_heders_lengt(self):                 # для расчета длинны столбца с заголовками под данные KOLESATYT
        kolesatyt_2 = 'цена конкурента KOLESATYT'
        head_lengh = 0
        for header_number in range(0,  KOLESATYT_HEADER_NUMBER):
            if kolesatyt_2:
                head_lengh += 3   
        return head_lengh  

    def kolesa_darom_heders_value(self):                 # для расчета количества столбцов с заголовками под данные KOLESA_DAROM
        #print('KOLESA_DAROM_HEADER_NUMBER', KOLESATYT_HEADER_NUMBER)
        kolesa_darom_header_1 = 'конкурент KOLESA_DAROM'
        kolesa_darom_header_2 = 'цена конкурента KOLESA_DAROM'
        kolesa_darom_header_3 = 'отклонение цены конкурента KOLESA_DAROM'
        list_kolesa_darom__main_headers = []
        for header_number in range(0, KOLESA_DAROM_HEADER_NUMBER):
            kolesa_darom_main_header = kolesa_darom_header_1, kolesa_darom_header_2, kolesa_darom_header_3
            list_kolesa_darom__main_headers.append(kolesa_darom_main_header)
        #print('list_kolesa_darom_main_headers =====================kjhdkfjdsjkhj', list_kolesa_darom__main_headers)
        return list_kolesa_darom__main_headers

    def kolesa_darom_heders_lengt(self):                 # для расчета длинны столбца с заголовками под данные KOLESA_DAROM
        kolesa_darom_2 = 'цена конкурента KOLESA_DAROM'
        head_lengh = 0
        for header_number in range(0,  KOLESA_DAROM_HEADER_NUMBER):
            if kolesa_darom_2:
                head_lengh += 3   
        return head_lengh  
class ComparativeAnalysisTyresModel(models.Model):
    table = models.ManyToManyField(
        ComparativeAnalysisTableModel,
        verbose_name='Таблица',
        related_name='comparative_table',
        #on_delete=models.PROTECT,
        #null=True,
        blank=True, 
    )
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='tyre_comparative',
        on_delete=models.CASCADE,
    )
    planned_costs = models.ForeignKey(
        PlannedCosstModel,
        related_name='tyre_planned_costs',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    semi_variable_prices = models.ForeignKey(
        SemiVariableCosstModel,
        related_name='tyre_semi_variable_prices',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    belarus902price = models.ForeignKey(
        Belarus902PriceModel,
        related_name='tyre_belarus902price',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    tpsrussiafcaprice = models.ForeignKey(
        TPSRussiaFCAModel,
        related_name='tyre_tpsrussiafcaprice',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    tpskazfcaprice = models.ForeignKey(
        TPSKazFCAModel,
        related_name='tyre_tpskazfcaprice',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    tpsmiddleasiafcaprice = models.ForeignKey(
        TPSMiddleAsiaFCAModel,
        related_name='tyre_tpsmiddleasiafcaprice',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    currentpricesprice = models.ForeignKey(
        CurrentPricesModel,
        related_name='tyre_currentpricesprice',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=0,
    )
    sale_data = models.DateField(
        verbose_name='Дата парсинга',
        #auto_now=False,
        #auto_now_add=False,
        blank=True,
        null=True
    )


    def currentpricesprice_from_currency_to_bel_rub(self):                                                                  # ДЛЯ ПЕРЕВОДА ИЗ РОСС РУБЛЯ В БЕЛ РУБЛЬ И ВЫВЕДЕНИЯ В TEMPLATE
        if self.currentpricesprice:
            if CURRENCY_VALUE_USD:
                currentpricesprice_from_currency_to_bel_rub = self.currentpricesprice.price * CURRENCY_VALUE_USD
            else:
                currentpricesprice_from_currency_to_bel_rub = self.currentpricesprice.price * 0
            return currentpricesprice_from_currency_to_bel_rub

    def planned_costs_from_currency_to_bel_rub(self):                                                                        # ДЛЯ ПЕРЕВОДА ИЗ РОСС РУБЛЯ В БЕЛ РУБЛЬ И ВЫВЕДЕНИЯ В TEMPLATE
        if self.planned_costs:
            if CURRENCY_VALUE_USD:
                planned_costs_from_currency_to_bel_rub = self.planned_costs.price * CURRENCY_VALUE_USD 
            else:
                planned_costs_from_currency_to_bel_rub = self.planned_costs.price * 0

            return planned_costs_from_currency_to_bel_rub

    def semi_variable_prices_from_currency_to_bel_rub(self):                                                                  # ДЛЯ ПЕРЕВОДА ИЗ РОСС РУБЛЯ В БЕЛ РУБЛЬ И ВЫВЕДЕНИЯ В TEMPLATE
        if self.semi_variable_prices:
            if CURRENCY_VALUE_USD:
                semi_variable_prices_from_currency_to_bel_rub = self.semi_variable_prices.price * CURRENCY_VALUE_USD 
            else:
                semi_variable_prices_from_currency_to_bel_rub = self.semi_variable_prices.price * 0
            return semi_variable_prices_from_currency_to_bel_rub

    def belarus902price_from_currency_to_bel_rub(self):                                                                  # ДЛЯ ПЕРЕВОДА ИЗ РОСС РУБЛЯ В БЕЛ РУБЛЬ И ВЫВЕДЕНИЯ В TEMPLATE
        if self.belarus902price:
            if CURRENCY_VALUE_USD:
                belarus902price_from_currency_to_bel_rub = self.belarus902price.price * CURRENCY_VALUE_USD 
            else:
                belarus902price_from_currency_to_bel_rub = self.belarus902price.price * 0
            return belarus902price_from_currency_to_bel_rub

    def planned_profitability_from_currency_to_bel_rub(self):            # плановая рентабьельность                          # ДЛЯ ПЕРЕВОДА ИЗ РОСС РУБЛЯ В БЕЛ РУБЛЬ И ВЫВЕДЕНИЯ В TEMPLATE
        if self.currentpricesprice and self.planned_costs:
            #print(self.currentpricesprice.price,  self.planned_costs.price)
            planned_profitability = ((self.currentpricesprice.price / self.planned_costs.price) - 1) * 100
            planned_profitability = float('{:.2f}'.format(planned_profitability))
            return planned_profitability
        return 0

    def direct_cost_variance_from_currency_to_bel_rub(self):             # отклонение прямых затрат                          # ДЛЯ ПЕРЕВОДА ИЗ РОСС РУБЛЯ В БЕЛ РУБЛЬ И ВЫВЕДЕНИЯ В TEMPLATE
        if self.currentpricesprice and self.semi_variable_prices:
            direct_cost_variance = ((self.currentpricesprice.price / self.semi_variable_prices.price) - 1) * 100
            direct_cost_variance = float('{:.2f}'.format(direct_cost_variance))
            return direct_cost_variance
        return 0

    def planned_profitability(self):            # плановая рентабьельность
        if self.currentpricesprice and self.planned_costs:
            #print(self.currentpricesprice.price,  self.planned_costs.price)
            planned_profitability = ((self.currentpricesprice.price / self.planned_costs.price) - 1) * 100
            planned_profitability = float('{:.2f}'.format(planned_profitability))
            return planned_profitability
        return 0

    def direct_cost_variance(self):             # отклонение прямых затрат
        if self.currentpricesprice and self.semi_variable_prices:
            direct_cost_variance = ((self.currentpricesprice.price / self.semi_variable_prices.price) - 1) * 100
            direct_cost_variance = float('{:.2f}'.format(direct_cost_variance))
            return direct_cost_variance
        return 0

    def onliner_competitor_on_date1(self):                                       # отдаем конкурентов и цены + отклонение цены 902 прайса от цены Onliner (+ прикрутить формулы сняьтия ценоой надбавки и НДС)   Onliner
        if self.tyre in ONLINER_COMPETITORS_DICTIONARY1.keys(): #and ONLINER_COMPETITORS_DICTIONARY1.values():
            #print(ONLINER_COMPETITORS_DICTIONARY1.keys(), 'ONLINER_COMPETITORS_DICTIONARY1.keys() ' )
            #print(ONLINER_COMPETITORS_DICTIONARY1.values(), 'ONLINER_COMPETITORS_DICTIONARY1.values()')
            competitors_values_list = ONLINER_COMPETITORS_DICTIONARY1[self.tyre]
            list_od_combined_comp_and_prices = []
            #print(competitors_values_list,'competitors_values_list', 'kk ')
            ######################### ДОП ФИЛЬТРАЦИЯ ПО ТИПОРАЗМЕРУ, ИНДЕКСАМ, СЕЗОННОСТИ:
            filtered_competitors_values_list = []
            for objject in competitors_values_list:
            #    print('objjectobjjectobjjectobjject======================================================', objject, objject.tyresize_competitor, objject.developer, objject.site, objject.date_period)
                competior_is_found = False
                tyre_in_base_season = ''
                if objject.season and self.tyre.added_features.all():            
                    tyre_in_base_season = self.tyre.added_features.all()[0].season_usage 
                    tyre_in_base_season = self.tyre.added_features.all()
                    for n in tyre_in_base_season:
                        if n.season_usage:
                            tyre_in_base_season = n.season_usage.season_usage_name 
                    #print('tyre_in_base_season111', tyre_in_base_season)
                    tyre_in_base_index = self.tyre.added_features.all()[0].indexes_list
                if tyre_in_base_season is None:
                    filtered_competitors_values_list.append(objject)
                else:
                    if objject.season:
                        try:
                            if tyre_in_base_season == objject.season.season_usage_name and tyre_in_base_index == objject.parametres_competitor:       # 1) ЗАОДНО совмещаем конкурентов с шинами в базе по сезонности  и индексам:
                                #print('OOOO')
                                #print(tyre_in_base_index, tyre_in_base_season, 'OOIIIIIOO', objject.parametres_competitor, objject.season.season_usage_name)
                                objject.tyre_to_compare.add(self)                           # ДОПОЛНИТЕЛЬНОЕ БАЛОВСТВО
                                filtered_competitors_values_list.append(objject)            # ВОТ ТУТ ВСЕ И ПРОИСХОДИТ
                                continue
                        except:
                            pass
                            #if tyre_in_base_season == objject.season.season_usage_name:                                                               # 2) ЗАОДНО если нет, то совмещаем конкурентов с шинами в базе по сезонности
                            #    #print(tyre_in_base_index, 'OOIIIIIOO', objject.parametres_competitor)
                            #    #print(tyre_in_base_season, objject.season.season_usage_name)
                            #    objject.tyre_to_compare.add(self)
                            #    filtered_competitors_values_list.append(objject)  
                            #    continue
            #########################
            list_comp_ids = []
            for comp in filtered_competitors_values_list:
                comp_name = comp.name_competitor + ' ' + comp.tyresize_competitor + ' ' + comp.parametres_competitor  + ' '+ comp.season.season_usage_name
                #print('!!!', comp_name)
                if DEFLECTION_VAL:                                                      # если есть введенные данные об скидке торговой надбавки
                    comp_price = comp.price * ((100 - DEFLECTION_VAL) * 0.01)
                else:
                    comp_price = comp.price  
                #if comp_price and self.belarus902price and type(comp_price) is float: 
                if comp_price and self.currentpricesprice and type(comp_price) is float: 
                    combined = None
                    #deflection = self.belarus902price.price * CURRENCY_VALUE_RUB  / comp_price       # для расчета отклонения  # ((self.currentpricesprice.price / self.semi_variable_prices.price) - 1) * 100
                #    deflection = ((self.currentpricesprice.price  * CURRENCY_VALUE_RUB  / comp_price) -1 ) * 100
                    if CURRENCY_VALUE_USD:
                        deflection = (self.currentpricesprice.price  * CURRENCY_VALUE_USD  / comp_price) -1 
                        combined = ((comp_name, comp_price, deflection), comp.developer, comp.date_period)
                        #print('====1', combined)
                    else:
                        deflection = ' '
                        combined = ((comp_name, comp_price, deflection), comp.developer, comp.date_period)
                    #print('====2', combined)
                    if combined:
                        list_comp_ids.append(comp.id)
                        list_od_combined_comp_and_prices.append(combined)
                        #print('====3', combined)

                else:                   # ЕСЛИ ДЕЙСТВУЮЩИХ ЦЕН НЕТ или в ценах ошибка формата:
                    deflection = ' '
                    combined = ((comp_name, comp_price, deflection), comp.developer, comp.date_period)
                    list_comp_ids.append(comp.id)
                    list_od_combined_comp_and_prices.append(combined)
                    #print('====4', combined)

                ONLINER_COMPETITORS_NAMES_FILTER.append(comp.developer.competitor_name)
            #    list_comp_ids.append(comp.id)
            ONLINER_COMPETITORS_NAMES_FILTER_IDS[self.pk] = list_comp_ids                                                                     #  ОТДЕЛЬНО ДЛЯ ФИЛЬТРА ПО ПРОИЗВОДИТЕЛЯМ ОНЛАЙНЕР
            list_od_combined_comp_and_prices = sorted(list(set(list_od_combined_comp_and_prices)))          # + sorted
            #print('list_od_combined_comp_and_prices', list_od_combined_comp_and_prices, len(list_od_combined_comp_and_prices))
            void_data_num = len(list_od_combined_comp_and_prices)               # доставить дополнительные пробелы там где инфы нет
            for n in range(0, 3-void_data_num):
                list_od_combined_comp_and_prices.append(('', '', ''))
            #print('AAA', list_od_combined_comp_and_prices)
            ONLINER_HEADER_DICT[self.pk] = list_od_combined_comp_and_prices
            
            return list_od_combined_comp_and_prices

    def avtoset_competitor_on_date1(self):                                       # отдаем конкурентов и цены + отклонение цены 902 прайса от цены AVTOSET (+ прикрутить формулы сняьтия ценоой надбавки и НДС)   AVTOSET
        if self.tyre in AVTOSET_COMPETITORS_DICTIONARY1.keys() and AVTOSET_COMPETITORS_DICTIONARY1.values():
            competitors_values_list = AVTOSET_COMPETITORS_DICTIONARY1[self.tyre]
            list_od_combined_comp_and_prices = []
            #print(competitors_values_list,'competitors_values_list avtoset')
            ######################### ДОП ФИЛЬТРАЦИЯ ПО ТИПОРАЗМЕРУ, ИНДЕКСАМ, СЕЗОННОСТИ:
            filtered_competitors_values_list = []
            for objject in competitors_values_list:
                #print('objjectobjjectobjjectobjject======================================================', objject, objject.developer , objject.site, objject.season)
                if objject is None:
                    pass
                else:
                    competior_is_found = False
                    tyre_in_base_season = str
                    if objject.season and self.tyre.added_features.all():
                        #tyre_in_base_season = self.tyre.added_features.all()[0].season_usage 
                        tyre_in_base_season = self.tyre.added_features.all()
                        for n in tyre_in_base_season:
                            if n.season_usage:
                                tyre_in_base_season = n.season_usage.season_usage_name 
                        #print('tyre_in_base_season111', tyre_in_base_season)
                        tyre_in_base_index = self.tyre.added_features.all()[0].indexes_list
                    if tyre_in_base_season is None or objject.season is None:                       #0 
                        filtered_competitors_values_list.append(objject)
            #            print('OOO22222O')
                    else:
                        try:
                            if tyre_in_base_season == objject.season.season_usage_name and tyre_in_base_index == objject.parametres_competitor:       # 1) ЗАОДНО совмещаем конкурентов с шинами в базе по сезонности  и индексам:
            #                    print('OOOO', 'tyre_in_base_season', tyre_in_base_season, 'objject.season.season_usage_name', objject.season.season_usage_name)
                                objject.tyre_to_compare.add(self)                           # ДОПОЛНИТЕЛЬНОЕ БАЛОВСТВО
                                filtered_competitors_values_list.append(objject)            # ВОТ ТУТ ВСЕ И ПРОИСХОДИТ
                                continue
                        except:
                            pass
                            #if tyre_in_base_season == objject.season.season_usage_name:                                                               # 2) ЗАОДНО если нет, то совмещаем конкурентов с шинами в базе по сезонности
            #                  #     print('OOIIIIIOO')
                            #    #print(tyre_in_base_season, objject.season.season_usage_name)
                            #    objject.tyre_to_compare.add(self)
                            #    filtered_competitors_values_list.append(objject)  
                            #    continue
            #print(filtered_competitors_values_list, 'filtered_competitors_values_list')          # [<CompetitorSiteModel: CompetitorSiteModel object (143)>, <CompetitorSiteModel: CompetitorSiteModel object (144)>, <CompetitorSiteModel: CompetitorSiteModel object (145)>
            ##########################
            list_comp_ids = []
            for comp in filtered_competitors_values_list:
                comp_name = comp.name_competitor + ' ' + comp.tyresize_competitor + ' ' + comp.parametres_competitor # + ' '+ comp.season.season_usage_name
                if DEFLECTION_VAL:                                                      # если есть введенные данные об скидке торговой надбавки
                    comp_price = comp.price * ((100 - DEFLECTION_VAL) * 0.01)
                else:
                    comp_price = comp.price  
                #if type(comp_price) is float and self.belarus902price != None:    
                if comp_price and self.currentpricesprice and type(comp_price) is float: 
                    combined = None
                    #deflection = self.belarus902price.price * CURRENCY_VALUE_RUB  / comp_price 
                    if CURRENCY_VALUE_USD:
                        deflection = (self.currentpricesprice.price  * CURRENCY_VALUE_USD  / comp_price) -1 
                        combined = ((comp_name, comp_price, deflection), comp.developer, comp.date_period)
                    else:
                        deflection = ' '
                        combined = ((comp_name, comp_price, deflection), comp.developer, comp.date_period)      
                    #deflection = ((self.currentpricesprice.price  * CURRENCY_VALUE_USD  / comp_price) -1 )
                    #deflection = self.belarus902price.price / comp_price       # для расчета отклонения     # для расчета отклонения  # ((self.currentpricesprice.price / self.semi_variable_prices.price) - 1) * 100
                    combined = None
                    if comp.season:
                        combined = comp.developer.competitor_name + ' ' + comp_name + comp.season.season_usage_name, comp_price, deflection
                    else:
                        combined = comp.developer.competitor_name + ' ' + comp_name, comp_price, deflection
                    combined = ((combined), comp.developer, comp.date_period) 
                    if combined:
                        list_comp_ids.append(comp.id)
                        list_od_combined_comp_and_prices.append(combined)                           # 1

                else:                   # ЕСЛИ ДЕЙСТВУЮЩИХ ЦЕН НЕТ или в ценах ошибка формата:
                    deflection = ' '
                    combined = ((comp_name, comp_price, deflection), comp.developer, comp.date_period)
                    list_comp_ids.append(comp.id)
                    list_od_combined_comp_and_prices.append(combined)

                AVTOSET_COMPETITORS_NAMES_FILTER.append(comp.developer.competitor_name) 
                #list_comp_ids.append(comp.id)                                               # 2
            AVTOSET_COMPETITORS_NAMES_FILTER_IDS[self.pk] = list_comp_ids                                                                     #  ОТДЕЛЬНО ДЛЯ ФИЛЬТРА ПО ПРОИЗВОДИТЕЛЯМ AVTOSET
            list_od_combined_comp_and_prices = sorted(list(set(list_od_combined_comp_and_prices)))          # + sorted
            #print('list_od_combined_comp_and_prices', list_od_combined_comp_and_prices)
            void_data_num = len(list_od_combined_comp_and_prices)               # доставить дополнительные пробелы там где инфы нет
            for n in range(0, 3-void_data_num):
                list_od_combined_comp_and_prices.append(('', '', ''))
            #print('BBB', list_od_combined_comp_and_prices)
            AVTOSET_HEADER_DICT[self.pk] = list_od_combined_comp_and_prices

            return list_od_combined_comp_and_prices

    def bagoria_competitor_on_date1(self):                                       # отдаем конкурентов и цены + отклонение цены 902 прайса от цены BAGORIA (+ прикрутить формулы сняьтия ценоой надбавки и НДС)   BAGORIA
        if self.tyre in BAGORIA_COMPETITORS_DICTIONARY1.keys() and BAGORIA_COMPETITORS_DICTIONARY1.values():
            competitors_values_list = BAGORIA_COMPETITORS_DICTIONARY1[self.tyre]
            list_od_combined_comp_and_prices = []
            #print(self.tyre, 'BAGORIA_COMPETITORS_DICTIONARY1', BAGORIA_COMPETITORS_DICTIONARY1)
            ######################### ДОП ФИЛЬТРАЦИЯ ПО ТИПОРАЗМЕРУ, ИНДЕКСАМ, СЕЗОННОСТИ:
            filtered_competitors_values_list = []
            for objject in competitors_values_list:
                #print('objjectobjjectobjjectobjject======================================================', objject, objject.tyresize_competitor, objject.developer, objject.site, objject.date_period)
                if objject is None:
                    pass
                else:
                    competior_is_found = False
                    tyre_in_base_season = str
                    if objject.season and self.tyre.added_features.all():
                        tyre_in_base_season = self.tyre.added_features.all()[0].season_usage 
                        tyre_in_base_season = self.tyre.added_features.all()
                        for n in tyre_in_base_season:
                            if n.season_usage:
                                tyre_in_base_season = n.season_usage.season_usage_name 
                        #print('tyre_in_base_season111', tyre_in_base_season)
                        tyre_in_base_index = self.tyre.added_features.all()[0].indexes_list
                    if tyre_in_base_season is None or objject.season is None:                       #0 
                        filtered_competitors_values_list.append(objject)
                        #print('OOO22222O')
                    else:
                        try:
                            if tyre_in_base_season == objject.season.season_usage_name and tyre_in_base_index == objject.parametres_competitor:       # 1) ЗАОДНО совмещаем конкурентов с шинами в базе по сезонности  и индексам:
                                #print('OOOO')
                                objject.tyre_to_compare.add(self)                           # ДОПОЛНИТЕЛЬНОЕ БАЛОВСТВО
                                filtered_competitors_values_list.append(objject)            # ВОТ ТУТ ВСЕ И ПРОИСХОДИТ
                                continue
                        except:
                            pass
                            #if tyre_in_base_season == objject.season.season_usage_name:                                                               # 2) ЗАОДНО если нет, то совмещаем конкурентов с шинами в базе по сезонности
                            #    #print('OOIIIIIOO')
                            #    #print(tyre_in_base_season, objject.season.season_usage_name)
                            #    objject.tyre_to_compare.add(self)
                            #    filtered_competitors_values_list.append(objject)  
                            #    continue
            #print(filtered_competitors_values_list, 'filtered_competitors_values_list')          # [<CompetitorSiteModel: CompetitorSiteModel object (143)>, <CompetitorSiteModel: CompetitorSiteModel object (144)>, <CompetitorSiteModel: CompetitorSiteModel object (145)>
            ##########################
            list_comp_ids = []
            for comp in filtered_competitors_values_list:
                comp_name = comp.developer.competitor_name + ' ' + comp.name_competitor + ' ' + comp.tyresize_competitor + ' ' + comp.parametres_competitor # + ' '+ comp.season.season_usage_name     #tyresize_competitor, developer
                comp_price = comp.price 
            #    print('LLL', comp_name, comp_price,  comp.developer, comp.site, comp.date_period)

                if DEFLECTION_VAL and comp_price:                                                      # если есть введенные данные об скидке торговой надбавки
                    comp_price = comp.price * ((100 - DEFLECTION_VAL) * 0.01)
                    
                #if type(comp_price) is float and self.belarus902price != None:   
                if comp_price and self.currentpricesprice and type(comp_price) is float:      
                    if CURRENCY_VALUE_USD:
                        deflection = (self.currentpricesprice.price  * CURRENCY_VALUE_USD  / comp_price) -1 
                        combined = ((comp_name, comp_price, deflection), comp.developer, comp.date_period)
                    else:
                        deflection = ' '
                        combined = ((comp_name, comp_price, deflection), comp.developer, comp.date_period)
                    if comp.season is None:
                        combined = comp_name, comp_price, deflection  
                    else:
                        combined = comp_name + comp.season.season_usage_name, comp_price, deflection    
                    #print('combined!!!!', combined)
                    combined = ((combined), comp.developer, comp.date_period) 
                    if combined:
                        list_comp_ids.append(comp.id)
                        list_od_combined_comp_and_prices.append(combined)

                else:                   # ЕСЛИ ДЕЙСТВУЮЩИХ ЦЕН НЕТ или в ценах ошибка формата:
                    deflection = ' '
                    combined = ((comp_name, comp_price, deflection), comp.developer, comp.date_period)
                    list_comp_ids.append(comp.id)
                    list_od_combined_comp_and_prices.append(combined)

                BAGORIA_COMPETITORS_NAMES_FILTER.append(comp.developer.competitor_name)                                                                     #  ОТДЕЛЬНО ДЛЯ ФИЛЬТРА ПО ПРОИЗВОДИТЕЛЯМ ОНЛАЙНЕР
                #list_comp_ids.append(comp.id)
            BAGORIA_COMPETITORS_NAMES_FILTER_IDS[self.pk] = list_comp_ids          
            list_od_combined_comp_and_prices = sorted(list(set(list_od_combined_comp_and_prices)))          # + sorted
            #print('list_od_combined_comp_and_pricesBAGORIA', list_od_combined_comp_and_prices)
            void_data_num = len(list_od_combined_comp_and_prices)               # доставить дополнительные пробелы там где инфы нет
            for n in range(0, 3-void_data_num):
                list_od_combined_comp_and_prices.append(('', '', ''))
            #print('CCC', list_od_combined_comp_and_prices)
            #if len(list_od_combined_comp_and_prices) > 3:
            #    list_od_combined_comp_and_prices = list_od_combined_comp_and_prices[0:3]
            #else:
            #    pass
            BAGORIA_HEADER_DICT[self.pk] = list_od_combined_comp_and_prices

            return list_od_combined_comp_and_prices

    def onliner_table_header(self):
        the_very_final_list_of_competitors_for_current_model_for_header_list = [] 
        the_very_final_list_of_competitors_for_current_model_for_header = [] 
        final_list_of_competitors_for_current_model_for_header = []       
        if self.id in ONLINER_HEADER_DICT.keys():
            model_tyr_table_competitores_for_this_tyre = ONLINER_HEADER_DICT.get(self.id)
  
            # отбор данный для заголовка таблицы
            # 1) получаем перечень производителей - кто есть для вывода
            producer_list_cleaned_data = []
            dates_list_cleaned_data = []
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                producer_list_cleaned_data.append(compet_cleaned_data[1])
                dates_list_cleaned_data.append(compet_cleaned_data[2])
            producer_list_cleaned_data = list(set(producer_list_cleaned_data))
            dates_list_cleaned_data = list(set(dates_list_cleaned_data))
            #print('producer_list_cleaned_data', producer_list_cleaned_data)
            # 2) получаем последнюю дату для вывода:
                #2.1) если вводилась дата:
            if COMPETITORS_DATE_FROM_USER_ON_FILTER and COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                current_data_header = datetime.datetime.strptime(COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
            #2.2) если не вводилась дата: 
            else:
                current_data_header = max(dates_list_cleaned_data)   
            #print('current_data_header', current_data_header)
            #3 отбор по последней дате для вывода в таблицу:
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                for prod_vrand in producer_list_cleaned_data:
                    if compet_cleaned_data[2] == current_data_header and compet_cleaned_data[1] == prod_vrand:
                        #print('compet_cleaned_data SS', compet_cleaned_data)
                        final_list_of_competitors_for_current_model_for_header.append(compet_cleaned_data[0])

        ##    #4 количество выводимых конкурентов для конкурента (можно вклиниться в п.3 - сделать отбор конкретиных производителей)
        ##    max_number_of_shown_competitores_in_table = 3
        ##    if final_list_of_competitors_for_current_model_for_header:
        ##        if len(final_list_of_competitors_for_current_model_for_header) > 3:
        ##            the_very_final_list_of_competitors_for_current_model_for_header = final_list_of_competitors_for_current_model_for_header[:max_number_of_shown_competitores_in_table] 
        ##        else:
        ##            the_very_final_list_of_competitors_for_current_model_for_header = final_list_of_competitors_for_current_model_for_header 

        if final_list_of_competitors_for_current_model_for_header:
            the_very_final_list_of_competitors_for_current_model_for_header = final_list_of_competitors_for_current_model_for_header 
        if the_very_final_list_of_competitors_for_current_model_for_header:              
            for final_data in the_very_final_list_of_competitors_for_current_model_for_header:   # разбор нга составляющие для представления в таблице
                tuple_len = len(final_data)
                if tuple_len == 3:
                #    print(final_data, type(final_data), len(final_data))
                    brand_name, comp_price, deflection = final_data
                    brand_name_comp_price_deflection = brand_name, comp_price, deflection
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(brand_name_comp_price_deflection)
        #5 дорисовка выводимых в таблице столбцов/конкурентов по типоразмеру:
        if COMPET_PER_SITE:
            void_data_num = len(the_very_final_list_of_competitors_for_current_model_for_header_list)               # доставить дополнительные пробелы там где инфы нет
            #print('!!!!!!!!!!!!!!!', the_very_final_list_of_competitors_for_current_model_for_header_list)
            #print('COMPET_PER_SITE', COMPET_PER_SITE, 'LLLENN',  void_data_num)
    #        print('!!!!!!!!!!!!!!!','void_data_num', void_data_num, 'COMPET_PER_SITE', COMPET_PER_SITE)
            if void_data_num > COMPET_PER_SITE or void_data_num == COMPET_PER_SITE:
                the_very_final_list_of_competitors_for_current_model_for_header_list = the_very_final_list_of_competitors_for_current_model_for_header_list[:COMPET_PER_SITE]
            else:
                for n in range(0, COMPET_PER_SITE-void_data_num):
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(('', '', ''))

    #    print('!! FINAL OCHKA ONLINER', the_very_final_list_of_competitors_for_current_model_for_header_list)  
        return the_very_final_list_of_competitors_for_current_model_for_header_list

    def avtoset_table_header(self):
        the_very_final_list_of_competitors_for_current_model_for_header_list = [] 
        the_very_final_list_of_competitors_for_current_model_for_header = [] 
        final_list_of_competitors_for_current_model_for_header = []       
        if self.id in AVTOSET_HEADER_DICT.keys():
            model_tyr_table_competitores_for_this_tyre = AVTOSET_HEADER_DICT.get(self.id) 
            # отбор данный для заголовка таблицы
            # 1) получаем перечень производителей - кто есть для вывода
            producer_list_cleaned_data = []
            dates_list_cleaned_data = []
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                producer_list_cleaned_data.append(compet_cleaned_data[1])
                dates_list_cleaned_data.append(compet_cleaned_data[2])
            producer_list_cleaned_data = list(set(producer_list_cleaned_data))
            dates_list_cleaned_data = list(set(dates_list_cleaned_data))
            #print('!!!!!', dates_list_cleaned_data )
            #print('producer_list_cleaned_data', producer_list_cleaned_data)
            # 2) получаем последнюю дату для вывода:
                #2.1) если вводилась дата:
            if COMPETITORS_DATE_FROM_USER_ON_FILTER and COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                current_data_header = datetime.datetime.strptime(COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
            #2.2) если не вводилась дата: 
            else:
                current_data_header = max(dates_list_cleaned_data)   
            #print('current_data_header', current_data_header)
            #3 отбор по последней дате для вывода в таблицу:
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                for prod_vrand in producer_list_cleaned_data:
                    if compet_cleaned_data[2] == current_data_header and compet_cleaned_data[1] == prod_vrand:
                        #print('compet_cleaned_data SS', compet_cleaned_data)
                        final_list_of_competitors_for_current_model_for_header.append(compet_cleaned_data[0])

        if final_list_of_competitors_for_current_model_for_header:
            the_very_final_list_of_competitors_for_current_model_for_header = final_list_of_competitors_for_current_model_for_header  
        if the_very_final_list_of_competitors_for_current_model_for_header:              
            for final_data in the_very_final_list_of_competitors_for_current_model_for_header:   # разбор нга составляющие для представления в таблице
                tuple_len = len(final_data)
                if tuple_len == 3:
                #    print(final_data, type(final_data), len(final_data))
                    brand_name, comp_price, deflection = final_data
                    brand_name_comp_price_deflection = brand_name, comp_price, deflection
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(brand_name_comp_price_deflection)
        #5 дорисовка выводимых в таблице столбцов/конкурентов по типоразмеру:
        if COMPET_PER_SITE:
            void_data_num = len(the_very_final_list_of_competitors_for_current_model_for_header_list)               # доставить дополнительные пробелы там где инфы нет
            #print('!!!!!!!!!!!!!!!', the_very_final_list_of_competitors_for_current_model_for_header_list)
            #print('COMPET_PER_SITE', COMPET_PER_SITE, 'LLLENN',  void_data_num)
    #        print('!!!!!!!!!!!!!!!','void_data_num', void_data_num, 'COMPET_PER_SITE', COMPET_PER_SITE)
            if void_data_num > COMPET_PER_SITE or void_data_num == COMPET_PER_SITE:
                the_very_final_list_of_competitors_for_current_model_for_header_list = the_very_final_list_of_competitors_for_current_model_for_header_list[:COMPET_PER_SITE]
            else:
                for n in range(0, COMPET_PER_SITE-void_data_num):
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(('', '', ''))

    #    print('!! FINAL OCHKA AVTOSET', the_very_final_list_of_competitors_for_current_model_for_header_list)
        return the_very_final_list_of_competitors_for_current_model_for_header_list
      
    def bagoria_table_header(self):
        the_very_final_list_of_competitors_for_current_model_for_header_list = [] 
        the_very_final_list_of_competitors_for_current_model_for_header = []   
        final_list_of_competitors_for_current_model_for_header = []     
        if self.id in BAGORIA_HEADER_DICT.keys():
            model_tyr_table_competitores_for_this_tyre = BAGORIA_HEADER_DICT.get(self.id)
            #print('&&&&&&&&model_tyr_table_competitores_for_this_tyre', model_tyr_table_competitores_for_this_tyre)
 
            # отбор данный для заголовка таблицы
            # 1) получаем перечень производителей - кто есть для вывода
            producer_list_cleaned_data = []
            dates_list_cleaned_data = []
    #        print('!!!!!!!!!!!!!!!',  model_tyr_table_competitores_for_this_tyre)
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                producer_list_cleaned_data.append(compet_cleaned_data[1])
                dates_list_cleaned_data.append(compet_cleaned_data[2])
            producer_list_cleaned_data = list(set(producer_list_cleaned_data))
            dates_list_cleaned_data = list(set(dates_list_cleaned_data))
    ##        print("+++", producer_list_cleaned_data, dates_list_cleaned_data)
    ##        for kk in dates_list_cleaned_data:
    ##            print("LLL:", kk)
            # 2) получаем последнюю дату для вывода:
                #2.1) если вводилась дата:
            if COMPETITORS_DATE_FROM_USER_ON_FILTER and COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                current_data_header = datetime.datetime.strptime(COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
            #2.2) если не вводилась дата: 
            else:
    #            print('OCELOT!!!', dates_list_cleaned_data)
                current_data_header = max(dates_list_cleaned_data)   
    #        print('current_data_header IIIII', current_data_header)
            #3 отбор по последней дате для вывода в таблицу:
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                for prod_vrand in producer_list_cleaned_data:
                #    print(compet_cleaned_data[2], '||', current_data_header, '||', compet_cleaned_data[1], '||', prod_vrand)
                    if compet_cleaned_data[2] == current_data_header and compet_cleaned_data[1] == prod_vrand:
            ##            print('compet_cleaned_data SS', compet_cleaned_data)
                        final_list_of_competitors_for_current_model_for_header.append(compet_cleaned_data[0])

        if final_list_of_competitors_for_current_model_for_header:
            the_very_final_list_of_competitors_for_current_model_for_header = final_list_of_competitors_for_current_model_for_header 
        if the_very_final_list_of_competitors_for_current_model_for_header:              
            for final_data in the_very_final_list_of_competitors_for_current_model_for_header:   # разбор нга составляющие для представления в таблице
                tuple_len = len(final_data)
                if tuple_len == 3:
                #    print(final_data, type(final_data), len(final_data))
                    brand_name, comp_price, deflection = final_data
                    brand_name_comp_price_deflection = brand_name, comp_price, deflection
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(brand_name_comp_price_deflection)
        #5 дорисовка выводимых в таблице столбцов/конкурентов по типоразмеру:
        if COMPET_PER_SITE:
            void_data_num = len(the_very_final_list_of_competitors_for_current_model_for_header_list)               # доставить дополнительные пробелы там где инфы нет
            #print('!!!!!!!!!!!!!!!', the_very_final_list_of_competitors_for_current_model_for_header_list)
            #print('COMPET_PER_SITE', COMPET_PER_SITE, 'LLLENN',  void_data_num)
    #        print('!!!!!!!!!!!!!!!','void_data_num', void_data_num, 'COMPET_PER_SITE', COMPET_PER_SITE)
            if void_data_num > COMPET_PER_SITE or void_data_num == COMPET_PER_SITE:
                the_very_final_list_of_competitors_for_current_model_for_header_list = the_very_final_list_of_competitors_for_current_model_for_header_list[:COMPET_PER_SITE]
            else:
                for n in range(0, COMPET_PER_SITE-void_data_num):
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(('', '', ''))
                       
    #    print('!! FINAL OCHKA BAGORIA', the_very_final_list_of_competitors_for_current_model_for_header_list)    
        return the_very_final_list_of_competitors_for_current_model_for_header_list

    def chemcurier_competitor_on_date1(self):                                       # отдаем конкурентов и цены + отклонение цены 902 прайса от цены CHEMCURIER (+ прикрутить формулы сняьтия ценоой надбавки и НДС)   CHEMCURIER                                                           
        try:
            chemcurier_unique_result = ''
            if self.tyre in CHEMCURIER_COMPETITORS_DICTIONARY1.keys():                  # Tyre object (1926) [<ChemCurierTyresModel: ChemCurierTyresModel object (98)>, <ChemCurierTyresModel: ChemCurierTyresModel object (99)>, <ChemCurierTyresModel: ChemCurierTyresModel object (100)>, <ChemCurierTyresModel: ChemCurierTyresModel object (101)>]
                min_value = '' # минимальное значение из всех прозодителей последнего периода поставки
                result_min_value_producer = ''  # наименование производителя с наименьшим значением (ценой) в последний период поствки
                index_of_min_value = ''        # просто индекс, нужен для вылавливания из списков значений index_of_min_value и result_min_value_producer    
                month_num = '' # номер месяца - на всякий случай

                competitors_values_list = CHEMCURIER_COMPETITORS_DICTIONARY1[self.tyre] 
                ######################### ДОП ФИЛЬТРАЦИЯ ПО ТИПОРАЗМЕРУ, ИНДЕКСАМ, СЕЗОННОСТИ:
                gathered_tyresizes_by_producer_name_dict = {}
                list_of_producer_names_list = []
                for objject in competitors_values_list:         # пройтись по хикуреровским объектам данного типоразмера
                    #print('objjectobjjectobjjectobjject======================================================', objject,)
                    if objject is None:
                        pass
                    else:
                        list_of_producer_names_list.append(objject.producer_chem)
            #    print('list_of_producer_names_list', list_of_producer_names_list) 
                list_of_producer_names_list = list(set(list_of_producer_names_list)) 
                for prod_name in list_of_producer_names_list:
                    gathered_tyresizes_by_producer_name_list = []  
                    for objject in competitors_values_list:         # пройтись по хикуреровским объектам данного типоразмера
                    # 1. выбрать все строки (типоразмеры) одного производителя:             
                        if objject.producer_chem == prod_name:
                            gathered_tyresizes_by_producer_name_list.append(objject)
            #        print('GAZERET', gathered_tyresizes_by_producer_name_list, 'PPP', prod_name)
                    gathered_tyresizes_by_producer_name_dict[prod_name] = gathered_tyresizes_by_producer_name_list
            #    print('|||||', gathered_tyresizes_by_producer_name_dict)   # ||||| {'Nexen': [<ChemCurierTyresModel: ChemCurierTyresModel object (112)>, <ChemCurierTyresModel: ChemCurierTyresModel object (128)>, <ChemCurierTyresModel: ChemCurierTyresModel object (136)>], 'Continental': [<ChemCurierTyresModel: ChemCurierTyresModel object (120)>]}
                # 2 есть словарь gathered_tyresizes_by_producer_name_dict - все размеры отфильтрованы по производителю, теперь выведение средних их цен по каждому периоду из всех размеров одного производителя:
                motnth_periods_vol = []
                motnth_periods_vol_dates = []
                for val in gathered_tyresizes_by_producer_name_dict.values():
                    for chemcur_obj in val:                 # ChemCurierTyresModel object (109)):
                        motnth_periods_vol_dates.append(chemcur_obj.data_month_chem)
                    eldest_date = min(motnth_periods_vol_dates)
                    latest_date = max(motnth_periods_vol_dates)
                    motnth_periods_vol = pd.date_range(start=eldest_date, end=latest_date).date
                #print('=========', motnth_periods_vol)         #========= 1
                # Собираем словарь производитель - все его одинакового типоразмера сложенные по месяцам СО СРЕДНВЗВЕШЕННЫМ ЗНАЧЕНИЕМ        -  сюда можно вмешаться - подмешать проверки по объемам, например
                gazered_all_sizws_by_periods_in_one_producer = {}                                                                                                                                                             
                for key, val in gathered_tyresizes_by_producer_name_dict.items(): 
                    all_prices_by_producer_gathered = {} 
                    for per_num in motnth_periods_vol:
                        list_of_values = [] 
                        for chemcur_obj in val:
                            if chemcur_obj.data_month_chem == per_num:
                                mon_val = chemcur_obj.average_price_in_usd
                                list_of_values.append(mon_val)
                        all_prices_by_producer_gathered[per_num] = list_of_values   
                    gazered_all_sizws_by_periods_in_one_producer[key] = all_prices_by_producer_gathered     
    #            print('UU', gazered_all_sizws_by_periods_in_one_producer)                                          # здесь все годно  - все норм посчитано
                # 1 ОПЦИЯ ДЛЯ ВЫВОДА: расчет средневзвешенной стоимости типоразмера одного производителя:
                result_main_per_producer_size_calculated_dict = {}
                for producer, perid_mumb_periods in gazered_all_sizws_by_periods_in_one_producer.items():
                #    print('=-=-=-=', producer, '=-=-=-=', perid_mumb_periods)
                    periods_dict = {}
                    for perid_mumb, values in perid_mumb_periods.items():
                #        print(values, len(values))
                        result_summ_in_period = 0           
                        val_quqnt_calc = 0
                        for numb in values:
                #            print('NUMB', numb)
                            result_summ_in_period += numb
                            val_quqnt_calc +=1

                        if result_summ_in_period !=0 and val_quqnt_calc > 0:
                            periods_dict[perid_mumb] = result_summ_in_period / val_quqnt_calc
                        else:
                            periods_dict[perid_mumb] = None
            #        print('!!', periods_dict)
                    result_main_per_producer_size_calculated_dict[producer] = periods_dict
        #        print('GGGG', result_main_per_producer_size_calculated_dict)
        #        print('---------')
#
                ##### РАСЧЕТ ДЛЯ ВЫВОДА 3 произдводителя с наменьшей ценой последнего периода:
                periods_value = None            # количество периодов
                for val in result_main_per_producer_size_calculated_dict.values():
                    periods_value  = len(val)
                    if periods_value and type(periods_value) is int:
                        continue
                #print(periods_value, 'HHHH')
                
                values_on_period_for_comparison_dict = {}                                                               ## ИТОГОВЫЙ СЛОВАРЬ ключ -период, значение - высчитанная средняя цена ВСЕХ типоразмеров данного производителя (списком) и эти производители (списком)
                if periods_value:                                                                                          # Для работы словарь может не пригодиться но наглядно демонстрирует результат
                    #for per in range(periods_value, -1, -1):
                    for per in range(periods_value, 0, -1):     #reversed()      # ЕСЛИ ФОРМИРОВАТЬ СЛОВАРЬ 0 - ноябрь, 1 - октябрь (т.е. от конца года) 
                    #for per in range(0, periods_value):     #reversed()             # ЕСЛИ ФОРМИРОВАТЬ СЛОВАРЬ 0 - январь, 1 - февраль (т.е. от начала года) 
                        list_of_values_in_one_period_for_comarison = [] 
                        list_of_producers = []
                        from_num_to_month_onverter = {}     #для понимания -  номер - какой это месяц
                        for producer_name, per_vvalues in result_main_per_producer_size_calculated_dict.items(): 
                            pperiod_count = 1                                        
                            for per_num_key, per_num_val in per_vvalues.items():
        #                        print(per_num_key, 'PP', per_num_val, '++', per, '==', pperiod_count)
                                if pperiod_count == per:
                                    from_num_to_month_onverter[per] = per_num_key
                            #        print(per_num_val, '!!!!!!', per_num_key, producer_name)                    
                                    # работа с данными:
                                    # 1) выборка минимально
                                    if per_num_val is None:
                                        pass
                                    else:
                                        list_of_values_in_one_period_for_comarison.append(per_num_val)
                                        list_of_producers.append(producer_name)
                                    continue
                                pperiod_count += 1
                        #print('llsdfsdf', list_of_values_in_one_period_for_comarison, 'per_num_key ===', per_num_key)
                        values_on_period_for_comparison_dict[per] = list_of_values_in_one_period_for_comarison, list_of_producers
        #        print('LL', values_on_period_for_comparison_dict)
        #        print('from_num_to_month_onverter', from_num_to_month_onverter)

                ######  1.1 подготовка производителя с минимальным значением. Впринципе, есть готовый словарь values_on_period_for_comparison_dict, где собраны средние значения производителей данного типорамера по периодам. Получим  прямо находу хдесь
                month_name_from_number_dict = { 1 : 'январь', 2: 'февраль', 3 : 'март', 4 : 'апрель', 5 : 'май', 6 :'июнь', 7 : 'июль', 8 : 'август', 9 : 'сентябрь', 10 : 'октябрь', 11 : 'ноябрь', 12 : 'декабрь'}
                for period_nnum_prod, vval in values_on_period_for_comparison_dict.items():
                    for values in vval:
                        if values:                  # переборка до первого периода ценами:
                            min_value = min(vval[0])
                            index_of_min_value = vval[0].index(min_value)
                            result_min_value_producer = vval[1][index_of_min_value]
                            month_num = from_num_to_month_onverter[period_nnum_prod].month
                            month_num_name = month_name_from_number_dict[month_num]
                            period = month_num_name + ' ' + str(from_num_to_month_onverter[period_nnum_prod].year)
                    #        print('producer = ', result_min_value_producer, 'min value = ', min_value, 'month =', period)
                    if min_value:           # если есть значение в периоде - то закончить переборку
                        break
            # ПЕРЕВОД ПО КУРСУ НАЦБАНКА
                min_value_usd = None
            if CURRENCY_VALUE_USD:
                min_value_usd = min_value * CURRENCY_VALUE_USD

            # РАСЧЕТ ОТКЛОНЕНИЯ:        
                deflection = '' 
                try:                                                                                                                     # для расчета отклонения 
                    if type(min_value) is float and self.belarus902price != None:  
                        deflection = self.belarus902price.price / min_value       # для расчета отклонения

                        # перевод в удобоваримый вид
                        min_value =float('{:.2f}'.format(min_value))
                        min_value = '{:,}'.format(min_value).replace(',', ' ')
                        min_value_usd =float('{:.2f}'.format(min_value_usd))
                        min_value_usd = '{:,}'.format(min_value_usd).replace(',', ' ')
                        deflection =float('{:.2f}'.format(deflection))
                        deflection = '{:,}'.format(deflection).replace(',', ' ')
                        #  END перевод в удобоваримый вид
                        chemcurier_unique_result = result_min_value_producer, min_value, min_value_usd, deflection, period
                except:                      
                        # перевод в удобоваримый вид
                        min_value =float('{:.2f}'.format(min_value))
                        min_value = '{:,}'.format(min_value).replace(',', ' ')
                        min_value_usd =float('{:.2f}'.format(min_value_usd))
                        min_value_usd = '{:,}'.format(min_value_usd).replace(',', ' ')
                        #  END перевод в удобоваримый вид
                        chemcurier_unique_result = result_min_value_producer, min_value, min_value_usd, deflection, period
            #print('producer = ', result_min_value_producer, 'min_value_usd = ', min_value_usd, 'min value = ', min_value, 'month =', period)
    #        print('11!!', chemcurier_unique_result)
            return chemcurier_unique_result
        except:
            #chemcurier_unique_result = ('', '', '', '', '')
            #return chemcurier_unique_result
            pass

    
# ______ RUS_____

    def express_shina_competitor_on_date1(self):                                       # отдаем конкурентов и цены + отклонение цены 902 прайса от цены express_shina 
            competitors_values_list = EXPRESS_SHINA_COMPETITORS_DICTIONARY1[self.tyre]
            list_od_combined_comp_and_prices = []
            #print(competitors_values_list,'competitors_values_list ')
            ######################### ДОП ФИЛЬТРАЦИЯ ПО ТИПОРАЗМЕРУ, ИНДЕКСАМ, СЕЗОННОСТИ:
            filtered_competitors_values_list = []
            for objject in competitors_values_list:
                #print('objjectobjjectobjjectobjject======================================================', objject, objject.developer , objject.site, objject.season)
                if objject is None:
                    pass
                else:
                    competior_is_found = False
                    tyre_in_base_season = str
                    if objject.season and self.tyre.added_features.all():
                        #tyre_in_base_season = self.tyre.added_features.all()[0].season_usage 
                        tyre_in_base_season = self.tyre.added_features.all()
                        for n in tyre_in_base_season:
                            if n.season_usage:
                                tyre_in_base_season = n.season_usage.season_usage_name 
                        #print('tyre_in_base_season111', tyre_in_base_season)
                        tyre_in_base_index = self.tyre.added_features.all()[0].indexes_list
                    if tyre_in_base_season is None or objject.season is None:                       #0 
                        filtered_competitors_values_list.append(objject)
            #            print('OOO22222O')
                    else:
                        if tyre_in_base_season == objject.season.season_usage_name and tyre_in_base_index == objject.parametres_competitor:       # 1) ЗАОДНО совмещаем конкурентов с шинами в базе по сезонности  и индексам:
            #                print('OOOO', 'tyre_in_base_season', tyre_in_base_season, 'objject.season.season_usage_name', objject.season.season_usage_name)
                            objject.tyre_to_compare.add(self)                           # ДОПОЛНИТЕЛЬНОЕ БАЛОВСТВО
                            filtered_competitors_values_list.append(objject)            # ВОТ ТУТ ВСЕ И ПРОИСХОДИТ
                            continue
                        if tyre_in_base_season == objject.season.season_usage_name:                                                               # 2) ЗАОДНО если нет, то совмещаем конкурентов с шинами в базе по сезонности
            #                print('OOIIIIIOO')
                            #print(tyre_in_base_season, objject.season.season_usage_name)
                            objject.tyre_to_compare.add(self)
                            filtered_competitors_values_list.append(objject)  
                            continue
            #print(filtered_competitors_values_list, 'filtered_competitors_values_list')          # [<CompetitorSiteModel: CompetitorSiteModel object (143)>, <CompetitorSiteModel: CompetitorSiteModel object (144)>, <CompetitorSiteModel: CompetitorSiteModel object (145)>
            ##########################
            list_comp_ids = []
            for comp in filtered_competitors_values_list:
                comp_name = comp.name_competitor + ' ' + comp.tyresize_competitor + ' ' + comp.parametres_competitor # + ' '+ comp.season.season_usage_name
                if DEFLECTION_VAL:                                                      # если есть введенные данные об скидке торговой надбавки
                    comp_price = comp.price * ((100 - DEFLECTION_VAL) * 0.01)
                else:
                    comp_price = comp.price  
                #if type(comp_price) is float and self.belarus902price != None:    
                if comp_price and self.currentpricesprice and type(comp_price) is float: 
                    combined = None
                    #deflection = self.belarus902price.price * CURRENCY_VALUE_RUB  / comp_price 
                    if CURRENCY_VALUE_USD:
                        deflection = (self.currentpricesprice.price  * CURRENCY_VALUE_USD  / comp_price) -1 
                        combined = ((comp_name, comp_price, deflection), comp.developer, comp.date_period)
                    else:
                        deflection = ' '
                        combined = ((comp_name, comp_price, deflection), comp.developer, comp.date_period)      
                    #deflection = ((self.currentpricesprice.price  * CURRENCY_VALUE_USD  / comp_price) -1 )
                    #deflection = self.belarus902price.price / comp_price       # для расчета отклонения     # для расчета отклонения  # ((self.currentpricesprice.price / self.semi_variable_prices.price) - 1) * 100
                    combined = None
                    if comp.season:
                        combined = comp.developer.competitor_name + ' ' + comp_name + comp.season.season_usage_name, comp_price, deflection
                    else:
                        combined = comp.developer.competitor_name + ' ' + comp_name, comp_price, deflection
                    combined = ((combined), comp.developer, comp.date_period) 
                    if combined:
                        list_comp_ids.append(comp.id)
                        list_od_combined_comp_and_prices.append(combined)                           # 1
                EXPRESS_SHINA_COMPETITORS_NAMES_FILTER.append(comp.developer.competitor_name) 
                #list_comp_ids.append(comp.id)                                               # 2
            EXPRESS_SHINA_COMPETITORS_NAMES_FILTER_IDS[self.pk] = list_comp_ids                                                                     #  ОТДЕЛЬНО ДЛЯ ФИЛЬТРА ПО ПРОИЗВОДИТЕЛЯМ AVTOSET
            list_od_combined_comp_and_prices = sorted(list(set(list_od_combined_comp_and_prices)))          # + sorted
            #print('list_od_combined_comp_and_prices', list_od_combined_comp_and_prices)
            void_data_num = len(list_od_combined_comp_and_prices)               # доставить дополнительные пробелы там где инфы нет
            for n in range(0, 3-void_data_num):
                list_od_combined_comp_and_prices.append(('', '', ''))
            #print('BBB', list_od_combined_comp_and_prices)
            EXPRESS_SHINA_HEADER_DICT[self.pk] = list_od_combined_comp_and_prices

            return list_od_combined_comp_and_prices
    
    def express_shina_competitor_on_date1(self):                                       # отдаем конкурентов и цены + отклонение цены 902 прайса от цены express_shina 
            competitors_values_list = EXPRESS_SHINA_COMPETITORS_DICTIONARY1[self.tyre]
            list_od_combined_comp_and_prices = []
            #print(competitors_values_list,'competitors_values_list ')
            ######################### ДОП ФИЛЬТРАЦИЯ ПО ТИПОРАЗМЕРУ, ИНДЕКСАМ, СЕЗОННОСТИ:
            filtered_competitors_values_list = []
            for objject in competitors_values_list:
                #print('objjectobjjectobjjectobjject======================================================', objject, objject.developer , objject.site, objject.season)
                if objject is None:
                    pass
                else:
                    competior_is_found = False
                    tyre_in_base_season = str
                    if objject.season and self.tyre.added_features.all():
                        #tyre_in_base_season = self.tyre.added_features.all()[0].season_usage 
                        tyre_in_base_season = self.tyre.added_features.all()
                        for n in tyre_in_base_season:
                            if n.season_usage:
                                tyre_in_base_season = n.season_usage.season_usage_name 
                        #print('tyre_in_base_season111', tyre_in_base_season)
                        tyre_in_base_index = self.tyre.added_features.all()[0].indexes_list
                    if tyre_in_base_season is None or objject.season is None:                       #0 
                        filtered_competitors_values_list.append(objject)
            #            print('OOO22222O')
                    else:
                        if tyre_in_base_season == objject.season.season_usage_name and tyre_in_base_index == objject.parametres_competitor:       # 1) ЗАОДНО совмещаем конкурентов с шинами в базе по сезонности  и индексам:
            #                print('OOOO', 'tyre_in_base_season', tyre_in_base_season, 'objject.season.season_usage_name', objject.season.season_usage_name)
                            objject.tyre_to_compare.add(self)                           # ДОПОЛНИТЕЛЬНОЕ БАЛОВСТВО
                            filtered_competitors_values_list.append(objject)            # ВОТ ТУТ ВСЕ И ПРОИСХОДИТ
                            continue
                        if tyre_in_base_season == objject.season.season_usage_name:                                                               # 2) ЗАОДНО если нет, то совмещаем конкурентов с шинами в базе по сезонности
            #                print('OOIIIIIOO')
                            #print(tyre_in_base_season, objject.season.season_usage_name)
                            objject.tyre_to_compare.add(self)
                            filtered_competitors_values_list.append(objject)  
                            continue
            #print(filtered_competitors_values_list, 'filtered_competitors_values_list')          # [<CompetitorSiteModel: CompetitorSiteModel object (143)>, <CompetitorSiteModel: CompetitorSiteModel object (144)>, <CompetitorSiteModel: CompetitorSiteModel object (145)>
            ##########################
            list_comp_ids = []
            for comp in filtered_competitors_values_list:
                comp_name = comp.name_competitor + ' ' + comp.tyresize_competitor + ' ' + comp.parametres_competitor # + ' '+ comp.season.season_usage_name
                if DEFLECTION_VAL:                                                      # если есть введенные данные об скидке торговой надбавки
                    comp_price = comp.price * ((100 - DEFLECTION_VAL) * 0.01)
                else:
                    comp_price = comp.price  
                #if type(comp_price) is float and self.belarus902price != None:    
                if comp_price and self.currentpricesprice and type(comp_price) is float: 
                    combined = None
                    #deflection = self.belarus902price.price * CURRENCY_VALUE_RUB  / comp_price 
                    if CURRENCY_VALUE_USD:
                        deflection = (self.currentpricesprice.price  * CURRENCY_VALUE_USD  / comp_price) -1 
                        combined = ((comp_name, comp_price, deflection), comp.developer, comp.date_period)
                    else:
                        deflection = ' '
                        combined = ((comp_name, comp_price, deflection), comp.developer, comp.date_period)      
                    #deflection = ((self.currentpricesprice.price  * CURRENCY_VALUE_USD  / comp_price) -1 )
                    #deflection = self.belarus902price.price / comp_price       # для расчета отклонения     # для расчета отклонения  # ((self.currentpricesprice.price / self.semi_variable_prices.price) - 1) * 100
                    combined = None
                    if comp.season:
                        combined = comp.developer.competitor_name + ' ' + comp_name + comp.season.season_usage_name, comp_price, deflection
                    else:
                        combined = comp.developer.competitor_name + ' ' + comp_name, comp_price, deflection
                    combined = ((combined), comp.developer, comp.date_period) 
                    if combined:
                        list_comp_ids.append(comp.id)
                        list_od_combined_comp_and_prices.append(combined)                           # 1
                EXPRESS_SHINA_COMPETITORS_NAMES_FILTER.append(comp.developer.competitor_name) 
                #list_comp_ids.append(comp.id)                                               # 2
            EXPRESS_SHINA_COMPETITORS_NAMES_FILTER_IDS[self.pk] = list_comp_ids                                                                     #  ОТДЕЛЬНО ДЛЯ ФИЛЬТРА ПО ПРОИЗВОДИТЕЛЯМ AVTOSET
            list_od_combined_comp_and_prices = sorted(list(set(list_od_combined_comp_and_prices)))          # + sorted
            #print('list_od_combined_comp_and_prices', list_od_combined_comp_and_prices)
            void_data_num = len(list_od_combined_comp_and_prices)               # доставить дополнительные пробелы там где инфы нет
            for n in range(0, 3-void_data_num):
                list_od_combined_comp_and_prices.append(('', '', ''))
            #print('BBB', list_od_combined_comp_and_prices)
            EXPRESS_SHINA_HEADER_DICT[self.pk] = list_od_combined_comp_and_prices

            return list_od_combined_comp_and_prices
        

    def kolesatyt_competitor_on_date1(self): 
        the_very_final_list_of_competitors_for_current_model_for_header_list = [] 
        the_very_final_list_of_competitors_for_current_model_for_header = [] 
        final_list_of_competitors_for_current_model_for_header = []       
        if self.id in KOLESATYT_HEADER_DICT.keys():
            model_tyr_table_competitores_for_this_tyre = KOLESATYT_HEADER_DICT.get(self.id) 
            # отбор данный для заголовка таблицы
            # 1) получаем перечень производителей - кто есть для вывода
            producer_list_cleaned_data = []
            dates_list_cleaned_data = []
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                producer_list_cleaned_data.append(compet_cleaned_data[1])
                dates_list_cleaned_data.append(compet_cleaned_data[2])
            producer_list_cleaned_data = list(set(producer_list_cleaned_data))
            dates_list_cleaned_data = list(set(dates_list_cleaned_data))
            #print('!!!!!', dates_list_cleaned_data )
            #print('producer_list_cleaned_data', producer_list_cleaned_data)
            # 2) получаем последнюю дату для вывода:
                #2.1) если вводилась дата:
            if COMPETITORS_DATE_FROM_USER_ON_FILTER and COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                current_data_header = datetime.datetime.strptime(COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
            #2.2) если не вводилась дата: 
            else:
                current_data_header = max(dates_list_cleaned_data)   
            #print('current_data_header', current_data_header)
            #3 отбор по последней дате для вывода в таблицу:
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                for prod_vrand in producer_list_cleaned_data:
                    if compet_cleaned_data[2] == current_data_header and compet_cleaned_data[1] == prod_vrand:
                        #print('compet_cleaned_data SS', compet_cleaned_data)
                        final_list_of_competitors_for_current_model_for_header.append(compet_cleaned_data[0])

        if final_list_of_competitors_for_current_model_for_header:
            the_very_final_list_of_competitors_for_current_model_for_header = final_list_of_competitors_for_current_model_for_header  
        if the_very_final_list_of_competitors_for_current_model_for_header:              
            for final_data in the_very_final_list_of_competitors_for_current_model_for_header:   # разбор нга составляющие для представления в таблице
                tuple_len = len(final_data)
                if tuple_len == 3:
                #    print(final_data, type(final_data), len(final_data))
                    brand_name, comp_price, deflection = final_data
                    brand_name_comp_price_deflection = brand_name, comp_price, deflection
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(brand_name_comp_price_deflection)
        #5 дорисовка выводимых в таблице столбцов/конкурентов по типоразмеру:
        if COMPET_PER_SITE:
            void_data_num = len(the_very_final_list_of_competitors_for_current_model_for_header_list)               # доставить дополнительные пробелы там где инфы нет
            #print('!!!!!!!!!!!!!!!', the_very_final_list_of_competitors_for_current_model_for_header_list)
            #print('COMPET_PER_SITE', COMPET_PER_SITE, 'LLLENN',  void_data_num)
    #        print('!!!!!!!!!!!!!!!','void_data_num', void_data_num, 'COMPET_PER_SITE', COMPET_PER_SITE)
            if void_data_num > COMPET_PER_SITE or void_data_num == COMPET_PER_SITE:
                the_very_final_list_of_competitors_for_current_model_for_header_list = the_very_final_list_of_competitors_for_current_model_for_header_list[:COMPET_PER_SITE]
            else:
                for n in range(0, COMPET_PER_SITE-void_data_num):
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(('', '', ''))

    #    print('!! FINAL OCHKA EXPRESS_SHINA', the_very_final_list_of_competitors_for_current_model_for_header_list)
        return the_very_final_list_of_competitors_for_current_model_for_header_list
    
    
    def kolesa_darom_competitor_on_date1(self):  
        the_very_final_list_of_competitors_for_current_model_for_header_list = [] 
        the_very_final_list_of_competitors_for_current_model_for_header = [] 
        final_list_of_competitors_for_current_model_for_header = []       
        if self.id in KOLESA_DAROM_HEADER_DICT.keys():
            model_tyr_table_competitores_for_this_tyre = KOLESA_DAROM_HEADER_DICT.get(self.id) 
            # отбор данный для заголовка таблицы
            # 1) получаем перечень производителей - кто есть для вывода
            producer_list_cleaned_data = []
            dates_list_cleaned_data = []
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                producer_list_cleaned_data.append(compet_cleaned_data[1])
                dates_list_cleaned_data.append(compet_cleaned_data[2])
            producer_list_cleaned_data = list(set(producer_list_cleaned_data))
            dates_list_cleaned_data = list(set(dates_list_cleaned_data))
            #print('!!!!!', dates_list_cleaned_data )
            #print('producer_list_cleaned_data', producer_list_cleaned_data)
            # 2) получаем последнюю дату для вывода:
                #2.1) если вводилась дата:
            if COMPETITORS_DATE_FROM_USER_ON_FILTER and COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                current_data_header = datetime.datetime.strptime(COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
            #2.2) если не вводилась дата: 
            else:
                current_data_header = max(dates_list_cleaned_data)   
            #print('current_data_header', current_data_header)
            #3 отбор по последней дате для вывода в таблицу:
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                for prod_vrand in producer_list_cleaned_data:
                    if compet_cleaned_data[2] == current_data_header and compet_cleaned_data[1] == prod_vrand:
                        #print('compet_cleaned_data SS', compet_cleaned_data)
                        final_list_of_competitors_for_current_model_for_header.append(compet_cleaned_data[0])

        if final_list_of_competitors_for_current_model_for_header:
            the_very_final_list_of_competitors_for_current_model_for_header = final_list_of_competitors_for_current_model_for_header  
        if the_very_final_list_of_competitors_for_current_model_for_header:              
            for final_data in the_very_final_list_of_competitors_for_current_model_for_header:   # разбор нга составляющие для представления в таблице
                tuple_len = len(final_data)
                if tuple_len == 3:
                #    print(final_data, type(final_data), len(final_data))
                    brand_name, comp_price, deflection = final_data
                    brand_name_comp_price_deflection = brand_name, comp_price, deflection
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(brand_name_comp_price_deflection)
        #5 дорисовка выводимых в таблице столбцов/конкурентов по типоразмеру:
        if COMPET_PER_SITE:
            void_data_num = len(the_very_final_list_of_competitors_for_current_model_for_header_list)               # доставить дополнительные пробелы там где инфы нет
            #print('!!!!!!!!!!!!!!!', the_very_final_list_of_competitors_for_current_model_for_header_list)
            #print('COMPET_PER_SITE', COMPET_PER_SITE, 'LLLENN',  void_data_num)
    #        print('!!!!!!!!!!!!!!!','void_data_num', void_data_num, 'COMPET_PER_SITE', COMPET_PER_SITE)
            if void_data_num > COMPET_PER_SITE or void_data_num == COMPET_PER_SITE:
                the_very_final_list_of_competitors_for_current_model_for_header_list = the_very_final_list_of_competitors_for_current_model_for_header_list[:COMPET_PER_SITE]
            else:
                for n in range(0, COMPET_PER_SITE-void_data_num):
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(('', '', ''))

    #    print('!! FINAL OCHKA KOLESATYT_HEADER_DICT', the_very_final_list_of_competitors_for_current_model_for_header_list)
        return the_very_final_list_of_competitors_for_current_model_for_header_list
    


    def express_shina_table_header(self):
        the_very_final_list_of_competitors_for_current_model_for_header_list = [] 
        the_very_final_list_of_competitors_for_current_model_for_header = [] 
        final_list_of_competitors_for_current_model_for_header = []       
        if self.id in EXPRESS_SHINA_HEADER_DICT.keys():
            model_tyr_table_competitores_for_this_tyre = EXPRESS_SHINA_HEADER_DICT.get(self.id) 
            # отбор данный для заголовка таблицы
            # 1) получаем перечень производителей - кто есть для вывода
            producer_list_cleaned_data = []
            dates_list_cleaned_data = []
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                producer_list_cleaned_data.append(compet_cleaned_data[1])
                dates_list_cleaned_data.append(compet_cleaned_data[2])
            producer_list_cleaned_data = list(set(producer_list_cleaned_data))
            dates_list_cleaned_data = list(set(dates_list_cleaned_data))
            #print('!!!!!', dates_list_cleaned_data )
            #print('producer_list_cleaned_data', producer_list_cleaned_data)
            # 2) получаем последнюю дату для вывода:
                #2.1) если вводилась дата:
            if COMPETITORS_DATE_FROM_USER_ON_FILTER and COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                current_data_header = datetime.datetime.strptime(COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
            #2.2) если не вводилась дата: 
            else:
                current_data_header = max(dates_list_cleaned_data)   
            #print('current_data_header', current_data_header)
            #3 отбор по последней дате для вывода в таблицу:
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                for prod_vrand in producer_list_cleaned_data:
                    if compet_cleaned_data[2] == current_data_header and compet_cleaned_data[1] == prod_vrand:
                        #print('compet_cleaned_data SS', compet_cleaned_data)
                        final_list_of_competitors_for_current_model_for_header.append(compet_cleaned_data[0])

        if final_list_of_competitors_for_current_model_for_header:
            the_very_final_list_of_competitors_for_current_model_for_header = final_list_of_competitors_for_current_model_for_header  
        if the_very_final_list_of_competitors_for_current_model_for_header:              
            for final_data in the_very_final_list_of_competitors_for_current_model_for_header:   # разбор нга составляющие для представления в таблице
                tuple_len = len(final_data)
                if tuple_len == 3:
                #    print(final_data, type(final_data), len(final_data))
                    brand_name, comp_price, deflection = final_data
                    brand_name_comp_price_deflection = brand_name, comp_price, deflection
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(brand_name_comp_price_deflection)
        #5 дорисовка выводимых в таблице столбцов/конкурентов по типоразмеру:
        if COMPET_PER_SITE:
            void_data_num = len(the_very_final_list_of_competitors_for_current_model_for_header_list)               # доставить дополнительные пробелы там где инфы нет
            #print('!!!!!!!!!!!!!!!', the_very_final_list_of_competitors_for_current_model_for_header_list)
            #print('COMPET_PER_SITE', COMPET_PER_SITE, 'LLLENN',  void_data_num)
    #        print('!!!!!!!!!!!!!!!','void_data_num', void_data_num, 'COMPET_PER_SITE', COMPET_PER_SITE)
            if void_data_num > COMPET_PER_SITE or void_data_num == COMPET_PER_SITE:
                the_very_final_list_of_competitors_for_current_model_for_header_list = the_very_final_list_of_competitors_for_current_model_for_header_list[:COMPET_PER_SITE]
            else:
                for n in range(0, COMPET_PER_SITE-void_data_num):
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(('', '', ''))

    #    print('!! FINAL OCHKA EXPRESS_SHINA', the_very_final_list_of_competitors_for_current_model_for_header_list)
        return the_very_final_list_of_competitors_for_current_model_for_header_list

    def kolesa_darom_table_header(self):
        the_very_final_list_of_competitors_for_current_model_for_header_list = [] 
        the_very_final_list_of_competitors_for_current_model_for_header = [] 
        final_list_of_competitors_for_current_model_for_header = []       
        if self.id in KOLESA_DAROM_HEADER_DICT.keys():
            model_tyr_table_competitores_for_this_tyre = KOLESA_DAROM_HEADER_DICT.get(self.id) 
            # отбор данный для заголовка таблицы
            # 1) получаем перечень производителей - кто есть для вывода
            producer_list_cleaned_data = []
            dates_list_cleaned_data = []
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                producer_list_cleaned_data.append(compet_cleaned_data[1])
                dates_list_cleaned_data.append(compet_cleaned_data[2])
            producer_list_cleaned_data = list(set(producer_list_cleaned_data))
            dates_list_cleaned_data = list(set(dates_list_cleaned_data))
            #print('!!!!!', dates_list_cleaned_data )
            #print('producer_list_cleaned_data', producer_list_cleaned_data)
            # 2) получаем последнюю дату для вывода:
                #2.1) если вводилась дата:
            if COMPETITORS_DATE_FROM_USER_ON_FILTER and COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                current_data_header = datetime.datetime.strptime(COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
            #2.2) если не вводилась дата: 
            else:
                current_data_header = max(dates_list_cleaned_data)   
            #print('current_data_header', current_data_header)
            #3 отбор по последней дате для вывода в таблицу:
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                for prod_vrand in producer_list_cleaned_data:
                    if compet_cleaned_data[2] == current_data_header and compet_cleaned_data[1] == prod_vrand:
                        #print('compet_cleaned_data SS', compet_cleaned_data)
                        final_list_of_competitors_for_current_model_for_header.append(compet_cleaned_data[0])

        if final_list_of_competitors_for_current_model_for_header:
            the_very_final_list_of_competitors_for_current_model_for_header = final_list_of_competitors_for_current_model_for_header  
        if the_very_final_list_of_competitors_for_current_model_for_header:              
            for final_data in the_very_final_list_of_competitors_for_current_model_for_header:   # разбор нга составляющие для представления в таблице
                tuple_len = len(final_data)
                if tuple_len == 3:
                #    print(final_data, type(final_data), len(final_data))
                    brand_name, comp_price, deflection = final_data
                    brand_name_comp_price_deflection = brand_name, comp_price, deflection
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(brand_name_comp_price_deflection)
        #5 дорисовка выводимых в таблице столбцов/конкурентов по типоразмеру:
        if COMPET_PER_SITE:
            void_data_num = len(the_very_final_list_of_competitors_for_current_model_for_header_list)               # доставить дополнительные пробелы там где инфы нет
            #print('!!!!!!!!!!!!!!!', the_very_final_list_of_competitors_for_current_model_for_header_list)
            #print('COMPET_PER_SITE', COMPET_PER_SITE, 'LLLENN',  void_data_num)
    #        print('!!!!!!!!!!!!!!!','void_data_num', void_data_num, 'COMPET_PER_SITE', COMPET_PER_SITE)
            if void_data_num > COMPET_PER_SITE or void_data_num == COMPET_PER_SITE:
                the_very_final_list_of_competitors_for_current_model_for_header_list = the_very_final_list_of_competitors_for_current_model_for_header_list[:COMPET_PER_SITE]
            else:
                for n in range(0, COMPET_PER_SITE-void_data_num):
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(('', '', ''))

    #    print('!! FINAL OCHKA KOLESA_DAROM_HEADER_DICT_HEADER_DICT', the_very_final_list_of_competitors_for_current_model_for_header_list)
        return the_very_final_list_of_competitors_for_current_model_for_header_list

    def kolesatyt_table_header(self):
        the_very_final_list_of_competitors_for_current_model_for_header_list = [] 
        the_very_final_list_of_competitors_for_current_model_for_header = [] 
        final_list_of_competitors_for_current_model_for_header = []       
        if self.id in KOLESA_DAROM_HEADER_DICT.keys():
            model_tyr_table_competitores_for_this_tyre = KOLESA_DAROM_HEADER_DICT.get(self.id) 
            # отбор данный для заголовка таблицы
            # 1) получаем перечень производителей - кто есть для вывода
            producer_list_cleaned_data = []
            dates_list_cleaned_data = []
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                producer_list_cleaned_data.append(compet_cleaned_data[1])
                dates_list_cleaned_data.append(compet_cleaned_data[2])
            producer_list_cleaned_data = list(set(producer_list_cleaned_data))
            dates_list_cleaned_data = list(set(dates_list_cleaned_data))
            #print('!!!!!', dates_list_cleaned_data )
            #print('producer_list_cleaned_data', producer_list_cleaned_data)
            # 2) получаем последнюю дату для вывода:
                #2.1) если вводилась дата:
            if COMPETITORS_DATE_FROM_USER_ON_FILTER and COMPETITORS_DATE_FROM_USER_ON_FILTER != ['']:
                current_data_header = datetime.datetime.strptime(COMPETITORS_DATE_FROM_USER_ON_FILTER[0], "%Y-%m-%d").date()
            #2.2) если не вводилась дата: 
            else:
                current_data_header = max(dates_list_cleaned_data)   
            #print('current_data_header', current_data_header)
            #3 отбор по последней дате для вывода в таблицу:
            for compet_cleaned_data in model_tyr_table_competitores_for_this_tyre:
                for prod_vrand in producer_list_cleaned_data:
                    if compet_cleaned_data[2] == current_data_header and compet_cleaned_data[1] == prod_vrand:
                        #print('compet_cleaned_data SS', compet_cleaned_data)
                        final_list_of_competitors_for_current_model_for_header.append(compet_cleaned_data[0])

        if final_list_of_competitors_for_current_model_for_header:
            the_very_final_list_of_competitors_for_current_model_for_header = final_list_of_competitors_for_current_model_for_header  
        if the_very_final_list_of_competitors_for_current_model_for_header:              
            for final_data in the_very_final_list_of_competitors_for_current_model_for_header:   # разбор нга составляющие для представления в таблице
                tuple_len = len(final_data)
                if tuple_len == 3:
                #    print(final_data, type(final_data), len(final_data))
                    brand_name, comp_price, deflection = final_data
                    brand_name_comp_price_deflection = brand_name, comp_price, deflection
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(brand_name_comp_price_deflection)
        #5 дорисовка выводимых в таблице столбцов/конкурентов по типоразмеру:
        if COMPET_PER_SITE:
            void_data_num = len(the_very_final_list_of_competitors_for_current_model_for_header_list)               # доставить дополнительные пробелы там где инфы нет
            #print('!!!!!!!!!!!!!!!', the_very_final_list_of_competitors_for_current_model_for_header_list)
            #print('COMPET_PER_SITE', COMPET_PER_SITE, 'LLLENN',  void_data_num)
    #        print('!!!!!!!!!!!!!!!','void_data_num', void_data_num, 'COMPET_PER_SITE', COMPET_PER_SITE)
            if void_data_num > COMPET_PER_SITE or void_data_num == COMPET_PER_SITE:
                the_very_final_list_of_competitors_for_current_model_for_header_list = the_very_final_list_of_competitors_for_current_model_for_header_list[:COMPET_PER_SITE]
            else:
                for n in range(0, COMPET_PER_SITE-void_data_num):
                    the_very_final_list_of_competitors_for_current_model_for_header_list.append(('', '', ''))

    #    print('!! FINAL OCHKA KOLESA_DAROM', the_very_final_list_of_competitors_for_current_model_for_header_list)
        return the_very_final_list_of_competitors_for_current_model_for_header_list


class CompetitorSiteModel(models.Model):
    site = models.CharField(
        max_length=60,
        verbose_name='наименование сайта',
        null=True,
        blank=True,
    )
    tyre_to_compare = models.ManyToManyField(
        ComparativeAnalysisTyresModel,
        related_name='price_tyre_to_compare',
        #on_delete=models.PROTECT,
        #null=True,
        blank=True, 
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        on_delete=models.CASCADE,
    )
    price = models.FloatField(
        verbose_name='цена конкурента',
        blank=True,
        null=True,
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True, 
    ) 
    developer = models.ForeignKey(
        dictionaries_models.CompetitorModel,
        related_name='developer_competitor',
        on_delete=models.CASCADE,
        null=False,
        blank=True, 
    )
    tyresize_competitor = models.CharField(
        verbose_name='типоразмер конкурент',                
        null=False,
        blank=True, 
        max_length=60,
    )
    name_competitor = models.CharField(
        verbose_name='наименование конкурент',
        null=False,
        blank=True, 
        max_length=60,
    )
    parametres_competitor = models.CharField(
        verbose_name='параметры конкурент',
        null=False,
        blank=True, 
        max_length=60,
    )
    season = models.ForeignKey(
        dictionaries_models.SeasonUsageModel,
        verbose_name='сезонность',
        related_name='competitor_site_sseason_uusage',
        on_delete=models.CASCADE,
        null=True,
        blank=True, 
    )
    group = models.ForeignKey(
        dictionaries_models.TyreGroupModel,
        verbose_name='группа шин',
        related_name='competitor_site_group_uusage',
        on_delete=models.CASCADE,
        null=True,
        blank=True, 
    )    
class ChemCurierTyresModel(models.Model):
    tyre_size_chem = models.CharField(
        verbose_name='типоразмер химкурьер',            
        max_length=60,
    )
    producer_chem = models.CharField(
        verbose_name='производитель химкурьер',
        max_length=60,
    )
    reciever_chem = models.CharField(
        verbose_name='получатель химкурьер',
        max_length=50,
        null=False,
        blank=True,
    )
    prod_country = models.CharField(
        verbose_name='страна производства',
        max_length=60,
        null=False,
        blank=True,
    )    
    group_chem = models.ForeignKey(
        dictionaries_models.TyreGroupModel,
        verbose_name='группа шин',
        related_name='chemcurier_group_uusage',
        on_delete=models.CASCADE,
        null=True,
        blank=True, 
    ) 
    currency_chem = models.ForeignKey(
        dictionaries_models.Currency,
        on_delete=models.CASCADE,
    )
    data_month_chem = models.DateField(
        verbose_name='месяц (дата) поставки',
        null=False,
        blank=True,     
        auto_now=False,
        auto_now_add=False   
    )
    val_on_moth_chem = models.IntegerField(
        verbose_name='объем поставки на дату(месяц) шт.',
        blank=True,
        null=True
    )
    money_on_moth_chem = models.FloatField(                     #  Decimal
        verbose_name='объем поставки на дату(месяц) деньги',
        max_length=60,
        blank=True,
        null=True
    )
    average_price_in_usd = models.FloatField(
        verbose_name='средневзвешеная цена, в USD',
        max_length=60,
        blank=True,
        null=True
    )

    def average_from_usd_to_bel(self):              # для вывода щначения в удобовримом виде ( знаки после запятой, разделение на разряды)
        average_from_usd_to_be = CURRENCY_VALUE_USD * self.average_price_in_usd
        average_from_usd_to_be =float('{:.2f}'.format(average_from_usd_to_be))
        average_from_usd_to_be = '{:,}'.format(average_from_usd_to_be).replace(',', ' ')        
        return average_from_usd_to_be
    
    def obj_val_on_moth_chem_for_table(self):       # для вывода щначения в удобовримом виде ( знаки после запятой, разделение на разряды)
        resurrected_value = self.val_on_moth_chem
        resurrected_value =float('{:.2f}'.format(resurrected_value))
        resurrected_value = '{:,}'.format(resurrected_value).replace(',', ' ')      
        return resurrected_value

    def obj_money_on_moth_chem_for_table(self):       # для вывода щначения в удобовримом виде ( знаки после запятой, разделение на разряды)
        resurrected_value = self.money_on_moth_chem
        resurrected_value =float('{:.2f}'.format(resurrected_value))
        resurrected_value = '{:,}'.format(resurrected_value).replace(',', ' ')        
        return resurrected_value

    def obj_average_price_in_usd_chem_for_table(self):       # для вывода щначения в удобовримом виде ( знаки после запятой, разделение на разряды)
        resurrected_value = self.average_price_in_usd
        resurrected_value =float('{:.2f}'.format(resurrected_value))
        resurrected_value = '{:,}'.format(resurrected_value).replace(',', ' ')        
        return resurrected_value  

class DataPriceValMoneyChemCurierModel(models.Model):
    data_month_chem = models.DateTimeField(
        verbose_name='месяц (дата) поставки',
        auto_now=False,
        auto_now_add=False
    )
    val_on_moth_chem = models.IntegerField(
        verbose_name='объем поставки на дату(месяц) шт.',
        blank=True,
        null=True
    )
    money_on_moth_chem = models.FloatField(
        verbose_name='объем поставки на дату(месяц) деньги',
        max_length=20,
        blank=True,
        null=True
    )
    price_on_date_chem = models.FloatField(
        verbose_name='цена на дату(месяц) деньги',
        max_length=20,
        blank=True,
        null=True
    )
    price_val_money_data = models.ForeignKey(
        ChemCurierTyresModel,
        on_delete=models.CASCADE,
        verbose_name='цены, объемы продаж на дату',
        related_name='price_val_money_data_obj',
        null=True, 
        blank=True
    )


