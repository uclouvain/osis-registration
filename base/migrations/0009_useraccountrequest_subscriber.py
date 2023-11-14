# Generated by Django 3.2.3 on 2022-08-22 09:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_pollingsubscriber_redirection_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccountrequest',
            name='subscriber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.pollingsubscriber'),
        ),
    ]
