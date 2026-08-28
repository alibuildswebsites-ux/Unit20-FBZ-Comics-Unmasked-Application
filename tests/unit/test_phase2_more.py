from pathlib import Path

from fbz.domain.comic import Comic
from fbz.repositories.comic_repository import InMemoryComicRepository
from fbz.repositories.csv_comic_repository import CsvComicRepository
from fbz.repositories.xml_comic_repository import XmlComicRepository
from fbz.services.encyclopedia_service import EncyclopediaService


def make(rid: str = '1') -> Comic:
    return Comic.from_mapping({
        'BL record ID': rid, 'Title': 'Alpha Title', 'Name': 'Ada',
        'Genre': 'Fantasy', 'Dewey classification': '741.5',
        'Topics': 'Crime;Magic', 'Edition': 'First', 'Languages': 'English',
        'ISBN': '123'
    })


def test_generic_phase2_field_search_supports_classification_and_topics() -> None:
    service = EncyclopediaService(InMemoryComicRepository([make()]))
    assert service.search_field('classification', '741.5')[0].record_id == '1'
    assert service.search_field('topics', 'magic')[0].record_id == '1'
    assert service.search_field('names', 'ada')[0].record_id == '1'
    assert service.search_field('titles', 'alpha')[0].record_id == '1'


def test_xml_repository_loads_multiple_sources_with_same_domain_model(tmp_path: Path) -> None:
    xml = tmp_path / 'source.xml'
    xml.write_text('''<records><record><BL_record_ID>0009</BL_record_ID><Title>Cafe</Title><Name>Ada</Name><Genre>Fantasy</Genre></record></records>''', encoding='utf-8')
    comic = XmlComicRepository(xml).all()[0]
    assert comic.record_id == '0009'
    assert comic.title == 'Cafe'


def test_search_list_does_not_persist_to_disk(tmp_path: Path) -> None:
    service = EncyclopediaService(InMemoryComicRepository([make()]))
    service.save_to_search_list(make())
    assert not list(tmp_path.iterdir())


def test_format_record_displays_all_missing_fields_as_missing() -> None:
    comic = Comic.from_mapping({"BL record ID": "0001", "Title": "Incomplete"})
    service = EncyclopediaService(InMemoryComicRepository([comic]))
    formatted = service.format_record(comic)
    assert formatted["ISBN"] == "missing"
    assert formatted["Publisher"] == "missing"
    assert formatted["Topics"] == "missing"


def test_format_record_displays_multiple_values_consistently() -> None:
    comic = Comic.from_mapping({
        "BL record ID": "0002", "Title": "Multi",
        "Name": "Alice;Bob", "ISBN": "111;222", "Publisher": "One;Two",
        "Genre": "Fantasy;Horror",
    })
    service = EncyclopediaService(InMemoryComicRepository([comic]))
    formatted = service.format_record(comic)
    assert formatted["Name"] == ["Name: Alice", "Name: Bob"]
    assert formatted["ISBN"] == ["ISBN: 111", "ISBN: 222"]
    assert formatted["Publisher"] == ["Publisher: One", "Publisher: Two"]
    assert formatted["Genre"] == ["Genre: Fantasy", "Genre: Horror"]
