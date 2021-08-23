"""
osis_registration URL Configuration
"""

from django.contrib import admin
from django.urls import path, include

from osis_registration.api import url_v1
from osis_registration.api.views.check_account_creation_request import UserAccountCreationCheck
from osis_registration.views import common
from osis_registration.views.common import edit_language
from osis_registration.views.registration import RegistrationFormView, UserAccountCreationRequestedView, \
    ValidateEmailView

urlpatterns = [
    path('', RegistrationFormView.as_view(), name=RegistrationFormView.name),
    path('home/', RegistrationFormView.as_view(), name=RegistrationFormView.name),
    path('admin/', admin.site.urls),
    path('noscript/', common.noscript, name='noscript'),
    path('captcha/', include('captcha.urls')),
    path('lang/edit/<lang>/', edit_language, name='lang_edit'),
    path('user_account_creation_requested/', UserAccountCreationRequestedView.as_view(), name=UserAccountCreationRequestedView.name),
    path('validate_email/<uacr_uuid>/<token>', ValidateEmailView.as_view(), name=ValidateEmailView.name),
    path('ajax/user_account_creation_check/<uacr_uuid>/', UserAccountCreationCheck.as_view(), name=UserAccountCreationCheck.name),
    path('api/v1/', include(url_v1.urlpatterns)),
]
