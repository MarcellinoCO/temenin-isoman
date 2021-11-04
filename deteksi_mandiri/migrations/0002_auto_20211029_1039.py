# Generated by Django 3.2.8 on 2021-10-29 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deteksi_mandiri', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='required_score_to_pass',
            field=models.IntegerField(help_text='Required score to pass the test'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='time',
            field=models.IntegerField(help_text='Duration of the Quiz in minutes'),
        ),
    ]
