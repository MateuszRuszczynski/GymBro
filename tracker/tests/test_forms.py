from django.test import TestCase

from tracker.forms import MuscleGroupForm, ExerciseForm, GymUserUpdateForm
from tracker.models import MuscleGroup


class MuscleGroupFormTest(TestCase):
    def test_name_too_short(self):
        form = MuscleGroupForm(
            data={
                "name": "Tr"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_with_valid_data(self):
        form = MuscleGroupForm(
            data={
                "name": "Triceps"
            }
        )
        self.assertTrue(form.is_valid())


class ExerciseFormTest(TestCase):
    def setUp(self):
        self.muscle_group = MuscleGroup.objects.create(
            name="Legs"
        )

    def test_name_too_short(self):
        form = ExerciseForm(
            data={
                "name": "Sq",
                "description": "",
                "difficulty": "intermediate",
                "equipment": "barbell",
                "muscle_group": self.muscle_group.pk
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
                "muscle_group": self.muscle_group.pk
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
                "muscle_group": self.muscle_group.pk
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
                "muscle_group": self.muscle_group.pk
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


