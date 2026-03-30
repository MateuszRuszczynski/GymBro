from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tracker.models import GymUser, MuscleGroup, Exercise, WorkoutPlan, WorkoutLog


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(GymUser)
class GymUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional information",
            {
                "fields": (
                    "bio",
                    "height",
                    "weight",
                    "date_of_birth",
                    "membership_type",
                )
            },
        ),
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional information",
            {
                "fields": (
                    "bio",
                    "height",
                    "weight",
                    "date_of_birth",
                    "membership_type",
                )
            },
        ),
    )
    list_display = UserAdmin.list_display + (
        "bio",
        "height",
        "weight",
        "date_of_birth",
        "membership_type",
    )


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["name", "difficulty", "equipment", "muscle_group"]
    search_fields = ["name"]
    list_filter = ["difficulty", "muscle_group"]


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "goal", "created_by", "created_at"]
    search_fields = ["name"]
    list_filter = ["goal"]


@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "workout_plan",
        "date",
        "duration_minutes",
        "is_personal_record",
    ]
    list_filter = ["is_personal_record"]
