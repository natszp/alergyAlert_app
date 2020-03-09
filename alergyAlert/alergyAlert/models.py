from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.template.defaultfilters import slugify

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

# HOW_ALERGIZING = (
#     (1, 'poor'),
#     (2, 'moderate'),
#     # (3, 'strong'),
# )
class Meal(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=50)
    description = models.TextField()
    date = models.DateField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    alergens = models.ManyToManyField(Alergen)
    how_allergizing = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Meal, self).save(*args, **kwargs)

    def how_allergize(self):
        number_of_alergens = self.alergens.all().count()
        if number_of_alergens<=2:
            self.how_allergizing = 1
        elif number_of_alergens==3:
            self.how_allergizing = 2
        else:
            self.how_allergizing = 3


class Symptom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    strength = models.IntegerField(choices=STRENGTH)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.name)
