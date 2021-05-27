"""
osis_registration URL Configuration
"""

from django.contrib import admin
from django.urls import path

from osis_registration.views import common
from osis_registration.views.registration import RegistrationView

urlpatterns = [
    path('', RegistrationView.as_view(), name=RegistrationView.name),
    path('home/', RegistrationView.as_view(), name=RegistrationView.name),
    path('admin/', admin.site.urls),
    path('noscript/', common.noscript, name='noscript'),
]
