"""
osis_registration URL Configuration
"""

from django.contrib import admin
from django.urls import path, include

from osis_registration.views import common
from osis_registration.views.common import edit_language
from osis_registration.views.registration import RegistrationFormView, UserAccountCreationRequestedView, ValidateEmailView

urlpatterns = [
    path('', RegistrationFormView.as_view(), name=RegistrationFormView.name),
    path('home/', RegistrationFormView.as_view(), name=RegistrationFormView.name),
    path('admin/', admin.site.urls),
    path('noscript/', common.noscript, name='noscript'),
    path('captcha/', include('captcha.urls')),
    path('lang/edit/<lang>/', edit_language, name='lang_edit'),
    path('user_account_creation_requested/', UserAccountCreationRequestedView.as_view(), name=UserAccountCreationRequestedView.name),
    path('validate_email/<uacr_uuid>/<token>', ValidateEmailView.as_view(), name='validate_email'),
]
