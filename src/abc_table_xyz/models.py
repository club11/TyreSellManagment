from django.db import models
from tyres import models as tyres_model

class AbcxyzTable(models.Model):

    def sales_on_date_total_amount(self):                          
        sales_on_date_total_amount = 0                    
        tyres = self.table.all()                         
        for tyre in tyres:
            sales_on_date_total_amount += tyre.sales_on_date    
        return sales_on_date_total_amount

class Abcxyz(models.Model):
    table = models.ForeignKey(
        AbcxyzTable,
        verbose_name='Таблица',
        related_name='table',                    
        on_delete=models.CASCADE,        
    )
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='tyre_abc',
        on_delete=models.PROTECT,
    )
    date_of_sales = models.DateField(
        verbose_name='дата реализации',    
        null=False,
        blank=True,    
    )
    sales_on_date = models.IntegerField(
        verbose_name='объем продаж',
        blank=True,
    )

      

    #def total_sales_of_of_tyre_in_period(self):
    #    total_sales = self.sales * 3
    #    return total_sales