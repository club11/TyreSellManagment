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
        #home_table = models.HomePageModel.objects.all()[0].pk          # возьмем первый сохданный объект HomePageModel - он для всех один - его будут видеть все юзеры

        abc_table_xyz_table = abc_table_xyz_models.AbcxyzTable.objects.all()[0]
        print(abc_table_xyz_table.table.all())
        tyres_list = tyre_models.Tyre.objects.all()
        print(tyres_list )
        tyre_card_list = tyre_models.TyreCard.objects.all()

        for tyre_ob in tyres_list:
            tyre_in_abctable = abc_table_xyz_table.table.all().get(tyre=tyre_ob)
            home_table, created = models.HomePageModel.objects.get_or_create(
                tyre = tyre_ob, 
                #abcxyz_group = abc_table_xyz_table.table.abc_xyz_gr
                abcxyz_group = tyre_in_abctable.abc_xyz_gr()
        
            )

        #home_table, created = models.HomePageModel.objects.get_or_create()             #распаковка тапла

        #return home_table
        return abc_table_xyz_table