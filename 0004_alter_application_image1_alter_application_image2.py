# Generated by Django 4.1.2 on 2023-02-08 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_application_delete_assignlocker_delete_lockertype"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="image1",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="application",
            name="image2",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
    ]
