from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from .models import Course, Category


class CoursesTests(TestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.create_user(
            username='teacher1', password='StrongPass123', role='teacher'
        )
        self.category = Category.objects.create(name='Programming')

    def test_course_creation_by_teacher(self):
        self.client.login(username='teacher1', password='StrongPass123')
        response = self.client.post(reverse('courses:course_create'), {
            'title': 'Django Basics',
            'description': 'Intro course',
            'category': self.category.id,
            'price': '1000',
            'is_active': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Course.objects.filter(title='Django Basics').exists())

    def test_course_list_view(self):
        Course.objects.create(
            teacher=self.teacher,
            title='Test Course',
            description='Desc',
            category=self.category,
            price=500
        )
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')
