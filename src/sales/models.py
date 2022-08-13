from django.db import models
from tyres import models as tyres_model

class Sales(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='sales',
        on_delete=models.PROTECT,
    )
    date_of_sales = models.DateField(
        verbose_name='дата реализации',    
        null=False,
        blank=True,    
    )
    contragent = models.CharField(
        verbose_name='контрагент',
        max_length=10,
    )
    sales_value = models.IntegerField(
        verbose_name='объем продаж контрагенту',
        blank=True,
    )