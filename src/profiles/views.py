from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from . import forms
from . import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib.auth.forms import PasswordChangeForm

class RegisterFormView(LoginRequiredMixin, FormView):
    template_name = 'profiles/create_user.html'
    form_class = forms.RegisterForm

    login_url = "/login/"   # ссылочка на авторизацию *mixin LoginRequiredMixin
    redirect_field_name = "redirect_to"     # верннуть на страницу после авторизации *mixin LoginRequiredMixin

    def form_valid(self, form):
        #print('||||||||||||||||||||||', self.request.session.ge)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username=username, password=password)
        profile = models.Profiles.objects.create(user=user, email=email)
        return HttpResponseRedirect(reverse_lazy('profiles:register'))
    
class SomeUserLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    redirect_field_name = 'next'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
    #    print('===============', kwargs.keys())
        if self.request.GET.get('data'):
            # remember old state
            _mutable = kwargs['data']._mutable
            # set to mutable
            kwargs['data']._mutable = True
            # сhange the values
            got_username = self.request.POST.get('username')
            got_password = self.request.POST.get('password')
            kwargs['data']['username'] = got_username
            kwargs['data']['password'] = got_password
            # set mutable flag back
            kwargs['data']._mutable = _mutable
    #    print("+++++", kwargs)
        return kwargs
    

class SomePasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'registration/chp.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('chemcurier:chemcurier_table')

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        #print('===000===', kwargs)
        return kwargs
    
class SomeLogoutView(auth_views.LogoutView):
    #template_name = 'registration/logged_out.html'
    next_page = reverse_lazy('login')

