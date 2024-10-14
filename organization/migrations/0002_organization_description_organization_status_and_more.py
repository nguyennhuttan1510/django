# Generated by Django 5.1.1 on 2024-10-07 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=30),
        ),
        migrations.AddField(
            model_name='organization',
            name='type',
            field=models.CharField(blank=True, choices=[('APARTMENT', 'Apartment'), ('VILLA', 'Villa'), ('HOSTEL', 'Hostel'), ('LODGE', 'Lodge'), ('STUDIO', 'Studio'), ('VACATION_HOME', 'Vacation Home'), ('BUNGALOW', 'Bungalow'), ('CHALET', 'Chalet')], max_length=20, null=True),
        ),
    ]