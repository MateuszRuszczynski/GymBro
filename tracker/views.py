from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from tracker.forms import ExerciseForm, WorkoutPlanForm, GymUserCreationForm, GymUserUpdateForm, WorkoutLogForm, \
    MuscleGroupForm
from tracker.models import Exercise, MuscleGroup, GymUser, WorkoutLog, WorkoutPlan


@login_required
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
        "personal_records": WorkoutLog.objects.filter(
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
        form = GymUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


class ExerciseListView(LoginRequiredMixin, ListView):
    model = Exercise
    context_object_name = "exercises"
    paginate_by = 5

    def get_queryset(self):
        queryset = Exercise.objects.select_related("muscle_group")
        exercise_search = self.request.GET.get("exercise")
        if exercise_search:
            return queryset.filter(
                Q(name__icontains=exercise_search) |
                Q(muscle_group__name__icontains=exercise_search)
            )
        return queryset


class ExerciseDetailView(LoginRequiredMixin, DetailView):
    model = Exercise
    context_object_name = "exercise"
    queryset = Exercise.objects.select_related("muscle_group")


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = Exercise
    context_object_name = "exercise"
    form_class = ExerciseForm
    success_url = reverse_lazy("tracker:exercise-list")


class ExerciseUpdateView(LoginRequiredMixin, UpdateView):
    model = Exercise
    context_object_name = "exercise"
    form_class = ExerciseForm
    success_url = reverse_lazy("tracker:exercise-list")


class ExerciseDeleteView(LoginRequiredMixin, DeleteView):
    model = Exercise
    context_object_name = "exercise"
    success_url = reverse_lazy("tracker:exercise-list")


class MuscleGroupListView(LoginRequiredMixin, ListView):
    model = MuscleGroup
    context_object_name = "muscle_groups"


class MuscleGroupDetailView(LoginRequiredMixin, DetailView):
    model = MuscleGroup
    context_object_name = "muscle_group"


class MuscleGroupCreateView(LoginRequiredMixin, CreateView):
    model = MuscleGroup
    form_class = MuscleGroupForm
    context_object_name = "muscle_group"
    success_url = reverse_lazy("tracker:muscle-group-list")


class MuscleGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = MuscleGroup
    form_class = MuscleGroupForm
    context_object_name = "muscle_group"
    success_url = reverse_lazy("tracker:muscle-group-list")


class MuscleGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = MuscleGroup
    context_object_name = "muscle_group"
    success_url = reverse_lazy("tracker:muscle-group-list")


class GymUserListView(LoginRequiredMixin, ListView):
    model = GymUser
    context_object_name = "gym_users"
    ordering = ["username"]
    paginate_by = 5

    def get_queryset(self):
        queryset = GymUser.objects.all()
        gym_search = self.request.GET.get("gym_user")
        if gym_search:
            return queryset.filter(
                Q(username__icontains=gym_search) |
                Q(first_name__icontains=gym_search) |
                Q(last_name__icontains=gym_search)
            )
        return queryset


class GymUserDetailView(LoginRequiredMixin, DetailView):
    model = GymUser
    context_object_name = "gym_user"


class GymUserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = GymUser
    context_object_name = "gym_user"
    form_class = GymUserCreationForm
    success_url = reverse_lazy("tracker:gym-user-list")

    def test_func(self):
        return self.request.user.is_staff


class GymUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = GymUser
    context_object_name = "gym_user"
    form_class = GymUserUpdateForm
    success_url = reverse_lazy("tracker:gym-user-list")

    def test_func(self):
        return self.request.user.is_staff


class GymUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GymUser
    context_object_name = "gym_user"
    success_url = reverse_lazy("tracker:gym-user-list")

    def test_func(self):
        return self.request.user.is_staff


class WorkoutLogListView(LoginRequiredMixin, ListView):
    model = WorkoutLog
    context_object_name = "workout_logs"
    queryset = WorkoutLog.objects.select_related(
        "user",
        "workout_plan",
    )


class WorkoutLogDetailView(LoginRequiredMixin, DetailView):
    model = WorkoutLog
    context_object_name = "workout_log"
    queryset = WorkoutLog.objects.select_related(
        "user",
        "workout_plan",
    )


class WorkoutLogCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutLog
    context_object_name = "workout_log"
    form_class = WorkoutLogForm
    success_url = reverse_lazy("tracker:workout-log-list")


class WorkoutLogUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkoutLog
    context_object_name = "workout_log"
    form_class = WorkoutLogForm
    success_url = reverse_lazy("tracker:workout-log-list")


class WorkoutLogDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutLog
    context_object_name = "workout_log"
    success_url = reverse_lazy("tracker:workout-log-list")


class WorkoutPlanListView(LoginRequiredMixin, ListView):
    model = WorkoutPlan
    context_object_name = "workout_plans"
    queryset = WorkoutPlan.objects.select_related(
        "created_by"
    ).prefetch_related("exercises")


class WorkoutPlanDetailView(LoginRequiredMixin, DetailView):
    model = WorkoutPlan
    context_object_name = "workout_plan"
    queryset = WorkoutPlan.objects.select_related(
        "created_by"
    ).prefetch_related("exercises")


class WorkoutPlanCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutPlan
    context_object_name = "workout_plan"
    form_class = WorkoutPlanForm
    success_url = reverse_lazy("tracker:workout-plan-list")


class WorkoutPlanUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkoutPlan
    context_object_name = "workout_plan"
    form_class = WorkoutPlanForm
    success_url = reverse_lazy("tracker:workout-plan-list")


class WorkoutPlanDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutPlan
    context_object_name = "workout_plan"
    success_url = reverse_lazy("tracker:workout-plan-list")
