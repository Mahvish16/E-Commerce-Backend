# Generated by Django 5.1.5 on 2025-04-01 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0028_alter_productimages_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresses',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
