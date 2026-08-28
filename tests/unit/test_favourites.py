from pathlib import Path

from fbz.services.favourite_service import FavouriteService


def test_favourite_service_add_remove_and_persist(tmp_path: Path) -> None:
    path = tmp_path / "favourites.json"
    service = FavouriteService(path)
    assert service.list_ids() == []
    assert service.add("000123")
    assert not service.add("000123")
    assert FavouriteService(path).list_ids() == ["000123"]
    assert service.remove("000123")
    assert not service.remove("000123")
