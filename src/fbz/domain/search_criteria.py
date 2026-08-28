from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SearchCriteria:
    """Optional multi-criteria search request."""

    text: str = ""
    author: str = ""
    genre: str = ""
    year: str = ""
    sort_ascending: bool = True
