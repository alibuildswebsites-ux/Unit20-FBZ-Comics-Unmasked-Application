"""Domain model for a Comics Unmasked / FBZ record."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class Comic:
    """Immutable domain representation of one catalogue record."""

    record_id: str
    title: str
    name: str = ""
    dates_associated_with_name: str = ""
    type_of_name: str = ""
    role: str = ""
    other_names: str = ""
    type_of_resource: str = ""
    content_type: str = ""
    material_type: str = ""
    bnb_number: str = ""
    isbn: str = ""
    variant_titles: str = ""
    series_title: str = ""
    number_within_series: str = ""
    country_of_publication: str = ""
    place_of_publication: str = ""
    publisher: str = ""
    date_of_publication: str = ""
    physical_description: str = ""
    dewey_classification: str = ""
    bl_shelfmark: str = ""
    topics: str = ""
    genre: str = ""
    languages: str = ""
    notes: str = ""

    @classmethod
    def from_mapping(cls, row: Mapping[str, str]) -> "Comic":
        """Create a Comic from a CSV mapping, preserving identifiers as strings."""
        aliases = {
            "BL record ID": "record_id",
            "BL record Id": "record_id",
            "Title": "title",
        }
        values: dict[str, str] = {}
        for csv_key, field_name in aliases.items():
            if csv_key in row:
                values[field_name] = _clean(row.get(csv_key))
                break
        if "record_id" not in values:
            values["record_id"] = _clean(row.get("BL record ID") or row.get("BL record Id"))
        if "title" not in values:
            values["title"] = _clean(row.get("Title"))

        field_map = {
            "Name": "name",
            "Dates associated with name": "dates_associated_with_name",
            "Type of name": "type_of_name",
            "Role": "role",
            "Other names": "other_names",
            "Type of resource": "type_of_resource",
            "Content type": "content_type",
            "Material type": "material_type",
            "BNB number": "bnb_number",
            "ISBN": "isbn",
            "Variant titles": "variant_titles",
            "Series title": "series_title",
            "Number within series": "number_within_series",
            "Country of publication": "country_of_publication",
            "Place of publication": "place_of_publication",
            "Publisher": "publisher",
            "Date of publication": "date_of_publication",
            "Physical description": "physical_description",
            "Dewey classification": "dewey_classification",
            "BL shelfmark": "bl_shelfmark",
            "Topics": "topics",
            "Genre": "genre",
            "Languages": "languages",
            "Notes": "notes",
        }
        for csv_key, field_name in field_map.items():
            values[field_name] = _clean(row.get(csv_key))
        if not values["record_id"]:
            raise ValueError("Record is missing BL record ID")
        if not values["title"]:
            raise ValueError("Record is missing Title")
        return cls(**values)

    def tokens(self, field: str) -> tuple[str, ...]:
        """Return normalised multi-value tokens for semicolon/slash-delimited fields."""
        raw = getattr(self, field, "")
        return tuple(token for token in _split_multivalue(raw) if token)

    def matches_text(self, query: str) -> bool:
        needle = _normalise(query)
        return bool(needle) and any(
            needle in _normalise(value)
            for value in (self.title, self.variant_titles, self.name, self.other_names, self.topics, self.notes)
        )


def _clean(value: object) -> str:
    return "" if value is None else str(value).strip()


def _normalise(value: str) -> str:
    return " ".join(value.casefold().split())


def _split_multivalue(value: str) -> tuple[str, ...]:
    if not value:
        return ()
    normalised = value.replace(" / ", ";").replace("|", ";")
    return tuple(part.strip() for part in normalised.split(";") if part.strip())
