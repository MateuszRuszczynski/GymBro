from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from tracker.models import Exercise, WorkoutPlan, GymUser


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "description", "difficulty", "equipment", "muscle_group"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")
        return name

    def clean_equipment(self):
        equipment = self.cleaned_data["equipment"]
        if len(equipment) < 3:
            raise forms.ValidationError("Equipment must be at least 3 characters long.")
        return equipment


class GymUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = GymUser
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "bio",
            "height",
            "weight",
            "date_of_birth",
            "membership_type"
        )
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_height(self):
        return validate_height(self.cleaned_data["height"])

    def clean_weight(self):
        return validate_weight(self.cleaned_data["weight"])


class GymUserUpdateForm(forms.ModelForm):
    class Meta():
        model = GymUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "bio",
            "height",
            "weight",
            "date_of_birth",
            "membership_type",
        )
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_height(self):
        return validate_height(self.cleaned_data["height"])

    def clean_weight(self):
        return validate_weight(self.cleaned_data["weight"])


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ["name", "description", "created_by", "exercises", "goal"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "exercises": forms.CheckboxSelectMultiple(),
        }

    def clean_exercises(self):
        exercises = self.cleaned_data["exercises"]
        if len(exercises) < 1:
            raise forms.ValidationError("The workout plan must have at least one exercise.")
        return exercises


def validate_height(user_height: float) -> float:
    if user_height <= 0:
        raise forms.ValidationError("Enter a valid height.")
    return user_height


def validate_weight(user_weight: float) -> float:
    if user_weight <= 0:
        raise forms.ValidationError("Enter a valid weight.")
    return user_weight
