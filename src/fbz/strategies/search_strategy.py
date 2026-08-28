from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from fbz.domain.comic import Comic


class SearchStrategy(ABC):
    """Common contract for interchangeable search algorithms."""

    @abstractmethod
    def search(self, comics: Sequence[Comic], query: str) -> list[Comic]:
        raise NotImplementedError


class TitleSearchStrategy(SearchStrategy):
    def search(self, comics: Sequence[Comic], query: str) -> list[Comic]:
        needle = query.strip().casefold()
        return [comic for comic in comics if needle and needle in comic.title.casefold()]


class AuthorSearchStrategy(SearchStrategy):
    def search(self, comics: Sequence[Comic], query: str) -> list[Comic]:
        needle = query.strip().casefold()
        return [
            comic for comic in comics
            if needle and any(needle in author.casefold() for author in comic.authors())
        ]


class GenreSearchStrategy(SearchStrategy):
    def search(self, comics: Sequence[Comic], query: str) -> list[Comic]:
        needle = query.strip().casefold()
        return [
            comic for comic in comics
            if needle and any(needle == token.casefold() or needle in token.casefold() for token in comic.tokens("genre"))
        ]


class YearSearchStrategy(SearchStrategy):
    def search(self, comics: Sequence[Comic], query: str) -> list[Comic]:
        needle = query.strip()
        return [comic for comic in comics if needle and needle in comic.date_of_publication]
