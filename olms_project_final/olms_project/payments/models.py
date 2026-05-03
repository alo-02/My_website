from django.conf import settings
from django.db import models
from courses.models import Course

User = settings.AUTH_USER_MODEL


class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='enrollments'
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='enrollments'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.course.title} ({self.status})"


class Payment(models.Model):
    METHOD_CHOICES = (
        ('bkash', 'bKash'),
    )
    enrollment = models.OneToOneField(
        Enrollment, on_delete=models.CASCADE, related_name='payment'
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='bkash')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.enrollment} - {self.amount} BDT"


class Invoice(models.Model):
    payment = models.OneToOneField(
        Payment, on_delete=models.CASCADE, related_name='invoice'
    )
    invoice_number = models.CharField(max_length=50, unique=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number
