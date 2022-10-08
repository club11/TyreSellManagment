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

PERIOD_UPDATE_SALES = ''

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
               
    #def contragents_sales(self):
    #    tyre_sal_dict = SAL_PER_DICTIONARY
    #    contragent = CONTRAGENT
    #    #print('CONTR_SAL_LISTCONTR_SAL_LISTCONTR_SAL_LIST 1= ',  CONTR_SAL_LIST)
    #    for key, value in tyre_sal_dict.items():
    #        for bj in self.tyre.sales.all():
    #        #for bj in self.tyre.sales.all():.filter(date_of_sales__range=asked_dates)
    #            if self.tyre == key and bj.contragent == contragent:
    #                all_sal_on_date = []
    #                for val in value:
    #                    sale_val_on_date = 0
    #                    for v in val:
    #                        if  v[2] == contragent:
    #                            sale_val_on_date = v[0]
    #                            print('all_sal_on_date', all_sal_on_date)
    #                            CONTR_SAL_LIST[v[2]] = all_sal_on_date
    #                            #CONTR_SAL_LIST[v[2]] = [3,]
    #                            TYR_CONTR_SAL_LIST[key] = CONTR_SAL_LIST
    #                            #print('CONTR_SAL_LISTCONTR_SAL_LISTCONTR_SAL_LIST### = ',  CONTR_SAL_LIST)
    #                    all_sal_on_date.append(sale_val_on_date)
    #                print(CONTR_SAL_LIST, 'IWONTCHANGEFORUuuuuuuu')
    #                #print(TYR_CONTR_SAL_LIST, 'IWONTCHANGEFORUuuuuuuu')
    #                #print(all_sal_on_date)
    #                return all_sal_on_date


    def contragents_sales(self):
        tyre_sal_dict = SAL_PER_DICTIONARY

        asked_dates = SALES_DATES

        CONTR_UNIQUE_NAME_LIST
        contr_dict = {}
        for name in CONTR_UNIQUE_NAME_LIST:
            contr_dict[name] = None

        for key, value in tyre_sal_dict.items():
            #print(key, value )
            for k in contr_dict.keys():
                for bj in self.tyre.sales.filter(date_of_sales__in=asked_dates):
                    if self.tyre == key:
                        sal_values_list = []                     
                        #for period in value:
                        #    for doma in period:
                        #        #  (12, datetime.date(2022, 5, 15), 'БНХ Польска')
                        #        if doma[1] in asked_dates and k == doma[2]:
                        #            sal_values_list.append(doma[0])
                        #contr_dict[k] = sal_values_list
                        all_sal_on_date = []
                        for period in value:
                            sale_val_on_date = 0
                            for doma in period:
                                if doma[1] in asked_dates and k == doma[2]:
                                    sale_val_on_date = doma[0]

                                    CONTR_SAL_LIST[doma[2]] = all_sal_on_date
                                    #CONTR_SAL_LIST[v[2]] = contr_dict.get(v[2])

                                    TYR_CONTR_SAL_LIST[key] = CONTR_SAL_LIST
                                    print('CONTR_SAL_LISTCONTR_SAL_LISTCONTR_SAL_LIST### = ',  CONTR_SAL_LIST)
                            all_sal_on_date.append(sale_val_on_date)
                        #print('CONTR_SAL_LISTCONTR_SAL_LISTCONTR_SAL_LIST### = ',  CONTR_SAL_LIST)

        #print('DICT',  contr_dict)


        #tyre_sal_dict = SAL_PER_DICTIONARY
        #contragent = CONTRAGENT
        ##print('CONTR_SAL_LISTCONTR_SAL_LISTCONTR_SAL_LIST 1= ',  CONTR_SAL_LIST)
        #for key, value in tyre_sal_dict.items():
        #    for bj in self.tyre.sales.all():
        #    #for bj in self.tyre.sales.all():.filter(date_of_sales__range=asked_dates)
        #        if self.tyre == key and bj.contragent == contragent:
        #            all_sal_on_date = []
        #            for val in value:
        #                sale_val_on_date = 0
        #                for v in val:
        #                    if  v[2] == contragent:
        #                        sale_val_on_date = v[0]
        #                        #print('all_sal_on_date', all_sal_on_date)
#
        #                        CONTR_SAL_LIST[v[2]] = all_sal_on_date
        #                        #CONTR_SAL_LIST[v[2]] = contr_dict.get(v[2])
#
        #                        TYR_CONTR_SAL_LIST[key] = CONTR_SAL_LIST
        #                        #print('CONTR_SAL_LISTCONTR_SAL_LISTCONTR_SAL_LIST### = ',  CONTR_SAL_LIST)
        #                all_sal_on_date.append(sale_val_on_date)
        #            print(CONTR_SAL_LIST, 'IWONTCHANGEFORUuuuuuuu')
        #            #print(all_sal_on_date)
        #            return all_sal_on_date

    
                            



        #for key, value in tyre_sal_dict.items():
        #    for bj in self.tyre.sales.all():
        #        if self.tyre == key :
        #            all_sal_on_date = []
        #            for val in value:
        #                sale_val_on_date = 0
        #                all_sal_on_date.append(sale_val_on_date)
    #
#
        #            return all_sal_on_date


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



