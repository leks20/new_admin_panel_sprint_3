# Generated by Django 3.2 on 2022-11-08 13:21
import django.core.validators
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="filmwork",
            options={"verbose_name": "Filmwork", "verbose_name_plural": "Filmworks"},
        ),
        migrations.AlterModelOptions(
            name="genre",
            options={"verbose_name": "Genre", "verbose_name_plural": "Genres"},
        ),
        migrations.AlterModelOptions(
            name="person",
            options={"verbose_name": "Person", "verbose_name_plural": "Persons"},
        ),
        migrations.RenameField(
            model_name="filmwork",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="filmwork",
            old_name="modified",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="genre",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="genre",
            old_name="modified",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="genrefilmwork",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="person",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="person",
            old_name="modified",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="personfilmwork",
            old_name="created",
            new_name="created_at",
        ),
        migrations.AddField(
            model_name="filmwork",
            name="file_path",
            field=models.FileField(
                blank=True, null=True, upload_to="movies/", verbose_name="file"
            ),
        ),
        migrations.AlterField(
            model_name="filmwork",
            name="creation_date",
            field=models.DateField(blank=True, null=True, verbose_name="creation_date"),
        ),
        migrations.AlterField(
            model_name="filmwork",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="filmwork",
            name="rating",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
                verbose_name="rating",
            ),
        ),
        migrations.AlterField(
            model_name="filmwork",
            name="type",
            field=models.CharField(
                choices=[("T", "TV_show"), ("M", "Movie")], default="M", max_length=50
            ),
        ),
        migrations.AlterField(
            model_name="genre",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="personfilmwork",
            name="role",
            field=models.TextField(
                choices=[
                    ("actor", "actor"),
                    ("writer", "writer"),
                    ("director", "director"),
                ],
                null=True,
                verbose_name="role",
            ),
        ),
        migrations.AddIndex(
            model_name="filmwork",
            index=models.Index(
                fields=["creation_date"], name="film_work_creation_date_idx"
            ),
        ),
    ]
