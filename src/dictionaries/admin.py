from operator import mod
from django.contrib import admin
from . import models


class TyreSizeModelAdmin(admin.ModelAdmin):
    list_display = [
        'tyre_size',
    ]

class ModelNameModelAdmin(admin.ModelAdmin):
    tyre_size = [
        'model',
    ]

admin.site.register(models.TyreSizeModel, TyreSizeModelAdmin)
admin.site.register(models.ModelNameModel, ModelNameModelAdmin)