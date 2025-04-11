# Generated by Django 5.0.7 on 2025-01-29 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('delivered', 'delivered'), ('shipped', 'shipped'), ('pending', 'pending')], max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'cash')], max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('cancelled', 'cancelled'), ('completed', 'completed')], max_length=50),
        ),
    ]
