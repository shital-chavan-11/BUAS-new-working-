# Generated by Django 5.1.2 on 2024-10-14 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_otp_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='otp_expires_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
