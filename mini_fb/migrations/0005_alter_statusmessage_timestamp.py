# Generated by Django 5.1.5 on 2025-02-26 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0004_alter_statusmessage_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusmessage',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
