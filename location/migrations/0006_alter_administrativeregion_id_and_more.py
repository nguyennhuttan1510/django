# Generated by Django 4.2.11 on 2024-06-13 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0005_rename_administrativeregions_administrativeregion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrativeregion',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='administrativeunit',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
