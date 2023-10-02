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

class TyreAddedFeatureModelAdmin(admin.ModelAdmin):
    list_display = [
        'tyre',
        'indexes_list',
        'season_usage',
        'tyre_thread',
        'ax',
        'usability',  
        'studded_usage'    
    ]


admin.site.register(models.Tyre, TyreAdmin)
admin.site.register(models.TyreCard, TyreCardAdmin)
admin.site.register(models.TyreAddedFeatureModel, TyreAddedFeatureModelAdmin)

