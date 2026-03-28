from django.test import TestCase

from tracker.models import MuscleGroup


class MuscleGroupTests(TestCase):
    def setUp(self):
        self.muscle_group = MuscleGroup.objects.create(name="Legs")

    def test_str(self):
        self.assertEqual(str(self.muscle_group), "Legs")




