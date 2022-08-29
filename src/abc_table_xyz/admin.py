from django.contrib import admin
from . import models


class AbcxyzTableAdmin(admin.ModelAdmin):
    list_display = [
        #'sales_on_date_total_amount',
        'pk',
    ]


class AbcxyzAdmin(admin.ModelAdmin):
    list_display = [
        'table',
        'tyre',
    ]
admin.site.register(models.AbcxyzTable, AbcxyzTableAdmin)
admin.site.register(models.Abcxyz, AbcxyzAdmin)