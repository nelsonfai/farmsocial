# Generated by Django 3.2.16 on 2023-01-22 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='profile',
        ),
    ]
