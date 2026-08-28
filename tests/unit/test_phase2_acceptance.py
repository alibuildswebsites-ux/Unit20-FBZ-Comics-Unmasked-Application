from pathlib import Path

from fbz.domain.comic import Comic
from fbz.repositories.comic_repository import InMemoryComicRepository
from fbz.services.encyclopedia_service import EncyclopediaService


def c(rid: str, title: str, name: str, genre: str, year: str, edition: str = "", language: str = "English", dewey: str = "741.5") -> Comic:
    return Comic.from_mapping({
        "BL record ID": rid, "Title": title, "Name": name, "Genre": genre,
        "Date of publication": year, "Edition": edition, "Languages": language,
        "Dewey classification": dewey, "Topics": "Masks;Crime",
    })


def test_phase2_search_list_is_in_memory_and_clearable() -> None:
    service = EncyclopediaService(InMemoryComicRepository([c("1", "Alpha", "Ada", "Fantasy", "1999")]))
    result = service.search_title("Alpha")[0]
    service.save_to_search_list(result)
    assert [x.record_id for x in service.search_list] == ["1"]
    service.reset()
    assert service.search_list == ()
    assert service.current_results == ()


def test_phase2_advanced_search_combines_edition_and_language() -> None:
    service = EncyclopediaService(InMemoryComicRepository([
        c("1", "Alpha", "Ada", "Fantasy", "1999", edition="First", language="English"),
        c("2", "Beta", "Ada", "Fantasy", "1999", edition="Second", language="French"),
    ]))
    results = service.advanced_search(author="Ada", year="1999", genre="Fantasy", edition="First", languages="English")
    assert [x.title for x in results] == ["Alpha"]


def test_phase2_search_threshold_notification_after_101_requests() -> None:
    seen: list[str] = []
    service = EncyclopediaService(InMemoryComicRepository([c("1", "Alpha", "Ada", "Fantasy", "1999")]), alert_callback=seen.append)
    for _ in range(101):
        service.search_title("Alpha")
    assert service.search_count("1") == 101
    assert seen and "1" in seen[-1]
