from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Filmwork
from .models import Genre
from .models import GenreFilmwork
from .models import Person
from .models import PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ("person",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name",)
    search_fields = ("full_name",)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (
        GenreFilmworkInline,
        PersonFilmworkInline,
    )
    list_display = (
        "title",
        "type",
        "get_genres",
        "creation_date",
        "rating",
    )
    list_filter = (
        "type",
        "genres",
    )
    search_fields = (
        "title",
        "description",
        "id",
    )

    list_prefetch_related = ("genres",)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = (
            super().get_queryset(request).prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    @admin.display(description="Жанры фильма")
    def get_genres(self, obj: Filmwork) -> str:
        return ",".join([genre.name for genre in obj.genres.all()])
