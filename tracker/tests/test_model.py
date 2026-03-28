from django.test import TestCase

from tracker.models import MuscleGroup, GymUser


class MuscleGroupTests(TestCase):
    def setUp(self):
        self.muscle_group = MuscleGroup.objects.create(name="Legs")

    def test_str(self):
        self.assertEqual(str(self.muscle_group), "Legs")


class GymUserTests(TestCase):
    def setUp(self):
        self.gym_user = GymUser.objects.create_user(
            username="Marco_body_builder",
            password="test123",
            first_name="Marco",
            last_name="Doe",
            membership_type="premium"
        )

    def test_str(self):
        self.assertEqual(str(self.gym_user), "Marco Doe")

    def test_default_membership_type(self):
        user = GymUser.objects.create_user(
            username="Joe",
            password="testpass123",
        )
        self.assertEqual(user.membership_type, "free")

    def test_membership_choices(self):
        valid_choices = ["free", "premium", "coach"]
        self.assertIn(self.gym_user.membership_type, valid_choices)

