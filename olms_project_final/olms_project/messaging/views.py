from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, Q
from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import CustomUser
from courses.models import Course
from payments.models import Enrollment
from .forms import MessageForm
from .models import Conversation, Message


def _flag(user, attr_name: str) -> bool:
    """
    Supports either:
      - user.is_teacher (property/bool), or
      - user.is_teacher() (method)
    """
    val = getattr(user, attr_name, False)
    return val() if callable(val) else bool(val)


def _is_teacher(user) -> bool:
    return _flag(user, "is_teacher")


def _is_student(user) -> bool:
    return _flag(user, "is_student")


@login_required
def inbox_view(request):
    user = request.user

    if _is_teacher(user):
        base_qs = Conversation.objects.filter(teacher=user).select_related("course", "student", "teacher")
    else:
        base_qs = Conversation.objects.filter(student=user).select_related("course", "student", "teacher")

    conversations = (
        base_qs.annotate(
            last_message_at=Max("messages__created_at"),
            unread_count=Count(
                "messages",
                filter=Q(messages__is_read=False) & ~Q(messages__sender=user),
            ),
        )
        .order_by("-last_message_at", "-created_at")
    )

    return render(
        request,
        "messaging/inbox.html",
        {
            "conversations": conversations,
        },
    )


@login_required
def conversation_detail_view(request, course_pk, other_user_pk):
    course = get_object_or_404(Course, pk=course_pk)
    other_user = get_object_or_404(CustomUser, pk=other_user_pk)

    course_teacher = getattr(course, "teacher", None)

    # Student: must be paid-enrolled AND can only message the course teacher
    if _is_student(request.user):
        enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course,
            status="paid",
        ).exists()
        if not enrolled:
            django_messages.error(request, "You must enroll in this course to message the instructor.")
            return redirect("courses:course_detail", pk=course.pk)

        if course_teacher and other_user.pk != course_teacher.pk:
            django_messages.error(request, "You can only message the teacher of this course.")
            return redirect("courses:course_detail", pk=course.pk)

        teacher = course_teacher if course_teacher else other_user
        student = request.user

    # Teacher: must own the course AND can only message paid students of that course
    elif _is_teacher(request.user):
        if course_teacher and request.user.pk != course_teacher.pk:
            django_messages.error(request, "You can only message students of your own course.")
            return redirect("courses:course_detail", pk=course.pk)

        student_is_paid = Enrollment.objects.filter(
            student=other_user,
            course=course,
            status="paid",
        ).exists()
        if not student_is_paid:
            django_messages.error(request, "This student is not enrolled (paid) in this course.")
            return redirect("courses:course_detail", pk=course.pk)

        teacher = request.user
        student = other_user

    else:
        django_messages.error(request, "Messaging is available for teachers and students only.")
        return redirect("accounts:dashboard")

    conversation, _ = Conversation.objects.get_or_create(
        course=course,
        student=student,
        teacher=teacher,
    )

    # Mark messages from other side as read when opening chat
    Message.objects.filter(
        conversation=conversation,
        sender=other_user,
        is_read=False,
    ).update(is_read=True)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender = request.user
            msg.is_read = False
            msg.save()
            return redirect(
                "messaging:conversation_detail",
                course_pk=course.pk,
                other_user_pk=other_user.pk,
            )
    else:
        form = MessageForm()

    messages_qs = conversation.messages.select_related("sender").order_by("created_at")

    return render(
        request,
        "messaging/conversation_detail.html",
        {
            "conversation": conversation,
            "messages": messages_qs,
            "form": form,
            "course": course,
            "other_user": other_user,
        },
    )
