from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from tracker.models import Exercise, MuscleGroup, GymUser, WorkoutLog, WorkoutPlan


def index(request):
    return render(request, "tracker/index.html")


exercise_queryset = Exercise.objects.select_related("muscle_group")


class ExerciseListView(ListView):
    model = Exercise
    context_object_name = "exercises"
    queryset = exercise_queryset


class ExerciseDetailView(DetailView):
    model = Exercise
    context_object_name = "exercise"
    queryset = exercise_queryset


class ExerciseCreateView(CreateView):
    model = Exercise
    success_url = reverse_lazy("tracker:exercise-list")
    fields = "__all__"


class ExerciseUpdateView(UpdateView):
    model = Exercise
    success_url = reverse_lazy("tracker:exercise-list")
    fields = "__all__"


class ExerciseDeleteView(DeleteView):
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
    fields = "__all__"


class MuscleGroupUpdateView(UpdateView):
    model = MuscleGroup
    fields = "__all__"
    success_url = reverse_lazy("tracker:muscle-group-list")


class MuscleGroupDeleteView(DeleteView):
    model = MuscleGroup
    success_url = reverse_lazy("tracker:muscle-group-list")


class GymUserListView(ListView):
    model = GymUser
    context_object_name = "gym_users"
    ordering = ["username"]


class GymUserDetailView(DetailView):
    model = GymUser
    context_object_name = "gym_user"


gymuser_fields = ("username", "first_name", "last_name", "email", "bio", "height", "weight", "date_of_birth",
                  "membership_type")


class GymUserCreateView(CreateView):
    model = GymUser
    fields = gymuser_fields
    success_url = reverse_lazy("tracker:gym-user-list")


class GymUserUpdateView(UpdateView):
    model = GymUser
    fields = gymuser_fields
    success_url = reverse_lazy("tracker:gym-user-list")


class GymUserDeleteView(DeleteView):
    model = GymUser
    success_url = reverse_lazy("tracker:gym-user-list")


workoutlog_queryset = WorkoutLog.objects.select_related(
    "user",
    "workout_plan",
)


class WorkoutLogListView(ListView):
    model = WorkoutLog
    context_object_name = "workout_logs"
    queryset = workoutlog_queryset


class WorkoutLogDetailView(DetailView):
    model = WorkoutLog
    context_object_name = "workout_log"
    queryset = workoutlog_queryset


class WorkoutLogCreateView(CreateView):
    model = WorkoutLog
    success_url = reverse_lazy("tracker:workout-log-list")
    fields = "__all__"


class WorkoutLogUpdateView(UpdateView):
    model = WorkoutLog
    fields = "__all__"
    success_url = reverse_lazy("tracker:workout-log-list")


class WorkoutLogDeleteView(DeleteView):
    model = WorkoutLog
    success_url = reverse_lazy("tracker:workout-log-list")


workoutplan_queryset = WorkoutPlan.objects.select_related(
    "created_by"
).prefetch_related("exercises")


class WorkoutPlanListView(ListView):
    model = WorkoutPlan
    context_object_name = "workout_plans"
    queryset = workoutplan_queryset


class WorkoutPlanDetailView(DetailView):
    model = WorkoutPlan
    context_object_name = "workout_plan"
    queryset = workoutplan_queryset


class WorkoutPlanCreateView(CreateView):
    model = WorkoutPlan
    success_url = reverse_lazy("tracker:workout-plan-list")
    fields = "__all__"


class WorkoutPlanUpdateView(UpdateView):
    model = WorkoutPlan
    fields = "__all__"
    success_url = reverse_lazy("tracker:workout-plan-list")


class WorkoutPlanDeleteView(DeleteView):
    model = WorkoutPlan
    success_url = reverse_lazy("tracker:workout-plan-list")
