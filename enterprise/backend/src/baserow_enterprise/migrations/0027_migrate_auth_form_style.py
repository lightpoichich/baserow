# Generated by Django 4.1.13 on 2024-06-19 22:51

from django.db import migrations


def migrate_auth_form_styles(apps, schema_editor):
    """
    Migrates on model element styles into the style property.
    """

    AuthFormElement = apps.get_model("baserow_enterprise", "authformelement")
    AuthFormElement.objects.all().update(
        styles={"login_button": {"button_width": "full"}}
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0087_userprofile_completed_onboarding"),
        ("builder", "0026_add_more_style_properties"),
        ("baserow_enterprise", "0026_localbaserowusersource_role_field"),
    ]

    operations = [
        migrations.RunPython(
            migrate_auth_form_styles, reverse_code=migrations.RunPython.noop
        ),
    ]
