# Generated by Django 2.2.11 on 2021-01-05 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0023_convert_int_to_bigint'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='calls',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='token',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
