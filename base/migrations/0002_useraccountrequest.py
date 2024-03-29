# Generated by Django 3.2.3 on 2022-07-14 14:39

import base.models.enum
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccountRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('email', models.EmailField(max_length=254)),
                ('type', models.CharField(choices=[(base.models.enum.UserAccountRequestType['CREATION'], 'CREATION'), (base.models.enum.UserAccountRequestType['DELETION'], 'DELETION'), (base.models.enum.UserAccountRequestType['RENEWAL'], 'RENEWAL')], max_length=50)),
            ],
        ),
    ]
