# Generated by Django 3.0.7 on 2020-10-14 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0011_auto_20201015_0330'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Periorty',
            new_name='Priority',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='periorty',
            new_name='priority',
        ),
    ]