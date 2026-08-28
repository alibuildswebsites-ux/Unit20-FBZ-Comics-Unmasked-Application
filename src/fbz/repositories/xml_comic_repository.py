from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

from fbz.domain.comic import Comic
from fbz.repositories.comic_repository import ComicRepository


class XmlComicRepository(ComicRepository):
    """Future-proof repository adapter for XML sources with record-shaped elements."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._comics: tuple[Comic, ...] | None = None

    def all(self) -> tuple[Comic, ...]:
        if self._comics is None:
            if not self._path.is_file():
                raise FileNotFoundError(f"XML dataset not found: {self._path}")
            root = ET.parse(self._path).getroot()
            rows: list[Comic] = []
            for node in root.findall('.//record'):
                row = {child.tag.replace('_', ' '): (child.text or '') for child in node}
                row['BL record ID'] = row.get('BL record ID', row.get('BL Record ID', ''))
                rows.append(Comic.from_mapping(row))
            self._comics = tuple(rows)
        return self._comics
