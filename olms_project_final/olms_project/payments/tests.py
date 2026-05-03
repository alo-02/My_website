from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from courses.models import Course, Category
from .models import Enrollment, Payment


class PaymentsTests(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(
            username='student1', password='StrongPass123', role='student'
        )
        self.teacher = CustomUser.objects.create_user(
            username='teacher1', password='StrongPass123', role='teacher'
        )
        self.category = Category.objects.create(name='Programming')
        self.course = Course.objects.create(
            teacher=self.teacher,
            title='Paid Course',
            description='Desc',
            category=self.category,
            price=1000
        )

    def test_start_enrollment(self):
        self.client.login(username='student1', password='StrongPass123')
        url = reverse('payments:start_enrollment', args=[self.course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enrollment.objects.filter(student=self.student, course=self.course).exists())

    def test_bkash_checkout_mock(self):
        self.client.login(username='student1', password='StrongPass123')
        start_url = reverse('payments:start_enrollment', args=[self.course.pk])
        self.client.get(start_url)
        enrollment = Enrollment.objects.get(student=self.student, course=self.course)
        checkout_url = reverse('payments:bkash_checkout', args=[enrollment.id])
        response = self.client.post(checkout_url, {
            'bkash_number': '01700000000',
            'transaction_id': 'TRX12345'
        })
        self.assertEqual(response.status_code, 302)
        payment = Payment.objects.get(enrollment=enrollment)
        self.assertTrue(payment.is_successful)
