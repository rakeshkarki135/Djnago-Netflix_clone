# Generated by Django 5.0.1 on 2024-01-25 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='forget_password_token',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
