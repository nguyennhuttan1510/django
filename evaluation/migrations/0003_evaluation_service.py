# Generated by Django 4.2.11 on 2024-05-31 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_service_rate'),
        ('evaluation', '0002_remove_evaluation_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='service',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='service.service'),
        ),
    ]
