from django.contrib import admin
from .models import Movie, Review
from .models import Description

admin.site.register(Movie)
admin.site.register(Description)
# Register your models here.
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)