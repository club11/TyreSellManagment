from django.db import models
from tyres import models as tyres_model
from django.contrib.auth import get_user_model
User = get_user_model()

SALES_DATES = []
SAL_PER_DICTIONARY ={}
CONTRAGENT = ''
CONTR_SAL_LIST = {}
TYR_CONTR_SAL_LIST = {}


class SalesTable(models.Model):
    customer = models.ForeignKey(
        User,
        verbose_name='Таблица продаж',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    def dates(self):
        datess = SALES_DATES
        return datess


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
    sales_value = models.IntegerField(
        verbose_name='объем продаж контрагенту',
        blank=True,
    )
    contragent = models.CharField(
        verbose_name='контрагент',
        max_length=10,
    )
    table = models.ForeignKey(
        SalesTable,
        verbose_name='Таблица',
        related_name='sales_table',                    
        on_delete=models.CASCADE,  
        null=True                       # Заглушка
    ) 

class Tyre_Sale(models.Model):
    tyre = models.ForeignKey(
        tyres_model.Tyre,
        related_name='tyr_sales',
        on_delete=models.PROTECT,
    )
    table = models.ForeignKey(
        SalesTable,
        verbose_name='Таблица',
        related_name='table_sales',                    
        on_delete=models.CASCADE,  
        null=True                      
    ) 

    def sale_on_date(self):
        tyre_sal_dict = SAL_PER_DICTIONARY
        for key, value in tyre_sal_dict.items():
            if self.tyre == key:
                all_sal_on_date = []
                for val in value:
                    sale_val_on_date = 0
                    for v in val:
                        sale_val_on_date += v[0]
                    all_sal_on_date.append(sale_val_on_date)
                return all_sal_on_date
        return 0
    
    def contragents(self):
        tyre_sal_dict = SAL_PER_DICTIONARY
        for key, value in tyre_sal_dict.items():
            if self.tyre == key:
                contragents_list = []
                for val in value:
                    for v in val:
                        contragents_list.append(v[2])
        unique_names_list = list(set(contragents_list))                       
        # ['БНХ Укр', 'БНХ Польска']
        return unique_names_list
                
    def contragents_sales(self):
        tyre_sal_dict = SAL_PER_DICTIONARY
        contragent = CONTRAGENT
        for key, value in tyre_sal_dict.items():
            for bj in self.tyre.sales.all():
                if self.tyre == key and bj.contragent == contragent:
                    all_sal_on_date = []
                    for val in value:
                        sale_val_on_date = 0
                        for v in val:
                            if  v[2] == contragent:
                                sale_val_on_date = v[0]
                                CONTR_SAL_LIST[v[2]] = all_sal_on_date
                                TYR_CONTR_SAL_LIST[key] = CONTR_SAL_LIST
                        all_sal_on_date.append(sale_val_on_date)
                    #print(CONTR_SAL_LIST, 'IWONTCHANGEFORU')
                    #print(all_sal_on_date)
                    return all_sal_on_date
        return 0




    def contragents_sales_joined(self):
        #print(len(TYR_CONTR_SAL_LIST))
        if self.tyre in TYR_CONTR_SAL_LIST.keys():
            tyr_sal = TYR_CONTR_SAL_LIST.get(self.tyre)
            #print(tyr_sal)
            #print(tyr_sal.keys())
            total_final_list = []
            for key in tyr_sal:
                list_sales = []
                val = tyr_sal.get(key)
                list_sales.append(key)
                for v in val:
                    list_sales.append(v)
                total_final_list.append(list_sales)
        #print(total_final_list)
        return total_final_list
        #return [['БНХ УКР',1,2,3], ['БНХ РОС',8,4,5]]