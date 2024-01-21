from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Profiles(models.Model):
    user = models.OneToOneField(
        User, 
        verbose_name='User account', 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    email = models.CharField(verbose_name='email', max_length=254, blank=True)
