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



admin.site.register(models.PlannedCosstModel, PlannedCosstModelAdmin)
admin.site.register(models.SemiVariableCosstModel, SemiVariableCosstModelAdmin)
admin.site.register(models.Belarus902PriceModel, Belarus902PriceModelAdmin)
admin.site.register(models.TPSRussiaFCAModel, TPSRussiaFCAModelAdmin)
admin.site.register(models.TPSKazFCAModel, TPSKazFCAModelAdmin)
admin.site.register(models.TPSMiddleAsiaFCAModel, TPSMiddleAsiaFCAModelAdmin)