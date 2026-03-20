from django.shortcuts import render
from django.views.generic import ListView, DetailView

from tracker.models import Exercise, MuscleGroup, GymUser, WorkoutLog, WorkoutPlan


def index(request):
    return render(request, "tracker/index.html")


class ExerciseListView(ListView):
    model = Exercise
    context_object_name = "exercises"


class ExerciseDetailView(DetailView):
    model = Exercise
    context_object_name = "exercise"


class MuscleGroupListView(ListView):
    model = MuscleGroup
    context_object_name = "muscle_groups"


class MuscleGroupDetailView(DetailView):
    model = MuscleGroup
    context_object_name = "muscle_group"


class GymUserListView(ListView):
    model = GymUser
    context_object_name = "gym_users"
    ordering = ["username"]


class GymUserDetailView(DetailView):
    model = GymUser
    context_object_name = "gym_user"


class WorkoutLogListView(ListView):
    model = WorkoutLog
    context_object_name = "workout_logs"


class WorkoutLogDetailView(DetailView):
    model = WorkoutLog
    context_object_name = "workout_log"


class WorkoutPlanListView(ListView):
    model = WorkoutPlan
    context_object_name = "workout_plans"


class WorkoutPlanDetailView(DetailView):
    model = WorkoutPlan
    context_object_name = "workout_plan"
