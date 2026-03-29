from django.test import TestCase

from tracker.forms import MuscleGroupForm


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
