from django.contrib import admin
from .models import Enrollment, Payment, Invoice


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'created_at')
    list_filter = ('status', 'course')
    search_fields = ('student__username', 'course__title')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'amount', 'method', 'transaction_id', 'is_successful', 'created_at')
    list_filter = ('method', 'is_successful')
    search_fields = ('enrollment__student__username', 'enrollment__course__title', 'transaction_id')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'payment', 'generated_at')
    search_fields = ('invoice_number', 'payment__enrollment__student__username')
