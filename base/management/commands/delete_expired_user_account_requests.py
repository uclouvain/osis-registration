import datetime
import requests
import os

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from base.models.enum import UserAccountRequestType
from base.models.user_account_request import UserAccountRequest


class Command(BaseCommand):
    help = 'Deletes user account creation requests that are expired and unvalidated'

    def handle(self, *args, **options):
        # Calculate the time threshold (24 hours ago)
        time_threshold = timezone.now() - datetime.timedelta(hours=24)

        # Query for requests that match the criteria
        requests_to_delete = UserAccountRequest.objects.filter(
            type=UserAccountRequestType.CREATION.value,
            email_validated=False,
            updated_at__lte=time_threshold
        )

        deleted_count = 0
        for request in requests_to_delete:
            try:
                # Call the delete_account API
                api_url = os.path.join(settings.APPLICATION_URL, 'api/v1/delete_account/')
                data = {'email': request.email}
                response = requests.post(api_url, data=data)

                if response.status_code == 201:  # Assuming 201 Created is the success status
                    # Delete the request if the API call was successful
                    request.delete()
                    deleted_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully deleted account for email: {request.email}'
                    ))
                else:
                    self.stdout.write(self.style.ERROR(
                        f'Failed to delete account for email: {request.email}. API returned status code: {response.status_code}'
                    ))

            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(
                    f'Failed to delete account for email: {request.email}. An error occurred: {e}'
                ))

        self.stdout.write(self.style.SUCCESS(
            f'Successfully deleted {deleted_count} expired user account creation requests'
        ))
