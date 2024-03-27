"""
osis_registration URL Configuration
"""

from django.contrib import admin
from django.urls import path, include

from base.api import url_v1
from base.views import common
from base.views.common import edit_language
from base.views.recover_password import RecoverPasswordFormView, ModifyPasswordFormView
from base.views.registration import RegistrationFormView
from base.views.user_account_creation_status import UserAccountCreationStatusView
from base.views.validate_email import ValidateEmailView

urlpatterns = [
    path('', RegistrationFormView.as_view(), name=RegistrationFormView.name),
    path('home/', RegistrationFormView.as_view(), name=RegistrationFormView.name),
    path('recover_password/', RecoverPasswordFormView.as_view(), name=RecoverPasswordFormView.name),
    path('recover_password/<uprr_uuid>/<token>', ModifyPasswordFormView.as_view(), name=ModifyPasswordFormView.name),
    path('admin/', admin.site.urls),
    path('noscript/', common.noscript, name='noscript'),
    path('captcha/', include('captcha.urls')),
    path('lang/edit/<lang>/', edit_language, name='lang_edit'),
    path('user_account_status/<uacr_uuid>/', UserAccountCreationStatusView.as_view(), name=UserAccountCreationStatusView.name),
    path('validate_email/<uacr_uuid>/<token>', ValidateEmailView.as_view(), name=ValidateEmailView.name),
    path('api/v1/', include(url_v1.urlpatterns)),
]

handler404 = 'base.views.common.page_not_found'
handler403 = 'base.views.common.access_denied'
handler405 = 'base.views.common.method_not_allowed'
handler500 = 'base.views.common.server_error'
