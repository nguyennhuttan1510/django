# Generated by Django 5.1.1 on 2024-10-08 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(blank=True, choices=[('ORDERED', 'ORDERED'), ('COMPLETED', 'COMPLETED'), ('CLOSE', 'CLOSE'), ('PENDING', 'PENDING'), ('CANCEL', 'CANCEL')], default=None, max_length=30, null=True),
        ),
    ]
