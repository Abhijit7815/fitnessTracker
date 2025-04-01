# Generated by Django 4.1 on 2024-06-19 17:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fitness", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Workout",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("workout_type", models.CharField(max_length=50)),
                ("image", models.ImageField(upload_to="workout_images/")),
                ("description", models.TextField()),
            ],
        ),
    ]
