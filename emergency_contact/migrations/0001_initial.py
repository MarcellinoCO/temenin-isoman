# Generated by Django 3.2.8 on 2021-11-05 06:10

from django.db import migrations, models
import django.db.models.deletion
import emergency_contact.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Daerah',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daerah', models.CharField(default='', max_length=15, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RumahSakit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=40, unique=True)),
                ('alamat', models.CharField(max_length=60)),
                ('telepon', models.CharField(max_length=25, validators=[emergency_contact.models.validate_telepon])),
                ('daerah', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='emergency_contact.daerah')),
            ],
        ),
    ]
