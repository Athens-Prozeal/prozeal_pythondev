# Generated by Django 5.0.6 on 2024-10-21 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ptw', '0008_rename_approved_by_signature_general_verified_by_signature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='general',
            name='submitted_by_signature',
            field=models.ImageField(default='null', upload_to='ptw/signatures/'),
            preserve_default=False,
        ),
    ]
