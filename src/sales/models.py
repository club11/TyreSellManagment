from django.db import models
from tyres import models as tyres_model
from django.contrib.auth import get_user_model
User = get_user_model()
from datetime import timedelta 

#from datetime_periods import period

SALES_DATES = []
SAL_PER_DICTIONARY ={}
CONTRAGENT = ''
CONTR_SAL_LIST = {}
TYR_CONTR_SAL_LIST = {}
TYRE_SAL_TOTAL_DICT ={}

CONTR_UNIQUE_NAME_LIST = []

#UPDATE_VIEW:
PERIOD_UPDATE_SALES = ''
TYRE_GROUP_NAMES = []
TYRE_GROUP_SIZES = []
TYRE_GROUP_MODELS = []

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
        #print(timedelta(datess[1], datess[0]))
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
               
    def contragents_sales(self):
        tyre_sal_dict = SAL_PER_DICTIONARY                  #{<Tyre: Tyre object (76)>: [[(12, datetime.date(2022, 5, 15), 'БНХ Польска'), (10, datetime.date(2022, 5, 15), 'БНХ УКР'), (3, datetime.date(2022, 5, 15), 'БНХ РОС')], [(8, datetime.date(2022, 8, 15), 'БНХ УКР')], [(8, datetime.date(2022, 9, 15), 'БНХ РОС')]],
        CONTR_UNIQUE_NAME_LIST                              #['БНХ УКР', 'БНХ РОС', 'БНХ Польска']
        contr_dict = {}
        for name in CONTR_UNIQUE_NAME_LIST:
            contr_dict[name] = None
        if self.tyre in tyre_sal_dict.keys():
            value = tyre_sal_dict.get(self.tyre)
            #print(value)
            for key in contr_dict.keys():
                n = 0
                pos = 0
                list_val = []
                for per in value:
                    znch = 0
                    for dom in per:
                        if key == dom[2]:
                            znch = dom[0]
                    n = znch     
                    list_val.append(n)
                contr_dict[key] = list_val
            #print(contr_dict)
            TYR_CONTR_SAL_LIST[self.tyre] = contr_dict
        return contr_dict

    def contragents_sales_joined(self):
        total_final_list = []
        #print('TYR_CONTR_SAL_LIST', TYR_CONTR_SAL_LIST)
        if self.tyre in TYR_CONTR_SAL_LIST.keys():
            tyr_sal = TYR_CONTR_SAL_LIST.get(self.tyre)
            
            for key in tyr_sal:
                list_sales = []
                val = tyr_sal.get(key)
                list_sales.append(key)
                sum1 = 0
                for v in val:
                    sum1 += v
                    #print(v)
                    list_sales.append(v)
                list_sales.append(sum1)
                total_final_list.append(list_sales)
        #print(total_final_list)
        return total_final_list

    def total_sale_in_period(self):
        if self in TYRE_SAL_TOTAL_DICT:
            total_sal = TYRE_SAL_TOTAL_DICT.get(self)
        return total_sal



