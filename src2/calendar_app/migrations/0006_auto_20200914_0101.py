# Generated by Django 3.0.8 on 2020-09-13 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0005_auto_20200914_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
