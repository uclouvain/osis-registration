# Generated by Django 3.2.3 on 2021-08-09 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osis_registration', '0004_auto_20210809_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('content_txt', models.TextField()),
                ('content_html', models.TextField()),
                ('receiver_person_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('receiver_email', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(editable=False)),
                ('sent', models.DateTimeField(null=True)),
                ('reference', models.CharField(db_index=True, max_length=100, null=True)),
                ('show_to_user', models.BooleanField(default=True)),
                ('read_by_user', models.BooleanField(default=False)),
            ],
        ),
    ]
