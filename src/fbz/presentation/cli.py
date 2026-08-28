from __future__ import annotations

import argparse
import json
from pathlib import Path

from fbz.domain.comic import Comic
from fbz.repositories.aggregating_comic_repository import AggregatingComicRepository
from fbz.repositories.csv_comic_repository import CsvComicRepository
from fbz.services.encyclopedia_service import ALLOWED_GENRES, EncyclopediaService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fantasy Bazaar Comics Unmasked dataset processor")
    parser.add_argument("dataset", nargs="?", type=Path, default=Path("data/raw/extracted/names.csv"), help="CSV dataset path")
    parser.add_argument("--interactive", action="store_true", help="Run the interactive encyclopedia menu")
    parser.add_argument("--search-type", choices=("title", "author", "genre", "year"))
    parser.add_argument("--query", default="")
    parser.add_argument("--author", default="")
    parser.add_argument("--genre", default="")
    parser.add_argument("--year", default="")
    parser.add_argument("--edition", default="")
    parser.add_argument("--languages", default="")
    parser.add_argument("--name-type", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--field", choices=("classification", "names", "titles", "topics"))
    parser.add_argument("--order", choices=("az", "za"), default="az", help="Sort result titles A-Z or Z-A")
    parser.add_argument("--group-by", choices=("author", "year"), help="Group genre results by author or publication year")
    parser.add_argument("--report", type=Path, help="Write session report as JSON")
    return parser


def _service(dataset: Path) -> EncyclopediaService:
    return EncyclopediaService(AggregatingComicRepository(CsvComicRepository(dataset)))


def _print_results(service: EncyclopediaService, results: list[Comic], limit: int = 20) -> None:
    print(f"Results: {len(results)}")
    for number, comic in enumerate(results[:limit], start=1):
        print(f"[{number}] {comic.title} | {comic.record_id} | {comic.name} | {comic.genre} | {comic.date_of_publication}")
    if not results:
        print("No results found.")


def _interactive(service: EncyclopediaService) -> None:
    print("FBZ Encyclopedia — Comics Unmasked")
    while True:
        print("\n1. Browse genre\n2. Search title\n3. Advanced search\n4. Phase 2 field search\n5. Save current result to search list\n6. View search list\n7. Show top 10 report\n8. Clear current results\n9. Exit")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                genre = input("Genre (Fantasy/Horror/Science fiction): ").strip()
                results = service.filter_genre(genre)
                mode = input("Group by author or year? [author/year]: ").strip().casefold()
                if mode not in {"author", "year"}:
                    raise ValueError("Grouping must be author or year")
                grouped = service.group_results(results, mode)
                ordered = service.sorted_titles(results, ascending=True)
                _print_results(service, ordered)
                print(f"Groups: {len(grouped)}")
            elif choice == "2":
                results = service.search_title(input("Title: "))
                _print_results(service, results)
            elif choice == "3":
                results = service.advanced_search(
                    author=input("Author (optional): "), year=input("Publication year (optional): "),
                    genre=input("Genre (optional): "), edition=input("Edition (optional): "),
                    languages=input("Languages (optional): "), name_type=input("Name type (optional): "),
                    title=input("Title (optional): "),
                )
                _print_results(service, results)
            elif choice == "4":
                field = input("Field (classification/names/titles/topics): ").strip()
                results = service.search_field(field, input("Query: "))
                _print_results(service, results)
            elif choice == "5":
                if not service.current_results:
                    print("There are no current results to save.")
                    continue
                _print_results(service, list(service.current_results))
                try:
                    index = int(input("Result number to save: ")) - 1
                    comic = service.current_results[index]
                except (ValueError, IndexError):
                    print("Invalid result number.")
                else:
                    service.save_to_search_list(comic)
                    print("Saved to in-memory search list.")
            elif choice == "6":
                _print_results(service, list(service.search_list))
            elif choice == "7":
                print("Top 10 search queries:")
                for query, count in service.top_search_queries():
                    print(f"{count:>4}  {query}")
                print("Top 10 search results:")
                for comic, count in service.top_search_results():
                    print(f"{count:>4}  {comic.title} ({comic.record_id})")
                threshold = service.comics_over_threshold(100)
                if threshold:
                    print("Comics included in more than 100 search results:")
                    for comic, count in threshold:
                        print(f"{comic.title} ({comic.record_id}) — {count}")
            elif choice == "8":
                service.clear_search_results()
                print("Current in-memory search results cleared.")
            elif choice == "9":
                service.reset()
                print("Session cleared. Goodbye.")
                return
            else:
                print("Please choose 1–9.")
        except (ValueError, FileNotFoundError) as exc:
            print(f"Error: {exc}")


def _write_report(service: EncyclopediaService, path: Path) -> None:
    report = {
        "top_search_queries": service.top_search_queries(),
        "top_search_results": [
            {"record_id": comic.record_id, "title": comic.title, "count": count}
            for comic, count in service.top_search_results()
        ],
        "over_100_search_results": [
            {"record_id": comic.record_id, "title": comic.title, "count": count}
            for comic, count in service.comics_over_threshold(100)
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    service = _service(args.dataset)
    try:
        if args.interactive:
            _interactive(service)
            return 0
        if args.search_type:
            if args.search_type == "title":
                results = service.search_title(args.query)
            elif args.search_type == "author":
                results = service.search_author(args.query)
            elif args.search_type == "genre":
                results = service.search_by_type("genre", args.query)
            else:
                results = service.search_by_type("year", args.query)
        elif args.field:
            results = service.search_field(args.field, args.query)
        else:
            results = service.advanced_search(
                author=args.author, year=args.year, genre=args.genre, edition=args.edition,
                languages=args.languages, name_type=args.name_type, title=args.title or args.query,
            )
        results = service.sorted_titles(results, ascending=args.order == "az")
        if args.group_by:
            genre = args.genre or (args.query if args.search_type == "genre" else "")
            if not genre:
                raise ValueError("--group-by requires a genre filter")
            grouped = service.group_results(results, args.group_by)
            print(f"Groups by {args.group_by}: {len(grouped)}")
            for group_name, group_items in list(grouped.items())[:20]:
                print(f"  {group_name}: {len(group_items)}")
        _print_results(service, results)
        if args.report:
            _write_report(service, args.report)
        service.clear_search_results()
        return 0
    finally:
        service.reset()


if __name__ == "__main__":
    raise SystemExit(main())
