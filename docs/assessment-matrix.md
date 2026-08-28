# Unit 20 Assessment Compliance Matrix — Final Audit

| Criterion | Evidence | Status |
|---|---|---|
| P1 | OOP/SOLID sections in design report; class diagram; `src/fbz/domain`, repositories and strategies | PASS |
| P2 | Clean coding + data structures/algorithms section; complexity discussion | PASS |
| P3 | Layered design, real dataset analysis, architecture/class diagrams | PASS |
| P4 | Automated testing regime, matrix and test hierarchy | PASS |
| P5 | Working FBZ application under `src/fbz/`, five real CSV views integrated | PASS |
| P6 | Unit/integration/E2E/real-data testing approaches compared | PASS |
| P7 | 27 automated tests passing in final run | PASS |
| M1 | Creational, structural/architectural and behavioural pattern analysis | PASS |
| M2 | Strategy + Factory + Repository + aggregation adapter implemented | PASS |
| M3 | Design report evaluates effectiveness/trade-offs | PASS |
| M4 | Developer-produced tests vs pytest tooling comparison | PASS |
| D1 | SOLID impact evaluation with benefits/costs | PASS |
| D2 | Automated testing benefits/drawbacks across application types | PASS |

## Functional acceptance audit

- [x] Real Comics Unmasked package integrated under `data/raw/`
- [x] Five official CSV views extracted under `data/raw/extracted/`
- [x] `records.csv` 57,746 rows / 27 columns
- [x] `names.csv` 117,873 rows / 27 columns
- [x] `titles.csv` 77,280 rows / 27 columns
- [x] `topics.csv` 77,919 rows / 28 columns
- [x] `classification.csv` 57,844 rows / 27 columns
- [x] Leading-zero BL record IDs preserved
- [x] Multiple rows aggregated by BL record ID for user-facing records
- [x] Fantasy/Horror/Science Fiction exact filtering
- [x] Author grouping
- [x] Publication-year grouping
- [x] A–Z and Z–A title sorting
- [x] Manual title search
- [x] Special-character/Unicode-safe handling
- [x] Repeated-value tokenisation
- [x] Missing ISBN display handling
- [x] In-memory search list
- [x] Advanced search: author/year/genre/edition/languages/name type/title
- [x] Phase 2 searches: classification/names/titles/topics
- [x] XML source adapter
- [x] Search telemetry
- [x] Top-10 query/result reporting
- [x] >100 search-result threshold notification
- [x] Reset/clear behaviour
- [x] Automated tests
- [x] Final design report
- [x] Final testing report
- [x] 10-minute presentation with speaker notes
- [x] Architecture and class diagrams

## Verification record

Final command: `.venv/bin/pytest -q --cov=fbz --cov-report=term-missing`

Result: **27 passed**. Overall measured coverage in the final run: **82%**. The lower total compared with the earlier 93% run is primarily because the final implementation added the interactive CLI and additional production paths; coverage is reported transparently rather than hidden. The functional tests and real-data acceptance tests all pass.
