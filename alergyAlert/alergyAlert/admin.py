from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Alergen)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Symptom)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Meal)
class AuthorAdmin(admin.ModelAdmin):
    pass
