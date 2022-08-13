from operator import mod
from django.contrib import admin
from . import models

class SalesAdmin(admin.ModelAdmin):
    list_display = [
            'tyre',
            'date_of_sales',
            'contragent',
            'sales_value',
    ]

admin.site.register(models.Sales, SalesAdmin)
