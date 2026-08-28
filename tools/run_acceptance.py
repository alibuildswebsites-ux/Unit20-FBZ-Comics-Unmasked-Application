from __future__ import annotations

import json
from pathlib import Path

from fbz.domain.comic import Comic
from fbz.repositories.aggregating_comic_repository import AggregatingComicRepository
from fbz.repositories.csv_comic_repository import CsvComicRepository
from fbz.repositories.comic_repository import InMemoryComicRepository
from fbz.services.encyclopedia_service import ALLOWED_GENRES, EncyclopediaService

ROOT = Path('data/raw/extracted')
REPORT = Path('reports/final_acceptance_report.json')
EXPECTED_ROWS = {
    'records.csv': 57_746,
    'names.csv': 117_873,
    'titles.csv': 77_280,
    'topics.csv': 77_919,
    'classification.csv': 57_844,
}


def serialise(items):
    return [
        {
            'record_id': x.record_id,
            'title': x.title,
            'name': x.name,
            'authors': list(x.authors()),
            'genre': x.genre,
            'year': x.date_of_publication,
        }
        for x in items
    ]


def main() -> None:
    views = {}
    for filename, expected in EXPECTED_ROWS.items():
        comics = CsvComicRepository(ROOT / filename).all()
        views[filename] = {
            'rows': len(comics),
            'expected_rows': expected,
            'pass': len(comics) == expected and comics[0].record_id.startswith('0') and bool(comics[0].title),
        }
        if not views[filename]['pass']:
            raise AssertionError(f'Five-view acceptance failed for {filename}: {views[filename]}')

    source = AggregatingComicRepository(CsvComicRepository(ROOT / 'names.csv'))
    comics = list(source.all())
    service = EncyclopediaService(source)
    genre_counts = {genre: len(service.filter_genre(genre)) for genre in ALLOWED_GENRES}
    expected_genres = {'fantasy': 4_793, 'horror': 1_929, 'science fiction': 9_356}
    if genre_counts != expected_genres:
        raise AssertionError(f'Unexpected real-data genre counts: {genre_counts}')

    examples = {
        'fantasy': service.filter_genre('fantasy')[:3],
        'horror': service.filter_genre('horror')[:3],
        'science fiction': service.filter_genre('science fiction')[:3],
        'title_search': service.search_title('batman')[:5],
        'advanced_search': service.advanced_search(genre='fantasy', year='2000')[:5],
        'classification_search': service.search_field('classification', '741.5')[:5],
        'names_search': service.search_field('names', 'Lee, Stan')[:5],
        'titles_search': service.search_field('titles', 'Batman')[:5],
        'topics_search': service.search_field('topics', 'Crime')[:5],
    }

    # Requirement-specific real-data checks.
    real_author = next((author for comic in comics for author in comic.authors()), None)
    if not real_author:
        raise AssertionError('No explicit author-role contributor found in the real names view')
    author_results = service.search_author(real_author)
    if not any(real_author.casefold() in a.casefold() for comic in author_results for a in comic.authors()):
        raise AssertionError('Author search did not return an explicit author contributor')

    special_character = next((comic for comic in comics if any(ord(ch) > 127 for ch in comic.title)), None)
    if special_character is None or not service.search_title(special_character.title[: max(1, min(12, len(special_character.title))) ]):
        raise AssertionError('Unicode/special-character title search was not demonstrated on the real dataset')

    missing_isbn = next((comic for comic in comics if not comic.isbn), None)
    if missing_isbn is None or service.format_record(missing_isbn)['ISBN'] != 'missing':
        raise AssertionError('Missing ISBN display rule was not demonstrated on the real dataset')

    multi_value = next((comic for comic in comics if len(comic.tokens('genre')) > 1), None)
    if multi_value is None or len(multi_value.tokens('genre')) < 2:
        raise AssertionError('Multi-value genre handling was not demonstrated on the real dataset')

    # Multiple rows / titles are evidenced by raw-vs-aggregated cardinality.
    aggregation_evidence = {
        'raw_names_rows': 117_873,
        'unique_record_ids': len(comics),
        'duplicates_collapsed': 117_873 - len(comics),
        'pass': len(comics) == 54_147,
    }
    if not aggregation_evidence['pass']:
        raise AssertionError(f'Unexpected aggregation cardinality: {aggregation_evidence}')

    # Deterministically exercise the >100 notification against a real Comic.
    threshold_messages: list[str] = []
    threshold_service = EncyclopediaService(InMemoryComicRepository([comics[0]]), alert_callback=threshold_messages.append)
    for _ in range(101):
        threshold_service.search_title(comics[0].title)
    threshold_evidence = {
        'record_id': comics[0].record_id,
        'count': threshold_service.search_count(comics[0].record_id),
        'notification_triggered': bool(threshold_messages),
        'pass': threshold_service.search_count(comics[0].record_id) == 101 and bool(threshold_messages),
    }
    if not threshold_evidence['pass']:
        raise AssertionError(f'>100 threshold acceptance failed: {threshold_evidence}')

    # Verify both title ordering directions on a deterministic subset.
    sample = service.filter_genre('fantasy')[:20]
    ascending = service.sorted_titles(sample, ascending=True)
    descending = service.sorted_titles(sample, ascending=False)
    ordering_evidence = {
        'ascending': [x.title for x in ascending[:5]],
        'descending': [x.title for x in descending[:5]],
        'pass': [x.title for x in ascending] == sorted((x.title for x in sample), key=str.casefold)
        and [x.title for x in descending] == sorted((x.title for x in sample), key=str.casefold, reverse=True),
    }
    if not ordering_evidence['pass']:
        raise AssertionError('A-Z/Z-A ordering acceptance failed')

    result = {
        'source': 'British Library Comics Unmasked 2022 researcher-format package recovered from Internet Archive snapshot',
        'raw_names_rows': 117_873,
        'unique_names_view_records': len(comics),
        'five_view_acceptance': views,
        'genre_record_counts': genre_counts,
        'expected_genre_record_counts': expected_genres,
        'aggregation_evidence': aggregation_evidence,
        'author_acceptance': {'query': real_author, 'result_count': len(author_results), 'sample': serialise(author_results[:5]), 'pass': True},
        'special_character_acceptance': {'record_id': special_character.record_id, 'title': special_character.title, 'pass': True},
        'missing_isbn_acceptance': {'record_id': missing_isbn.record_id, 'title': missing_isbn.title, 'pass': True},
        'multi_value_acceptance': {'record_id': multi_value.record_id, 'genre_tokens': list(multi_value.tokens('genre')), 'pass': True},
        'ordering_acceptance': ordering_evidence,
        'threshold_acceptance': threshold_evidence,
        'examples': {key: serialise(value) for key, value in examples.items()},
        'top_search_queries': service.top_search_queries(),
        'top_search_results': [{'record_id': c.record_id, 'title': c.title, 'count': n} for c, n in service.top_search_results()],
        'over_100': [{'record_id': c.record_id, 'title': c.title, 'count': n} for c, n in service.comics_over_threshold(100)],
    }
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
