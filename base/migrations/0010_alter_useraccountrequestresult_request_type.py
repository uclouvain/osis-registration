# Generated by Django 3.2.3 on 2021-08-23 12:42

from django.db import migrations, models
import base.models.user_account_creation_request
import base.models.user_account_deletion_request
import base.models.user_account_renewal_request


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20210819_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccountrequestresult',
            name='request_type',
            field=models.CharField(choices=[(base.models.user_account_creation_request.UserAccountCreationRequest, 'CREATION'), (base.models.user_account_deletion_request.UserAccountDeletionRequest, 'DELETION'), (base.models.user_account_renewal_request.UserAccountRenewalRequest, 'RENEWAL')], max_length=50),
        ),
    ]