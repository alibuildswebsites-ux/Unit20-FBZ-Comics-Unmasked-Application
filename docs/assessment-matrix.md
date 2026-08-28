# Unit 20 Assessment Compliance Matrix — Evidence-backed Audit

| Criterion | Evidence | Status |
|---|---|---|
| P1 | OOP relationships, SOLID analysis, class diagram, domain/repository/strategy code | PASS |
| P2 | Clean-code research, modular design, data structures, algorithm complexity and concrete FBZ examples | PASS |
| P3 | Real five-view dataset, architecture, class relationships and implemented application | PASS |
| P4 | Layered automated testing strategy, test matrix and real-data acceptance | PASS |
| P5 | Working application with five real CSV views, complete interactive browse/group/sort workflow, search/filter/list/report behaviours, and real-data acceptance | PASS |
| P6 | Unit, integration, E2E and real-data testing methods examined and implemented | PASS |
| P7 | 33 automated tests pass; real-data acceptance script passes | PASS |
| M1 | Creational, structural/architectural and behavioural pattern research, comparison and examples | PASS |
| M2 | Strategy + simple Factory + Repository + aggregation refinement implemented and justified | PASS |
| M3 | Critical effectiveness/trade-off analysis of SOLID, clean coding and patterns | PASS |
| M4 | Developer-produced tests vs framework/vendor approaches; framework and automation-method comparison | PASS |
| D1 | Critical evaluation of SOLID's impact, change boundaries, testability and abstraction cost | PASS |
| D2 | Critical comparison of automated testing across application types and test levels | PASS |

## Functional acceptance evidence

- [x] Authentic Comics Unmasked 2022 package retained under `data/raw/`
- [x] records.csv 57,746 rows
- [x] names.csv 117,873 rows
- [x] titles.csv 77,280 rows
- [x] topics.csv 77,919 rows
- [x] classification.csv 57,844 rows
- [x] Leading-zero BL record IDs preserved
- [x] 117,873 names rows aggregated to 54,147 unique records
- [x] Fantasy 4,793 / Horror 1,929 / Science Fiction 9,356 exact filtering
- [x] Author grouping based on explicit author/writer roles
- [x] Publication-year grouping
- [x] A–Z and Z–A sorting
- [x] Interactive genre → author/year → group selection → A–Z/Z–A workflow
- [x] Manual title search
- [x] Unicode/special-character title search
- [x] Repeated-value tokenisation
- [x] Consistent multi-value display across catalogue fields
- [x] Universal missing-value display (`missing`)
- [x] Missing ISBN display
- [x] Multiple title/row aggregation
- [x] In-memory search list
- [x] Advanced author/year/genre/edition/languages/name-type/title search
- [x] Classification/names/titles/topics searches
- [x] XML repository adapter
- [x] Top-10 query/result reporting
- [x] >100 notification verified at 101 inclusions
- [x] Automated tests: 33 passed
- [x] Real-data acceptance report generated
- [x] Design/implementation report regenerated
- [x] Automated testing report regenerated
- [x] 12-slide presentation with substantive notes regenerated
- [x] Harvard references added

## Final verification commands

```text
.venv/bin/pytest -q
PYTHONPATH=src .venv/bin/python tools/run_acceptance.py
PYTHONPATH=src .venv/bin/python tools/analyze_real_dataset.py
PYTHONPATH=src .venv/bin/python tools/build_submission.py
```
