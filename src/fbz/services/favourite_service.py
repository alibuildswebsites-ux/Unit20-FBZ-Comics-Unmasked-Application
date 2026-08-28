from __future__ import annotations

import json
from pathlib import Path


class FavouriteService:
    """Persists favourite record IDs separately from the source dataset."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    def list_ids(self) -> list[str]:
        if not self._path.exists():
            return []
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            raise ValueError(f"Cannot read favourites: {exc}") from exc
        if not isinstance(payload, list) or not all(isinstance(item, str) for item in payload):
            raise ValueError("Favourites file must contain a JSON list of string IDs")
        return payload

    def add(self, record_id: str) -> bool:
        favourites = self.list_ids()
        if record_id in favourites:
            return False
        favourites.append(record_id)
        self._save(favourites)
        return True

    def remove(self, record_id: str) -> bool:
        favourites = self.list_ids()
        if record_id not in favourites:
            return False
        favourites.remove(record_id)
        self._save(favourites)
        return True

    def _save(self, favourites: list[str]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(favourites, indent=2), encoding="utf-8")
