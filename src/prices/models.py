from django.db import models
from dictionaries import models as dictionaries_models
from tyres import models as tyres_model
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

#ONLINER_COMPETITORS_DICTIONARY = {}
ONLINER_COMPETITORS_DICTIONARY1 = {}
ONLINER_HEADER_NUMBER = int
#ONLINER UPDATEVIEW:
ONLINER_COMPETITORS = []


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
        default=0
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



#comparative analysis
class ComparativeAnalysisTableModel(models.Model):
    customer = models.ForeignKey(
        User,
        verbose_name='Таблица сравнительного анализа',
        related_name='comparative_analysis_table',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
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
        

class ComparativeAnalysisTyresModel(models.Model):
    table = models.ForeignKey(
        ComparativeAnalysisTableModel,
        verbose_name='Таблица',
        related_name='comparative_table',                    
        on_delete=models.CASCADE,  
        null=True                       # Заглушка
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
    sale_data = models.DateTimeField(
        verbose_name='Дата парсинга',
        auto_now=False,
        auto_now_add=True
    )


    def planned_profitability(self):            # плановая рентабьельность
        if self.currentpricesprice and self.planned_costs:
            print(self.currentpricesprice.price,  self.planned_costs.price)
            planned_profitability = (self.currentpricesprice.price / self.planned_costs.price) - 1 
            planned_profitability = float('{:.2f}'.format(planned_profitability))
            return planned_profitability
        return 0

    def direct_cost_variance(self):             # отклонение прямых затрат
        if self.currentpricesprice and self.semi_variable_prices:
            direct_cost_variance = (self.currentpricesprice.price / self.semi_variable_prices.price) - 1 
            direct_cost_variance = float('{:.2f}'.format(direct_cost_variance))
            return direct_cost_variance
        return 0

    def onliner_competitor_on_date1(self):                                       # отдаем конкурентов и цены + отклонение цены 902 прайса от цены Onliner (+ прикрутить формулы сняьтия ценоой надбавки и НДС)   Onliner
        if self.tyre in ONLINER_COMPETITORS_DICTIONARY1.keys() and ONLINER_COMPETITORS_DICTIONARY1.values():
            competitors_values_list = ONLINER_COMPETITORS_DICTIONARY1[self.tyre]
            list_od_combined_comp_and_prices = []
            for comp in competitors_values_list:
                comp_name = comp.name_competitor + ' ' + comp.tyresize_competitor + comp.parametres_competitor
                comp_price = comp.price  
                if type(comp_price) is float:                                                                    # для расчета отклонения
                    deflection = self.belarus902price.price / comp_price       # для расчета отклонения
                combined = comp_name, comp_price, deflection
                list_od_combined_comp_and_prices.append(combined)
            list_od_combined_comp_and_prices = sorted(list(set(list_od_combined_comp_and_prices)))          # + sorted
            #print('list_od_combined_comp_and_prices', list_od_combined_comp_and_prices)
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
    #tyre = models.ForeignKey(
    #    tyres_model.Tyre,
    #    related_name='competitortyre',
    #    on_delete=models.PROTECT,
    #)
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        on_delete=models.PROTECT,
    )
    price = models.FloatField(
        verbose_name='цена конкурента',
        blank=True,
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True, 
    ) 
    #developer = models.CharField(
    #    verbose_name='производитель',
    #    null=False,
    #    blank=True, 
    #    max_length=25,
    #)
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
