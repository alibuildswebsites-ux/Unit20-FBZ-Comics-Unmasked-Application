from __future__ import annotations

from collections import OrderedDict

from fbz.domain.comic import Comic
from fbz.repositories.comic_repository import ComicRepository


class AggregatingComicRepository(ComicRepository):
    """Collapses facet-view rows into one record per BL record ID.

    The assignment explicitly requires multiple title rows to be displayed as one
    record entry, with variant metadata such as years and ISBNs represented as lists.
    """

    def __init__(self, source: ComicRepository) -> None:
        self._source = source
        self._records: tuple[Comic, ...] | None = None

    def all(self) -> tuple[Comic, ...]:
        if self._records is None:
            groups: OrderedDict[str, list[Comic]] = OrderedDict()
            for comic in self._source.all():
                groups.setdefault(comic.record_id, []).append(comic)
            self._records = tuple(self._merge(rows) for rows in groups.values())
        return self._records

    @staticmethod
    def _merge(rows: list[Comic]) -> Comic:
        first = rows[0]
        field_names = (
            "name", "dates_associated_with_name", "type_of_name", "role", "other_names",
            "type_of_resource", "content_type", "material_type", "bnb_number", "isbn",
            "variant_titles", "series_title", "number_within_series", "country_of_publication",
            "place_of_publication", "publisher", "date_of_publication", "edition",
            "physical_description", "dewey_classification", "bl_shelfmark", "topics",
            "genre", "languages", "notes",
        )
        merged: dict[str, str] = {}
        for field in field_names:
            values: list[str] = []
            for row in rows:
                raw = getattr(row, field)
                for part in raw.split(";") if raw else []:
                    cleaned = part.strip()
                    if cleaned and cleaned not in values:
                        values.append(cleaned)
            merged[field] = ";".join(values)
        variant_titles = []
        for row in rows:
            for title in (row.title, *([part.strip() for part in row.variant_titles.split(";") if part.strip()] if row.variant_titles else [])):
                if title and title != first.title and title not in variant_titles:
                    variant_titles.append(title)
        merged["variant_titles"] = ";".join(variant_titles)
        return Comic(record_id=first.record_id, title=first.title, **merged)
