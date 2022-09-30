from operator import mod
from django.contrib import admin
from . import models

class SalesAdmin(admin.ModelAdmin):
    list_display = [
            'tyre',
            'date_of_sales',
            'contragent',
            'sales_value',
            'table', 
    ]

class SalesTableAdmin(admin.ModelAdmin):
    list_display = [
            'customer',
    ]

class Tyre_SaleAdmin(admin.ModelAdmin):
    list_display = [
            'tyre',
            'table',
    ]

admin.site.register(models.Sales, SalesAdmin)
admin.site.register(models.SalesTable, SalesTableAdmin)
admin.site.register(models.Tyre_Sale, Tyre_SaleAdmin)
