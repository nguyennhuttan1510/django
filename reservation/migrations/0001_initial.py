# Generated by Django 5.1.1 on 2024-10-06 10:20

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
        ('service', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('check_in', models.DateTimeField(default=django.utils.timezone.now)),
                ('check_out', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('ORDERED', 'ordered'), ('COMPLETED', 'completed'), ('CLOSE', 'close'), ('PENDING', 'pending'), ('CANCEL', 'cancel')], default='ORDERED', max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('pin_code', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_by', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='organization.organization')),
                ('services', models.ManyToManyField(related_name='reservations', related_query_name='reservation', to='service.service')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
