# Generated by Django 3.2.3 on 2022-08-22 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_useraccountrequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollingsubscriber',
            name='redirection_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
