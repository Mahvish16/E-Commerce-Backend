# Generated by Django 5.1.5 on 2025-04-10 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0035_remove_passwordreset_email_passwordreset_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passwordreset',
            name='user',
        ),
        migrations.AddField(
            model_name='passwordreset',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
