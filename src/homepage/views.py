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
        abc_table_xyz_table = abc_table_xyz_models.AbcxyzTable.objects.all()[0]
        tyres_list = tyre_models.Tyre.objects.all()
        tyre_card_list = tyre_models.TyreCard.objects.all()

        for tyre_ob in tyres_list:
            tyre_in_abctable = abc_table_xyz_table.table.all().get(tyre=tyre_ob)
            home_table, created = models.HomePageModel.objects.get(
                tyre = tyre_ob, 
                abcxyz_group = tyre_in_abctable.abc_xyz_group()
            )
        home_table = models.HomePageModel.objects.all()
        #home_table, created = models.HomePageModel.objects.get_or_create()             #распаковка тапла
        return home_table


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #.objects.order_by
        obj = context.get('object')



        #context['periods'] = periods_dates_table_names

        
        return context