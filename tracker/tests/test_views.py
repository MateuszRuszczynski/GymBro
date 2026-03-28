from django.test import TestCase
from django.urls import reverse


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
