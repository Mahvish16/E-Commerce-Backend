# Generated by Django 5.1.5 on 2025-02-13 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0008_remove_order_item_order_alter_productimages_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('delivered', 'delivered'), ('shipped', 'shipped'), ('pending', 'pending')], default='pending', max_length=20),
        ),
    ]
