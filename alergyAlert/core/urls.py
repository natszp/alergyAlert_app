"""alert URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from alergyAlert.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('about/', AboutView.as_view(), name='about'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('meals/', MealsView.as_view(), name='meals'),
    path('meal/<str:slug>', MealDetailView.as_view(), name='meal_details'),
    path('add_meal/', AddMealView.as_view(), name='add_meal'),
    path('update_meal/<str:slug>', UpdateMealView.as_view(), name='update_meal'),
    path('delete_meal/<str:slug>', DeleteMealView.as_view(), name='delete_meal'),
    path('recommendations/', RecommendationsView.as_view(), name='recommendations'),


]
