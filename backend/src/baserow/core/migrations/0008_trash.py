# Generated by Django 2.2.11 on 2021-06-15 12:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0007_userlogentry"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="trashed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="group",
            name="trashed",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="Trash",
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
                ("trash_item_type", models.TextField()),
                (
                    "parent_trash_item_id",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ("trash_item_id", models.PositiveIntegerField()),
                ("should_be_permanently_deleted", models.BooleanField(default=False)),
                ("trashed_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.TextField()),
                ("parent_name", models.TextField(blank=True, null=True)),
                ("extra_description", models.TextField(blank=True, null=True)),
                (
                    "application",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.Application",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.Group"
                    ),
                ),
                (
                    "parent_entry",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.Trash",
                    ),
                ),
                (
                    "user_who_trashed",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="trash",
            index=models.Index(
                fields=["-trashed_at", "trash_item_type", "group", "application"],
                name="core_trash_trashed_c3738e_idx",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="trash",
            unique_together={
                ("trash_item_type", "parent_trash_item_id", "trash_item_id")
            },
        ),
    ]
