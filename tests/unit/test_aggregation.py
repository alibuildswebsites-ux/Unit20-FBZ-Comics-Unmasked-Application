from fbz.domain.comic import Comic
from fbz.repositories.comic_repository import InMemoryComicRepository
from fbz.repositories.aggregating_comic_repository import AggregatingComicRepository


def test_multiple_rows_for_one_record_are_merged_into_one_record_entry() -> None:
    rows = [
        Comic.from_mapping({"BL record ID": "0001", "Title": "Main", "Date of publication": "1990", "ISBN": "111", "Name": "Alice"}),
        Comic.from_mapping({"BL record ID": "0001", "Title": "Variant", "Date of publication": "1991", "ISBN": "222", "Name": "Bob"}),
        Comic.from_mapping({"BL record ID": "0002", "Title": "Other", "Date of publication": "2000"}),
    ]
    aggregated = AggregatingComicRepository(InMemoryComicRepository(rows)).all()
    assert len(aggregated) == 2
    first = aggregated[0]
    assert first.record_id == "0001"
    assert first.title == "Main"
    assert "Variant" in first.variant_titles
    assert set(first.date_of_publication.split(";")) == {"1990", "1991"}
    assert set(first.isbn.split(";")) == {"111", "222"}
    assert set(first.name.split(";")) == {"Alice", "Bob"}
