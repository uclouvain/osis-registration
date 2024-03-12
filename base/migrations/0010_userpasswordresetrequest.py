# Generated by Django 3.2.3 on 2024-03-07 17:07

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_useraccountrequest_subscriber'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPasswordResetRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('email', models.EmailField(max_length=254)),
                ('status', models.CharField(choices=[('SUCCESS', 'SUCCESS'), ('ERROR', 'ERROR'), ('PENDING', 'PENDING')], default='PENDING', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subscriber', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.pollingsubscriber')),
            ],
        ),
    ]
