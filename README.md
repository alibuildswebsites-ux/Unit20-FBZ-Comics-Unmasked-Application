# Unit 20 — FBZ Dataset Processing Application

## Purpose

This project implements the Fantasy Bazaar (FBZ) dataset-processing application described in the Unit 20 Applied Programming and Design Principles assignment brief. The implementation is structured to make SOLID principles, clean coding, OOP relationships, multiple design patterns, and automated testing visible in both code and evidence.

## Technology

- Python 3.11+
- Standard-library CSV and JSON handling
- pytest + pytest-cov for automated testing

## Architecture

The application is separated into domain, repository, service, strategy, factory, and presentation layers. Business services depend on the `ComicRepository` abstraction rather than a concrete CSV reader. Search algorithms are interchangeable Strategy implementations and are created through a Factory.

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
PYTHONPATH=src .venv/bin/python -m fbz.presentation.cli --help
```

## Test

```bash
.venv/bin/pytest -q
.venv/bin/pytest -q --cov=fbz --cov-report=term-missing
```

## Dataset

The authentic Comics Unmasked 2022 package is already integrated under `data/raw/`, with the five extracted views under `data/raw/extracted/`. The loader preserves CSV values as strings, including identifiers with leading zeros, and validates the required `BL record ID` and `Title` columns. See `RUN.md` for assessor commands and final acceptance steps.

## Mandatory implementation workflow

See `WORKFLOW_RULES.md`. Before every future edit, read the relevant current files and requirements. If anything fails, stop implementation, research/reproduce/root-cause the failure, fix the underlying problem, preflight again, rerun, and only then continue.
