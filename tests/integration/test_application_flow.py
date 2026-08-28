from pathlib import Path

from fbz.domain.search_criteria import SearchCriteria
from fbz.repositories.csv_comic_repository import CsvComicRepository
from fbz.services.favourite_service import FavouriteService
from fbz.services.search_service import SearchService


def test_end_to_end_csv_search_and_favourite_flow(tmp_path: Path) -> None:
    csv_path = tmp_path / "comics.csv"
    csv_path.write_text(
        "BL record ID,Title,Name,Date of publication,Genre,Topics\n"
        "0001,Bravo,Ada Lovelace,1998,Fantasy; Comic books,Magic;Science\n"
        "0002,Alpha,Bob Jones,2001,History,History\n"
        "0003,Charlie,Ada Lovelace,1998,Fantasy,Magic\n",
        encoding="utf-8",
    )
    service = SearchService(CsvComicRepository(csv_path))
    results = service.advanced_search(SearchCriteria(author="Ada", genre="Fantasy", year="1998"))
    assert [comic.title for comic in results] == ["Bravo", "Charlie"]

    favourites = FavouriteService(tmp_path / "favourites.json")
    assert favourites.add(results[0].record_id)
    assert FavouriteService(tmp_path / "favourites.json").list_ids() == ["0001"]
