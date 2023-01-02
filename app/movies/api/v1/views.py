from typing import Any

from config.settings import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ["get"]

    def get_queryset(self) -> QuerySet[model, dict[str, Any]]:

        movies = (
            self.model.objects.prefetch_related(
                "genres",
                "persons",
            )
            .values("id", "title", "description", "creation_date", "rating", "type")
            .annotate(
                genres=ArrayAgg("genres__name", distinct=True),
                actors=ArrayAgg(
                    "persons__full_name",
                    distinct=True,
                    filter=Q(personfilmwork__role="actor"),
                ),
                directors=ArrayAgg(
                    "persons__full_name",
                    distinct=True,
                    filter=Q(personfilmwork__role="director"),
                ),
                writers=ArrayAgg(
                    "persons__full_name",
                    distinct=True,
                    filter=Q(personfilmwork__role="writer"),
                ),
            )
        )

        return movies

    def render_to_response(
        self, context: dict[str, Any], **response_kwargs: dict[str, Any]
    ) -> object:
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = settings.PAGE_SIZE

    def get_context_data(
        self, *, object_list: Any = None, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        queryset = self.get_queryset()

        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )

        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": paginator.page(page.number).previous_page_number()
            if page.number > 1
            else None,
            "next": paginator.page(page.number).next_page_number()
            if page.number < paginator.num_pages
            else None,
            "results": list(queryset),
        }

        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any] | None:
        return kwargs.get("object", None)
