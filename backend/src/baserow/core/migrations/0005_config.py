# Generated by Django 2.2.11 on 2021-02-15 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210126_1950'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('allow_new_signups', models.BooleanField(
                    default=True,
                    help_text='Indicates whether new users can create a new account '
                              'when signing up.'
                )),
            ],
        ),
    ]
