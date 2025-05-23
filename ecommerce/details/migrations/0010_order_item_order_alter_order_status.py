# Generated by Django 5.1.5 on 2025-02-13 11:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0009_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_item',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='details.order'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('delivered', 'delivered'), ('shipped', 'shipped'), ('pending', 'pending')], max_length=20),
        ),
    ]
