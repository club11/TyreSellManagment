from django.db import models
from django.urls import reverse
from tyres import models as tyres_models

TOTAL_SALES_DICT = {}
ABC_XYZ_GROP_HOME_DICT = {}
CONTRAGENT_SALES_SORTED_DICT = {}

PERIOD = ''
TYRE_GROUP_NAMES = []
TYRE_GROUP_SIZES = []
TYRE_GROUP_MODELS = []

class HomePageModel(models.Model):
    tyre = models.ForeignKey(
        tyres_models.Tyre,
        related_name='tyres_home',
        on_delete=models.PROTECT,
    )
    #tyre_card = models.ForeignKey(
    #    tyres_models.TyreCard,
    #    related_name='tyre_card_home',
    #    on_delete=models.PROTECT,
    #    default=0
    #)

    def abc_xyz_value(self):
        return 'abc_xyz'
    
    def get_absolute_url(self):
        return reverse('homepage:home')

    def total_sale(self):
        pass

    def period(self):
        return PERIOD
  
class Tyre_Homepage(models.Model):
    tyre = models.ForeignKey(
        tyres_models.Tyre,
        related_name='tyr_homepage',
        on_delete=models.PROTECT,
    )
    table = models.ForeignKey(
        HomePageModel,
        verbose_name='Таблица главная',
        related_name='table_home',                    
        on_delete=models.CASCADE,  
        null=True                      
    )

    def total_sales(self):
        total_sal_val = 0
        if TOTAL_SALES_DICT:
            total_sal_val = TOTAL_SALES_DICT.get(self.tyre)
        return total_sal_val

    def tyre_group(self):
        for group in self.tyre.tyre_group.all():
            return group.tyre_group

    def abc_xyz_group_home(self):
        total_sal_val = ''
        if ABC_XYZ_GROP_HOME_DICT:
            total_sal_val = ABC_XYZ_GROP_HOME_DICT.get(self.tyre)
        return total_sal_val

    def top_contragents_by_sales(self):
        contragents_top_by_sale = {}
        if self.tyre in CONTRAGENT_SALES_SORTED_DICT:
            contragents_top_by_sale = CONTRAGENT_SALES_SORTED_DICT.get(self.tyre)
        #print(self.tyre, 'gg', CONTRAGENT_SALES_SORTED_DICT.get(self.tyre))
        top_two_contragent_by_sale = list(contragents_top_by_sale.keys())
        list_of_contr = []
        for contyrag in top_two_contragent_by_sale[:2]:
            list_of_contr.append(contyrag)
        return list_of_contr


