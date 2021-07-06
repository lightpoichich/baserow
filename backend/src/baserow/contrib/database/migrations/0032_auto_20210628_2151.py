# Generated by Django 2.2.11 on 2021-06-28 21:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_userlogentry"),
        ("database", "0031_fix_url_field_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="FormView",
            fields=[
                (
                    "view_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="database.View",
                    ),
                ),
                (
                    "slug",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        help_text="The unique slug where the form can be accessed "
                        "publicly on.",
                        unique=True,
                    ),
                ),
                (
                    "public",
                    models.BooleanField(
                        default=False,
                        help_text="Indicates whether the form is publicly accessible "
                        "to visitors and if they can fill it out.",
                    ),
                ),
                (
                    "title",
                    models.TextField(
                        blank=True,
                        help_text="The title that is displayed at the beginning of "
                        "the form.",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="The description that is displayed at the beginning "
                        "of the form.",
                    ),
                ),
                (
                    "submit_action",
                    models.CharField(
                        choices=[("MESSAGE", "Message"), ("REDIRECT", "Redirect")],
                        default="MESSAGE",
                        help_text="The action that must be performed after the visitor "
                        "has filled out the form.",
                        max_length=32,
                    ),
                ),
                (
                    "submit_action_message",
                    models.TextField(
                        blank=True,
                        help_text="If the `submit_action` is MESSAGE, then this "
                        "message will be shown to the visitor after "
                        "submitting the form.",
                    ),
                ),
                (
                    "submit_action_redirect_url",
                    models.URLField(
                        blank=True,
                        help_text="If the `submit_action` is REDIRECT,then the "
                        "visitors will be redirected to the this URL after submitting "
                        "the form.",
                    ),
                ),
                (
                    "cover_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="form_view_cover_image",
                        to="core.UserFile",
                        help_text="The user file cover image that is displayed at the "
                        "top of the form.",
                    ),
                ),
                (
                    "logo_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="form_view_logo_image",
                        to="core.UserFile",
                        help_text="The user file logo image that is displayed at the "
                        "top of the form.",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("database.view",),
        ),
        migrations.AlterField(
            model_name="gridviewfieldoptions",
            name="hidden",
            field=models.BooleanField(
                default=False,
                help_text="Whether or not the field should be hidden in the current "
                "view.",
            ),
        ),
        migrations.AlterField(
            model_name="gridviewfieldoptions",
            name="order",
            field=models.SmallIntegerField(
                default=32767,
                help_text="The position that the field has within the view, lowest "
                "first. If there is another field with the same order value "
                "then the field with the lowest id must be shown first.",
            ),
        ),
        migrations.AlterField(
            model_name="gridviewfieldoptions",
            name="width",
            field=models.PositiveIntegerField(
                default=200,
                help_text="The width of the table field in the related view.",
            ),
        ),
        migrations.CreateModel(
            name="FormViewFieldOptions",
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
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="By default, the name of the related field will be "
                        "shown to the visitor. Optionally another name can "
                        "be used by setting this name.",
                        max_length=255,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="If provided, then this value be will be shown under "
                        "the field name.",
                    ),
                ),
                (
                    "enabled",
                    models.BooleanField(
                        default=False,
                        help_text="Indicates whether the field is included in the "
                        "form.",
                    ),
                ),
                (
                    "required",
                    models.BooleanField(
                        default=True,
                        help_text="Indicates whether the field is required for the "
                        "visitor to fill out.",
                    ),
                ),
                (
                    "order",
                    models.SmallIntegerField(
                        default=32767,
                        help_text="The order that the field has in the form. Lower "
                        "value is first.",
                    ),
                ),
                (
                    "field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="database.Field"
                    ),
                ),
                (
                    "form_view",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="database.FormView",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "field_id"),
            },
        ),
        migrations.AddField(
            model_name="formview",
            name="field_options",
            field=models.ManyToManyField(
                through="database.FormViewFieldOptions", to="database.Field"
            ),
        ),
    ]
