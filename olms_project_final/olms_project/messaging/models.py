from django.conf import settings
from django.db import models
from courses.models import Course

User = settings.AUTH_USER_MODEL


class Conversation(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="conversations"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="student_conversations"
    )
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="teacher_conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("course", "student", "teacher")
        indexes = [
            models.Index(fields=["course", "student", "teacher"]),
        ]

    def __str__(self):
        return f"{self.course.title} - {self.student} & {self.teacher}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["conversation", "created_at"]),
            models.Index(fields=["is_read"]),
        ]

    def __str__(self):
        return f"From {self.sender} at {self.created_at}"
