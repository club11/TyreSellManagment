from django.db import models
from django.urls import reverse

# Create your models here.

class Currency(models.Model):
    currency = models.CharField(
        max_length=50,
        verbose_name='валюта',
    )
    def get_absolute_url(self):
        return reverse('dictionaries:curr_list')

    def __str__(self):
        return str(self.currency) 


class TyreSizeModel(models.Model):
    tyre_size = models.CharField(
        verbose_name='типоразмер',
        max_length=30,
    )

    def get_absolute_url(self):
        return reverse('dictionaries:ts_list')

class ModelNameModel(models.Model):
    model = models.CharField(
        verbose_name='модель',
        max_length=60,
    )

    def get_absolute_url(self):
        return reverse('dictionaries:model_list')
        #return reverse('dictionaries:dictionaries', args = [self.pk])

class TyreParametersModel(models.Model):
    tyre_type = models.CharField(
        verbose_name='параметры шины',
        max_length=50,
    )

    def get_absolute_url(self):
        return reverse('dictionaries:param_list')

class TyreGroupModel(models.Model):
    tyre_group = models.CharField(
        verbose_name='группа шин',
        max_length=60,
    )

    def get_absolute_url(self):
        return reverse('dictionaries:tg_list')

class QantityCountModel(models.Model):
    quantity_count = models.CharField(
        verbose_name='ед. измерения',
        max_length=30,
    )

    def get_absolute_url(self):
        return reverse('dictionaries:qnt_list')

class ContragentsModel(models.Model):
    contragent_name = models.CharField(
        verbose_name='наименование контрагента',
        max_length=60,
    )

    def get_absolute_url(self):
        return reverse('dictionaries:tg_list')


class CompetitorModel(models.Model):
    competitor_name = models.CharField(
        verbose_name='наименование производителя-конкурента',
        max_length=80,
    )

    def get_absolute_url(self):
        return reverse('dictionaries:tg_list')
    
    def __str__(self):
        return str(self.competitor_name)


class SeasonUsageModel(models.Model):
    season_usage_name = models.CharField(
        verbose_name='сезонность',
        max_length=60,
    )

    def get_absolute_url(self):
        return reverse('dictionaries:tg_list')

class StuddedUsageModel(models.Model):
    studded_name = models.CharField(
        verbose_name='ошиповка',
        max_length=60,
    )

    def get_absolute_url(self):
        return reverse('dictionaries:tg_list')