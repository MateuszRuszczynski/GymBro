from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from tracker.forms import ExerciseForm, WorkoutPlanForm, GymUserCreationForm, GymUserUpdateForm, WorkoutLogForm, \
    MuscleGroupForm
from tracker.models import Exercise, MuscleGroup, GymUser, WorkoutLog, WorkoutPlan


def index(request):
    context = {
        "total_exercises": Exercise.objects.count(),
        "total_members": GymUser.objects.count(),
        "total_plans": WorkoutPlan.objects.count(),
        "total_logs": WorkoutLog.objects.count(),
        "recent_logs": WorkoutLog.objects.select_related(
            "user",
            "workout_plan"
        ).order_by("-date")[:5],
        "personal_record": WorkoutLog.objects.filter(
            is_personal_record=True
        ).select_related("user", "workout_plan").order_by("-date")[:5],
    }
    return render(request, "tracker/index.html", context=context)

def register(request):
    if request.method == "POST":
        form = GymUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = GymUserUpdateForm()
    return render(request, "registration/register.html", {"form": form})

class ExerciseListView(ListView):
    model = Exercise
    context_object_name = "exercises"

    def get_queryset(self):
        queryset = Exercise.objects.select_related("muscle_group")
        exercise_search = self.request.GET.get("exercise")
        if exercise_search:
            return queryset.filter(
                Q(name__icontains=exercise_search) |
                Q(muscle_group__name__icontains=exercise_search)
            )
        return queryset


class ExerciseDetailView(DetailView):
    model = Exercise
    context_object_name = "exercise"
    queryset = Exercise.objects.select_related("muscle_group")


class ExerciseCreateView(CreateView):
    model = Exercise
    context_object_name = "exercise"
    form_class = ExerciseForm
    success_url = reverse_lazy("tracker:exercise-list")


class ExerciseUpdateView(UpdateView):
    model = Exercise
    context_object_name = "exercise"
    form_class = ExerciseForm
    success_url = reverse_lazy("tracker:exercise-list")


class ExerciseDeleteView(DeleteView):
    model = Exercise
    context_object_name = "exercise"
    success_url = reverse_lazy("tracker:exercise-list")


class MuscleGroupListView(ListView):
    model = MuscleGroup
    context_object_name = "muscle_groups"


class MuscleGroupDetailView(DetailView):
    model = MuscleGroup
    context_object_name = "muscle_group"


class MuscleGroupCreateView(CreateView):
    model = MuscleGroup
    form_class = MuscleGroupForm
    context_object_name = "muscle_group"
    success_url = reverse_lazy("tracker:muscle-group-list")


class MuscleGroupUpdateView(UpdateView):
    model = MuscleGroup
    form_class = MuscleGroupForm
    context_object_name = "muscle_group"
    success_url = reverse_lazy("tracker:muscle-group-list")


class MuscleGroupDeleteView(DeleteView):
    model = MuscleGroup
    context_object_name = "muscle_group"
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
    context_object_name = "gym_user"
    form_class = GymUserCreationForm
    success_url = reverse_lazy("tracker:gym-user-list")


class GymUserUpdateView(UpdateView):
    model = GymUser
    context_object_name = "gym_user"
    form_class = GymUserUpdateForm
    success_url = reverse_lazy("tracker:gym-user-list")


class GymUserDeleteView(DeleteView):
    model = GymUser
    context_object_name = "gym_user"
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
    queryset = WorkoutLog.objects.select_related(
        "user",
        "workout_plan",
    )


class WorkoutLogCreateView(CreateView):
    model = WorkoutLog
    context_object_name = "workout_log"
    form_class = WorkoutLogForm
    success_url = reverse_lazy("tracker:workout-log-list")


class WorkoutLogUpdateView(UpdateView):
    model = WorkoutLog
    context_object_name = "workout_log"
    form_class = WorkoutLogForm
    success_url = reverse_lazy("tracker:workout-log-list")


class WorkoutLogDeleteView(DeleteView):
    model = WorkoutLog
    context_object_name = "workout_log"
    success_url = reverse_lazy("tracker:workout-log-list")


class WorkoutPlanListView(ListView):
    model = WorkoutPlan
    context_object_name = "workout_plans"
    queryset = WorkoutPlan.objects.select_related(
        "created_by"
    ).prefetch_related("exercises")


class WorkoutPlanDetailView(DetailView):
    model = WorkoutPlan
    context_object_name = "workout_plan"
    queryset = WorkoutPlan.objects.select_related(
        "created_by"
    ).prefetch_related("exercises")


class WorkoutPlanCreateView(CreateView):
    model = WorkoutPlan
    context_object_name = "workout_plan"
    form_class = WorkoutPlanForm
    success_url = reverse_lazy("tracker:workout-plan-list")


class WorkoutPlanUpdateView(UpdateView):
    model = WorkoutPlan
    context_object_name = "workout_plan"
    form_class = WorkoutPlanForm
    success_url = reverse_lazy("tracker:workout-plan-list")


class WorkoutPlanDeleteView(DeleteView):
    model = WorkoutPlan
    context_object_name = "workout_plan"
    success_url = reverse_lazy("tracker:workout-plan-list")
