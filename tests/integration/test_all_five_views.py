from pathlib import Path

from fbz.repositories.csv_comic_repository import CsvComicRepository

ROOT = Path(__file__).parents[2] / 'data/raw/extracted'
EXPECTED_ROWS = {
    'records.csv': 57746,
    'names.csv': 117873,
    'titles.csv': 77280,
    'topics.csv': 77919,
    'classification.csv': 57844,
}


def test_all_five_official_views_load() -> None:
    for filename, expected in EXPECTED_ROWS.items():
        comics = CsvComicRepository(ROOT / filename).all()
        assert len(comics) == expected, filename
        assert comics[0].record_id.startswith('0'), filename
        assert comics[0].title, filename
