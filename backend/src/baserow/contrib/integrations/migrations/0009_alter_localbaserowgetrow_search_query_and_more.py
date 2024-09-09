# Generated by Django 5.0.9 on 2024-09-23 14:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("integrations", "0008_local_baserow_delete_row_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="localbaserowgetrow",
            name="search_query",
            field=models.TextField(
                blank=True,
                default="",
                help_text="The query to apply to the service to narrow the results down.",
                max_length=225,
            ),
        ),
        migrations.AlterField(
            model_name="localbaserowlistrows",
            name="search_query",
            field=models.TextField(
                blank=True,
                default="",
                help_text="The query to apply to the service to narrow the results down.",
                max_length=225,
            ),
        ),
    ]
