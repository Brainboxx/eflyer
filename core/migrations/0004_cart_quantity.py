# Generated by Django 4.1.6 on 2023-04-30 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
