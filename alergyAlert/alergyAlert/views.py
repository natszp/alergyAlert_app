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
        return render(request, 'alergyAlert/meal_details.html', {'meal': meal})

    def post(self, request, slug):
        form = SymptomsForm(request.POST)
        form_class = SymptomsForm
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            strength = form.cleaned_data['strength']
            new_symptom = Symptom.objects.create(name=name, description=description, strength=strength)
            return redirect('meals')
        else:
            return render(request, 'alergyAlert/meal_details.html', context={'form': form})

    # model = Meal
    # form_class = SymptomsForm
    # template_name = 'alergyAlert/meal_details.html'
    # success_url = reverse_lazy('meals')
    #
    # def get_queryset(self):
    #     queryset = super(MealDetailView, self).get_queryset()
    #     return queryset.filter(user_id__id=self.request.user.id, slug=self.kwargs.get(self.slug_url_kwarg))

    # def form_valid(self, form):
    #     form.instance.user_id = self.request.user
    #     return super(MealDetailView, self).form_valid(form)


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
