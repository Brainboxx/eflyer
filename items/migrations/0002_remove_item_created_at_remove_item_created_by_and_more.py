# Generated by Django 4.1.6 on 2023-04-25 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='item',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='item',
            name='is_sold',
        ),
    ]
