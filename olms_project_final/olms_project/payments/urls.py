from django.urls import path
from .views import (
    start_enrollment_view,
    bkash_checkout_view,
    my_enrollments_view,
    invoice_detail_view,
)

app_name = 'payments'

urlpatterns = [
    path('enroll/<int:course_pk>/', start_enrollment_view, name='start_enrollment'),
    path('bkash/<int:enrollment_id>/', bkash_checkout_view, name='bkash_checkout'),
    path('my-courses/', my_enrollments_view, name='my_enrollments'),
    path('invoice/<int:payment_id>/', invoice_detail_view, name='invoice_detail'),
]
