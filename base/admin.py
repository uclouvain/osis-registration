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
from django import forms
from django.contrib import admin, auth, messages
from django.core.management import call_command
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from base.management.commands.delete_expired_user_account_requests import get_accounts_to_delete
from base.messaging import message_history, message_template
from base.models import user_account_request
from base.models.polling_subscriber import PollingSubscriber, PollingSubscriberAdmin
from base.models.user import OsisRegistrationUserAdmin
from base.models.user_account_request import UserAccountRequest
from base.models.user_password_reset_request import UserPasswordResetRequest, UserPasswordResetRequestAdmin


class DeleteExpiredRequestsForm(forms.Form):
    confirm = forms.BooleanField(
        required=False,
        label=_("Are you sure you want to proceed with the deletion?"),
        widget=forms.HiddenInput(),
        initial=True,
    )

class UserAccountRequestAdmin(user_account_request.UserAccountRequestAdmin):
    change_list_template = 'admin/user_account_request_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('delete_expired/', self.admin_site.admin_view(self.delete_expired_requests_view)),
        ]
        return my_urls + urls

    def delete_expired_requests_view(self, request):
        expired_requests = get_accounts_to_delete()
        emails_to_delete = [req.email for req in expired_requests]

        if request.method == 'POST':
            form = DeleteExpiredRequestsForm(request.POST)
            if form.is_valid() and form.cleaned_data['confirm']:
                try:
                    call_command('delete_expired_user_account_requests', force_delete=True)
                    self.message_user(request, _("The expired requests have been deleted"), level=messages.SUCCESS)
                    return redirect("..")
                except Exception as e:
                    self.message_user(request, mark_safe(e), level=messages.ERROR)
            else:
                self.message_user(request, _("Please confirm deletion"), level=messages.ERROR)
        else:
            form = DeleteExpiredRequestsForm()

        context = dict(
            self.admin_site.each_context(request),
            title=_('Delete expired requests'),
            form=form,
            emails_to_delete=emails_to_delete,
        )
        return render(request, "admin/delete_expired_requests.html", context)


admin.site.register(
    message_history.MessageHistory,
    message_history.MessageHistoryAdmin,
)

admin.site.register(
    message_template.MessageTemplate,
    message_template.MessageTemplateAdmin,
)

admin.site.register(
    PollingSubscriber,
    PollingSubscriberAdmin,
)

admin.site.register(
    UserPasswordResetRequest,
    UserPasswordResetRequestAdmin,
)

# replace user admin with custom admin
User = auth.get_user_model()
admin.site.unregister(User)
admin.site.register(User, OsisRegistrationUserAdmin)
admin.site.register(UserAccountRequest, UserAccountRequestAdmin)
