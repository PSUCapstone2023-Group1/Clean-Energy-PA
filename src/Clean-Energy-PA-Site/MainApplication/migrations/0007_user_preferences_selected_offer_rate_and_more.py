# Generated by Django 4.1.1 on 2023-06-03 04:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("MainApplication", "0006_alter_user_preferences_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="user_preferences",
            name="selected_offer_rate",
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name="user_preferences",
            name="distributor_id",
            field=models.BigIntegerField(default=None),
        ),
        migrations.AlterField(
            model_name="user_preferences",
            name="rate_schedule",
            field=models.CharField(default=None, max_length=80),
        ),
        migrations.AlterField(
            model_name="user_preferences",
            name="selected_offer_id",
            field=models.BigIntegerField(default=None),
        ),
        migrations.AlterField(
            model_name="user_preferences",
            name="user_id",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="user_preferences",
            name="zip_code",
            field=models.CharField(default=None, max_length=10),
        ),
    ]
