# Generated by Django 5.1.1 on 2024-10-06 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convenience', '0005_convenience_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='convenience',
            name='code',
            field=models.CharField(blank=True, default=None, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='convenience',
            name='priority',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]