# Generated by Django 3.0.8 on 2020-11-22 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0012_auto_20201015_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(unique=True),
        ),
    ]
