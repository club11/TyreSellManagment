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