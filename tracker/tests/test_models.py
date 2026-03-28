from django.test import TestCase

from tracker.models import MuscleGroup, GymUser, Exercise, WorkoutPlan


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


class ExerciseTests(TestCase):
    def setUp(self):
        self.muscle_group = MuscleGroup.objects.create(name="Biceps")
        self.exercise = Exercise.objects.create(
            name="Leg press",
            description="One of the best exercise for legs",
            difficulty="intermediate",
            equipment="barbell",
            muscle_group=self.muscle_group,
        )

    def test_str(self):
        self.assertEqual(str(self.exercise), "Leg press")

    def test_muscle_group_relationship(self):
        self.assertEqual(str(self.muscle_group.name), "Biceps")

    def test_difficulty_choices(self):
        valid_choices = ["beginner", "intermediate", "advanced"]
        self.assertIn(self.exercise.difficulty, valid_choices)


class WorkoutPlanModelTest(TestCase):
    def setUp(self):
        self.user = GymUser.objects.create_user(
            username="Willy",
            password="testpass123",
        )
        self.muscle_group = MuscleGroup.objects.create(name="Legs")
        self.exercise = Exercise.objects.create(
            name="Squat",
            difficulty="intermediate",
            equipment="Barbell",
            muscle_group=self.muscle_group,
        )
        self.plan = WorkoutPlan.objects.create(
            name="Leg Day",
            goal="strength",
            created_by=self.user,
        )
        self.plan.exercises.add(self.exercise)

    def test_str(self):
        self.assertEqual(str(self.plan), "Leg Day")

    def test_exercises_relationship(self):
        self.assertIn(self.exercise, self.plan.exercises.all())

    def test_created_by_relationship(self):
        self.assertEqual(self.plan.created_by.username, "Willy")
