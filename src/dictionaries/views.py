from django.shortcuts import render
from . import models
from . import forms
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView, TemplateView
from django.urls import reverse_lazy


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


class TyreGroupCreateView(CreateView):
    model = models.TyreGroupModel
    form_class = forms.TyreGroupForm
    template_name = 'dictionaries/tg_create.html'
class TyreGroupDetailView(DetailView):
    model = models.TyreGroupModel
    form_class = forms.TyreGroupForm
    template_name = 'dictionaries/tg_detail.html'
class TyreGroupUpdateView(UpdateView):
    model = models.TyreGroupModel
    form_class = forms.TyreGroupForm
    template_name = 'dictionaries/tg_update.html'
class TyreGroupListView(ListView):
    template_name = 'dictionaries/tg_list.html'
    model = models.TyreGroupModel
class TyreGroupDeleteView(DeleteView):
    model = models.TyreGroupModel
    template_name = 'dictionaries/model_delete.html'
    success_url = reverse_lazy('dictionaries:tg_list')


class QantityCountCreateView(CreateView):
    model = models.QantityCountModel
    form_class = forms.QantityCountModelForm
    template_name = 'dictionaries/qnt_create.html'
class QantityCountDetailView(DetailView):
    model = models.QantityCountModel
    form_class = forms.QantityCountModelForm
    template_name = 'dictionaries/qnt_detail.html'
class QantityCountUpdateView(UpdateView):
    model = models.QantityCountModel
    form_class = forms.QantityCountModelForm
    template_name = 'dictionaries/qnt_update.html'
class QantityCountListView(ListView):
    template_name = 'dictionaries/qnt_list.html'
    model = models.QantityCountModel
class QantityCountDeleteView(DeleteView):
    model = models.QantityCountModel
    template_name = 'dictionaries/model_delete.html'
    success_url = reverse_lazy('dictionaries:qnt_list')

class CurrencyCreateView(CreateView):
    model = models.Currency
    form_class = forms.CurrencytModelForm
    template_name = 'dictionaries/curr_create.html'
class CurrencyDetailView(DetailView):
    model = models.Currency
    form_class = forms.CurrencytModelForm
    template_name = 'dictionaries/curr_detail.html'
class CurrencyUpdateView(UpdateView):
    model = models.Currency
    form_class = forms.CurrencytModelForm
    template_name = 'dictionaries/curr_update.html'
class CurrencyListView(ListView):
    template_name = 'dictionaries/curr_list.html'
    model = models.Currency
class CurrencyDeleteView(DeleteView):
    model = models.Currency
    template_name = 'dictionaries/curr_delete.html'
    success_url = reverse_lazy('dictionaries:curr_list')


