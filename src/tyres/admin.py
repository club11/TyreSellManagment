from django.contrib import admin
from . import models

class TyreAdmin(admin.ModelAdmin):
    list_display = [
        'tyre_model',
        'tyre_size',
        'tyre_type',
        'prime_cost',
        'direct_costs',
    ]

class TyreCardAdmin(admin.ModelAdmin):
    list_display = [
            'tyre',
            'serie_date',
            'picture',
    ]

admin.site.register(models.Tyre, TyreAdmin)
admin.site.register(models.TyreCard, TyreCardAdmin)

