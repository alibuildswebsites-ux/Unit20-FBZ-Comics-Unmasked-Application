from __future__ import annotations

from collections.abc import Sequence

from fbz.domain.comic import Comic
from fbz.domain.search_criteria import SearchCriteria
from fbz.factories.search_strategy_factory import SearchStrategyFactory
from fbz.repositories.comic_repository import ComicRepository


class SearchService:
    """Application service coordinating search without owning data-access details."""

    def __init__(self, repository: ComicRepository) -> None:
        self._repository = repository

    def search(self, search_type: str, query: str) -> list[Comic]:
        strategy = SearchStrategyFactory.create(search_type)
        return strategy.search(self._repository.all(), query)

    def advanced_search(self, criteria: SearchCriteria) -> list[Comic]:
        results: Sequence[Comic] = self._repository.all()
        if criteria.text.strip():
            results = [comic for comic in results if comic.matches_text(criteria.text)]
        if criteria.author.strip():
            results = SearchStrategyFactory.create("author").search(results, criteria.author)
        if criteria.genre.strip():
            results = SearchStrategyFactory.create("genre").search(results, criteria.genre)
        if criteria.year.strip():
            results = SearchStrategyFactory.create("year").search(results, criteria.year)
        return sorted(results, key=lambda comic: comic.title.casefold(), reverse=not criteria.sort_ascending)

    def alphabetical(self, descending: bool = False) -> list[Comic]:
        return sorted(self._repository.all(), key=lambda comic: comic.title.casefold(), reverse=descending)
