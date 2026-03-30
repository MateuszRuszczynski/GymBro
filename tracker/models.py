from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class MuscleGroup(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class GymUser(AbstractUser):
    bio = models.TextField(max_length=250, blank=True)
    height = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    membership_choices = [
        ("free", "Free"),
        ("premium", "Premium"),
        ("coach", "Coach"),
    ]
    membership_type = models.CharField(
        max_length=20, choices=membership_choices, default="free"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    difficulty_choices = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]
    difficulty = models.CharField(max_length=20, choices=difficulty_choices)
    equipment = models.CharField(max_length=100)
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercises = models.ManyToManyField(Exercise, related_name="workout_plans")
    status_choices = [
        ("strength", "Strength"),
        ("hypertrophy", "Hypertrophy"),
        ("endurance", "Endurance"),
        ("weight_loss", "Weight loss"),
    ]
    goal = models.CharField(max_length=20, choices=status_choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WorkoutLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    date = models.DateField()
    duration_minutes = models.IntegerField()
    notes = models.TextField(max_length=200, blank=True)
    is_personal_record = models.BooleanField(default=False)

    def __str__(self):
        return self.workout_plan.name
