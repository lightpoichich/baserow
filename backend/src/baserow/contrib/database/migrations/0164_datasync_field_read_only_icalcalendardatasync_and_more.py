# Generated by Django 4.2.13 on 2024-09-09 20:17

import django.db.models.deletion
from django.db import migrations, models

import baserow.core.fields
import baserow.core.mixins


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0088_remove_blacklistedtoken_user"),
        ("database", "0163_alter_formulafield_expand_formula_when_referenced"),
    ]

    operations = [
        migrations.CreateModel(
            name="DataSync",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", baserow.core.fields.SyncedDateTimeField(auto_now=True)),
                (
                    "last_sync",
                    models.DateTimeField(
                        help_text="Timestamp when the table was last synced.", null=True
                    ),
                ),
                ("last_error", models.TextField(null=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="data_syncs",
                        to="contenttypes.contenttype",
                        verbose_name="content type",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                baserow.core.mixins.PolymorphicContentTypeMixin,
                models.Model,
                baserow.core.mixins.WithRegistry,
            ),
        ),
        migrations.AddField(
            model_name="field",
            name="read_only",
            field=models.BooleanField(
                default=False,
                help_text="Indicates whether the field is read-only regardless of the field type. If true, then it won't be possible to update the cell value via theAPI.",
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="ICalCalendarDataSync",
            fields=[
                (
                    "datasync_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="database.datasync",
                    ),
                ),
                ("ical_url", models.URLField(max_length=2000)),
            ],
            options={
                "abstract": False,
            },
            bases=("database.datasync",),
        ),
        migrations.CreateModel(
            name="SyncDataSyncTableJob",
            fields=[
                (
                    "job_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.job",
                    ),
                ),
                (
                    "data_sync",
                    models.ForeignKey(
                        help_text="The data sync of which the table must be synced.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sync_data_sync_table_job",
                        to="database.datasync",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("core.job",),
        ),
        migrations.CreateModel(
            name="DataSyncProperty",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "key",
                    models.CharField(
                        help_text="The matching `key` of the `DataSyncProperty`.",
                        max_length=255,
                    ),
                ),
                (
                    "data_sync",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="data_sync_properties",
                        to="database.datasync",
                    ),
                ),
                (
                    "field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="database.field"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="datasync",
            name="properties",
            field=models.ManyToManyField(
                through="database.DataSyncProperty", to="database.field"
            ),
        ),
        migrations.AddField(
            model_name="datasync",
            name="table",
            field=models.OneToOneField(
                help_text="The table where the data is synced into.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="data_sync",
                to="database.table",
            ),
        ),
    ]
