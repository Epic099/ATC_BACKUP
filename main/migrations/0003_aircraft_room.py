# Generated by Django 3.2.21 on 2023-09-29 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20230929_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='aircraft',
            name='room',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.room'),
        ),
    ]
