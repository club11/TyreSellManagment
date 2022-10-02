from django.contrib import admin
from . import models

class TyreAdmin(admin.ModelAdmin):
    list_display = [
        'tyre_model',
        'tyre_size',

    ]

class TyreCardAdmin(admin.ModelAdmin):
    list_display = [
            'tyre',
            'serie_date',
            'picture',
    ]

admin.site.register(models.Tyre, TyreAdmin)
admin.site.register(models.TyreCard, TyreCardAdmin)

