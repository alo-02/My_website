from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='courses'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Material(models.Model):
    MATERIAL_TYPE_CHOICES = (
        ('pdf', 'PDF'),
        ('video', 'Video'),
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='materials'
    )
    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPE_CHOICES)
    pdf_file = models.FileField(upload_to='materials/pdfs/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_material_type_display()})"
