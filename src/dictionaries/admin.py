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
    list_display = [
        'model',
    ]

class TyreParametersModelAdmin(admin.ModelAdmin):
    list_display = [
        'tyre_type',
    ]

class TyreGroupModelModelAdmin(admin.ModelAdmin):
    list_display = [
        'tyre_group',
    ]

class QantityCountModelAdmin(admin.ModelAdmin):
    list_display = [
        'quantity_count',
    ]

class ContragentsModelAdmin(admin.ModelAdmin):
    list_display = [
        'contragent_name',
    ]

class CompetitorModelAdmin(admin.ModelAdmin):
    list_display = [
        'competitor_name',
    ]

admin.site.register(models.Currency, CurrencyAdmin)
admin.site.register(models.TyreSizeModel, TyreSizeModelAdmin)
admin.site.register(models.ModelNameModel, ModelNameModelAdmin)
admin.site.register(models.TyreParametersModel, TyreParametersModelAdmin)
admin.site.register(models.TyreGroupModel, TyreGroupModelModelAdmin)
admin.site.register(models.QantityCountModel, QantityCountModelAdmin)
admin.site.register(models.ContragentsModel, ContragentsModelAdmin)
admin.site.register(models.CompetitorModel, CompetitorModelAdmin)
