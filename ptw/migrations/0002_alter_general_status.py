# Generated by Django 5.0.6 on 2024-10-13 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ptw', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='general',
            name='status',
            field=models.CharField(choices=[('submitted', 'Submitted'), ('epc_approved', 'EPC Approved'), ('client_approved', 'Client Approved'), ('client_rejected', 'Client Rejected'), ('closed', 'Closed'), ('auto_closed', 'Auto Closed')], default='submitted', max_length=255),
        ),
    ]
