from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from courses.views import course_list_view  # import


urlpatterns = [
    path('', course_list_view, name='home'),  # root shows course list

    path('admin/', admin.site.urls),

    path('', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),
    path('messages/', include(('messaging.urls', 'messaging'), namespace='messaging')),
    path('payments/', include(('payments.urls', 'payments'), namespace='payments')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
