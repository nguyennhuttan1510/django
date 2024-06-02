# Generated by Django 4.2.11 on 2024-05-24 14:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('convenience', '0002_convenience_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='convenience',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='convenience',
            name='parent',
            field=models.IntegerField(null=True),
        ),
    ]
