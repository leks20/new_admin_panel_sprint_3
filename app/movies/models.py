import uuid

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(TimeStampedMixin, UUIDMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self) -> str:
        return self.name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "genre_id"], name="film_work_genre"
            ),
        ]


class Gender(models.TextChoices):
    MALE = "male", _("male")
    FEMALE = "female", _("female")


class Person(TimeStampedMixin, UUIDMixin):
    full_name = models.CharField(_("full_name"), max_length=255)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    def __str__(self) -> str:
        return self.full_name


class RoleType(models.TextChoices):
    actor = "actor", _("actor")
    writer = "writer", _("writer")
    director = "director", _("director")


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.TextField(_("role"), choices=RoleType.choices, null=True)

    class Meta:
        db_table = 'content"."person_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "person_id", "role"],
                name="film_work_person_role",
            ),
        ]


class Filmwork(TimeStampedMixin, UUIDMixin):
    class Type(models.TextChoices):
        TV_SHOW = "T", _("TV_show")
        MOVIE = "M", _("Movie")

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(_("creation_date"), blank=True, null=True)
    file_path = models.FileField(_("file"), blank=True, null=True, upload_to="movies/")
    rating = models.FloatField(
        _("rating"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(max_length=50, choices=Type.choices, default=Type.MOVIE)
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    persons = models.ManyToManyField(Person, through="PersonFilmwork")

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Filmwork")
        verbose_name_plural = _("Filmworks")

        indexes = [
            models.Index(fields=["creation_date"], name="film_work_creation_date_idx"),
        ]

    def __str__(self) -> str:
        return self.title
