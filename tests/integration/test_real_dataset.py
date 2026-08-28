from pathlib import Path

from fbz.repositories.csv_comic_repository import CsvComicRepository
from fbz.services.encyclopedia_service import ALLOWED_GENRES, EncyclopediaService


PROJECT_ROOT = Path(__file__).parents[2]
RAW_NAMES = PROJECT_ROOT / 'data/raw/extracted/names.csv'
FILTERED_NAMES = PROJECT_ROOT / 'data/filtered/fbz_comics_names_fantasy_horror_scifi.csv'


def test_real_names_dataset_has_expected_scale_and_schema() -> None:
    comics = CsvComicRepository(RAW_NAMES).all()
    assert len(comics) == 117_873
    assert all(comic.record_id for comic in comics)
    assert all(comic.title for comic in comics)


def test_real_filtered_dataset_contains_only_three_requested_genres() -> None:
    comics = CsvComicRepository(FILTERED_NAMES).all()
    assert len(comics) == 38_037
    observed = {token.casefold() for comic in comics for token in comic.tokens('genre') if token.casefold() in ALLOWED_GENRES}
    assert observed == set(ALLOWED_GENRES)
