from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from tracker.models import Exercise, MuscleGroup, GymUser, WorkoutLog, WorkoutPlan


def index(request):
    return render(request, "tracker/index.html")


class ExerciseListView(ListView):
    model = Exercise
    context_object_name = "exercises"
    queryset = Exercise.objects.select_related("muscle_group")


class ExerciseDetailView(DetailView):
    model = Exercise
    context_object_name = "exercise"


class ExerciseCreateView(CreateView):
    model = Exercise
    success_url = reverse_lazy("tracker:exercise-list")


class MuscleGroupListView(ListView):
    model = MuscleGroup
    context_object_name = "muscle_groups"


class MuscleGroupDetailView(DetailView):
    model = MuscleGroup
    context_object_name = "muscle_group"


class MuscleGroupCreateView(CreateView):
    model = MuscleGroup
    success_url = reverse_lazy("tracker:muscle-group-list")


class GymUserListView(ListView):
    model = GymUser
    context_object_name = "gym_users"
    ordering = ["username"]


class GymUserDetailView(DetailView):
    model = GymUser
    context_object_name = "gym_user"


class GymUserCreateView(CreateView):
    model = GymUser
    success_url = reverse_lazy("tracker:gym-user-list")


class WorkoutLogListView(ListView):
    model = WorkoutLog
    context_object_name = "workout_logs"
    queryset = WorkoutLog.objects.select_related(
        "user",
        "workout_plan",
    )


class WorkoutLogDetailView(DetailView):
    model = WorkoutLog
    context_object_name = "workout_log"


class WorkoutLogCreateView(CreateView):
    model = WorkoutLog
    success_url = reverse_lazy("tracker:workout-log-list")


class WorkoutPlanListView(ListView):
    model = WorkoutPlan
    context_object_name = "workout_plans"
    queryset = WorkoutPlan.objects.select_related("created_by").prefetch_related("exercises")


class WorkoutPlanDetailView(DetailView):
    model = WorkoutPlan
    context_object_name = "workout_plan"


class WorkoutPlanCreateView(CreateView):
    model = WorkoutPlan
    success_url = reverse_lazy("tracker:workout-plan-list")
