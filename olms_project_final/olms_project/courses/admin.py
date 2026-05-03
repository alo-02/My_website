from django.contrib import admin
from .models import Category, Course, Material


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'category', 'price', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description', 'teacher__username')
    autocomplete_fields = ('teacher', 'category')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'material_type', 'uploaded_at')
    list_filter = ('material_type', 'course')
    search_fields = ('title', 'course__title')
