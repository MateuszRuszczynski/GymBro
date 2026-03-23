from django.urls import path
from tracker import views


app_name = "tracker"

urlpatterns = [
    path("", views.index, name="index"),
    path("exercises/", views.ExerciseListView.as_view(), name="exercise-list"),
    path("exercises/create/", views.ExerciseCreateView.as_view(), name="exercise-create"),
    path("exercises/<int:pk>/", views.ExerciseDetailView.as_view(), name="exercise-detail"),
    path("exercises/<int:pk>/update/", views.ExerciseUpdateView.as_view(), name="exercise-update"),
    path("exercises/<int:pk>/delete/",views.ExerciseDeleteView.as_view(), name="exercise-delete" ),
    path("musclegroups/", views.MuscleGroupListView.as_view(), name="muscle-group-list"),
    path("musclegroups/create/", views.MuscleGroupCreateView.as_view(), name="muscle-group-create"),
    path("musclegroups/<int:pk>/", views.MuscleGroupDetailView.as_view(), name="muscle-group-detail"),
    path("musclegroups/<int:pk>/update/", views.MuscleGroupUpdateView.as_view(), name="muscle-group-update"),
    path("musclegroups/<int:pk>/delete/",views.MuscleGroupDeleteView.as_view(), name="muscle-group-delete"),
    path("gymusers/", views.GymUserListView.as_view(), name="gym-user-list"),
    path("gymusers/create/", views.GymUserCreateView.as_view(), name="gym-user-create"),
    path("gymusers/<int:pk>/", views.GymUserDetailView.as_view(), name="gym-user-detail"),
    path("gymusers/<int:pk>/update/", views.GymUserUpdateView.as_view(), name="gym-user-update"),
    path("gymusers/<int:pk>/delete/",views.GymUserDeleteView.as_view(), name="gym-user-delete"),
    path("workoutlogs/", views.WorkoutLogListView.as_view(), name="workout-log-list"),
    path("workoutlogs/create/", views.WorkoutLogCreateView.as_view(), name="workout-log-create"),
    path("workoutlogs/<int:pk>/", views.WorkoutLogDetailView.as_view(), name="workout-log-detail"),
    path("workoutlogs/<int:pk>/update/", views.WorkoutLogUpdateView.as_view(), name="workout-log-update"),
    path("workoutlogs/<int:pk>/delete/",views.WorkoutLogDeleteView.as_view(), name="workout-log-delete"),
    path("workoutplans/", views.WorkoutPlanListView.as_view(), name="workout-plan-list"),
    path("workoutplans/create/", views.WorkoutPlanCreateView.as_view(), name="workout-plan-create"),
    path("workoutplans/<int:pk>/", views.WorkoutPlanDetailView.as_view(), name="workout-plan-detail"),
    path("workoutplans/<int:pk>/update/", views.WorkoutPlanUpdateView.as_view(), name="workout-plan-update"),
    path("workoutplans/<int:pk>/delete/",views.WorkoutPlanDeleteView.as_view(), name="workout-plan-delete"),
]
