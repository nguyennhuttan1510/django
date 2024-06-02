# Generated by Django 4.2.11 on 2024-05-24 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
        ('service', '0001_initial'),
        ('asset', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetmodel',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.organization'),
        ),
        migrations.AlterField(
            model_name='assetmodel',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='service.service'),
        ),
    ]
