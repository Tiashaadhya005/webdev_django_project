# Generated by Django 3.2.7 on 2021-09-08 08:12

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('busbookreg', '0002_auto_20210908_0751'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='bus_booking',
            managers=[
                ('Bus_book_tool', django.db.models.manager.Manager()),
            ],
        ),
    ]
