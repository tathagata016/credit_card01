# Generated by Django 4.1.2 on 2023-02-10 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0005_trackinghistory"),
    ]

    operations = [
        migrations.AddField(
            model_name="trackinghistory",
            name="limit",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
