"""
osis_registration URL Configuration
"""

from django.contrib import admin
from django.urls import path, include

from osis_registration.views import common
from osis_registration.views.common import edit_language
from osis_registration.views.registration import RegistrationFormView, RegistrationSuccessView, ValidateEmailView

urlpatterns = [
    path('', RegistrationFormView.as_view(), name=RegistrationFormView.name),
    path('home/', RegistrationFormView.as_view(), name=RegistrationFormView.name),
    path('admin/', admin.site.urls),
    path('noscript/', common.noscript, name='noscript'),
    path('captcha/', include('captcha.urls')),
    path('lang/edit/<lang>/', edit_language, name='lang_edit'),
    path('registration_success/', RegistrationSuccessView.as_view(), name=RegistrationSuccessView.name),
    path('validate_email/<email>/<token>', ValidateEmailView.as_view(), name='validate_email'),
]
