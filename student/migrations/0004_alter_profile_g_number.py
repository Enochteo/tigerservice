# Generated by Django 5.0.7 on 2025-03-17 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_profile_g_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='g_number',
            field=models.CharField(max_length=9),
        ),
    ]
