from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tracker.models import MuscleGroup, Exercise, GymUser, WorkoutPlan, WorkoutLog


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
        response = self.client.get(reverse("tracker:exercise-detail", kwargs={"pk": self.exercise.pk}))
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
            reverse("tracker:exercise-update", kwargs={"pk": self.exercise.pk}),
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
            reverse("tracker:exercise-delete", kwargs={"pk": self.exercise.pk}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Exercise.objects.filter(pk=self.exercise.pk).exists())


class WorkoutLogViewTest(TestCase):
    def setUp(self):
        self.user = GymUser.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.login(username="testuser", password="testpass123")
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
        self.plan.exercises.add(self.exercise)
        self.log = WorkoutLog.objects.create(
            user=self.user,
            workout_plan=self.plan,
            date=date.today(),
            duration_minutes=60,
            notes="Great session!",
            is_personal_record=False,
        )

    def test_workout_log_list_view(self):
        response = self.client.get(reverse("tracker:workout-log-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/workoutlog_list.html")
        self.assertContains(response, self.plan.name)

    def test_list_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("tracker:workout-log-list"))
        self.assertEqual(response.status_code, 302)

    def test_detail_view(self):
        response = self.client.get(reverse("tracker:workout-log-detail", kwargs={"pk": self.log.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/workoutlog_detail.html")
        self.assertContains(response, self.log.notes)

    def test_create_redirects_to_list(self):
        response = self.client.post(
            reverse("tracker:workout-log-create"),
            {
                "workout_plan": self.plan.pk,
                "date": date.today().strftime("%Y-%m-%d"),
                "duration_minutes": 30,
                "notes": "Short session.",
                "is_personal_record": False,
            }
        )
        self.assertRedirects(response, reverse("tracker:workout-log-list"))

    def test_update_changes_duration(self):
        response = self.client.post(
            reverse("tracker:workout-log-update", kwargs={"pk": self.log.pk}),
            {
                "workout_plan": self.plan.pk,
                "date": date.today().strftime("%Y-%m-%d"),
                "duration_minutes": 90,
                "notes": "Great session!",
                "is_personal_record": False,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.log.refresh_from_db()
        self.assertEqual(self.log.duration_minutes, 90)

    def test_delete_removes_log(self):
        response = self.client.post(
            reverse("tracker:workout-log-delete", kwargs={"pk": self.log.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(WorkoutLog.objects.filter(pk=self.log.pk).exists())

    def test_personal_record_flag(self):
        pr_log = WorkoutLog.objects.create(
            user=self.user,
            workout_plan=self.plan,
            date=date.today(),
            duration_minutes=75,
            is_personal_record=True,
        )
        response = self.client.get(
            reverse("tracker:workout-log-detail", kwargs={"pk": pr_log.pk})
        )
        self.assertContains(response, "PR")
