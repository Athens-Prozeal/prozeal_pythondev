# Generated by Django 5.0.6 on 2024-10-12 15:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0029_alter_correctiveactionuser_work_site'),
        ('inspection', '0059_rename_data_earthingsystem_earth_tester_details_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HTCablePreComm',
            new_name='HTCablePreCom',
        ),
    ]
