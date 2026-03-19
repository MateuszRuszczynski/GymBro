from django.shortcuts import render
from django.views.generic import ListView

from tracker.models import Exercise, MuscleGroup, GymUser, WorkoutLog, WorkoutPlan


def index(request):
    return render(request, "tracker/index.html")


class ExerciseListView(ListView):
    model = Exercise
    context_object_name = "exercises"


class MuscleGroupListView(ListView):
    model = MuscleGroup
    context_object_name = "muscle_groups"


class GymUserListView(ListView):
    model = GymUser
    context_object_name = "gym_users"
    ordering = ["username"]


class WorkoutLogListView(ListView):
    model = WorkoutLog
    context_object_name = "workout_logs"


class WorkoutPlanListView(ListView):
    model = WorkoutPlan
    context_object_name = "workout_plans"
