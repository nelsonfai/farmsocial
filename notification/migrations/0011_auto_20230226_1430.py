# Generated by Django 3.2.16 on 2023-02-26 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_company_pagefollowers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0010_remove_notification_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='trigger_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trigger_page', to='company.company'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='trigger',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trigger', to=settings.AUTH_USER_MODEL),
        ),
    ]
