from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.crypto import get_random_string

from courses.models import Course
from .forms import BkashPaymentForm
from .models import Enrollment, Payment, Invoice


@login_required
def start_enrollment_view(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk, is_active=True)

    if request.user == course.teacher:
        messages.error(request, 'Teachers cannot purchase their own course.')
        return redirect('courses:course_detail', pk=course.pk)

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course,
        defaults={'status': 'pending'}
    )

    if enrollment.status == 'paid':
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('courses:course_detail', pk=course.pk)

    return redirect('payments:bkash_checkout', enrollment_id=enrollment.id)


@login_required
def bkash_checkout_view(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    course = enrollment.course

    try:
        payment = enrollment.payment
    except Payment.DoesNotExist:
        payment = Payment.objects.create(
            enrollment=enrollment,
            amount=course.price,
            method='bkash'
        )

    if request.method == 'POST':
        form = BkashPaymentForm(request.POST)
        if form.is_valid():
            trx_id = form.cleaned_data['transaction_id']
            payment.transaction_id = trx_id
            payment.is_successful = True  # mock success
            payment.save()

            enrollment.status = 'paid'
            enrollment.save()

            invoice_number = f"INV-{get_random_string(8).upper()}"
            Invoice.objects.get_or_create(payment=payment, defaults={
                'invoice_number': invoice_number
            })

            messages.success(request, 'Payment successful! You are now enrolled.')
            return redirect('payments:invoice_detail', payment_id=payment.id)
    else:
        form = BkashPaymentForm()

    return render(request, 'payments/bkash_checkout.html', {
        'form': form,
        'course': course,
        'enrollment': enrollment,
        'payment': payment,
    })


@login_required
def my_enrollments_view(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, 'payments/my_enrollments.html', {'enrollments': enrollments})


@login_required
def invoice_detail_view(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, enrollment__student=request.user)
    invoice = getattr(payment, 'invoice', None)
    return render(request, 'payments/invoice_detail.html', {
        'payment': payment,
        'invoice': invoice,
    })
