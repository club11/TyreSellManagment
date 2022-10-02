from operator import index
from turtle import update
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from . import models 
from tyres import models as tyre_models
from abc_table_xyz import models as abc_table_xyz_models


class HomeTemplateDetailView(DetailView):
#class HomeTemplateListView(ListView):
    template_name = 'homepage/home.html'
    model = models.HomePageModel

    def get_object(self, queryset=None):                
        # get table
        #abc_table_xyz_table = abc_table_xyz_models.AbcxyzTable.objects.all()[0]
        tyres_list = tyre_models.Tyre.objects.all()
        for tyr in tyres_list: 
            models.Tyre_Homepage.objects.get_or_create(
                tyre=tyr
            )
        home_table_tyres = []    
        for object in models.Tyre_Homepage.objects.all():
            home_table_tyres.append(object)
        #print(home_table_tyres)

        # 1 Объем продаж по шине всего
        tyres_all__dict = {}
        for tyre in tyres_list:
            total_sal = 0
            for sale in tyre.sales.all():
                #print(sale.sales_value)
                total_sal += sale.sales_value
            tyres_all__dict[tyre] = total_sal
        models.TOTAL_SALES_DICT = tyres_all__dict

        #2  # Доля  в общем объеме, %  
        #2.1 Общий объем:
        total_value = 0                             # Общий оъем продаж по периоду
        for values in tyres_all__dict.values():
            total_value += values

        #3 СОРТИРОВКА шин по итоговому объему продаж в период:
        tyres_all__dict_sorted = {}             # ОТСОРТИРОВАННЫЙ СЛОВАРЬ ШИНА  ПО ОБЪЕМУ ПРОДАЖ     -   tyres_all__dict_sorted
        for k in sorted(tyres_all__dict, key=tyres_all__dict.get, reverse=True):
            tyres_all__dict_sorted[k] = tyres_all__dict[k]

        #4 доля в общем объеме:
        #tyres_all__dict_sorted_with_percents = {}
        tyres_all__dict_sorted_with_percents_final = {}
        tyre_contragent_top_by_sale = {}    # продажи контрагентам отсортированные по объемам
        for tyre in tyres_all__dict_sorted:
            list_of_index = list(tyres_all__dict_sorted.keys())
            #print(tyre, list_of_index)
            tyre_total_sal = tyres_all__dict_sorted.get(tyre)
            if tyre_total_sal == 0:
                #print('ERROR')
                pecent = 0.01
            else:
                pecent = tyre_total_sal/total_value 
            if list_of_index.index(tyre) == 0:
                accumulated_precent = pecent
            #4.1 доля с накопительным итогом
            else:
                prev_index = list_of_index.index(tyre)
                prev_tyres = list_of_index[0 : prev_index]
                accumulated_precents = 0
                for tyr in prev_tyres:
                    tyre_total_sal = tyres_all__dict_sorted.get(tyr)
                    pecents = tyre_total_sal/total_value
                    accumulated_precents += pecents 
                accumulated_precent = accumulated_precents + pecent
                #print(accumulated_precent, '+++++++', tyre)
            # 4.2 Группа ABC:
            accumulated_precent *= 100
            if accumulated_precent < 70:
                abc_group = 'A'
            elif accumulated_precent >=70 and accumulated_precent < 90:
                abc_group = 'B'
            else:
                abc_group = 'C'
            #5 среднемесячная выручка:
            list_of_dates = []
            for sal in tyre.sales.all():
                list_of_dates.append(sal.date_of_sales)
            num_periods = len(list(set(list_of_dates)))
            average_revenue = tyre_total_sal / num_periods

            #6 Стандартное отклонение:
            tyre_values_in_period = tyre.sales.all()
            sq_sum = 0
            if num_periods == 1:
                sq_sum = 0
                for value in tyre_values_in_period:
                    value = value.sales_value
                    sq_sum += (value - average_revenue) * (value - average_revenue) 
                std_deviation = (sq_sum/(num_periods)) ** (0.5)
            else:
                sq_sum = 0
                for value in tyre_values_in_period:
                    value = value.sales_value
                    sq_sum += (value - average_revenue) * (value - average_revenue) 
                std_deviation = (sq_sum/(num_periods - 1)) ** (0.5)

            #7. Коэффициент вариации:
            variation_coefficient = std_deviation / average_revenue
            #8 Группа XYZ:
            variation_coefficient *= 100
            if variation_coefficient <= 10:
                xyz_group = 'X'
            elif variation_coefficient <= 25:
                xyz_group = 'Y'
            elif variation_coefficient >= 25:
                xyz_group = 'Z'
            # #8 Группа ABC XYZ:
            abc_xyz_group = abc_group + xyz_group

            #8. Контрагенты:
            
            contragents_list = []
            for sal in tyre.sales.all():
                contragents_list.append(sal.contragent)
            contragents_list_filtered = list(set(contragents_list))
            contragent_sales_dict = {}
            for contragent in contragents_list_filtered:
                contragent_sales = tyre.sales.all().filter(contragent=contragent)
                tot_sale = 0
                for val in contragent_sales:
                    tot_sale += val.sales_value
                contragent_sales_value = tot_sale
                contragent_sales_dict[contragent] = contragent_sales_value
            #print(contragent_sales_dict, 'sssss')
            contragent_sales_dict_sorted = {}       
            for k in sorted(contragent_sales_dict, key=contragent_sales_dict.get, reverse=True):
                contragent_sales_dict_sorted[k] = contragent_sales_dict[k]     
            #print(contragent_sales_dict_sorted)
            tyre_contragent_top_by_sale[tyre] = contragent_sales_dict_sorted

            #tyres_all__dict_sorted_with_percents[tyre] = tyre_total_sal, pecent, accumulated_precent, abc_group, average_revenue, std_deviation, variation_coefficient, xyz_group, abc_xyz_group
            tyres_all__dict_sorted_with_percents_final[tyre] = abc_xyz_group
        
        #print(tyre_contragent_top_by_sale)
        models.ABC_XYZ_GROP_HOME_DICT = tyres_all__dict_sorted_with_percents_final
        models.CONTRAGENT_SALES_SORTED_DICT = tyre_contragent_top_by_sale
        

        [[obj.total_sales(), obj.tyre_group(), obj.abc_xyz_group_home(), obj.top_contragents_by_sales(), ] for obj in home_table_tyres]
        return home_table_tyres


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #obj = context.get('object')


        #if self in sales_models.TYRE_SAL_TOTAL_DICT:
        #    total_sal = sales_models.TYRE_SAL_TOTAL_DICT.get(self)
        #[[obj.total_sale_in_period_hpmepage(), ] for obj in tyres_list]
        #return total_sal

        return context