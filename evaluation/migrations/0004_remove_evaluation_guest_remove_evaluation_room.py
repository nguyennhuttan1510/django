# Generated by Django 5.0.2 on 2024-03-13 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0003_evaluation_reservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation',
            name='guest',
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='room',
        ),
    ]
