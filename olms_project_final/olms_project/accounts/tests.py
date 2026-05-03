from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class AccountsTests(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'teststudent',
            'email': 'test@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
            'role': 'student',
        })
        self.assertEqual(response.status_code, 302)  # redirect to login
        self.assertTrue(CustomUser.objects.filter(username='teststudent').exists())

    def test_login(self):
        user = CustomUser.objects.create_user(
            username='testuser', email='u@test.com',
            password='StrongPass123', role='student'
        )
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'StrongPass123',
        })
        self.assertEqual(response.status_code, 302)  # redirect to dashboard
