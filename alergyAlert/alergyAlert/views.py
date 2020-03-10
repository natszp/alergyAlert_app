import urllib

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView
from django.views.generic.base import *
from django.views.generic.detail import SingleObjectMixin

from alergyAlert.forms import LoginForm, MealForm, SymptomsForm
from alergyAlert.models import *
import requests
from requests.exceptions import HTTPError
import json

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
        return queryset.filter(user_id=self.request.user.id)

class MealDetailView(LoginRequiredMixin, View):

    def get(self, request, slug):
        meal = get_object_or_404(Meal, slug=slug)
        meal.how_allergizing = meal.alergen_strength()
        print(meal.alergen_strength())
        form = SymptomsForm()
        meal.save(update_fields=['how_allergizing'])
        external_meal_data = self.get_api(meal.name)
        return render(request, 'alergyAlert/meal_details.html', {'meal': meal, 'form': form, 'external_meal_data': external_meal_data})


    def post(self, request, slug):
        meal = get_object_or_404(Meal, slug=slug)
        form = SymptomsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            strength = form.cleaned_data['strength']
            Symptom.objects.create(name=name, description=description, strength=strength, meal=meal)
            return redirect('meal_details', slug)
        else:
            return render(request, 'alergyAlert/meal_details.html', context={'form': form})

    def get_api(self, mealName):
        external_search = requests.get('https://trackapi.nutritionix.com/v2/search/instant',
                params={'query': mealName},
                headers={
                    'Accept': 'application/json',
                    'x-app-id': 'd88ace4e',
                    'x-app-key': '185765650552a82832cfc281589781a5',
                    'x-remote-user-id': '0',
                })
        if (external_search.status_code == 200 and external_search.text is not None):
            parsed_external_text = json.loads(external_search.text)
        else:
            parsed_external_text = {}
        nf_calories_col = [x['nf_calories'] for x in parsed_external_text['branded'] if x['nf_calories'] is not None]
        kcal_avg = sum(nf_calories_col)/len(nf_calories_col)
        return (round(kcal_avg))


class AddMealView(LoginRequiredMixin, CreateView):
    model = Meal
    form_class = MealForm
    template_name = 'alergyAlert/form.html'
    success_url = reverse_lazy('meals')

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(AddMealView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('meals')


class UpdateMealView(LoginRequiredMixin, UpdateView):
    model = Meal
    form_class = MealForm
    template_name = 'alergyAlert/form.html'
    success_url = reverse_lazy('meals')

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(UpdateMealView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('meals')


class DeleteMealView(LoginRequiredMixin, DeleteView):
    model = Meal
    success_url = reverse_lazy('meals')

    def get_success_url(self, **kwargs):
        return reverse_lazy('meals')
