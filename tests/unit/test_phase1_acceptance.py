from fbz.domain.comic import Comic
from fbz.repositories.comic_repository import InMemoryComicRepository
from fbz.services.encyclopedia_service import EncyclopediaService


def c(rid: str, title: str, name: str, genre: str, year: str, isbn: str = "") -> Comic:
    return Comic.from_mapping({
        "BL record ID": rid, "Title": title, "Name": name, "Genre": genre,
        "Date of publication": year, "ISBN": isbn,
        "Topics": "A;B", "Variant titles": "Alt title",
    })


def test_phase1_filters_only_the_three_allowed_genres() -> None:
    service = EncyclopediaService(InMemoryComicRepository([
        c("1", "Fantasy One", "A", "Fantasy", "1990"),
        c("2", "Horror One", "B", "Horror", "1991"),
        c("3", "Science One", "C", "Science fiction", "1992"),
        c("4", "Other", "D", "History", "1993"),
    ]))
    assert [x.title for x in service.filter_genre("fantasy")] == ["Fantasy One"]
    assert sorted(x.title for x in service.filter_genre("science fiction")) == ["Science One"]


def test_phase1_groups_by_author_and_year_and_sorts_both_directions() -> None:
    service = EncyclopediaService(InMemoryComicRepository([
        c("1", "Zeta", "Alice", "Fantasy", "1990"),
        c("2", "Alpha", "Alice", "Fantasy", "1990"),
        c("3", "Beta", "Bob", "Fantasy", "1991"),
    ]))
    assert [x.title for x in service.group_by_author("fantasy")["Alice"]] == ["Zeta", "Alpha"]
    assert [x.title for x in service.group_by_year("fantasy")["1990"]] == ["Zeta", "Alpha"]
    assert [x.title for x in service.sorted_titles(service.filter_genre("fantasy"), ascending=True)] == ["Alpha", "Beta", "Zeta"]
    assert [x.title for x in service.sorted_titles(service.filter_genre("fantasy"), ascending=False)] == ["Zeta", "Beta", "Alpha"]


def test_phase1_clear_state_and_safe_display_values() -> None:
    service = EncyclopediaService(InMemoryComicRepository([
        c("1", "The café", "Author", "Fantasy", "1990", isbn=""),
    ]))
    results = service.search_title("café")
    assert results
    assert service.format_record(results[0])["ISBN"] == "missing"
    assert service.format_record(results[0])["Topics"] == ["Topics: A", "Topics: B"]
    service.clear_search_results()
    assert service.current_results == ()
