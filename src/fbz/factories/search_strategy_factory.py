from __future__ import annotations

from fbz.strategies.search_strategy import (
    AuthorSearchStrategy,
    GenreSearchStrategy,
    SearchStrategy,
    TitleSearchStrategy,
    YearSearchStrategy,
)


class SearchStrategyFactory:
    """Creates search strategies without exposing concrete classes to clients."""

    _strategies = {
        "title": TitleSearchStrategy,
        "author": AuthorSearchStrategy,
        "genre": GenreSearchStrategy,
        "year": YearSearchStrategy,
    }

    @classmethod
    def create(cls, search_type: str) -> SearchStrategy:
        try:
            strategy_type = cls._strategies[search_type.strip().casefold()]
        except KeyError as exc:
            valid = ", ".join(cls._strategies)
            raise ValueError(f"Unsupported search type. Choose: {valid}") from exc
        return strategy_type()
