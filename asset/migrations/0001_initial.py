# Generated by Django 5.1.1 on 2024-10-06 10:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.ImageField(upload_to='upload/')),
                ('type', models.TextField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('organization', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to='organization.organization')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='service.service')),
            ],
        ),
    ]
