# Generated by Django 3.2 on 2023-08-24 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gmaps', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterModelTable(
            name='user',
            table='gmaps_user',
        ),
    ]