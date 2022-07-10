from django.shortcuts import render
from . import models
from . import forms
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView, TemplateView
from django.urls import reverse_lazy

class HomeTemplateView(TemplateView):
    template_name = 'dictionaries/home.html'

class DictionariesTemplateView(TemplateView):
    template_name = 'dictionaries/dictionaries.html'

class TyreSizCreateView(CreateView):
    model = models.TyreSizeModel
    form_class = forms.TyreSizeForm
    template_name = 'dictionaries/ts_create.html'

class TyreSizeDetailView(DetailView):
    model = models.TyreSizeModel
    form_class = forms.TyreSizeForm
    template_name = 'dictionaries/ts_detail.html'

class TyreSizeUpdateView(UpdateView):
    model = models.TyreSizeModel
    form_class = forms.TyreSizeForm
    template_name = 'dictionaries/ts_update.html'

class TyreSizeListView(ListView):
    template_name = 'dictionaries/ts_list.html'
    model = models.TyreSizeModel

class TyreSizeDeleteView(DeleteView):
    model = models.TyreSizeModel
    template_name = 'dictionaries/ts_delete.html'
    success_url = reverse_lazy('dictionaries:ts_list')

class ModelNameCreateView(CreateView):
    model = models.ModelNameModel
    form_class = forms.ModelNameForm
    template_name = 'dictionaries/model_create.html'

class ModelNameDetailView(DetailView):
    model = models.ModelNameModel
    form_class = forms.ModelNameForm
    template_name = 'dictionaries/model_detail.html'

class ModelNameUpdateView(UpdateView):
    model = models.ModelNameModel
    form_class = forms.ModelNameForm
    template_name = 'dictionaries/model_update.html'

class ModelNameListView(ListView):
    template_name = 'dictionaries/model_list.html'
    model = models.ModelNameModel

class ModelNameDeleteView(DeleteView):
    model = models.ModelNameModel
    template_name = 'dictionaries/model_delete.html'
    success_url = reverse_lazy('dictionaries:model_list')
