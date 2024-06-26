# Generated by Django 4.2.11 on 2024-05-24 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
        ('asset', '0003_alter_assetmodel_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetmodel',
            name='organization',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to='organization.organization'),
        ),
    ]
