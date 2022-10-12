import http
from django.shortcuts import render
from . import models
from . import forms
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView, FormView
from django.urls import reverse_lazy
from dictionaries import models as dictionaries_models
from django.http import HttpResponseRedirect, HttpRequest

class TyreCardCreateView(FormView):
    model = models.TyreCard
    form_class = forms.TyreCardForm
    template_name = 'tyres/tyre_card_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Шина:
        tires = models.Tyre.objects.all()
        tyre_list = []
        for tyre in tires:
            tyre_list.append(tyre)
        context['tyre_list'] = tyre_list
        return context
  
    def post(self, request: HttpRequest, *args: str, **kwargs):
        #print(request.POST)
        # дата серийного освоения шины:
        tyre_serie_data = request.POST.get('serie_data')
        #print(tyre_serie_data)
        # картинка
        picture = request.FILES.get('picture')
        print(picture, 'HHHH')
        # шина
        tyre_chosen_id = request.POST.get('tyre_list')
        tyre_chosen = models.Tyre.objects.get(id=tyre_chosen_id )
        #print(tyre_chosen)

        # создание нового объекта TyreCard (КАРТОЧКА ШИНЫ):
        tyre_card = models.TyreCard.objects.get_or_create(
            tyre = tyre_chosen,
            serie_date = tyre_serie_data,
            picture = picture
        )
        return super().post(request, *args, **kwargs)



class TyreCardDetailView(DetailView):
    model = models.TyreCard
    form_class = forms.TyreCardForm
    template_name = 'tyres/tyre_card_detail.html'

class TyreCardUpdateView(UpdateView):
    model = models.TyreCard
    form_class = forms.TyreCardForm
    template_name = 'tyres/tyre_card_update.html'
    
class TyreCardListView(ListView):
    template_name = 'tyres/tyre_card_list.html'
    model = models.TyreCard

class TyreCardDeleteView(DeleteView):
    model = models.TyreCard
    template_name = 'tyres/model_delete.html'
    success_url = reverse_lazy('tyres:tyre_card_list')


class TyreListView(ListView):
    template_name = 'tyres/tyre_list.html'
    model = models.Tyre


class TyreCreateView(CreateView):
    model = models.Tyre
    form_class = forms.TyreForm
    template_name = 'tyres/tyre_create.html'
#class TyreDetailView(DetailView):
#    model = models.Tyre
#    form_class = forms.TyreForm
#    template_name = 'tyres/tyre_detail.html'
class TyreUpdateView(UpdateView):
    model = models.Tyre
    form_class = forms.TyreForm
    template_name = 'tyres/tyre_update.html'
class TyreDeleteView(DeleteView):
    model = models.Tyre
    template_name = 'tyres/tyre_delete.html'
    success_url = reverse_lazy('tyres:tyre_list')