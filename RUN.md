# Assessor Run Guide — Unit 20 FBZ

## 1. Environment

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## 2. Run the application

The default real dataset is the extracted Comics Unmasked names view:

```bash
PYTHONPATH=src .venv/bin/python -m fbz.presentation.cli data/raw/extracted/names.csv --help
PYTHONPATH=src .venv/bin/python -m fbz.presentation.cli data/raw/extracted/names.csv --search-type title --query Batman
PYTHONPATH=src .venv/bin/python -m fbz.presentation.cli data/raw/extracted/names.csv --search-type genre --query fantasy --order za --group-by author
```

Interactive mode:

```bash
PYTHONPATH=src .venv/bin/python -m fbz.presentation.cli data/raw/extracted/names.csv --interactive
```

## 3. Run automated tests

```bash
.venv/bin/pytest -q
.venv/bin/pytest -q --cov=fbz --cov-report=term-missing
```

## 4. Run real-data acceptance

```bash
PYTHONPATH=src .venv/bin/python tools/run_acceptance.py
PYTHONPATH=src .venv/bin/python tools/analyze_real_dataset.py
```

Evidence is written to `reports/`.

## 5. Rebuild final submission files

```bash
PYTHONPATH=src .venv/bin/python tools/build_submission.py
```

Outputs:

- `submission/Unit20_FBZ_Design_and_Programming_Report.docx`
- `submission/Unit20_FBZ_Automated_Testing_Report.docx`
- `submission/Unit20_FBZ_SOLID_OOP_Presentation.pptx`

## 6. Final verification

Read `WORKFLOW_RULES.md` before any future edit. If a command fails, stop implementation, reproduce and root-cause the failure, fix the underlying issue, preflight again, rerun, and only then continue.
