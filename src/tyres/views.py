from django.shortcuts import render
from . import models
from . import forms
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy

class TyreCardCreateView(CreateView):
    model = models.TyreCard
    form_class = forms.TyreCardForm
    template_name = 'tyres/tyre_card_create.html'

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
    success_url = reverse_lazy('dictionaries:tyre_card')


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