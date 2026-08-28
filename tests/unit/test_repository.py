from pathlib import Path

import pytest

from fbz.repositories.csv_comic_repository import CsvComicRepository


def test_csv_repository_loads_records_and_preserves_leading_zero(tmp_path: Path) -> None:
    dataset = tmp_path / "comics.csv"
    dataset.write_text("BL record ID,Title,Genre\n000007,Alpha,Fantasy\n", encoding="utf-8")
    comics = CsvComicRepository(dataset).all()
    assert len(comics) == 1
    assert comics[0].record_id == "000007"
    assert comics[0].title == "Alpha"


def test_csv_repository_rejects_missing_required_column(tmp_path: Path) -> None:
    dataset = tmp_path / "comics.csv"
    dataset.write_text("Title\nAlpha\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing required columns: BL record ID"):
        CsvComicRepository(dataset).all()


def test_csv_repository_reports_invalid_rows(tmp_path: Path) -> None:
    dataset = tmp_path / "comics.csv"
    dataset.write_text("BL record ID,Title\n123,\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid dataset row 2"):
        CsvComicRepository(dataset).all()
