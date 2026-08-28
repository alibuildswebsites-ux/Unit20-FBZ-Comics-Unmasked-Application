from fbz.domain.comic import Comic
from fbz.services.dataset_statistics import DatasetStatistics


def test_statistics_reports_counts_and_top_tokens() -> None:
    comics = [
        Comic.from_mapping({"BL record ID": "1", "Title": "A", "Genre": "Fantasy;Comic books"}),
        Comic.from_mapping({"BL record ID": "2", "Title": "B", "Genre": "Fantasy"}),
    ]
    assert DatasetStatistics.summary(comics)["records"] == 2
    assert DatasetStatistics.top_searchable_tokens(comics, "genre", 2)[0] == ("fantasy", 2)
