# Generated by Django 5.1.5 on 2025-03-14 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0021_order_item_addresses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_item',
            name='addresses',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='details.addresses'),
        ),
    ]
