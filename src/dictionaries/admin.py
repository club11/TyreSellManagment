from operator import mod
from django.contrib import admin
from . import models


class CurrencyAdmin(admin.ModelAdmin):
    list_display = [
            'currency',
    ]
class TyreSizeModelAdmin(admin.ModelAdmin):
    list_display = [
        'tyre_size',
    ]

class ModelNameModelAdmin(admin.ModelAdmin):
    tyre_size = [
        'model',
    ]

class TyreGroupModelModelAdmin(admin.ModelAdmin):
    tyre_size = [
        'tyre_group',
    ]

class QantityCountModelAdmin(admin.ModelAdmin):
    tyre_size = [
        'quantity_count',
    ]

admin.site.register(models.Currency, CurrencyAdmin)
admin.site.register(models.TyreSizeModel, TyreSizeModelAdmin)
admin.site.register(models.ModelNameModel, ModelNameModelAdmin)
admin.site.register(models.TyreGroupModel, TyreGroupModelModelAdmin)
admin.site.register(models.QantityCountModel, QantityCountModelAdmin)