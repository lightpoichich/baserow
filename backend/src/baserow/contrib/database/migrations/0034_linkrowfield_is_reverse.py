# Generated by Django 2.2.11 on 2021-06-08 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0033_remove_field_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkrowfield',
            name='is_reverse',
            field=models.BooleanField(default=True),
        ),
    ]
