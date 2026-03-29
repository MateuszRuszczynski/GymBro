from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class MuscleGroup(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


MEMBERSHIP_CHOICES = [
    ("free", "Free"),
    ("premium", "Premium"),
    ("coach", "Coach"),
]


class GymUser(AbstractUser):
    bio = models.TextField(max_length=250, blank=True)
    height = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default="free")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


DIFFICULTY_CHOICES = [
    ("beginner", "Beginner"),
    ("intermediate", "Intermediate"),
    ("advanced", "Advanced"),
]


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    equipment = models.CharField(max_length=100)
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


STATUS_CHOICES = [
    ("strength", "Strength"),
    ("hypertrophy", "Hypertrophy"),
    ("endurance", "Endurance"),
    ("weight_loss", "Weight loss"),
]


class WorkoutPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercises = models.ManyToManyField(Exercise, related_name="workout_plans")
    goal = models.CharField(max_length=20, choices=STATUS_CHOICES)
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
