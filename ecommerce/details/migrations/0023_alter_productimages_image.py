# Generated by Django 5.1.5 on 2025-03-21 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0022_alter_order_item_addresses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimages',
            name='image',
            field=models.ImageField(null=True, upload_to='media/'),
        ),
    ]
