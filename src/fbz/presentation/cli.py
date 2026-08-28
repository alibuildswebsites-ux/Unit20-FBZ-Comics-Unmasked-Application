from __future__ import annotations

import argparse
from pathlib import Path

from fbz.domain.search_criteria import SearchCriteria
from fbz.repositories.csv_comic_repository import CsvComicRepository
from fbz.services.favourite_service import FavouriteService
from fbz.services.search_service import SearchService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fantasy Bazaar Comics Unmasked dataset processor")
    parser.add_argument("dataset", type=Path, help="CSV dataset path")
    parser.add_argument("--search-type", choices=("title", "author", "genre", "year"))
    parser.add_argument("--query", default="")
    parser.add_argument("--author", default="")
    parser.add_argument("--genre", default="")
    parser.add_argument("--year", default="")
    parser.add_argument("--favourite-id")
    parser.add_argument("--favourites-file", type=Path, default=Path("data/favourites.json"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    search = SearchService(CsvComicRepository(args.dataset))
    if args.search_type:
        results = search.search(args.search_type, args.query)
    else:
        results = search.advanced_search(
            SearchCriteria(text=args.query, author=args.author, genre=args.genre, year=args.year)
        )
    print(f"Results: {len(results)}")
    for comic in results[:20]:
        print(f"{comic.record_id}\t{comic.title}\t{comic.name}\t{comic.genre}\t{comic.date_of_publication}")
    if not results:
        print("No results found.")
    if args.favourite_id:
        favourites = FavouriteService(args.favourites_file)
        print("Favourite saved." if favourites.add(args.favourite_id) else "Already a favourite.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
