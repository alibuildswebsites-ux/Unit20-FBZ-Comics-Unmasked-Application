from __future__ import annotations

import csv
from pathlib import Path

RAW = Path('data/raw/extracted/names.csv')
OUT = Path('data/filtered/fbz_comics_names_fantasy_horror_scifi.csv')
ALLOWED = {'fantasy', 'horror', 'science fiction'}


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    total = selected = 0
    with RAW.open('r', encoding='utf-8-sig', newline='') as source, OUT.open('w', encoding='utf-8', newline='') as target:
        reader = csv.DictReader(source)
        if not reader.fieldnames:
            raise ValueError('names.csv has no header')
        writer = csv.DictWriter(target, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            total += 1
            genres = {part.strip().casefold() for part in (row.get('Genre') or '').split(';') if part.strip()}
            if genres & ALLOWED:
                writer.writerow(row)
                selected += 1
    if total < 115_000:
        raise RuntimeError(f'Unexpectedly small names.csv: {total} rows')
    print(f'raw_rows={total}')
    print(f'filtered_rows={selected}')
    print(f'output={OUT}')


if __name__ == '__main__':
    main()
