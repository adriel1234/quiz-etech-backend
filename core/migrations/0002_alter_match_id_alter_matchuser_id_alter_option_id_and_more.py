# Generated by Django 5.1.1 on 2024-11-11 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="match",
            name="id",
            field=models.BigAutoField(
                db_column="nb_id", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="matchuser",
            name="id",
            field=models.BigAutoField(
                db_column="nb_id", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="option",
            name="id",
            field=models.BigAutoField(
                db_column="nb_id", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="id",
            field=models.BigAutoField(
                db_column="nb_id", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="questiongroup",
            name="id",
            field=models.BigAutoField(
                db_column="nb_id", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.BigAutoField(
                db_column="nb_id", primary_key=True, serialize=False
            ),
        ),
    ]
