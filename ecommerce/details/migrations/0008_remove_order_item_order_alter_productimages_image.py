# Generated by Django 5.1.5 on 2025-02-12 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0007_remove_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_item',
            name='order',
        ),
        migrations.AlterField(
            model_name='productimages',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
