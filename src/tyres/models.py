from django.db import models
from dictionaries import models as dictionaries_models
from django.urls import reverse
import datetime

class Tyre(models.Model):
    tyre_model = models.ForeignKey(
        dictionaries_models.ModelNameModel,
        related_name='tire_models',
        on_delete=models.PROTECT,
        default=None,
        verbose_name='модель'
    )
    tyre_size = models.ForeignKey(
        dictionaries_models.TyreSizeModel,
        related_name='tire_size',
        on_delete=models.PROTECT,
        default=None,
    )
    tyre_type = models.ManyToManyField(
        dictionaries_models.TyreParametersModel,
        related_name='tire_parameters',
        default=None,
        blank=True,
    )
    tyre_group = models.ManyToManyField(
        dictionaries_models.TyreGroupModel,
        related_name='tire_group',
        default=None,
        blank=True,
    )

    #prime_cost = models.FloatField(
    #    verbose_name='полные затраты',
    #    blank=True,
    #    null=True
    #)
    #direct_costs = models.FloatField(
    #    verbose_name='прямые затраты',
    #    blank=True,
    #    null=True
    #)
    ##currency = models.ForeignKey(
    ##    dictionaries_models.Currency,
    ##    related_name='tyre_currency',
    ##    on_delete=models.PROTECT,
    ##    default=None,
    ##)
    def get_absolute_url(self):
        return reverse('tyres:tyre_list')

class TyreCard(models.Model):
    tyre = models.ForeignKey(
        Tyre,
        related_name='tyre_card',
        on_delete=models.PROTECT,
    )
    serie_date = models.DateField(
        verbose_name='Серийное освоение',
        blank=True, 
        default=datetime.date.today
    )
    picture = models.ImageField(
        verbose_name='картинка',
        upload_to = 'books/%Y/%m/%d/'           # указали куда upload ить
    )

    def get_absolute_url(self):
        return reverse('tyres:tyre_card_list')