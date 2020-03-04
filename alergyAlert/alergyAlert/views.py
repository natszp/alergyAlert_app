from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, CreateView
from django.views.generic.base import *

from alergyAlert.forms import LoginForm, AddMealForm
from alergyAlert.models import *


class MainView(View):
    def get(self, request):
        alergens = Alergen.objects.order_by('name')
        return render(request, 'alergyAlert/main.html', {'alergens':alergens})

class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'alergyAlert/form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                path = request.GET.get('next')
                if path is not None:
                    return redirect(path)
                return redirect('meals')
            else:
                return HttpResponse("There is no such an user, plase try again")
        else:
            return HttpResponse('there is an error in validation')

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('main')

class MealsView(LoginRequiredMixin, ListView):
    model = Meal
    template_name ='alergyAlert/meals.html'

    def get_queryset(self):
        queryset = super(MealsView, self).get_queryset()
        return queryset.filter(user_id__id=self.kwargs['id'])


class AddMealView(LoginRequiredMixin, CreateView):
    model = Meal
    fields = ['name', 'description', 'alergens']
    template_name = 'alergyAlert/form.html'
    success_url = reverse_lazy('meals')

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(AddMealView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('meals', kwargs={'id': self.request.user.id})

# class AddMealView(View):
    # def get(self, request):
    #     form = AddMealForm()
    #     return render(request, 'alergyAlert/form.html', {'form': form})
    #
    # def post(self, request):
    #     form = AddMealForm(request.POST)
    #     if form.is_valid():
    #         return redirect('meals')
    #     else:
    #         return render(request, 'alergyAlert/form.html', {'form': form})

