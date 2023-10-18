from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()


class ChemCourierTableModel(models.Model):
    customer = models.ForeignKey(
        User,
        verbose_name='Таблица Хим Курьер',
        related_name='chemcourier_table',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    chemcourier_table = models.CharField(
        verbose_name='Хим Курьер',
        max_length=15,
        blank=True,
        null=True
    )

