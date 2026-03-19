from django.urls import path

from .views import (
    index,
    ExerciseListView,
    MuscleGroupListView,
    GymUserListView,
    WorkoutLogListView,
    WorkoutPlanListView
)

app_name = "tracker"

urlpatterns = [
    path("", index, name="index"),
    path("exercises/", ExerciseListView.as_view(), name="exercise-list"),
    path("musclegroups/", MuscleGroupListView.as_view(), name="muscle-group-list"),
    path("gymusers/", GymUserListView.as_view(), name="gymu-uer-list"),
    path("workoutlogs/", WorkoutLogListView.as_view(), name="workout-log-list"),
    path("workoutplans/", WorkoutPlanListView.as_view(), name="workout-plan-list"),
]
