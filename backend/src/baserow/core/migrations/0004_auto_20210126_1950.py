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
                help_text='The permissions that the user has within the group.',
                max_length=32
            ),
        ),
        migrations.AlterField(
            model_name='groupuser',
            name='group',
            field=models.ForeignKey(
                help_text='The group that the user has access to.',
                on_delete=django.db.models.deletion.CASCADE,
                to='core.Group'
            ),
        ),
        migrations.AlterField(
            model_name='groupuser',
            name='order',
            field=models.PositiveIntegerField(
                help_text='Unique order that the group has for the user.'
            ),
        ),
        migrations.AlterField(
            model_name='groupuser',
            name='permissions',
            field=models.CharField(
                choices=[('ADMIN', 'Admin'), ('MEMBER', 'Member')],
                default='MEMBER',
                help_text='The permissions that the user has within the group.',
                max_length=32
            ),
        ),
        migrations.AlterField(
            model_name='groupuser',
            name='user',
            field=models.ForeignKey(
                help_text='The user that has access to the group.',
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL
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
                ('email', models.EmailField(
                    db_index=True,
                    max_length=254,
                    help_text='The email address of the user that the invitation is '
                              'meant for. Only a user with that email address can '
                              'accept it.'
                )),
                ('permissions', models.CharField(
                    choices=[
                        ('ADMIN', 'Admin'),
                        ('MEMBER', 'Member')
                    ],
                    default='MEMBER',
                    max_length=32,
                    help_text='The permissions that the user is going to get within '
                              'the group after accepting the invitation.'
                )),
                ('message', models.TextField(
                    blank=True,
                    help_text='An optional message that the creator can provide. This '
                              'will be visible to the receiver of the invitation.'
                )),
                ('group', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='core.Group',
                    help_text='The group that the user will get access to once the '
                              'invitation is accepted.'
                )),
                ('invited_by', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL,
                    help_text='The user that created the invitation.'
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
