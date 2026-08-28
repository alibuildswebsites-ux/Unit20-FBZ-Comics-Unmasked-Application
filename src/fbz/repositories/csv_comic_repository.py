from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from fbz.domain.comic import Comic
from fbz.repositories.comic_repository import ComicRepository


class CsvComicRepository(ComicRepository):
    """Loads Comic records from a CSV file using Python's standard CSV parser."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._comics: tuple[Comic, ...] | None = None

    def all(self) -> tuple[Comic, ...]:
        if self._comics is None:
            self._comics = tuple(self._load())
        return self._comics

    def _load(self) -> Iterable[Comic]:
        if not self._path.is_file():
            raise FileNotFoundError(f"Dataset not found: {self._path}")
        with self._path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise ValueError("Dataset is missing a header row")
            required = {"BL record ID", "Title"}
            if not required.issubset(set(reader.fieldnames)):
                missing = sorted(required.difference(reader.fieldnames))
                raise ValueError(f"Dataset missing required columns: {', '.join(missing)}")
            for row_number, row in enumerate(reader, start=2):
                try:
                    yield Comic.from_mapping(row)
                except ValueError as exc:
                    raise ValueError(f"Invalid dataset row {row_number}: {exc}") from exc
