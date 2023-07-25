from django.contrib import admin
from . import models


class PlannedCosstModelAdmin(admin.ModelAdmin):
    list_display = [
            'tyre',
            'currency',
            'price',
            'date_period',
    ]

class SemiVariableCosstModelAdmin(admin.ModelAdmin):
    list_display = [
            'tyre',
            'currency',
            'price',
            'date_period',
    ]

class Belarus902PriceModelAdmin(admin.ModelAdmin):
    list_display = [
            'tyre',
            'currency',
            'price',
            'date_period',
    ]

class TPSRussiaFCAModelAdmin(admin.ModelAdmin):
    list_display = [
            'tyre',
            'currency',
            'price',
            'date_period',
    ]

class TPSKazFCAModelAdmin(admin.ModelAdmin):
    list_display = [
            'tyre',
            'currency',
            'price',
            'date_period',
    ]

class TPSMiddleAsiaFCAModelAdmin(admin.ModelAdmin):
    list_display = [
            'tyre',
            'currency',
            'price',
            'date_period',
    ]

class CurrentPricesModelAdmin(admin.ModelAdmin):
    list_display = [
            'tyre',
            'currency',
            'price',
            'date_period',
    ]


class ComparativeAnalysisTableModelAdmin(admin.ModelAdmin):
    list_display = [
            'customer',
            'market_table',
    ]

class  ComparativeAnalysisTyresModelAdmin(admin.ModelAdmin):

    list_display = [
            #'table',
            'id',
            'tyre',
            'planned_costs',
            'semi_variable_prices',
            'belarus902price',
            'tpsrussiafcaprice',
            'tpskazfcaprice',
            'tpsmiddleasiafcaprice',
            'currentpricesprice',
            'sale_data',
    ]

class CompetitorSiteModelAdmin(admin.ModelAdmin):
    filter_horizontal = ('tyre_to_compare',)                # MANYTOMANYFIELD display on adminsite
    list_display = [
            'site',
            #'tyre_to_compare',
            'currency',
            'price',
            'date_period',
            'developer',
            'tyresize_competitor',
            'name_competitor',
            'parametres_competitor',
            'season',
    ]
class ChemCurierTyresModelAdmin(admin.ModelAdmin):
    list_display = [
            'tyre_size_chem',
            'producer_chem',
            'group_chem',
            'currency_chem',
    ]

class DataPriceValMoneyChemCurierModelAdmin(admin.ModelAdmin):
    list_display = [
            'data_month_chem',
            'val_on_moth_chem',
            'money_on_moth_chem',
            'price_on_date_chem'
            #'price_val_money_data',
            
    ]

admin.site.register(models.PlannedCosstModel, PlannedCosstModelAdmin)
admin.site.register(models.SemiVariableCosstModel, SemiVariableCosstModelAdmin)
admin.site.register(models.Belarus902PriceModel, Belarus902PriceModelAdmin)
admin.site.register(models.TPSRussiaFCAModel, TPSRussiaFCAModelAdmin)
admin.site.register(models.TPSKazFCAModel, TPSKazFCAModelAdmin)
admin.site.register(models.TPSMiddleAsiaFCAModel, TPSMiddleAsiaFCAModelAdmin)
admin.site.register(models.CurrentPricesModel, CurrentPricesModelAdmin)
admin.site.register(models.ComparativeAnalysisTableModel, ComparativeAnalysisTableModelAdmin)
admin.site.register(models.ComparativeAnalysisTyresModel, ComparativeAnalysisTyresModelAdmin)
admin.site.register(models.CompetitorSiteModel, CompetitorSiteModelAdmin)
admin.site.register(models.DataPriceValMoneyChemCurierModel, DataPriceValMoneyChemCurierModelAdmin)
admin.site.register(models.ChemCurierTyresModel, ChemCurierTyresModelAdmin)