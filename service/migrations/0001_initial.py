# Generated by Django 5.1.1 on 2024-10-06 10:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('convenience', '0006_convenience_code_convenience_priority'),
        ('location', '0001_initial'),
        ('organization', '0001_initial'),
        ('promotion', '0001_initial'),
        ('resource', '0003_publicdocument'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('capacity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('type', models.CharField(blank=True, choices=[('APARTMENT', 'Apartment'), ('VILLA', 'Villa'), ('HOSTEL', 'Hostel'), ('LODGE', 'Lodge'), ('STUDIO', 'Studio'), ('VACATION_HOME', 'Vacation Home'), ('BUNGALOW', 'Bungalow'), ('CHALET', 'Chalet')], max_length=20, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=30)),
                ('rate', models.FloatField(blank=True, default=0, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to='location.location')),
                ('organization', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to='organization.organization')),
                ('promotions', models.ManyToManyField(blank=True, null=True, to='promotion.promotion')),
                ('resource', models.ManyToManyField(blank=True, null=True, to='resource.privatedocument')),
            ],
        ),
        migrations.CreateModel(
            name='ServicesAssets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convenience.convenience')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.service')),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='conveniences',
            field=models.ManyToManyField(blank=True, null=True, through='service.ServicesAssets', to='convenience.convenience'),
        ),
    ]
