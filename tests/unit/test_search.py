from fbz.domain.comic import Comic
from fbz.domain.search_criteria import SearchCriteria
from fbz.factories.search_strategy_factory import SearchStrategyFactory
from fbz.repositories.comic_repository import InMemoryComicRepository
from fbz.services.search_service import SearchService


def comic(record_id: str, title: str, name: str = "", genre: str = "", year: str = "") -> Comic:
    return Comic.from_mapping({
        "BL record ID": record_id,
        "Title": title,
        "Name": name,
        "Genre": genre,
        "Date of publication": year,
    })


def test_strategy_factory_returns_interchangeable_strategies() -> None:
    assert SearchStrategyFactory.create("title").__class__.__name__ == "TitleSearchStrategy"
    assert SearchStrategyFactory.create("AUTHOR").__class__.__name__ == "AuthorSearchStrategy"
    assert SearchStrategyFactory.create("genre").__class__.__name__ == "GenreSearchStrategy"
    assert SearchStrategyFactory.create("year").__class__.__name__ == "YearSearchStrategy"


def test_search_service_filters_by_author() -> None:
    service = SearchService(InMemoryComicRepository([
        comic("1", "Alpha", "Alice Example", "Fantasy", "1998"),
        comic("2", "Beta", "Bob Example", "History", "2001"),
    ]))
    assert [item.title for item in service.search("author", "alice")] == ["Alpha"]


def test_advanced_search_applies_multiple_criteria_and_sorts() -> None:
    service = SearchService(InMemoryComicRepository([
        comic("1", "Zeta", "Alice", "Fantasy", "1998"),
        comic("2", "Alpha", "Alice", "Fantasy", "1998"),
        comic("3", "Beta", "Alice", "History", "1998"),
    ]))
    results = service.advanced_search(SearchCriteria(author="alice", genre="fantasy", year="1998"))
    assert [item.title for item in results] == ["Alpha", "Zeta"]
