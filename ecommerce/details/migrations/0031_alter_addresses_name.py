# Generated by Django 5.1.5 on 2025-04-02 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0030_alter_addresses_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresses',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
