# Generated by Django 5.0.6 on 2024-10-21 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptw', '0010_general_rejected_by_general_rejected_remark'),
    ]

    operations = [
        migrations.RenameField(
            model_name='general',
            old_name='accepted_by',
            new_name='approved_by',
        ),
        migrations.RenameField(
            model_name='general',
            old_name='accepted_by_signature',
            new_name='approved_by_signature',
        ),
        migrations.RenameField(
            model_name='general',
            old_name='accepted_datetime',
            new_name='approved_datetime',
        ),
    ]
