# Generated by Django 4.2.11 on 2024-06-13 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_remove_location_postal_code_alter_location_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativeRegions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('name_en', models.CharField(max_length=50)),
                ('code_name', models.CharField(max_length=50)),
                ('code_name_en', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AdministrativeUnits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=80)),
                ('full_name_en', models.CharField(max_length=80)),
                ('short_name', models.CharField(max_length=50)),
                ('short_name_en', models.CharField(max_length=50)),
                ('code_name', models.CharField(max_length=80)),
                ('code_name_en', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Provinces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=50)),
                ('name_en', models.CharField(max_length=50, null=True)),
                ('full_name', models.CharField(max_length=100)),
                ('full_name_en', models.CharField(max_length=100, null=True)),
                ('code_name', models.CharField(max_length=50, null=True)),
                ('administrative_region', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.administrativeregions')),
                ('administrative_unit', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.administrativeunits')),
            ],
        ),
        migrations.RenameField(
            model_name='district',
            old_name='district_name',
            new_name='full_name',
        ),
        migrations.RenameField(
            model_name='ward',
            old_name='ward_name',
            new_name='full_name',
        ),
        migrations.RemoveField(
            model_name='location',
            name='city',
        ),
        migrations.RemoveField(
            model_name='location',
            name='location_name',
        ),
        migrations.AddField(
            model_name='district',
            name='code_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='district',
            name='full_name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='district',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='district',
            name='name_en',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ward',
            name='code_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ward',
            name='district_code',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.district'),
        ),
        migrations.AddField(
            model_name='ward',
            name='full_name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ward',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='ward',
            name='name_en',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='district',
            name='code',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='ward',
            name='code',
            field=models.CharField(max_length=3),
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.AddField(
            model_name='district',
            name='administrative_unit',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.administrativeunits'),
        ),
        migrations.AddField(
            model_name='district',
            name='province_code',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.provinces'),
        ),
        migrations.AddField(
            model_name='location',
            name='province',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='location.provinces'),
        ),
        migrations.AddField(
            model_name='ward',
            name='administrative_unit',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.administrativeunits'),
        ),
    ]
