from operator import mod
from django.contrib import admin
from . import models


class HomePageAdmin(admin.ModelAdmin):
    list_display = [

    ]

admin.site.register(models.HomePageModel, HomePageAdmin)