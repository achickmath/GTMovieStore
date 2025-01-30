from .models import Movie
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404

from .models import Movie


# Create your views here.

def home(request):
    latest_movie_list = Movie.objects.all()
    context = {
        "latest_movie_list": latest_movie_list,
    }
    # output = ", ".join([m.movie_title for m in latest_movie_list])

    return render(request, "movies/index.html", context)

def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, "movies/detail.html", {"movie": movie})