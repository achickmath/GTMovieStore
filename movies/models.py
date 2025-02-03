from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    movie_title = models.CharField(max_length=100)

    def __str__(self):
        return self.movie_title

class Description(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.description

