# Generated by Django 4.2.2 on 2023-07-15 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GreenEnergySearch', '0008_alter_user_preferences_possible_selections'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_preferences',
            name='possible_selections',
            field=models.JSONField(default=list),
        ),
    ]
