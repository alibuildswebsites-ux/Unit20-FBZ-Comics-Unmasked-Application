from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from fbz.repositories.aggregating_comic_repository import AggregatingComicRepository
from fbz.repositories.csv_comic_repository import CsvComicRepository
from fbz.services.dataset_statistics import DatasetStatistics

ROOT = Path('data/raw/extracted')
OUT = Path('reports/real_dataset_analysis.json')
FILES = ['records.csv','names.csv','titles.csv','topics.csv','classification.csv']


def rows_and_header(path: Path) -> tuple[int, list[str], int, int]:
    import csv
    rows = 0; missing_title = 0; leading_zero = 0
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f)
        header = r.fieldnames or []
        for row in r:
            rows += 1
            if not (row.get('Title') or '').strip(): missing_title += 1
            rid = (row.get('BL record ID') or '').strip()
            if rid.startswith('0'): leading_zero += 1
    return rows, header, missing_title, leading_zero


def main() -> None:
    result = {'source_archive':'data/raw/ComicsResearcherFormat_202204_csv.zip','files':{}}
    for filename in FILES:
        rows, header, missing_title, leading_zero = rows_and_header(ROOT/filename)
        result['files'][filename] = {'rows':rows,'columns':len(header),'header':header,'missing_title':missing_title,'leading_zero_ids':leading_zero}
    names = CsvComicRepository(ROOT/'names.csv')
    aggregate = AggregatingComicRepository(names)
    comics = aggregate.all()
    stats = DatasetStatistics.summary(comics)
    author_names = sorted({author for comic in comics for author in comic.authors()})
    result['names_view_aggregated'] = {
        'raw_rows': 117873,
        'unique_record_ids': len(comics),
        'duplicates_collapsed': 117873 - len(comics),
        'explicit_author_contributors': len(author_names),
        **stats,
        'top_genres': DatasetStatistics.top_searchable_tokens(comics,'genre',20),
    }
    result['allowed_genre_records'] = {}
    for genre in ('fantasy','horror','science fiction'):
        subset = [c for c in comics if any(genre == t.casefold() for t in c.tokens('genre'))]
        result['allowed_genre_records'][genre] = len(subset)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__': main()
