from datetime import datetime

from django.contrib.auth.models import User

from models import Meal

meal1 = Meal.objects.create(name='coconut soup with rice', description='cooked 10 minutes with butter', date=datetime.now(), user_id=User.objects.get(id=2))
meal2 = Meal.objects.create(name='cereals with milk and honey', description='no lactose milk', date=datetime.now(), user_id=User.objects.get(id=3))
meal3 = Meal.objects.create(name='turkey with broccoli and potato puree', description='every ingridient from bio production', date=datetime.now(), user_id=User.objects.get(id=3))
