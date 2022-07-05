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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.test import TestCase

from base import tasks, settings
from base.tests.factories.user_account_creation_request import UserAccountCreationRequestFactory


class UserAccountCreationTaskTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.pending_requests = [UserAccountCreationRequestFactory(email_validated=True) for _ in range(2)]
        cls.pending_request_unvalidated_email = UserAccountCreationRequestFactory(email_validated=False)
        cls.exceeding_retry_requests = [UserAccountCreationRequestFactory(
            attempt=int(settings.REQUEST_ATTEMPT_LIMIT)+1) for _ in range(2)
        ]
        cls.processed_requests = [UserAccountCreationRequestFactory(success=True, attempt=1) for _ in range(2)]

    def test_task_should_attempt_to_create_user_account_for_pending_requests(self):
        tasks.user_account_creation.run()
        for request in self.pending_requests:
            request.refresh_from_db()
            self.assertEqual(request.attempt, 1)

    def test_task_should_not_attempt_to_create_user_account_for_pending_requests_email_not_validated(self):
        tasks.user_account_creation.run()
        self.pending_request_unvalidated_email.refresh_from_db()
        self.assertEqual(self.pending_request_unvalidated_email.attempt, 0)

    def test_task_should_not_attempt_to_create_user_account_for_exceeding_retry_requests(self):
        tasks.user_account_creation.run()
        for request in self.exceeding_retry_requests:
            request.refresh_from_db()
            self.assertEqual(request.attempt, int(settings.REQUEST_ATTEMPT_LIMIT)+1)

    def test_task_should_not_attempt_to_create_user_account_for_processed_requests(self):
        tasks.user_account_creation.run()
        for request in self.processed_requests:
            request.refresh_from_db()
            self.assertEqual(request.attempt, 1)
