from django.db import models
from prices import models as prices_models

from django.contrib.auth import get_user_model
User = get_user_model()

CHEM_PNJ_IN_TABLE_LIST = []


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

    chemurier_in_table = models.ManyToManyField(
        prices_models.ChemCurierTyresModel,
        related_name='chemuriers_for_table',
        #on_delete=models.PROTECT,
        #null=True,
        blank=True, 
    )

    def num_summ(self):
        # 1 сумма в штуках
        num_summ_itogo_in_pieces = 0
        # 2 сумма в доларах
        num_summ_itogo_in_usd = 0
        all_obs_in_table = CHEM_PNJ_IN_TABLE_LIST
        for obj in all_obs_in_table:
            num_summ_itogo_in_pieces += obj.val_on_moth_chem
            num_summ_itogo_in_usd += obj.money_on_moth_chem
        # 3 средняя в долларах
        average_itogo_in_usd = 0
        if num_summ_itogo_in_pieces != 0:
            average_itogo_in_usd = num_summ_itogo_in_usd / num_summ_itogo_in_pieces
        # 4 средняя в бел.руб.
        average_itogo_in_bel = average_itogo_in_usd * prices_models.CURRENCY_VALUE_USD
        total_sum_data_list = [num_summ_itogo_in_pieces, num_summ_itogo_in_usd, average_itogo_in_usd, average_itogo_in_bel]
        #total_sum_data_list = [num_summ_itogo_in_pieces, num_summ_itogo_in_usd]
        #print('total_sum_data_list', total_sum_data_list)
        return total_sum_data_list

