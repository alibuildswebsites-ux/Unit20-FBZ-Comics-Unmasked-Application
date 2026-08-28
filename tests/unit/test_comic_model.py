from fbz.domain.comic import Comic


def test_comic_from_mapping_preserves_record_identifier_and_title() -> None:
    comic = Comic.from_mapping({"BL record ID": "000123", "Title": " Test Comic ", "Genre": "Fantasy; Comic books"})
    assert comic.record_id == "000123"
    assert comic.title == "Test Comic"
    assert comic.tokens("genre") == ("Fantasy", "Comic books")


def test_comic_from_mapping_rejects_missing_required_fields() -> None:
    try:
        Comic.from_mapping({"BL record ID": "123"})
    except ValueError as exc:
        assert str(exc) == "Record is missing Title"
    else:
        raise AssertionError("Expected missing title to fail")


def test_comic_matches_text_search_across_relevant_metadata() -> None:
    comic = Comic.from_mapping({
        "BL record ID": "42",
        "Title": "Night Watch",
        "Topics": "Crime; Graphic novels",
        "Name": "Alice Example",
    })
    assert comic.matches_text("graphic")
    assert comic.matches_text("ALICE")
    assert not comic.matches_text("space opera")
