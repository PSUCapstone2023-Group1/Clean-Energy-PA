# Generated by Django 4.1.1 on 2023-07-23 01:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "GreenEnergySearch",
            "0008_user_preferences_selected_offer_expected_end_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="user_preferences",
            name="selected_offer_expected_end",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="user_preferences",
            name="selected_offer_selected_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]