from django.db.models import Q

from .models import Message, Conversation


def unread_counts(request):
    """
    Provides:
      - unread_messages_count: total unread messages for current user
      - unread_conversations_count: number of conversations with >=1 unread msg
    """
    if not request.user.is_authenticated:
        return {"unread_messages_count": 0, "unread_conversations_count": 0}

    user = request.user

    conv_ids = Conversation.objects.filter(Q(student=user) | Q(teacher=user)).values_list("id", flat=True)

    unread_messages_qs = Message.objects.filter(
        conversation_id__in=conv_ids,
        is_read=False,
    ).exclude(sender=user)

    unread_messages_count = unread_messages_qs.count()
    unread_conversations_count = unread_messages_qs.values("conversation_id").distinct().count()

    return {
        "unread_messages_count": unread_messages_count,
        "unread_conversations_count": unread_conversations_count,
    }
