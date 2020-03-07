from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.template.defaultfilters import slugify

ALERGENS = (
    (1, 'gluten'),
    (2, 'egg'),
    (3, 'cow milk'),
    (4, 'nuts'),
    (5, 'fish'),
    (6, 'seafood'),

)
class Alergen(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.name)

STRENGTH = (
    (1, 'very weak'),
    (2, 'rather weak'),
    (3, 'medium'),
    (4, 'rather strong'),
    (5, 'very strong'),
)
class Symptom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    strength = models.IntegerField(choices=STRENGTH)

    def __str__(self):
        return "{}".format(self.name)


class Meal(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=50)
    description = models.TextField()
    date = models.DateField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    alergens = models.ManyToManyField(Alergen)
    symptoms = models.ManyToManyField(Symptom)
    how_allergizing = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Meal, self).save(*args, **kwargs)

    def how_allergize(self, symptoms, alergens):
       pass


