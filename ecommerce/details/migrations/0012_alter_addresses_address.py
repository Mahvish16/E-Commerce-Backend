# Generated by Django 5.1.5 on 2025-02-14 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0011_remove_registeruser_address_addresses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresses',
            name='address',
            field=models.TextField(max_length=600),
        ),
    ]
