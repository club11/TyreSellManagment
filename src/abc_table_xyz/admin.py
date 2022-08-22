from django.contrib import admin
from . import models


class AbcxyzTableAdmin(admin.ModelAdmin):
    list_display = [
        #'sales_on_date_total_amount',
    ]


class AbcxyzAdmin(admin.ModelAdmin):
    list_display = [
        'table',
    ]
admin.site.register(models.AbcxyzTable, AbcxyzTableAdmin)
admin.site.register(models.Abcxyz, AbcxyzAdmin)