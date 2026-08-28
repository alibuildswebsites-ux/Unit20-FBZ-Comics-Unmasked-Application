from pathlib import Path

from fbz.presentation.cli import main


def test_cli_reports_no_results_and_returns_success(tmp_path: Path, capsys) -> None:
    dataset = tmp_path / "comics.csv"
    dataset.write_text("BL record ID,Title,Genre\n1,Alpha,Fantasy\n", encoding="utf-8")
    assert main([str(dataset), "--search-type", "title", "--query", "missing"]) == 0
    output = capsys.readouterr().out
    assert "Results: 0" in output
    assert "No results found." in output


def test_cli_supports_ascending_and_descending_title_order(tmp_path: Path, capsys) -> None:
    dataset = tmp_path / "comics.csv"
    dataset.write_text("BL record ID,Title,Genre\n1,Zeta,Fantasy\n2,Alpha,Fantasy\n", encoding="utf-8")
    assert main([str(dataset), "--search-type", "genre", "--query", "fantasy", "--order", "za"]) == 0
    output = capsys.readouterr().out
    assert output.index("Zeta") < output.index("Alpha")


def test_cli_reports_results(tmp_path: Path, capsys) -> None:
    dataset = tmp_path / "comics.csv"
    dataset.write_text("BL record ID,Title,Genre\n1,Alpha,Fantasy\n", encoding="utf-8")
    assert main([str(dataset), "--search-type", "genre", "--query", "fantasy"]) == 0
    output = capsys.readouterr().out
    assert "Results: 1" in output
    assert "Alpha" in output
