# Generated by Django 3.0.8 on 2020-09-14 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0006_auto_20200914_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
