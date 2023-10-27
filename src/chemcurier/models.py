from django.db import models
from prices import models as prices_models



from django.contrib.auth import get_user_model
User = get_user_model()

CHEM_PNJ_IN_TABLE_LIST = []
CHEM_TABLE_FINAL_DATA = {}
CHEM_TABLE_FINAL_DATA_FINAL = {}

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
   
    def table_content_creation(self):
        # 1 определение количества периодов для отрисовки колонок в таблице  - количество "чистых" уникальных периодов = кол колонок:
        columns_periods_nim_list = []
        for obj in CHEM_PNJ_IN_TABLE_LIST:
        #    print('obj', obj.tyre_size_chem)
            columns_periods_nim_list.append(obj.data_month_chem)
        columns_periods_nim_list = list(set(columns_periods_nim_list)) 

        #print('columns_periods_nim_list ', columns_periods_nim_list)
        # 2 сбор наименований брендов и получателей:                        
        brand_recipient = []
        for obj in CHEM_PNJ_IN_TABLE_LIST:
            brand_name_recipient_name = obj.producer_chem, obj.reciever_chem
            brand_recipient.append(brand_name_recipient_name)
        brand_recipient = list(set(brand_recipient))                # уникальыне бренд - получатель для ключей
        # 3 создание словаря для отрисовки таблицы - создание ключей словаря 
        final_dict = {}
        for brand_name_recipient_name_unique in brand_recipient:
            brand_name, recipient_name = brand_name_recipient_name_unique
            final_dict[brand_name, recipient_name] = 1
        # 4 создание значений для словаря - еще вложенные словари ключ - период - значения  - данные
        the_very_final_dict = {}
        #print('final_dict.keys()', final_dict.keys())           # ('Roadstone', 'Сталкер'), ('Nexen', 'ПКФ ПИН'),
        
        for key in final_dict.keys():
            val_b_periods_dict = {}
            for period in columns_periods_nim_list:
                for obj in CHEM_PNJ_IN_TABLE_LIST:
                    if (obj.producer_chem, obj.reciever_chem) == key and obj.data_month_chem == period:
                        val_b_periods_dict[period] = obj.val_on_moth_chem, obj.money_on_moth_chem, obj.average_price_in_usd

            the_very_final_dict[key] = val_b_periods_dict
            
        #for k, v in the_very_final_dict.items():        #все четко до данной позиции
        #    print('f!f!f!f!f!f!', k, v)
        # 5 дорисовка пустых значений в в датах с пустотой
        CHEM_TABLE_FINAL_DATA = {}
        for k, v in the_very_final_dict.items():
            values_period_list = []
            for period in columns_periods_nim_list:
                for val_key, val in v.items():
                    if val_key == period:
                        #print('k', k, period, '==999==', val_key,)
                        period_val = period, val
                        values_period_list.append(period_val)
                if period not in v.keys():
                    #print('k', k, period, '==666==')
                    period_val = period, (' ', ' ', ' ')
                    values_period_list.append(period_val)
                #if period in list(v.keys()):
                #    print('k', k, period)
            CHEM_TABLE_FINAL_DATA[k] = values_period_list
            #print('=====')

        #for k, v in CHEM_TABLE_FINAL_DATA.items():
        #    print('f++++++f!', k, v)

        # 5.1 пересборка в словарный вид 
        CHEM_TABLE_FINAL_DATA_FINAL_FOR_TABLE = {}          
        for k, v in CHEM_TABLE_FINAL_DATA.items():    
            avengers_in_dict_assebled = {}  
            avengers_in_dict_assebled_for_table = {}    
            for val in v:
            #    print(val, '====', k)
                avengers_in_dict_assebled[val[0]] = list(val[1])

                ###### ПЕРЕВОД В ЧИТАЕМЫЙ ВИД: СОКРАЩЕНИЕ ЧИСЕЛЬ ДО СТОТЫХ ПОСЛЕ ЗАПЯТОЙ, ПРОБЕЛЫ МЕЖДУ РАЗРЯДАМИ:   
                val1, val2, val3 = val[1]
                if val1 != ' ':
            #        print('val1, val2, val3', val1, val2, val3)
                    val1 = '{0:,}'.format(val1).replace(',', ' ')          
                    val2 =float('{:.2f}'.format(val2))
                    val2 = '{:,}'.format(val2).replace(',', ' ') 
                    val3 =float('{:.2f}'.format(val3))
                    val3 = '{:,}'.format(val3).replace(',', ' ') 
                    val_1 = val1, val2, val3 
                else:
                    val_1 = ' ', ' ', ' '
                ###### END ПЕРЕВОД В ЧИТАЕМЫЙ ВИД: СОКРАЩЕНИЕ ЧИСЕЛЬ ДО СТОТЫХ ПОСЛЕ ЗАПЯТОЙ, ПРОБЕЛЫ МЕЖДУ РАЗРЯДАМИ: 
                avengers_in_dict_assebled_for_table[val[0]] = list(val_1)
        #    print('=======')
            CHEM_TABLE_FINAL_DATA_FINAL[k] = avengers_in_dict_assebled                  # ДЛЯ РАСЧЕТОВ
            CHEM_TABLE_FINAL_DATA_FINAL_FOR_TABLE[k] = avengers_in_dict_assebled_for_table        # ДЛЯ ОТРИСОВКИ

        # 5.2 пересборка в словарный вид - ключи а алфавитном порядке для отрисовки в таблице
        sorted_dict = {key: value for key, value in sorted(CHEM_TABLE_FINAL_DATA_FINAL_FOR_TABLE.items())}   
        CHEM_TABLE_FINAL_DATA_FINAL_FOR_TABLE = sorted_dict 

        #for k, v in CHEM_TABLE_FINAL_DATA_FINAL.items():
        #    print('f-------f!', k, v)    
        ## 6 расчет ИТОГО
        ITOGO_RESULT_DICT = {}
        for per in columns_periods_nim_list:
            val = 0
            sum = 0
            aver = 0
            for v in CHEM_TABLE_FINAL_DATA_FINAL.values():    
                for k in v.keys():
                    if k == per:
                        vlues_is = v.get(k)
                        val1, sum1, aver1 = vlues_is
                        if val1 != ' ':
                                val += val1
                                sum +=sum1
                                aver = sum / val
                    #print('=========')
            #ITOGO_RESULT_DICT[per] = val, sum, aver

            ###### ПЕРЕВОД В ЧИТАЕМЫЙ ВИД: СОКРАЩЕНИЕ ЧИСЕЛЬ ДО СТОТЫХ ПОСЛЕ ЗАПЯТОЙ, ПРОБЕЛЫ МЕЖДУ РАЗРЯДАМИ:
            sum =float('{:.2f}'.format(sum))
            sum = '{:,}'.format(sum).replace(',', ' ') 
            aver =float('{:.2f}'.format(aver))
            aver = '{:,}'.format(aver).replace(',', ' ') 
            ###### END ПЕРЕВОД В ЧИТАЕМЫЙ ВИД: СОКРАЩЕНИЕ ЧИСЕЛЬ ДО СТОТЫХ ПОСЛЕ ЗАПЯТОЙ, ПРОБЕЛЫ МЕЖДУ РАЗРЯДАМИ:
            ITOGO_RESULT_DICT[per] = '{0:,}'.format(val).replace(',', ' '), sum, aver    
            
        #CHEM_TABLE_FINAL_DATA_FINAL['ИТОГО'] = ITOGO_RESULT_DICT
                 
        #for k, v in ITOGO_RESULT_DICT.items():
        #    print('f+=+=+=+=+=+f!', k, v)                      
                    
        return CHEM_TABLE_FINAL_DATA_FINAL_FOR_TABLE, ITOGO_RESULT_DICT
    



    #def num_summ(self):
        ## 1 сумма в штуках
        #num_summ_itogo_in_pieces = 0
        ## 2 сумма в доларах
        #num_summ_itogo_in_usd = 0
        #all_obs_in_table = CHEM_PNJ_IN_TABLE_LIST
        #for obj in all_obs_in_table:
        #    num_summ_itogo_in_pieces += obj.val_on_moth_chem
        #    num_summ_itogo_in_usd += obj.money_on_moth_chem
        #    num_summ_itogo_in_usd = float('{:.2f}'.format(num_summ_itogo_in_usd))
        ## 3 средняя в долларах
        #average_itogo_in_usd = 0
        #if num_summ_itogo_in_pieces != 0:
        #    average_itogo_in_usd = num_summ_itogo_in_usd / num_summ_itogo_in_pieces
        #    average_itogo_in_usd = float('{:.2f}'.format(average_itogo_in_usd))
        ## 4 средняя в бел.руб.
        #average_itogo_in_bel = 0
        #if average_itogo_in_usd and prices_models.CURRENCY_VALUE_USD:
        #    average_itogo_in_bel = average_itogo_in_usd * prices_models.CURRENCY_VALUE_USD
        #    average_itogo_in_bel = float('{:.2f}'.format(average_itogo_in_bel))
        #total_sum_data_list = [num_summ_itogo_in_pieces, num_summ_itogo_in_usd, average_itogo_in_usd, average_itogo_in_bel]
        ##total_sum_data_list = [num_summ_itogo_in_pieces, num_summ_itogo_in_usd]
        ##print('total_sum_data_list', total_sum_data_list)
        #return total_sum_data_list




