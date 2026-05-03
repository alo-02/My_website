from django.urls import path
from .views import inbox_view, conversation_detail_view

app_name = "messaging"

urlpatterns = [
    path("inbox/", inbox_view, name="inbox"),
    path(
        "course/<int:course_pk>/user/<int:other_user_pk>/",
        conversation_detail_view,
        name="conversation_detail",
    ),
]
