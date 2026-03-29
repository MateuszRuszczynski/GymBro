from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from datetime import date

from tracker.models import Exercise, WorkoutLog, MuscleGroup, WorkoutPlan


class MuscleGroupForm(forms.ModelForm):
    class Meta:
        model = MuscleGroup
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) <= 2:
            raise forms.ValidationError("Muscle group name must be at least 3 characters.")
        return name


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
        model = get_user_model()


class GymUserUpdateForm(forms.ModelForm):
    class Meta():
        model = get_user_model()
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
        user_height = self.cleaned_data["height"]
        if user_height is not None:
            if user_height < 0:
                raise forms.ValidationError("Enter a valid height.")
            if user_height > 400:
                raise forms.ValidationError("Enter a realistic height.")
        return user_height

    def clean_weight(self):
        user_weight = self.cleaned_data["weight"]
        if user_weight is not None:
            if user_weight < 0:
                raise forms.ValidationError("Enter a valid weight.")
            if user_weight > 600:
                raise forms.ValidationError("Enter a realistic weight.")
        return user_weight


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ["name", "description", "exercises", "goal"]
        widgets = {
            "exercises": forms.CheckboxSelectMultiple()
        }


class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ["workout_plan", "date", "duration_minutes", "notes", "is_personal_record"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_date(self):
        log_date = self.cleaned_data["date"]
        if log_date > date.today():
            raise forms.ValidationError("You can't log a workout in the future.")
        return log_date

    def clean_duration_minutes(self):
        duration = self.cleaned_data["duration_minutes"]
        if duration <= 0:
            raise forms.ValidationError("Duration must be greater than 0.")
        if duration > 300:
            raise forms.ValidationError("Duration can't be more than 300 minutes.")
        return duration


class ExerciseSearchForm(forms.Form):
    exercise = forms.CharField(
        max_length=50,
        required=False,
        label="",
    )


class GymUserSearchForm(forms.Form):
    gym_user = forms.CharField(
        max_length=50,
        required=False,
        label="",
    )
