# Generated by Django 4.2.1 on 2023-06-02 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('MainApplication', '0003_rename_userprofile_customuser'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomUser',
            new_name='UserProfile',
        ),
    ]
