# Generated by Django 3.2.16 on 2023-02-23 14:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0002_auto_20230223_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='pagefollowers',
            field=models.ManyToManyField(blank=True, null=True, related_name='pagefollowers', to=settings.AUTH_USER_MODEL),
        ),
    ]
