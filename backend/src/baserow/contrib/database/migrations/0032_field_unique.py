# Generated by Django 2.2.11 on 2021-06-04 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0031_fix_url_field_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='unique',
            field=models.BooleanField(default=False),
        ),
    ]
