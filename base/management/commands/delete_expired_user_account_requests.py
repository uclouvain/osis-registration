import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

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

        # Delete the requests
        deleted_count = requests_to_delete.delete()[0]

        for request in requests_to_delete:
            self.stdout.write(self.style.SUCCESS(
                f'will be deleted: {request.email}'
            ))
