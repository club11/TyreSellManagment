from operator import mod
from django.contrib import admin
from . import models


class HomePageAdmin(admin.ModelAdmin):
    list_display = [

    ]

class Tyre_HomepageAdmin(admin.ModelAdmin):
    list_display = [
        'tyre',
        'table',
    ]

admin.site.register(models.HomePageModel, HomePageAdmin)
admin.site.register(models.Tyre_Homepage, Tyre_HomepageAdmin)