# Generated by Django 2.2.11 on 2021-01-26 19:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def forward(apps, schema_editor):
    from baserow.core.models import GROUP_USER_PERMISSION_ADMIN

    GroupUser = apps.get_model('core', 'GroupUser')
    GroupUser.objects.all().update(permissions=GROUP_USER_PERMISSION_ADMIN)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_auto_20201215_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupuser',
            name='permissions',
            field=models.CharField(
                choices=[
                    ('ADMIN', 'Admin'),
                    ('MEMBER', 'Member')
                ],
                default='MEMBER',
                max_length=32
            ),
        ),
        migrations.CreateModel(
            name='GroupInvitation',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('email', models.EmailField(db_index=True, max_length=254)),
                ('permissions', models.CharField(
                    choices=[
                        ('ADMIN', 'Admin'),
                        ('MEMBER', 'Member')
                    ],
                    default='MEMBER',
                    max_length=32
                )),
                ('message', models.TextField(blank=True)),
                ('group', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='core.Group'
                )),
                ('invited_by', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL
                )),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True))
            ],
            options={'ordering': ('id',)}
        ),
        migrations.AlterUniqueTogether(
            name='groupuser',
            unique_together={('user', 'group')},
        ),
        migrations.RunPython(forward, migrations.RunPython.noop),
    ]
