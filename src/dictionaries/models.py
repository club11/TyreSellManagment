from django.db import models
from django.urls import reverse

# Create your models here.
class TyreSizeModel(models.Model):
    tyre_size = models.CharField(
        verbose_name='типоразмер',
        max_length=10,
    )

    def get_absolute_url(self):
        return reverse('dictionaries:ts_list')

class ModelNameModel(models.Model):
    model = models.CharField(
        verbose_name='модель',
        max_length=10,
    )

    def get_absolute_url(self):
        return reverse('dictionaries:model_list')
        #return reverse('dictionaries:dictionaries', args = [self.pk])