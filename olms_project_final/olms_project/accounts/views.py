from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import UserRegisterForm, UserLoginForm, ProfileUpdateForm
from .models import CustomUser

from courses.models import Course
from payments.models import Enrollment


def _flag(user, attr_name: str) -> bool:
    """
    Supports either:
      - user.is_teacher (property/bool), or
      - user.is_teacher() (method)
    """
    val = getattr(user, attr_name, False)
    return val() if callable(val) else bool(val)


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("accounts:login")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse_lazy("accounts:dashboard")


@login_required
def dashboard_view(request):
    user = request.user
    context = {"user": user}

    if _flag(user, "is_teacher"):
        courses = (
            Course.objects.filter(teacher=user)
            .prefetch_related("materials")  # reverse FK => prefetch_related
        )
        context.update(
            {
                "courses": courses,
            }
        )

    elif _flag(user, "is_student"):
        enrollments = (
            Enrollment.objects.filter(student=user, status="paid")
            .select_related("course", "course__teacher")
        )
        context.update(
            {
                "enrollments": enrollments,
                "available_courses": Course.objects.filter(is_active=True).select_related("teacher")[:6],
            }
        )

    elif user.is_superuser:
        context.update(
            {
                "total_users": CustomUser.objects.count(),
                "total_courses": Course.objects.count(),
                "total_enrollments": Enrollment.objects.count(),
            }
        )

    return render(request, "accounts/dashboard.html", context)


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"user": request.user})


@login_required
def profile_update_view(request):
    user = request.user
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, "accounts/profile_edit.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")
