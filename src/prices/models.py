from django.db import models
from dictionaries import models as dictionaries_models
from tyres import models as tyres_model
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

ONLINER_COMPETITORS_DICTIONARY1 = {}
ONLINER_HEADER_NUMBER = int
#ONLINER UPDATEVIEW:
ONLINER_COMPETITORS = []
ONLINER_COMPETITORS_NAMES_FILTER = []
ONLINER_COMPETITORS_NAMES_FILTER_IDS = {}           # id отфильтрованных для template точно подошедших конкурентов

AVTOSET_COMPETITORS = []
AVTOSET_COMPETITORS_DICTIONARY1 = {}
AVTOSET_HEADER_NUMBER = int
AVTOSET_COMPETITORS_NAMES_FILTER = []
AVTOSET_COMPETITORS_NAMES_FILTER_IDS = {}

BAGORIA_COMPETITORS = []
BAGORIA_COMPETITORS_DICTIONARY1 = {}
BAGORIA_HEADER_NUMBER = int
BAGORIA_COMPETITORS_NAMES_FILTER = []
BAGORIA_COMPETITORS_NAMES_FILTER_IDS = {}

CHEMCURIER_COMPETITORS = []
CHEMCURIER_COMPETITORS_DICTIONARY1 = {}
CHEMCURIER_HEADER_NUMBER = int

ONL_AVT_BAG_ALL_BRANDS_CHOSEN = None

SELF_PRODUCTION = []
SELF_PRODUCTION_ALL = []
SELF_PRODUCTION_FIRST = False
COMPETITORS_DATE_FROM_USER_ON_FILTER = []
TYRE_GROUPS = []
TYRE_GROUPS_ALL=[]

DEFLECTION_VAL = None
PAGINATION_VAL = None
# ______ RUS_____

EXPRESS_SHINA_COMPETITORS = []
EXPRESS_SHINA_COMPETITORS_DICTIONARY1 = {}
EXPRESS_SHINA_HEADER_NUMBER = int
EXPRESS_SHINA_COMPETITORS_NAMES_FILTER = []
EXPRESS_SHINA_COMPETITORS_NAMES_FILTER_IDS = {}

KOLESATYT_COMPETITORS = []
KOLESATYT_COMPETITORS_DICTIONARY1 = {}
KOLESATYT_HEADER_NUMBER = int
KOLESATYT_COMPETITORS_NAMES_FILTER = []
KOLESATYT_COMPETITORS_NAMES_FILTER_IDS = {}

KOLESA_DAROM_COMPETITORS = []
KOLESA_DAROM_COMPETITORS_DICTIONARY1 = {}
KOLESA_DAROM_HEADER_NUMBER = int
KOLESA_DAROM_COMPETITORS_NAMES_FILTER = []
KOLESA_DAROM_COMPETITORS_NAMES_FILTER_IDS = {}

SEARCH_USER_REQUEST = None

CURRENCY_DATE_GOT_FROM_USER = None
CURRENCY_VALUE_RUB = None

GOOGLECHART_MARKETPLACE_ON = False
WEIGHTED_AVERAGE_ON = False
FULL_LINED_CHART_ON = False
ONLY_ON_CURRENT_DATE = False


FOR_MENU_OBJECTS_LIST = [] # список объектов для вывода в меню (шины с конкурентами)
PRODUCER_FILTER_BRAND_LIST_CHECKED_ON = False

class PlannedCosstModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='planned_costs',
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='prices_currency',
        on_delete=models.PROTECT,
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

class SemiVariableCosstModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='semi_variable_costs',
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='semi_variable_prices_currency',
        on_delete=models.PROTECT,
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

class Belarus902PriceModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='belarus902price',
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='belarus902currency',
        on_delete=models.PROTECT,
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

class TPSRussiaFCAModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='tpsrussiafcaprice',
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='tpsrussiafcacurrency',
        on_delete=models.PROTECT,
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

class TPSKazFCAModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='tpskazfcaprice',
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='tpskazfcacurrency',
        on_delete=models.PROTECT,
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

class TPSMiddleAsiaFCAModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='tpsmiddleasiafcaprice',
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='tpsmiddleasiafcacurrency',
        on_delete=models.PROTECT,
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

class CurrentPricesModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='currentpricesprice',
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='currentpricescurrency',
        on_delete=models.PROTECT,
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

class ComparativeAnalysisTableModel(models.Model):
    customer = models.ForeignKey(
        User,
        verbose_name='Таблица сравнительного анализа',
        related_name='comparative_analysis_table',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    market_table = models.CharField(
        verbose_name='рынок сбыта',
        max_length=15,
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

    def chemcurier_heders_value(self):                 # для расчета количества столбцов с заголовками под данные Chemcurier
        #print('CHEMCURIER_HEADER_NUMBER', CHEMCURIER_HEADER_NUMBER)
        chemcurier_header_1 = 'конкурент Chemcurier'
        chemcurier_header_2 = 'цена конкурента Chemcurier'
        chemcurier_header_3 = 'отклонение цены конкурента Chemcurier'
        list_chemcurier_main_headers = []
        for header_number in range(0, CHEMCURIER_HEADER_NUMBER):
            chemcurier_main_header = chemcurier_header_1, chemcurier_header_2, chemcurier_header_3
            list_chemcurier_main_headers.append(chemcurier_main_header)
        #print('list_chemcurier_main_headers =====================kjhdkfjdsjkhj', list_chemcurier_main_headers)
        return list_chemcurier_main_headers

    def chemcurier_heders_lengt(self):                 # для расчета длинны столбца с заголовками под данные Avtoset
        chemcurier_header_2 = 'цена конкурента Chemcurier'
        head_lengh = 0
        for header_number in range(0, CHEMCURIER_HEADER_NUMBER):
            if chemcurier_header_2:
                head_lengh += 3   
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
        on_delete=models.PROTECT,
    )
    planned_costs = models.ForeignKey(
        PlannedCosstModel,
        related_name='tyre_planned_costs',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    semi_variable_prices = models.ForeignKey(
        SemiVariableCosstModel,
        related_name='tyre_semi_variable_prices',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    belarus902price = models.ForeignKey(
        Belarus902PriceModel,
        related_name='tyre_belarus902price',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    tpsrussiafcaprice = models.ForeignKey(
        TPSRussiaFCAModel,
        related_name='tyre_tpsrussiafcaprice',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    tpskazfcaprice = models.ForeignKey(
        TPSKazFCAModel,
        related_name='tyre_tpskazfcaprice',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    tpsmiddleasiafcaprice = models.ForeignKey(
        TPSMiddleAsiaFCAModel,
        related_name='tyre_tpsmiddleasiafcaprice',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    currentpricesprice = models.ForeignKey(
        CurrentPricesModel,
        related_name='tyre_currentpricesprice',
        on_delete=models.PROTECT,
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
            currentpricesprice_from_currency_to_bel_rub = self.currentpricesprice.price * CURRENCY_VALUE_RUB 
            return currentpricesprice_from_currency_to_bel_rub

    def planned_costs_from_currency_to_bel_rub(self):                                                                        # ДЛЯ ПЕРЕВОДА ИЗ РОСС РУБЛЯ В БЕЛ РУБЛЬ И ВЫВЕДЕНИЯ В TEMPLATE
        if self.planned_costs:
            planned_costs_from_currency_to_bel_rub = self.planned_costs.price * CURRENCY_VALUE_RUB 
            return planned_costs_from_currency_to_bel_rub

    def semi_variable_prices_from_currency_to_bel_rub(self):                                                                  # ДЛЯ ПЕРЕВОДА ИЗ РОСС РУБЛЯ В БЕЛ РУБЛЬ И ВЫВЕДЕНИЯ В TEMPLATE
        if self.semi_variable_prices:
            semi_variable_prices_from_currency_to_bel_rub = self.semi_variable_prices.price * CURRENCY_VALUE_RUB 
            return semi_variable_prices_from_currency_to_bel_rub

    def belarus902price_from_currency_to_bel_rub(self):                                                                  # ДЛЯ ПЕРЕВОДА ИЗ РОСС РУБЛЯ В БЕЛ РУБЛЬ И ВЫВЕДЕНИЯ В TEMPLATE
        if self.belarus902price:
            belarus902price_from_currency_to_bel_rub = self.belarus902price.price * CURRENCY_VALUE_RUB 
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
            #    print('objjectobjjectobjjectobjject======================================================', objject, objject.tyresize_competitor, objject.developer, objject.site, objject.season)
                competior_is_found = False
                tyre_in_base_season = ''
                if objject.season and self.tyre.added_features.all():            
                    #tyre_in_base_season = self.tyre.added_features.all()[0].season_usage 
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
                        if tyre_in_base_season == objject.season.season_usage_name and tyre_in_base_index == objject.parametres_competitor:       # 1) ЗАОДНО совмещаем конкурентов с шинами в базе по сезонности  и индексам:
                            #print('OOOO')
                            objject.tyre_to_compare.add(self)                           # ДОПОЛНИТЕЛЬНОЕ БАЛОВСТВО
                            filtered_competitors_values_list.append(objject)            # ВОТ ТУТ ВСЕ И ПРОИСХОДИТ
                            continue
                        if tyre_in_base_season == objject.season.season_usage_name:                                                               # 2) ЗАОДНО если нет, то совмещаем конкурентов с шинами в базе по сезонности
                            #print('OOIIIIIOO')
                            #print(tyre_in_base_season, objject.season.season_usage_name)
                            objject.tyre_to_compare.add(self)
                            filtered_competitors_values_list.append(objject)  
                            continue

            #########################
            list_comp_ids = []
            for comp in filtered_competitors_values_list:
                comp_name = comp.name_competitor + ' ' + comp.tyresize_competitor + ' ' + comp.parametres_competitor  + ' '+ comp.season.season_usage_name
                if DEFLECTION_VAL:                                                      # если есть введенные данные об скидке торговой надбавки
                    comp_price = comp.price * ((100 - DEFLECTION_VAL) * 0.01)
                else:
                    comp_price = comp.price  
                #if comp_price and self.belarus902price and type(comp_price) is float: 
                if comp_price and self.currentpricesprice and type(comp_price) is float: 
                    #deflection = self.belarus902price.price * CURRENCY_VALUE_RUB  / comp_price       # для расчета отклонения  # ((self.currentpricesprice.price / self.semi_variable_prices.price) - 1) * 100
                    deflection = ((self.currentpricesprice.price  * CURRENCY_VALUE_RUB  / comp_price) -1 ) * 100
                    combined = comp_name, comp_price, deflection
                    list_od_combined_comp_and_prices.append(combined)

                ONLINER_COMPETITORS_NAMES_FILTER.append(comp.developer.competitor_name)
                list_comp_ids.append(comp.id)
            ONLINER_COMPETITORS_NAMES_FILTER_IDS[self.pk] = list_comp_ids                                                                     #  ОТДЕЛЬНО ДЛЯ ФИЛЬТРА ПО ПРОИЗВОДИТЕЛЯМ ОНЛАЙНЕР

            list_od_combined_comp_and_prices = sorted(list(set(list_od_combined_comp_and_prices)))          # + sorted
            #print('list_od_combined_comp_and_prices', list_od_combined_comp_and_prices, len(list_od_combined_comp_and_prices))
            void_data_num = len(list_od_combined_comp_and_prices)               # доставить дополнительные пробелы там где инфы нет
            for n in range(0, 3-void_data_num):
                list_od_combined_comp_and_prices.append(('', '', ''))
            #print('AAA', list_od_combined_comp_and_prices)
            return list_od_combined_comp_and_prices

    def avtoset_competitor_on_date1(self):                                       # отдаем конкурентов и цены + отклонение цены 902 прайса от цены AVTOSET (+ прикрутить формулы сняьтия ценоой надбавки и НДС)   AVTOSET
        if self.tyre in AVTOSET_COMPETITORS_DICTIONARY1.keys() and AVTOSET_COMPETITORS_DICTIONARY1.values():
            competitors_values_list = AVTOSET_COMPETITORS_DICTIONARY1[self.tyre]
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
                        #print('OOO22222O')
                    else:
                        if tyre_in_base_season == objject.season.season_usage_name and tyre_in_base_index == objject.parametres_competitor:       # 1) ЗАОДНО совмещаем конкурентов с шинами в базе по сезонности  и индексам:
                            #print('OOOO')
                            objject.tyre_to_compare.add(self)                           # ДОПОЛНИТЕЛЬНОЕ БАЛОВСТВО
                            filtered_competitors_values_list.append(objject)            # ВОТ ТУТ ВСЕ И ПРОИСХОДИТ
                            continue
                        if tyre_in_base_season == objject.season.season_usage_name:                                                               # 2) ЗАОДНО если нет, то совмещаем конкурентов с шинами в базе по сезонности
                            #print('OOIIIIIOO')
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
                    #deflection = self.belarus902price.price * CURRENCY_VALUE_RUB  / comp_price       
                    deflection = ((self.currentpricesprice.price  * CURRENCY_VALUE_RUB  / comp_price) -1 ) * 100
                    #deflection = self.belarus902price.price / comp_price       # для расчета отклонения     # для расчета отклонения  # ((self.currentpricesprice.price / self.semi_variable_prices.price) - 1) * 100
                    combined = comp.developer.competitor_name + ' ' + comp_name, comp_price, deflection
                    list_od_combined_comp_and_prices.append(combined)
                AVTOSET_COMPETITORS_NAMES_FILTER.append(comp.developer.competitor_name) 
                list_comp_ids.append(comp.id)
            AVTOSET_COMPETITORS_NAMES_FILTER_IDS[self.pk] = list_comp_ids                                                                     #  ОТДЕЛЬНО ДЛЯ ФИЛЬТРА ПО ПРОИЗВОДИТЕЛЯМ AVTOSET
            list_od_combined_comp_and_prices = sorted(list(set(list_od_combined_comp_and_prices)))          # + sorted
            #print('list_od_combined_comp_and_prices', list_od_combined_comp_and_prices)
            void_data_num = len(list_od_combined_comp_and_prices)               # доставить дополнительные пробелы там где инфы нет
            for n in range(0, 3-void_data_num):
                list_od_combined_comp_and_prices.append(('', '', ''))
            #print('BBB', list_od_combined_comp_and_prices)
            return list_od_combined_comp_and_prices

    def bagoria_competitor_on_date1(self):                                       # отдаем конкурентов и цены + отклонение цены 902 прайса от цены BAGORIA (+ прикрутить формулы сняьтия ценоой надбавки и НДС)   BAGORIA
        if self.tyre in BAGORIA_COMPETITORS_DICTIONARY1.keys() and BAGORIA_COMPETITORS_DICTIONARY1.values():
            competitors_values_list = BAGORIA_COMPETITORS_DICTIONARY1[self.tyre]
            list_od_combined_comp_and_prices = []
            ######################### ДОП ФИЛЬТРАЦИЯ ПО ТИПОРАЗМЕРУ, ИНДЕКСАМ, СЕЗОННОСТИ:
            filtered_competitors_values_list = []
            for objject in competitors_values_list:
            #    print('objjectobjjectobjjectobjject======================================================', objject, objject.tyresize_competitor, objject.developer, objject.site, objject.season)
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
                        if tyre_in_base_season == objject.season.season_usage_name and tyre_in_base_index == objject.parametres_competitor:       # 1) ЗАОДНО совмещаем конкурентов с шинами в базе по сезонности  и индексам:
                            #print('OOOO')
                            objject.tyre_to_compare.add(self)                           # ДОПОЛНИТЕЛЬНОЕ БАЛОВСТВО
                            filtered_competitors_values_list.append(objject)            # ВОТ ТУТ ВСЕ И ПРОИСХОДИТ
                            continue
                        if tyre_in_base_season == objject.season.season_usage_name:                                                               # 2) ЗАОДНО если нет, то совмещаем конкурентов с шинами в базе по сезонности
                            #print('OOIIIIIOO')
                            #print(tyre_in_base_season, objject.season.season_usage_name)
                            objject.tyre_to_compare.add(self)
                            filtered_competitors_values_list.append(objject)  
                            continue
            #print(filtered_competitors_values_list, 'filtered_competitors_values_list')          # [<CompetitorSiteModel: CompetitorSiteModel object (143)>, <CompetitorSiteModel: CompetitorSiteModel object (144)>, <CompetitorSiteModel: CompetitorSiteModel object (145)>
            ##########################
            list_comp_ids = []
            for comp in filtered_competitors_values_list:
                comp_name = comp.developer.competitor_name + ' ' + comp.name_competitor + ' ' + comp.tyresize_competitor + ' ' + comp.parametres_competitor # + ' '+ comp.season.season_usage_name     #tyresize_competitor, developer
                comp_price = comp.price 
                #print('LLL', comp_name, comp_price)

                if DEFLECTION_VAL and comp_price:                                                      # если есть введенные данные об скидке торговой надбавки
                    comp_price = comp.price * ((100 - DEFLECTION_VAL) * 0.01)
                    
                #if type(comp_price) is float and self.belarus902price != None:   
                if comp_price and self.currentpricesprice and type(comp_price) is float:      
                    deflection = ((self.currentpricesprice.price  * CURRENCY_VALUE_RUB  / comp_price) -1 ) * 100                    
                    #deflection = self.belarus902price.price / comp_price       # для расчета отклонения
                    combined = comp_name, comp_price, deflection    
                    #print('combined!!!!', combined)
                    list_od_combined_comp_and_prices.append(combined)
                BAGORIA_COMPETITORS_NAMES_FILTER.append(comp.developer.competitor_name)                                                                     #  ОТДЕЛЬНО ДЛЯ ФИЛЬТРА ПО ПРОИЗВОДИТЕЛЯМ ОНЛАЙНЕР
                list_comp_ids.append(comp.id)
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
            return list_od_combined_comp_and_prices

    def chemcurier_competitor_on_date1(self):                                       # отдаем конкурентов и цены + отклонение цены 902 прайса от цены CHEMCURIER (+ прикрутить формулы сняьтия ценоой надбавки и НДС)   CHEMCURIER                                                           
        chemcurier_unique_result = ''
        if self.tyre in CHEMCURIER_COMPETITORS_DICTIONARY1.keys():                  # Tyre object (1926) [<ChemCurierTyresModel: ChemCurierTyresModel object (98)>, <ChemCurierTyresModel: ChemCurierTyresModel object (99)>, <ChemCurierTyresModel: ChemCurierTyresModel object (100)>, <ChemCurierTyresModel: ChemCurierTyresModel object (101)>]
            min_value = '' # минимальное значение из всех прозодителей последнего периода поставки
            result_min_value_producer = ''  # наименование производителя с наименьшим значением (ценой) в последний период поствки
            index_of_min_value = ''        # просто индекс, нужен для вылавливания из списков значений index_of_min_value и result_min_value_producer    
            month_num = '' # номер месяца - на всякий случай

            competitors_values_list = CHEMCURIER_COMPETITORS_DICTIONARY1[self.tyre] 
            ######################### ДОП ФИЛЬТРАЦИЯ ПО ТИПОРАЗМЕРУ, ИНДЕКСАМ, СЕЗОННОСТИ:
            gathered_tyresizes_by_producer_name_dict = {}
            #print('HHHFF', competitors_values_list)
            list_of_producer_names_list = []
            for objject in competitors_values_list:         # пройтись по хикуреровским объектам данного типоразмера
                #print('objjectobjjectobjjectobjject======================================================', objject,)
                if objject is None:
                    pass
                else:
                    list_of_producer_names_list.append(objject.producer_chem)
            #print('list_of_producer_names_list', list_of_producer_names_list)  
            for prod_name in list_of_producer_names_list:
                gathered_tyresizes_by_producer_name_list = []  
                for objject in competitors_values_list:         # пройтись по хикуреровским объектам данного типоразмера
                # 1. выбрать все строки (типоразмеры) одного производителя:             
                    if objject.producer_chem == prod_name:
                        gathered_tyresizes_by_producer_name_list.append(objject)
                #print('GAZERET', gathered_tyresizes_by_producer_name_list, 'PPP', prod_name)
                gathered_tyresizes_by_producer_name_dict[prod_name] = gathered_tyresizes_by_producer_name_list
            #print('|||||', gathered_tyresizes_by_producer_name_dict)    # {'Michelin': [<ChemCurierTyresModel: ChemCurierTyresModel object (109)>], 'Continental': [<ChemCurierTyresModel: ChemCurierTyresModel object (110)>], 'Bridgestone': [<ChemCurierTyresModel:
            # 2 есть словарь gathered_tyresizes_by_producer_name_dict - все размеры отфильтрованы по производителю, теперь выведение средних их цен по каждому периоду из всех размеров одного производителя:
            motnth_periods_vol = 0
            for key, val in gathered_tyresizes_by_producer_name_dict.items():
                for chemcur_obj in val:                 # ChemCurierTyresModel object (109)):
                    motnth_periods_vol  = len(chemcur_obj.price_val_money_data_obj.all())
            # Собираем словарь производитель - все его одинакового типоразмера сложенные по месяцам СО СРЕДНВЗВЕШЕННЫМ ЗНАЧЕНИЕМ
            gazered_all_sizws_by_periods_in_one_producer = {}                                                                                                                                                             
            for key, val in gathered_tyresizes_by_producer_name_dict.items(): 
                #print(key, val)
                all_prices_by_producer_gathered = {} 
                for per_num in range(0, motnth_periods_vol):
                    list_of_values = [] 
                    for chemcur_obj in val:

    #                    mon_val = chemcur_obj.price_val_money_data_obj.all()[per_num].price_on_date_chem               # ЗДЕСЬ неверно расчитано средневзвешенное значение
    #                    list_of_values.append(mon_val)
    #                all_prices_by_producer_gathered[per_num] = list_of_values   
    #            gazered_all_sizws_by_periods_in_one_producer[key] = all_prices_by_producer_gathered     
    #        #print('UU', gazered_all_sizws_by_periods_in_one_producer)                                          # здесь все годно  - все норм посчитано
    #        # 1 ОПЦИЯ ДЛЯ ВЫВОДА: расчет средневзвешенной стоимости типоразмера одного производителя:
    #        result_main_per_producer_size_calculated_dict = {}
    #        for producer, perid_mumb_periods in gazered_all_sizws_by_periods_in_one_producer.items():
    #            #print(producer, perid_mumb_periods)
    #            periods_dict = {}
    #            for perid_mumb, values in perid_mumb_periods.items():
    #                #print(values, len(values))
    #                result_summ_in_period = 0
    #                sum_val_num = 0
    #                sum_val = 0
    #                for numb in values:
    #                    if numb is None:
    #                        pass
    #                    else:
    #                        sum_val_num += 1
    #                        sum_val += numb
    #                if sum_val and sum_val_num:
    #                    result_summ_in_period = sum_val / sum_val_num
    #                if result_summ_in_period:
    #                    periods_dict[perid_mumb] = result_summ_in_period
    #                else:
    #                    periods_dict[perid_mumb] = None
    #            #print('!!', periods_dict)
    #            result_main_per_producer_size_calculated_dict[producer] = periods_dict

                        mon_val = chemcur_obj.price_val_money_data_obj.all()[per_num].val_on_moth_chem, chemcur_obj.price_val_money_data_obj.all()[per_num].money_on_moth_chem
                        list_of_values.append(mon_val)
                    all_prices_by_producer_gathered[per_num] = list_of_values   
                gazered_all_sizws_by_periods_in_one_producer[key] = all_prices_by_producer_gathered     
            #print('UU', gazered_all_sizws_by_periods_in_one_producer)                                          # здесь все годно  - все норм посчитано
            # 1 ОПЦИЯ ДЛЯ ВЫВОДА: расчет средневзвешенной стоимости типоразмера одного производителя:
            result_main_per_producer_size_calculated_dict = {}
            for producer, perid_mumb_periods in gazered_all_sizws_by_periods_in_one_producer.items():
                #print(producer, perid_mumb_periods)
                periods_dict = {}
                for perid_mumb, values in perid_mumb_periods.items():
                    #print(values, len(values))
                    result_summ_in_period = 0
                    sum_money_full = 0
                    sum_val_full = 0
                    for numb in values:
                        sum_val, sum_money = numb
                        if sum_val is None:
                            pass
                        else:
                            #print(sum_val, 'HJHHJGHG')
                            sum_val_full += sum_val
                            sum_money_full += sum_money
                    #print(sum_val_full, ' sum_valsum_valsum_valvsum_val')
                    if sum_money_full and sum_val_full:
                        result_summ_in_period = sum_money_full / sum_val_full
                    if result_summ_in_period:
                        periods_dict[perid_mumb] = result_summ_in_period
                    else:
                        periods_dict[perid_mumb] = None
                #print('!!', periods_dict)
                result_main_per_producer_size_calculated_dict[producer] = periods_dict
            #print('GGGG', result_main_per_producer_size_calculated_dict)
            #print('---------')

            ##### РАСЧЕТ ДЛЯ ВЫВОДА 3 произдводителя с наменьшей ценой последнего периода:
            periods_value = ''            # количество периодов
            for val in result_main_per_producer_size_calculated_dict.values():
                periods_value  = len(val)
                if periods_value and type(periods_value) is int:
                    continue
            #print(periods_value, 'HHHH')
            values_on_period_for_comparison_dict = {}                                                               ## ИТОГОВЫЙ СЛОВАРЬ ключ -период, значение - высчитанная средняя цена ВСЕХ типоразмеров данного производителя (списком) и эти производители (списком)
            if type(periods_value) is int:                                                                          # Для работы словарь может не пригодиться но наглядно демонстрирует результат
                for per in range(periods_value, -1, -1 ):     #reversed()      # ЕСЛИ ФОРМИРОВАТЬ СЛОВАРЬ 0 - ноябрь, 1 - октябрь (т.е. от конца года)
                #for per in range(0, periods_value):     #reversed()             # ЕСЛИ ФОРМИРОВАТЬ СЛОВАРЬ 0 - январь, 1 - февраль (т.е. от начала года)
                    list_of_values_in_one_period_for_comarison = [] 
                    list_of_producers = []
                    for producer_name, per_vvalues in result_main_per_producer_size_calculated_dict.items():                                         
                        for per_num_key, per_num_val in per_vvalues.items():
                            #print(per_num_key, 'PP', per_num_val)
                            if per_num_key == per:
                                #print(per_num_val, '!!!!!!', per_num_key, producer_name)                    
                                # работа с данными:
                                # 1) выборка минимально
                                if per_num_val is None:
                                    pass
                                else:
                                    list_of_values_in_one_period_for_comarison.append(per_num_val)
                                    list_of_producers.append(producer_name)
                                continue
                    #print('llsdfsdf', list_of_values_in_one_period_for_comarison, 'per_num_key ===', per_num_key)
                    values_on_period_for_comparison_dict[per] = list_of_values_in_one_period_for_comarison, list_of_producers
            ####################print('LL', values_on_period_for_comparison_dict)

            ######  1.1 подготовка производителя с минимальным значением. Впринципе, есть готовый словарь values_on_period_for_comparison_dict, где собраны средние значения производителей данного типорамера по периодам. Получим  прямо находу хдесь
            for period_nnum_prod, vval in values_on_period_for_comparison_dict.items():
                for values in vval:
                    if values:                  # переборка до первого периода ценами:
                        #print(vval[0], vval[1])
                        #print('period_nnum, vval', period_nnum_prod, vval, 'VALUES =', values)
                        min_value = min(vval[0])
                        index_of_min_value = vval[0].index(min_value)
                        result_min_value_producer = vval[1][index_of_min_value]
                        month_num = period_nnum_prod
                        #print('producer = ', result_min_value_producer, 'min value = ', min_value, 'month =', period_nnum_prod)
                if min_value:           # если есть значение в периоде - то закончить переборку
                    break

        #deflection = ''                                                                                                                      # для расчета отклонения 
        #if type(min_value) is float and self.belarus902price != None:  
        #    deflection = self.belarus902price.price / min_value       # для расчета отклонения
        ##print('producer = ', result_min_value_producer, 'min value = ', min_value, 'month =', month_num)
        ##print('++++')
        #chemcurier_unique_result = result_min_value_producer, min_value, deflection, #month_num,  #  1) конкурент 2) мин цена псоследнего периода поставки 3) ОТКЛОНЕНИЕ 4) ПЕРИОД № (НАПРИМЕР, 0 - Январь и т.д.) ! ДОПИЛИТЬ  =  перевод в рубли из долларов по курсу НБ
        #return chemcurier_unique_result

            deflection = ''                                                                                                                      # для расчета отклонения 
            if type(min_value) is float and self.belarus902price != None:  
                deflection = self.belarus902price.price / min_value       # для расчета отклонения
        #print('producer = ', result_min_value_producer, 'min value = ', min_value, 'month =', month_num)
        #print('++++')
            chemcurier_unique_result = result_min_value_producer, min_value, deflection, #month_num,  #  1) конкурент 2) мин цена псоследнего периода поставки 3) ОТКЛОНЕНИЕ 4) ПЕРИОД № (НАПРИМЕР, 0 - Январь и т.д.) ! ДОПИЛИТЬ  =  перевод в рубли из долларов по курсу НБ
        return chemcurier_unique_result
# ______ RUS_____

    def express_shina_competitor_on_date1(self):                                       # отдаем конкурентов и цены + отклонение цены 902 прайса от цены BAGORIA (+ прикрутить формулы сняьтия ценоой надбавки и НДС)   express_shina
        if self.tyre in EXPRESS_SHINA_COMPETITORS_DICTIONARY1.keys() and EXPRESS_SHINA_COMPETITORS_DICTIONARY1.values():
            competitors_values_list = EXPRESS_SHINA_COMPETITORS_DICTIONARY1[self.tyre]
            list_od_combined_comp_and_prices = []
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
                        if tyre_in_base_season == objject.season.season_usage_name and tyre_in_base_index == objject.parametres_competitor:       # 1) ЗАОДНО совмещаем конкурентов с шинами в базе по сезонности  и индексам:
                            #print('OOOO')
                            objject.tyre_to_compare.add(self)                           # ДОПОЛНИТЕЛЬНОЕ БАЛОВСТВО
                            filtered_competitors_values_list.append(objject)            # ВОТ ТУТ ВСЕ И ПРОИСХОДИТ
                            continue
                        if tyre_in_base_season == objject.season.season_usage_name:                                                               # 2) ЗАОДНО если нет, то совмещаем конкурентов с шинами в базе по сезонности
                            #print('OOIIIIIOO')
                            #print(tyre_in_base_season, objject.season.season_usage_name)
                            objject.tyre_to_compare.add(self)
                            filtered_competitors_values_list.append(objject)  
                            continue
            #print(filtered_competitors_values_list, 'filtered_competitors_values_list')          # [<CompetitorSiteModel: CompetitorSiteModel object (143)>, <CompetitorSiteModel: CompetitorSiteModel object (144)>, <CompetitorSiteModel: CompetitorSiteModel object (145)>
            ##########################
            list_comp_ids = []
            for comp in filtered_competitors_values_list:
                comp_name = comp.developer.competitor_name + ' ' + comp.name_competitor + ' ' + comp.tyresize_competitor + ' ' + comp.parametres_competitor # + ' '+ comp.season.season_usage_name     #tyresize_competitor, developer
                comp_price = comp.price 

                if DEFLECTION_VAL and comp_price:                                                      # если есть введенные данные об скидке торговой надбавки
                    comp_price = comp.price * ((100 - DEFLECTION_VAL) * 0.01)
                    
                #if type(comp_price) is float and self.belarus902price != None:    
                if comp_price and self.currentpricesprice and type(comp_price) is float:      
                    deflection = ((self.currentpricesprice.price  / comp_price) -1 ) * 100                                                                                                           # для расчета отклонения
                    #deflection = self.belarus902price.price / comp_price       # для расчета отклонения
                    combined = comp_name, comp_price, deflection    
                    list_od_combined_comp_and_prices.append(combined)
                EXPRESS_SHINA_COMPETITORS_NAMES_FILTER.append(comp.developer.competitor_name)                                                                     #  ОТДЕЛЬНО ДЛЯ ФИЛЬТРА ПО ПРОИЗВОДИТЕЛЯМ 
                list_comp_ids.append(comp.id)
            EXPRESS_SHINA_COMPETITORS_NAMES_FILTER_IDS[self.pk] = list_comp_ids         
            list_od_combined_comp_and_prices = sorted(list(set(list_od_combined_comp_and_prices)))          # + sorted
            #print('list_od_combined_comp_and_pricesBAGORIA', list_od_combined_comp_and_prices)
            void_data_num = len(list_od_combined_comp_and_prices)               # доставить дополнительные пробелы там где инфы нет
            for n in range(0, 3-void_data_num):
                list_od_combined_comp_and_prices.append(('', '', ''))
            #print('CCC', list_od_combined_comp_and_prices)
            return list_od_combined_comp_and_prices

    def kolesatyt_competitor_on_date1(self):                                       # отдаем конкурентов и цены + отклонение цены 902 прайса от цены BAGORIA (+ прикрутить формулы сняьтия ценоой надбавки и НДС) kolesatyt
        if self.tyre in KOLESATYT_COMPETITORS_DICTIONARY1.keys() and KOLESATYT_COMPETITORS_DICTIONARY1.values():
            competitors_values_list = KOLESATYT_COMPETITORS_DICTIONARY1[self.tyre]
            list_od_combined_comp_and_prices = []
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
                        if tyre_in_base_season == objject.season.season_usage_name and tyre_in_base_index == objject.parametres_competitor:       # 1) ЗАОДНО совмещаем конкурентов с шинами в базе по сезонности  и индексам:
                            #print('OOOO')
                            objject.tyre_to_compare.add(self)                           # ДОПОЛНИТЕЛЬНОЕ БАЛОВСТВО
                            filtered_competitors_values_list.append(objject)            # ВОТ ТУТ ВСЕ И ПРОИСХОДИТ
                            continue
                        if tyre_in_base_season == objject.season.season_usage_name:                                                               # 2) ЗАОДНО если нет, то совмещаем конкурентов с шинами в базе по сезонности
                            #print('OOIIIIIOO')
                            #print(tyre_in_base_season, objject.season.season_usage_name)
                            objject.tyre_to_compare.add(self)
                            filtered_competitors_values_list.append(objject)  
                            continue
            #print(filtered_competitors_values_list, 'filtered_competitors_values_list')          # [<CompetitorSiteModel: CompetitorSiteModel object (143)>, <CompetitorSiteModel: CompetitorSiteModel object (144)>, <CompetitorSiteModel: CompetitorSiteModel object (145)>
            ##########################
            list_comp_ids = []
            for comp in filtered_competitors_values_list:
                comp_name = comp.developer.competitor_name + ' ' + comp.name_competitor + ' ' + comp.tyresize_competitor + ' ' + comp.parametres_competitor # + ' '+ comp.season.season_usage_name     #tyresize_competitor, developer
                comp_price = comp.price 

                if DEFLECTION_VAL and comp_price:                                                      # если есть введенные данные об скидке торговой надбавки
                    comp_price = comp.price * ((100 - DEFLECTION_VAL) * 0.01)
                    
                #if type(comp_price) is float and self.belarus902price != None:                                                                    # для расчета отклонения
                if comp_price and self.currentpricesprice and type(comp_price) is float:      
                    deflection = ((self.currentpricesprice.price  / comp_price) -1 ) * 100  
                    #deflection = self.belarus902price.price / comp_price       # для расчета отклонения
                    combined = comp_name, comp_price, deflection    
                    list_od_combined_comp_and_prices.append(combined)
                KOLESATYT_COMPETITORS_NAMES_FILTER.append(comp.developer.competitor_name)                                                                     #  ОТДЕЛЬНО ДЛЯ ФИЛЬТРА ПО ПРОИЗВОДИТЕЛЯМ 
                list_comp_ids.append(comp.id)
            KOLESATYT_COMPETITORS_NAMES_FILTER_IDS[self.pk] = list_comp_ids 
            list_od_combined_comp_and_prices = sorted(list(set(list_od_combined_comp_and_prices)))          # + sorted
            #print('list_od_combined_comp_and_pricesBAGORIA', list_od_combined_comp_and_prices)
            void_data_num = len(list_od_combined_comp_and_prices)               # доставить дополнительные пробелы там где инфы нет
            for n in range(0, 3-void_data_num):
                list_od_combined_comp_and_prices.append(('', '', ''))
            #print('CCC', list_od_combined_comp_and_prices)
            return list_od_combined_comp_and_prices

    def kolesa_darom_competitor_on_date1(self):                                       # отдаем конкурентов и цены + отклонение цены 902 прайса от цены BAGORIA (+ прикрутить формулы сняьтия ценоой надбавки и НДС) kolesa_darom
        if self.tyre in KOLESA_DAROM_COMPETITORS_DICTIONARY1.keys() and KOLESA_DAROM_COMPETITORS_DICTIONARY1.values():
            competitors_values_list = KOLESA_DAROM_COMPETITORS_DICTIONARY1[self.tyre]
            list_od_combined_comp_and_prices = []
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
                        if tyre_in_base_season == objject.season.season_usage_name and tyre_in_base_index == objject.parametres_competitor:       # 1) ЗАОДНО совмещаем конкурентов с шинами в базе по сезонности  и индексам:
                            #print('OOOO')
                            objject.tyre_to_compare.add(self)                           # ДОПОЛНИТЕЛЬНОЕ БАЛОВСТВО
                            filtered_competitors_values_list.append(objject)            # ВОТ ТУТ ВСЕ И ПРОИСХОДИТ
                            continue
                        if tyre_in_base_season == objject.season.season_usage_name:                                                               # 2) ЗАОДНО если нет, то совмещаем конкурентов с шинами в базе по сезонности
                            #print('OOIIIIIOO')
                            #print(tyre_in_base_season, objject.season.season_usage_name)
                            objject.tyre_to_compare.add(self)
                            filtered_competitors_values_list.append(objject)  
                            continue
            #print(filtered_competitors_values_list, 'filtered_competitors_values_list')          # [<CompetitorSiteModel: CompetitorSiteModel object (143)>, <CompetitorSiteModel: CompetitorSiteModel object (144)>, <CompetitorSiteModel: CompetitorSiteModel object (145)>
            ##########################
            list_comp_ids = []
            for comp in filtered_competitors_values_list:
                comp_name = comp.developer.competitor_name + ' ' + comp.name_competitor + ' ' + comp.tyresize_competitor + ' ' + comp.parametres_competitor # + ' '+ comp.season.season_usage_name     #tyresize_competitor, developer
                comp_price = comp.price 

                if DEFLECTION_VAL and comp_price:                                                      # если есть введенные данные об скидке торговой надбавки
                    comp_price = comp.price * ((100 - DEFLECTION_VAL) * 0.01)
                    
                #if type(comp_price) is float and self.belarus902price != None:                                                                    # для расчета отклонения
                if comp_price and self.currentpricesprice and type(comp_price) is float:      
                    deflection = ((self.currentpricesprice.price  / comp_price) -1 ) * 100  
                    #deflection = self.belarus902price.price / comp_price       # для расчета отклонения
                    combined = comp_name, comp_price, deflection    
                    list_od_combined_comp_and_prices.append(combined)
                KOLESA_DAROM_COMPETITORS_NAMES_FILTER.append(comp.developer.competitor_name)                                                                     #  ОТДЕЛЬНО ДЛЯ ФИЛЬТРА ПО ПРОИЗВОДИТЕЛЯМ 
                list_comp_ids.append(comp.id)
            KOLESA_DAROM_COMPETITORS_NAMES_FILTER_IDS[self.pk] = list_comp_ids 
            list_od_combined_comp_and_prices = sorted(list(set(list_od_combined_comp_and_prices)))          # + sorted
            #print('list_od_combined_comp_and_pricesBAGORIA', list_od_combined_comp_and_prices)
            void_data_num = len(list_od_combined_comp_and_prices)               # доставить дополнительные пробелы там где инфы нет
            for n in range(0, 3-void_data_num):
                list_od_combined_comp_and_prices.append(('', '', ''))
            #print('CCC', list_od_combined_comp_and_prices)
            return list_od_combined_comp_and_prices
class CompetitorSiteModel(models.Model):
    site = models.CharField(
        max_length=30,
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
        on_delete=models.PROTECT,
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
        on_delete=models.PROTECT,
        null=False,
        blank=True, 
    )
    tyresize_competitor = models.CharField(
        verbose_name='типоразмер конкурент',                
        null=False,
        blank=True, 
        max_length=25
    )
    name_competitor = models.CharField(
        verbose_name='наименование конкурент',
        null=False,
        blank=True, 
        max_length=25
    )
    parametres_competitor = models.CharField(
        verbose_name='параметры конкурент',
        null=False,
        blank=True, 
        max_length=25
    )
    season = models.ForeignKey(
        dictionaries_models.SeasonUsageModel,
        verbose_name='сезонность',
        related_name='competitor_site_sseason_uusage',
        on_delete=models.PROTECT,
        null=True,
        blank=True, 
    )
class ChemCurierTyresModel(models.Model):
    tyre_size_chem = models.CharField(
        verbose_name='типоразмер химкурьер',            
        max_length=10,
    )
    producer_chem = models.CharField(
        verbose_name='производитель химкурьер',
        max_length=15,
    )
    group_chem = models.CharField(
        verbose_name='подгруппа химкурьер',
        max_length=20,
    )
    currency_chem = models.ForeignKey(
        dictionaries_models.Currency,
        on_delete=models.PROTECT,
    )
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
        on_delete=models.PROTECT,
        verbose_name='цены, объемы продаж на дату',
        related_name='price_val_money_data_obj',
        null=True, 
        blank=True
    )