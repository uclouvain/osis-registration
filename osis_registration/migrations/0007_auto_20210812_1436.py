# Generated by Django 3.2.3 on 2021-08-12 14:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('osis_registration', '0006_useraccountcreationrequest_email_validated'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccountcreationrequest',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='useraccountdeletionrequest',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='useraccountrenewalrequest',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='useraccountrequestresult',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
