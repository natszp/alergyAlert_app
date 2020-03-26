from django.test import TestCase, Client
import pytest

# Create your tests here.
from django.urls import reverse

from alergyAlert.models import *
from django.contrib.auth.models import User

class MealModelTest(TestCase):
    def setUp(self):
        User.objects.create()
        Meal.objects.create(name='pizza', description='simple&tasty', user_id=User.objects.get(id=1))

    def test_meal_setup(self):
        pizza= Meal.objects.get(name="pizza")
        self.assertEqual(pizza.description, "simple&tasty")


class LoginMealsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('user1', 'user1@user', 'classified')
        self.user = User.objects.create_user('user2', 'user2@user', 'classified2')
        self.meal = Meal.objects.create(name='scrumble eggs', description='tasty but fat rich', user_id=User.objects.get(id=2))

    def test_login_and_meals_view(self):
        self.client.login(username='user1', password='classified')
        response = self.client.get(reverse('meals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'alergyAlert/meals.html')

