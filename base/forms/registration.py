##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2021 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
import datetime

from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django.contrib.auth.password_validation import MinimumLengthValidator, UserAttributeSimilarityValidator, \
    NumericPasswordValidator
from django.forms import SelectDateWidget
from django.utils.translation import gettext_lazy as _

from base.admin import User

CURRENT_YEAR = datetime.date.today().year


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = "captcha.html"


class EmptySelectDateWidgetField(forms.DateField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.is_required = False


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label=_('First name'), max_length=100, required=True)
    last_name = forms.CharField(label=_('Last name'), max_length=100, required=True)
    email = forms.EmailField(label=_('Email'), max_length=100, required=True)

    password = forms.CharField(
        label=_('Password'),
        max_length=100,
        required=True,
        widget=forms.PasswordInput(),
        validators=[
            MinimumLengthValidator().validate,
            NumericPasswordValidator().validate
        ]
    )

    birth_date = EmptySelectDateWidgetField(
        label=_('Date of birth'),
        required=True,
        widget=SelectDateWidget(
            years=range(CURRENT_YEAR-100, CURRENT_YEAR+1),
            empty_label=(_('Year'), _('Month'), _('Day')),
        ),
    )
    captcha = CaptchaField(
        widget=CustomCaptchaTextInput(),
    )

    def clean_password(self):
        password = self.cleaned_data['password']

        user_info = User(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )

        UserAttributeSimilarityValidator().validate(password=password, user=user_info)

        return password
