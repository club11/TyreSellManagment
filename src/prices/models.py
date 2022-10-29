from django.db import models
from dictionaries import models as dictionaries_models
from tyres import models as tyres_model
from django.urls import reverse

class PlannedCosstModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='planned_costs',
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='prices_currency',
        on_delete=models.PROTECT,
    )
    price = models.FloatField(
        verbose_name='плановая себестоимость',
        blank=True,
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True,    
    )

    def get_absolute_url(self):
        return reverse('prices:planned_cost')

class SemiVariableCosstModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='semi_variable_costs',
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='semi_variable_prices_currency',
        on_delete=models.PROTECT,
    )
    price = models.FloatField(
        verbose_name='плановая себестоимость',
        blank=True,
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True,    
    )

    def get_absolute_url(self):
        return reverse('prices:semi_variable_planned_cost')

class Belarus902PriceModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='belarus902price',
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='belarus902currency',
        on_delete=models.PROTECT,
    )
    price = models.FloatField(
        verbose_name='прейскуранты №№9, 902',
        blank=True,
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True,    
    )

    def get_absolute_url(self):
        return reverse('prices:belarus902price')

class TPSRussiaFCAModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='tpsrussiafcaprice',
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='tpsrussiafcacurrency',
        on_delete=models.PROTECT,
    )
    price = models.FloatField(
        verbose_name='ТПС РФ FCA',
        blank=True,
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True,    
    )

    def get_absolute_url(self):
        return reverse('prices:tpsrussiafca')

class TPSKazFCAModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='tpskazfcaprice',
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='tpskazfcacurrency',
        on_delete=models.PROTECT,
    )
    price = models.FloatField(
        verbose_name='ТПС Казахстан FCA',
        blank=True,
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True,    
    )

    def get_absolute_url(self):
        return reverse('prices:tpskazfca')

class TPSMiddleAsiaFCAModel(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='tpsmiddleasiafcaprice',
        on_delete=models.PROTECT,
    )
    currency = models.ForeignKey(
        dictionaries_models.Currency,
        related_name='tpsmiddleasiafcacurrency',
        on_delete=models.PROTECT,
    )
    price = models.FloatField(
        verbose_name='ТПС Средняя Азия, Закавказье, Молдова FCA',
        blank=True,
    )
    date_period = models.DateField(
        verbose_name='период действия',    
        null=False,
        blank=True,    
    )

    def get_absolute_url(self):
        return reverse('prices:tpsmiddleasiafca')