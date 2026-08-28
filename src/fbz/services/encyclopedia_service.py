from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Callable, Iterable, Sequence

from fbz.domain.comic import Comic
from fbz.repositories.comic_repository import ComicRepository

ALLOWED_GENRES = ("fantasy", "horror", "science fiction")


class EncyclopediaService:
    """Application services for the FBZ encyclopedia and search-list workflow."""

    def __init__(self, repository: ComicRepository, alert_callback: Callable[[str], None] | None = None) -> None:
        self._repository = repository
        self._current_results: tuple[Comic, ...] = ()
        self._search_list: tuple[Comic, ...] = ()
        self._search_counts: Counter[str] = Counter()
        self._query_counts: Counter[str] = Counter()
        self._alert_callback = alert_callback or (lambda _message: None)

    @property
    def current_results(self) -> tuple[Comic, ...]:
        return self._current_results

    @property
    def search_list(self) -> tuple[Comic, ...]:
        return self._search_list

    def filter_genre(self, genre: str) -> list[Comic]:
        key = genre.strip().casefold()
        if key not in ALLOWED_GENRES:
            raise ValueError("Genre must be one of: Fantasy, Horror, Science fiction")
        self._query_counts[f"genre:{key}"] += 1
        results = [comic for comic in self._repository.all() if any(key == token.casefold() for token in comic.tokens("genre"))]
        self._record_results(results)
        return results

    def search_title(self, title: str) -> list[Comic]:
        needle = title.strip().casefold()
        self._query_counts[f"title:{needle}"] += 1
        results = [comic for comic in self._repository.all() if needle and needle in comic.title.casefold()]
        self._record_results(results)
        return results

    def group_by_author(self, genre: str) -> dict[str, list[Comic]]:
        grouped: dict[str, list[Comic]] = defaultdict(list)
        for comic in self.filter_genre(genre):
            names = comic.tokens("name") or ((comic.name or "Unknown"),)
            for author in names:
                grouped[author].append(comic)
        return dict(grouped)

    def group_by_year(self, genre: str) -> dict[str, list[Comic]]:
        grouped: dict[str, list[Comic]] = defaultdict(list)
        for comic in self.filter_genre(genre):
            years = comic.tokens("date_of_publication") or ((comic.date_of_publication or "Unknown"),)
            for year in years:
                grouped[year].append(comic)
        return dict(grouped)

    @staticmethod
    def sorted_titles(comics: Iterable[Comic], ascending: bool = True) -> list[Comic]:
        return sorted(comics, key=lambda comic: comic.title.casefold(), reverse=not ascending)

    def advanced_search(
        self,
        author: str = "",
        year: str = "",
        genre: str = "",
        edition: str = "",
        languages: str = "",
        name_type: str = "",
        title: str = "",
    ) -> list[Comic]:
        criteria = ",".join((f"author={author.strip().casefold()}", f"year={year.strip().casefold()}",
                              f"genre={genre.strip().casefold()}", f"edition={edition.strip().casefold()}",
                              f"languages={languages.strip().casefold()}", f"name_type={name_type.strip().casefold()}",
                              f"title={title.strip().casefold()}"))
        self._query_counts[f"advanced:{criteria}"] += 1
        results: Sequence[Comic] = self._repository.all()
        if genre.strip():
            key = genre.strip().casefold()
            if key not in ALLOWED_GENRES:
                raise ValueError("Genre must be one of: Fantasy, Horror, Science fiction")
            results = [comic for comic in results if any(key == token.casefold() for token in comic.tokens("genre"))]
        filters = (
            (author, "name"), (year, "date_of_publication"), (edition, "edition"),
            (languages, "languages"), (name_type, "type_of_name"),
        )
        for value, field in filters:
            if value.strip():
                needle = value.strip().casefold()
                results = [comic for comic in results if needle in getattr(comic, field).casefold()]
        if title.strip():
            needle = title.strip().casefold()
            results = [comic for comic in results if needle in comic.title.casefold()]
        final = list(results)
        self._record_results(final)
        return final

    def search_field(self, field: str, query: str) -> list[Comic]:
        """Search a Phase 2 view-oriented field by a human-friendly name."""
        aliases = {
            "classification": "dewey_classification", "names": "name", "titles": "title",
            "topics": "topics", "author": "name", "genre": "genre",
        }
        try:
            attribute = aliases[field.strip().casefold()]
        except KeyError as exc:
            raise ValueError("Supported searches: classification, names, titles, topics, author, genre") from exc
        needle = query.strip().casefold()
        self._query_counts[f"{field.strip().casefold()}:{needle}"] += 1
        results = []
        for comic in self._repository.all():
            value = getattr(comic, attribute, "")
            matched = (
                any(needle in token.casefold() for token in comic.tokens(attribute))
                if attribute in {"topics", "languages", "genre"} and needle
                else needle in value.casefold() if needle else False
            )
            if matched:
                results.append(comic)
        self._record_results(results)
        return results

    def save_to_search_list(self, comic: Comic) -> None:
        if comic not in self._search_list:
            self._search_list = (*self._search_list, comic)

    def clear_search_results(self) -> None:
        self._current_results = ()

    def reset(self) -> None:
        self._current_results = ()
        self._search_list = ()
        self._search_counts.clear()
        self._query_counts.clear()

    def search_count(self, record_id: str) -> int:
        return self._search_counts.get(record_id, 0)

    def top_search_queries(self, limit: int = 10) -> list[tuple[str, int]]:
        return self._query_counts.most_common(limit)

    def top_search_results(self, limit: int = 10) -> list[tuple[Comic, int]]:
        by_id = {comic.record_id: comic for comic in self._repository.all()}
        return [(by_id[record_id], count) for record_id, count in self._search_counts.most_common(limit) if record_id in by_id]

    def comics_over_threshold(self, threshold: int = 100) -> list[tuple[Comic, int]]:
        by_id = {comic.record_id: comic for comic in self._repository.all()}
        return [
            (by_id[record_id], count)
            for record_id, count in self._search_counts.most_common()
            if count > threshold and record_id in by_id
        ]

    def format_record(self, comic: Comic) -> dict[str, str | list[str]]:
        values: dict[str, str | list[str]] = {}
        for field_name, label in (
            ("record_id", "BL record ID"), ("name", "Name"), ("title", "Title"),
            ("variant_titles", "Variant titles"), ("genre", "Genre"), ("topics", "Topics"),
            ("languages", "Languages"), ("isbn", "ISBN"), ("edition", "Edition"),
            ("date_of_publication", "Date of publication"), ("type_of_resource", "Type of resource"),
            ("content_type", "Content type"), ("material_type", "Material type"),
            ("publisher", "Publisher"), ("place_of_publication", "Place of publication"),
            ("country_of_publication", "Country of publication"), ("physical_description", "Physical description"),
            ("dewey_classification", "Dewey classification"), ("bl_shelfmark", "BL shelfmark"),
            ("notes", "Notes"),
        ):
            raw = getattr(comic, field_name)
            if label == "ISBN" and not raw:
                raw = "missing"
            tokens = comic.tokens(field_name) if field_name in {"genre", "topics", "languages", "content_type"} else ()
            values[label] = [f"{label}: {token}" for token in tokens] if tokens else raw
        return values

    def _record_results(self, results: Iterable[Comic]) -> None:
        materialised = tuple(results)
        self._current_results = materialised
        for comic in materialised:
            self._search_counts[comic.record_id] += 1
            if self._search_counts[comic.record_id] == 101:
                self._alert_callback(f"Comic {comic.title} ({comic.record_id}) has been included in more than 100 search results")
