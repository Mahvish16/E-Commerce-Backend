# Generated by Django 5.1.5 on 2025-01-31 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0003_alter_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
