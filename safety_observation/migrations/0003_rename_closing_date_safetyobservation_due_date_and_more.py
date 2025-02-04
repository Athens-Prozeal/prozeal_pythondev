# Generated by Django 5.0.6 on 2024-09-05 10:13

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safety_observation', '0002_safetyobservation_safety_observation_found'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='safetyobservation',
            old_name='closing_date',
            new_name='due_date',
        ),
        migrations.AddField(
            model_name='safetyobservation',
            name='created_under',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='safety_observations', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='safetyobservation',
            name='observation_status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('expired', 'Expired')], max_length=155),
        ),
    ]
