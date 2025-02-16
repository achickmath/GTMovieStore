from django.contrib import admin
from .models import Movie, Review
from .models import Description
# from .models import CustomUser

admin.site.register(Movie)
admin.site.register(Description)
# admin.site.register(CustomUser)
# Register your models here.
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)