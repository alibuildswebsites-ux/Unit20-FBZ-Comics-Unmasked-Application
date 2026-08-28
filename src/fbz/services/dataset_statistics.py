from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

from fbz.domain.comic import Comic


class DatasetStatistics:
    """Computes deterministic dataset facts used in evidence and reports."""

    @staticmethod
    def summary(comics: Sequence[Comic]) -> dict[str, int]:
        return {
            "records": len(comics),
            "missing_titles": sum(not comic.title for comic in comics),
            "missing_names": sum(not comic.name for comic in comics),
            "missing_genres": sum(not comic.genre for comic in comics),
        }

    @staticmethod
    def top_searchable_tokens(comics: Sequence[Comic], field: str, limit: int = 10) -> list[tuple[str, int]]:
        counter: Counter[str] = Counter()
        for comic in comics:
            counter.update(token.casefold() for token in comic.tokens(field))
        return counter.most_common(limit)
