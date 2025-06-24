import datetime
import os

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from base.models.enum import UserAccountRequestType, UserAccountRequestStatus
from base.models.user_account_request import UserAccountRequest
from base.services.service_exceptions import RetrieveUserAccountInformationErrorException


class Command(BaseCommand):
    help = 'Deletes user account creation requests that are expired and unvalidated'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force_delete',
            action='store_true',
            help='Force deletion without confirmation',
        )

    def handle(self, *args, **options):
        force_delete = options['force_delete']
        requests_to_delete = get_accounts_to_delete()

        if requests_to_delete:
            self.stdout.write(f"Found {len(requests_to_delete)} expired user account creation requests:")
            for request in requests_to_delete:
                self.stdout.write(f"  - {request.email}")
            if force_delete:
                confirmation = 'yes'
            else:
                self.stdout.write("Do you want to delete them? (yes/no)")
                confirmation = input().lower()
            if confirmation != 'yes':
                self.stdout.write("Deletion cancelled.")
                return

        deleted_count = 0
        errors = []
        for request in requests_to_delete:
            try:
                # Call the delete_account API
                api_url = os.path.join(settings.APPLICATION_URL, 'api/v1/delete_account/')
                data = {'email': request.email}
                headers = {'Authorization': f"Token {settings.APPLICATION_TOKEN}"}
                response = requests.delete(api_url, data=data, headers=headers)
                if response.status_code == 200:
                    deleted_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully deleted account for email: {request.email}'
                    ))
                else:

                    # limit response text to 500 chars
                    error_message = response.text[:500] + ('...' if len(response.text) > 500 else '')

                    self.stdout.write(self.style.ERROR(
                        f'Failed to delete account for email: {request.email}. API returned status code: {response.status_code} \n'
                        f'Detailed error message: {error_message}'
                    ))
                    errors += [error_message]

            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(
                    f'Failed to delete account for email: {request.email}. An error occurred: {e}'
                ))
                self.stderr.write(f"Error during deletion: {e}")

            except RetrieveUserAccountInformationErrorException as e:
                self.stdout.write(self.style.ERROR(
                    f'Failed to retrieve account for email: {request.email}. An error occurred: {e}'
                ))

        if requests_to_delete and deleted_count > 0:
            self.stdout.write(self.style.SUCCESS(
                f'Successfully deleted {deleted_count} expired user account creation requests'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                'No expired user account creation requests found or there were some errors during deletion.'
            ))

        if errors:
            raise Exception('<br/>'.join(errors))

def get_accounts_to_delete():
    # Calculate the time threshold (24 hours ago)
    time_threshold = timezone.now() - datetime.timedelta(hours=24)
    # Query for requests that match the criteria
    requests_to_delete = UserAccountRequest.objects.filter(
        type=UserAccountRequestType.CREATION.value,
        status=UserAccountRequestStatus.PENDING.value,
        email_validated=False,
        updated_at__lte=time_threshold
    )
    requests_to_delete = [request for request in requests_to_delete]
    return requests_to_delete
