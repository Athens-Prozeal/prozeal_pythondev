# Generated by Django 5.0.6 on 2024-07-20 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_rename_is_admin_user_is_epc_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worksiterole',
            name='role',
            field=models.CharField(choices=[('epc', 'EPC User'), ('client', 'Client User'), ('sub_contractor', 'Sub Contractor')], max_length=50),
        ),
    ]
