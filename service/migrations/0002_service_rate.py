# Generated by Django 4.2.11 on 2024-05-30 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='rate',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5),
        ),
    ]