# Generated by Django 5.0.6 on 2024-08-28 19:53

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0022_alter_excavation_checked_by_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='antitermitetreatment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='antitermitetreatment',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='created_%(class)s', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='antitermitetreatment',
            name='grade_of_concrete',
            field=models.CharField(default='null', max_length=155),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='antitermitetreatment',
            name='last_updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='antitermitetreatment',
            name='last_updated_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='last_updated_%(class)s', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='antitermitetreatment',
            name='source_of_concrete',
            field=models.CharField(default='null', max_length=155),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='excavation',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_%(class)s', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='excavation',
            name='last_updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='last_updated_%(class)s', to=settings.AUTH_USER_MODEL),
        ),
    ]
