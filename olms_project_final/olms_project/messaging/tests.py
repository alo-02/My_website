from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from courses.models import Course, Category
from payments.models import Enrollment
from .models import Conversation, Message


class MessagingTests(TestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.create_user(
            username='teacher1', password='StrongPass123', role='teacher'
        )
        self.student = CustomUser.objects.create_user(
            username='student1', password='StrongPass123', role='student'
        )
        self.category = Category.objects.create(name='Programming')
        self.course = Course.objects.create(
            teacher=self.teacher,
            title='Chat Course',
            description='Desc',
            category=self.category,
            price=0
        )
        Enrollment.objects.create(
            student=self.student, course=self.course, status='paid'
        )

    def test_student_can_start_conversation(self):
        self.client.login(username='student1', password='StrongPass123')
        url = reverse('messaging:conversation_detail', args=[self.course.pk, self.teacher.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Conversation.objects.filter(course=self.course, student=self.student).exists())

    def test_send_message(self):
        self.client.login(username='student1', password='StrongPass123')
        url = reverse('messaging:conversation_detail', args=[self.course.pk, self.teacher.pk])
        self.client.get(url)  # ensure conversation exists
        response = self.client.post(url, {'text': 'Hello teacher'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Message.objects.filter(text='Hello teacher').exists())
