from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

from fbz.repositories.aggregating_comic_repository import AggregatingComicRepository
from fbz.repositories.csv_comic_repository import CsvComicRepository
from fbz.services.encyclopedia_service import ALLOWED_GENRES, EncyclopediaService

ROOT = Path('data/raw/extracted')
REPORT = Path('reports/final_acceptance_report.json')


def main() -> None:
    names = AggregatingComicRepository(CsvComicRepository(ROOT / 'names.csv'))
    comics = list(names.all())
    service = EncyclopediaService(names)
    genre_counts = {genre: len(service.filter_genre(genre)) for genre in ALLOWED_GENRES}
    examples = {
        'fantasy': service.filter_genre('fantasy')[:3],
        'horror': service.filter_genre('horror')[:3],
        'science fiction': service.filter_genre('science fiction')[:3],
        'title_search': service.search_title('batman')[:5],
        'advanced_search': service.advanced_search(genre='fantasy', year='2000')[:5],
        'classification_search': service.search_field('classification', '741.5')[:5],
        'names_search': service.search_field('names', 'Lee, Stan')[:5],
        'topics_search': service.search_field('topics', 'Crime')[:5],
    }
    def serialise(items):
        return [{'record_id': x.record_id, 'title': x.title, 'name': x.name, 'genre': x.genre, 'year': x.date_of_publication} for x in items]
    result = {
        'source': 'British Library Comics Unmasked 2022 researcher-format package recovered from Internet Archive snapshot',
        'raw_names_rows': 117873,
        'unique_names_view_records': len(comics),
        'genre_record_counts': genre_counts,
        'examples': {key: serialise(value) for key, value in examples.items()},
        'top_search_queries': service.top_search_queries(),
        'top_search_results': [{'record_id': c.record_id, 'title': c.title, 'count': n} for c,n in service.top_search_results()],
        'over_100': [{'record_id': c.record_id, 'title': c.title, 'count': n} for c,n in service.comics_over_threshold(100)],
    }
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__': main()
