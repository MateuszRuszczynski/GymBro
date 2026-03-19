from django.shortcuts import render
from django.views.generic import ListView

from tracker.models import Exercise


def index(request):
    return render(request, "tracker/index.html")


class ExerciseListView(ListView):
    model = Exercise

