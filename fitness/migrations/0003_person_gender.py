# Generated by Django 4.1 on 2024-06-22 14:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fitness", "0002_workout"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="gender",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
