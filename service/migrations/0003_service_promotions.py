# Generated by Django 4.2.11 on 2024-05-31 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0001_initial'),
        ('service', '0002_service_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='promotions',
            field=models.ManyToManyField(to='promotion.promotion'),
        ),
    ]
