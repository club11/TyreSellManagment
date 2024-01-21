from django.contrib import admin
from . import models

class ProfilesAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user',
        'email',
    ]

admin.site.register(models.Profiles, ProfilesAdmin)