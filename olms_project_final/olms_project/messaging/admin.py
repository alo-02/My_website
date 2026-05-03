from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("course", "student", "teacher", "created_at")
    list_filter = ("course", "created_at")
    search_fields = ("course__title", "student__username", "teacher__username")
    ordering = ("-created_at",)
    list_select_related = ("course", "student", "teacher")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "sender", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("text", "sender__username", "conversation__course__title")
    ordering = ("-created_at",)
    list_select_related = ("conversation", "sender")
