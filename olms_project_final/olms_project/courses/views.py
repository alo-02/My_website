from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .forms import CourseForm, MaterialForm
from .models import Course, Material, Category
from payments.models import Enrollment  # important for is_enrolled check


def course_list_view(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    courses = Course.objects.filter(is_active=True)

    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(teacher__username__icontains=query)
        )

    if category_id:
        courses = courses.filter(category_id=category_id)

    paginator = Paginator(courses.order_by('-created_at'), 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'query': query,
    }
    return render(request, 'courses/course_list.html', context)


@login_required
def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk, is_active=True)
    materials = course.materials.all().order_by('-uploaded_at')

    # check if current user is a paid/enrolled student
    is_enrolled = False
    if request.user.is_authenticated and hasattr(request.user, 'is_student') and request.user.is_student():
        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course,
            status='paid'
        ).exists()

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'materials': materials,
        'is_enrolled': is_enrolled,
    })


@login_required
def teacher_course_list_view(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'courses/teacher_course_list.html', {'courses': courses})


@login_required
def course_create_view(request):
    if not request.user.is_teacher():
        messages.error(request, 'Only teachers can create courses.')
        return redirect('courses:course_list')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, 'Course created successfully.')
            return redirect('courses:teacher_course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Create Course'})


@login_required
def course_update_view(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('courses:teacher_course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Edit Course'})


@login_required
def course_delete_view(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('courses:teacher_course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


@login_required
def material_create_view(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk, teacher=request.user)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            messages.success(request, 'Material uploaded successfully.')
            return redirect('courses:course_detail', pk=course.pk)
    else:
        form = MaterialForm()
    return render(request, 'courses/material_form.html', {
        'form': form,
        'course': course,
        'title': 'Add Material'
    })


@login_required
def material_delete_view(request, pk):
    material = get_object_or_404(Material, pk=pk, course__teacher=request.user)
    course = material.course
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Material deleted successfully.')
        return redirect('courses:course_detail', pk=course.pk)
    return render(request, 'courses/material_confirm_delete.html', {'material': material})
