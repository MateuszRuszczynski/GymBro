from datetime import date, timedelta

from django.test import TestCase

from tracker.forms import (
    MuscleGroupForm,
    ExerciseForm,
    GymUserUpdateForm,
    WorkoutPlanForm,
    WorkoutLogForm,
    ExerciseSearchForm,
    GymUserSearchForm,
)
from tracker.models import MuscleGroup, Exercise, GymUser, WorkoutPlan


class MuscleGroupFormTest(TestCase):
    def test_name_too_short(self):
        form = MuscleGroupForm(data={"name": "Tr"})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_with_valid_data(self):
        form = MuscleGroupForm(data={"name": "Triceps"})
        self.assertTrue(form.is_valid())


class ExerciseFormTest(TestCase):
    def setUp(self):
        self.muscle_group = MuscleGroup.objects.create(name="Legs")

    def test_name_too_short(self):
        form = ExerciseForm(
            data={
                "name": "Sq",
                "description": "",
                "difficulty": "intermediate",
                "equipment": "barbell",
                "muscle_group": self.muscle_group.pk,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_with_valid_data(self):
        form = ExerciseForm(
            data={
                "name": "Squat",
                "description": "",
                "difficulty": "intermediate",
                "equipment": "barbell",
                "muscle_group": self.muscle_group.pk,
            }
        )
        self.assertTrue(form.is_valid())

    def test_equipment_length_too_short(self):
        form = ExerciseForm(
            data={
                "name": "Squat",
                "description": "",
                "difficulty": "intermediate",
                "equipment": "ba",
                "muscle_group": self.muscle_group.pk,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("equipment", form.errors)

    def test_equipment_length_valid_data(self):
        form = ExerciseForm(
            data={
                "name": "Squat",
                "description": "",
                "difficulty": "intermediate",
                "equipment": "barbell",
                "muscle_group": self.muscle_group.pk,
            }
        )
        self.assertTrue(form.is_valid())


class GymUserUpdateFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@gymbro.com",
            "bio": "",
            "height": "182",
            "weight": "90",
            "date_of_birth": "",
            "membership_type": "free",
        }

    def test_valid_data_passes(self):
        form = GymUserUpdateForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_height_too_low(self):
        data = self.valid_data.copy()
        data["height"] = "-1"
        form = GymUserUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("height", form.errors)

    def test_height_too_high(self):
        data = self.valid_data.copy()
        data["height"] = "401"
        form = GymUserUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("height", form.errors)

    def test_weight_too_low(self):
        data = self.valid_data.copy()
        data["weight"] = "-1"
        form = GymUserUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("weight", form.errors)

    def test_weight_too_high(self):
        data = self.valid_data.copy()
        data["weight"] = "601"
        form = GymUserUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("weight", form.errors)

    def test_height_and_weight_empty_is_valid(self):
        data = self.valid_data.copy()
        data["height"] = ""
        data["weight"] = ""
        form = GymUserUpdateForm(data=data)
        self.assertTrue(form.is_valid())


class WorkoutPlanFormTest(TestCase):
    def setUp(self):
        self.muscle_group = MuscleGroup.objects.create(name="Legs")
        self.exercise = Exercise.objects.create(
            name="Squat",
            description="The best legs exercise",
            difficulty="intermediate",
            muscle_group=self.muscle_group,
        )
        self.valid_data = {
            "name": "Power",
            "description": "",
            "exercises": self.exercise.pk,
            "goal": "strength",
        }

    def test_multiple_exercises_valid(self):
        second_exercise = Exercise.objects.create(
            name="Leg press",
            description="The best legs exercise",
            difficulty="intermediate",
            muscle_group=self.muscle_group,
        )
        data = self.valid_data.copy()
        data["exercises"] = [second_exercise.pk, self.exercise.pk]
        form = WorkoutPlanForm(data=data)
        self.assertTrue(form.is_valid())


class WorkoutLogFormTest(TestCase):
    def setUp(self):
        self.user = GymUser.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.muscle_group = MuscleGroup.objects.create(name="Chest")
        self.exercise = Exercise.objects.create(
            name="Bench Press",
            difficulty="intermediate",
            equipment="Barbell",
            muscle_group=self.muscle_group,
        )
        self.plan = WorkoutPlan.objects.create(
            name="Push Day",
            goal="strength",
            created_by=self.user,
        )
        self.valid_data = {
            "workout_plan": self.plan.pk,
            "date": date.today().strftime("%Y-%m-%d"),
            "duration_minutes": 60,
            "notes": "",
            "is_personal_record": False,
        }

    def test_valid_data_passes(self):
        form = WorkoutLogForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_future_date_fails(self):
        data = self.valid_data.copy()
        data["date"] = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        form = WorkoutLogForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)

    def test_past_date_is_valid(self):
        data = self.valid_data.copy()
        data["date"] = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        form = WorkoutLogForm(data=data)
        self.assertTrue(form.is_valid())

    def test_negative_duration_fails(self):
        data = self.valid_data.copy()
        data["duration_minutes"] = -10
        form = WorkoutLogForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("duration_minutes", form.errors)

    def test_zero_duration_fails(self):
        data = self.valid_data.copy()
        data["duration_minutes"] = 0
        form = WorkoutLogForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("duration_minutes", form.errors)

    def test_duration_over_300_fails(self):
        data = self.valid_data.copy()
        data["duration_minutes"] = 301
        form = WorkoutLogForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("duration_minutes", form.errors)

    def test_duration_exactly_300_is_valid(self):
        data = self.valid_data.copy()
        data["duration_minutes"] = 300
        form = WorkoutLogForm(data=data)
        self.assertTrue(form.is_valid())


class ExerciseSearchFormTest(TestCase):
    def test_empty_search_is_valid(self):
        form = ExerciseSearchForm(data={"exercise": ""})
        self.assertTrue(form.is_valid())

    def test_valid_search_term(self):
        form = ExerciseSearchForm(data={"exercise": "Bench Press"})
        self.assertTrue(form.is_valid())

    def test_search_term_too_long(self):
        form = ExerciseSearchForm(data={"exercise": "x" * 51})
        self.assertFalse(form.is_valid())
        self.assertIn("exercise", form.errors)

    def test_search_term_exactly_50_chars_is_valid(self):
        form = ExerciseSearchForm(data={"exercise": "x" * 50})
        self.assertTrue(form.is_valid())


class GymUserSearchFormTest(TestCase):
    def test_empty_search_is_valid(self):
        form = GymUserSearchForm(data={"gym_user": ""})
        self.assertTrue(form.is_valid())

    def test_valid_search_term(self):
        form = GymUserSearchForm(data={"gym_user": "John"})
        self.assertTrue(form.is_valid())

    def test_search_term_too_long(self):
        form = GymUserSearchForm(data={"gym_user": "x" * 51})
        self.assertFalse(form.is_valid())
        self.assertIn("gym_user", form.errors)

    def test_search_term_exactly_50_chars_is_valid(self):
        form = GymUserSearchForm(data={"gym_user": "x" * 50})
        self.assertTrue(form.is_valid())
