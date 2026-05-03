from django.urls import path
from .views import (
    course_list_view,
    course_detail_view,
    teacher_course_list_view,
    course_create_view,
    course_update_view,
    course_delete_view,
    material_create_view,
    material_delete_view,
)

app_name = 'courses'

urlpatterns = [
    path('', course_list_view, name='course_list'),
    path('<int:pk>/', course_detail_view, name='course_detail'),

    path('teacher/', teacher_course_list_view, name='teacher_course_list'),
    path('teacher/create/', course_create_view, name='course_create'),
    path('teacher/<int:pk>/edit/', course_update_view, name='course_edit'),
    path('teacher/<int:pk>/delete/', course_delete_view, name='course_delete'),

    path('<int:course_pk>/materials/add/', material_create_view, name='material_add'),
    path('materials/<int:pk>/delete/', material_delete_view, name='material_delete'),
]
