from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from fbz.domain.comic import Comic


class ComicRepository(ABC):
    """Abstraction for accessing comic records."""

    @abstractmethod
    def all(self) -> Sequence[Comic]:
        raise NotImplementedError


class InMemoryComicRepository(ComicRepository):
    """Repository used by the app and tests without coupling them to CSV I/O."""

    def __init__(self, comics: Sequence[Comic]) -> None:
        self._comics = tuple(comics)

    def all(self) -> Sequence[Comic]:
        return self._comics
