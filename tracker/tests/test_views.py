from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tracker.models import MuscleGroup, Exercise, GymUser


class PublicAccessTest(TestCase):
    def test_login_page_accessible(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_register_page_accessible(self):
        response = self.client.get(reverse("tracker:register"))
        self.assertEqual(response.status_code, 200)

    def test_exercise_list_redirects_if_not_logged_in(self):
        response = self.client.get(reverse("tracker:exercise-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/exercises/"
        )


class ExerciseViewTest(TestCase):
    def setUp(self):
        self.user = GymUser.objects.create_user(
            username="Andrew",
            password="test123"
        )
        self.client.login(username="Andrew", password="test123")
        self.muscle_group = MuscleGroup.objects.create(name="Chest")
        self.exercise = Exercise.objects.create(
            name="Bench press",
            description="Basic chest exercise",
            difficulty="intermediate",
            equipment="Barbell",
            muscle_group=self.muscle_group
        )

    def test_exercise_list_view(self):
        response = self.client.get(reverse("tracker:exercise-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/exercise_list.html")
        self.assertContains(response, self.exercise.name)

    def test_exercise_detail_view(self):
        response = self.client.get(reverse("tracker:exercise-detail", args=(self.exercise.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/exercise_detail.html")
        self.assertContains(response, self.exercise.name)

    def test_exercise_create_view_get(self):
        response = self.client.get(reverse("tracker:exercise-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/exercise_form.html")

    def test_exercise_create_view_post(self):
        response = self.client.post(
            reverse("tracker:exercise-create"),
            {
                "name": "Pull up",
                "description": "Bodyweight back exercise",
                "difficulty": "intermediate",
                "equipment": "Pull-up bar",
                "muscle_group": self.muscle_group.pk,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Exercise.objects.filter(name="Pull up").exists())

    def test_exercise_update_view(self):
        response = self.client.post(
            reverse("tracker:exercise-update", args=(self.exercise.pk,)),
            {
                "name": "Pull up updated",
                "description": "Bodyweight back exercise",
                "difficulty": "advanced",
                "equipment": "Pull-up bar",
                "muscle_group": self.muscle_group.pk,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.exercise.refresh_from_db()
        self.assertEqual(self.exercise.name, "Pull up updated")

    def exercise_delete_view(self):
        response = self.client.post(
            reverse("tracker:exercise-delete", args=(self.exercise.pk,)),
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Exercise.objects.filter(pk=self.exercise.pk).exists())
