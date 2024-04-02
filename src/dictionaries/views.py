from django.shortcuts import render
from . import models
from . import forms
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class DictionariesTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dictionaries/dictionaries.html'

class TyreSizCreateView(LoginRequiredMixin, CreateView):
    model = models.TyreSizeModel
    form_class = forms.TyreSizeForm
    template_name = 'dictionaries/ts_create.html'

class TyreSizeDetailView(LoginRequiredMixin, DetailView):
    model = models.TyreSizeModel
    form_class = forms.TyreSizeForm
    template_name = 'dictionaries/ts_detail.html'

class TyreSizeUpdateView(LoginRequiredMixin, UpdateView):
    model = models.TyreSizeModel
    form_class = forms.TyreSizeForm
    template_name = 'dictionaries/ts_update.html'

class TyreSizeListView(LoginRequiredMixin, ListView):
    template_name = 'dictionaries/ts_list.html'
    model = models.TyreSizeModel

class TyreSizeDeleteView(LoginRequiredMixin, DeleteView):
    model = models.TyreSizeModel
    template_name = 'dictionaries/ts_delete.html'
    success_url = reverse_lazy('dictionaries:ts_list')

class ModelNameCreateView(LoginRequiredMixin, CreateView):
    model = models.ModelNameModel
    form_class = forms.ModelNameForm
    template_name = 'dictionaries/model_create.html'

class ModelNameDetailView(LoginRequiredMixin, DetailView):
    model = models.ModelNameModel
    form_class = forms.ModelNameForm
    template_name = 'dictionaries/model_detail.html'

class ModelNameUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ModelNameModel
    form_class = forms.ModelNameForm
    template_name = 'dictionaries/model_update.html'

class ModelNameListView(LoginRequiredMixin, ListView):
    template_name = 'dictionaries/model_list.html'
    model = models.ModelNameModel

class ModelNameDeleteView(DeleteView):
    model = models.ModelNameModel
    template_name = 'dictionaries/model_delete.html'
    success_url = reverse_lazy('dictionaries:model_list')


class TyreGroupCreateView(LoginRequiredMixin, CreateView):
    model = models.TyreGroupModel
    form_class = forms.TyreGroupForm
    template_name = 'dictionaries/tg_create.html'
class TyreGroupDetailView(DetailView):
    model = models.TyreGroupModel
    form_class = forms.TyreGroupForm
    template_name = 'dictionaries/tg_detail.html'
class TyreGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = models.TyreGroupModel
    form_class = forms.TyreGroupForm
    template_name = 'dictionaries/tg_update.html'
class TyreGroupListView(LoginRequiredMixin, ListView):
    template_name = 'dictionaries/tg_list.html'
    model = models.TyreGroupModel
class TyreGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = models.TyreGroupModel
    template_name = 'dictionaries/model_delete.html'
    success_url = reverse_lazy('dictionaries:tg_list')


class QantityCountCreateView(LoginRequiredMixin, CreateView):
    model = models.QantityCountModel
    form_class = forms.QantityCountModelForm
    template_name = 'dictionaries/qnt_create.html'
class QantityCountDetailView(LoginRequiredMixin, DetailView):
    model = models.QantityCountModel
    form_class = forms.QantityCountModelForm
    template_name = 'dictionaries/qnt_detail.html'
class QantityCountUpdateView(LoginRequiredMixin, UpdateView):
    model = models.QantityCountModel
    form_class = forms.QantityCountModelForm
    template_name = 'dictionaries/qnt_update.html'
class QantityCountListView(LoginRequiredMixin, ListView):
    template_name = 'dictionaries/qnt_list.html'
    model = models.QantityCountModel
class QantityCountDeleteView(LoginRequiredMixin, DeleteView):
    model = models.QantityCountModel
    template_name = 'dictionaries/model_delete.html'
    success_url = reverse_lazy('dictionaries:qnt_list')

class CurrencyCreateView(LoginRequiredMixin, CreateView):
    model = models.Currency
    form_class = forms.CurrencytModelForm
    template_name = 'dictionaries/curr_create.html'
class CurrencyDetailView(LoginRequiredMixin, DetailView):
    model = models.Currency
    form_class = forms.CurrencytModelForm
    template_name = 'dictionaries/curr_detail.html'
class CurrencyUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Currency
    form_class = forms.CurrencytModelForm
    template_name = 'dictionaries/curr_update.html'
class CurrencyListView(LoginRequiredMixin, ListView):
    template_name = 'dictionaries/curr_list.html'
    model = models.Currency
class CurrencyDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Currency
    template_name = 'dictionaries/curr_delete.html'
    success_url = reverse_lazy('dictionaries:curr_list')


class ContragentsModelCreateView(LoginRequiredMixin, CreateView):
    model = models.ContragentsModel
    form_class = forms.ModelNameForm
    template_name = 'dictionaries/contragent_create.html'

class ContragentsModelDetailView(LoginRequiredMixin, DetailView):
    model = models.ContragentsModel
    form_class = forms.ContragentsModelForm
    template_name = 'dictionaries/contragent_detail.html'

class ContragentsModelUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ContragentsModel
    form_class = forms.ContragentsModelForm
    template_name = 'dictionaries/contragent_update.html'

class ContragentsModelListView(LoginRequiredMixin, ListView):
    template_name = 'dictionaries/contragent_list.html'
    model = models.ContragentsModel

class ContragentsModelDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ContragentsModel
    template_name = 'dictionaries/contragent_delete.html'
    success_url = reverse_lazy('dictionaries:contragent_list')