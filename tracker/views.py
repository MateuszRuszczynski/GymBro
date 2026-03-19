from django.shortcuts import render
from django.views.generic import ListView

from tracker.models import Exercise, MuscleGroup, GymUser, WorkoutLog, WorkoutPlan


def index(request):
    return render(request, "tracker/index.html")


class ExerciseListView(ListView):
    model = Exercise


class MuscleGroupListView(ListView):
    model = MuscleGroup


class GymUserListView(ListView):
    model = GymUser
    ordering = ["username"]


class WorkoutLogListView(ListView):
    model = WorkoutLog


class WorkoutPlanListView(ListView):
    model = WorkoutPlan
