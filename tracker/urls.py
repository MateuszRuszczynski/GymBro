from django.urls import path
from tracker import views


app_name = "tracker"

urlpatterns = [
    path("", views.index, name="index"),
    path("exercises/", views.ExerciseListView.as_view(), name="exercise-list"),
    path("exercises/create/", views.ExerciseCreateView.as_view(), name="exercise-create"),
    path("exercises/<int:pk>/", views.ExerciseDetailView.as_view(), name="exercise-detail"),
    path("musclegroups/", views.MuscleGroupListView.as_view(), name="muscle-group-list"),
    path("musclegroups/create/", views.MuscleGroupCreateView.as_view(), name="muscle-group-create"),
    path("musclegroups/<int:pk>/", views.MuscleGroupDetailView.as_view(), name="muscle-group-detail"),
    path("gymusers/", views.GymUserListView.as_view(), name="gym-user-list"),
    path("gymusers/create/", views.GymUserCreateView.as_view(), name="gym-user-create"),
    path("gymusers/<int:pk>/", views.GymUserDetailView.as_view(), name="gym-user-detail"),
    path("workoutlogs/", views.WorkoutLogListView.as_view(), name="workout-log-list"),
    path("workoutlogs/create/", views.WorkoutLogCreateView.as_view(), name="workout-log-create"),
    path("workoutlogs/<int:pk>/", views.WorkoutLogDetailView.as_view(), name="workout-log-detail"),
    path("workoutplans/", views.WorkoutPlanListView.as_view(), name="workout-plan-list"),
    path("workoutplans/create/", views.WorkoutPlanCreateView.as_view(), name="workout-plan-create"),
    path("workoutplans/<int:pk>/", views.WorkoutPlanDetailView.as_view(), name="workout-plan-detail"),
]
