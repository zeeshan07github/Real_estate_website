# Generated by Django 4.2.3 on 2023-09-05 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="area",
            field=models.IntegerField(),
        ),
    ]