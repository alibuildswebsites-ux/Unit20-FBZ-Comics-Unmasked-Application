# Security Finding Discovery — Repository Coverage Ledger

**Scope:** `/root/Desktop/Unit20-FBZ-Comics-Unmasked-Application` (repository/scoped-path discovery)
**Mode:** exhaustive scoped-path discovery
**Date:** 2026-08-29

The requested Finding Discovery workflow was applied to the project. The installed skill references require a shared `scan-artifacts.md` and `security-guidance.md`, but those reference files are absent from the installed `/root/Desktop/skills` tree. Project-local `WORKFLOW_RULES.md` was therefore used as repository-specific guidance; no source-file edits were made.

| Row | Boundary / area | Files checked | Family | Source / boundary | Sink / control | Disposition | Evidence |
|---|---|---|---|---|---|---|---|
| COV-01 | CLI entrypoint | `src/fbz/presentation/cli.py` | File/path input | User-supplied dataset/report paths | `Path` file access | suppressed | Paths are used for local reads/writes; no shell, network, query, or dynamic evaluation sink. |
| COV-02 | CSV repository | `src/fbz/repositories/csv_comic_repository.py` | Unsafe parsing / file input | Local dataset path passed by CLI/API | `Path.open` + stdlib CSV parser | suppressed | Header and per-row domain validation are enforced; values remain strings. |
| COV-03 | XML adapter | `src/fbz/repositories/xml_comic_repository.py` | XML parser | Local XML path | `ET.parse` | deferred | Exact parser behavior is not exercised against attacker-controlled XML and the shared security reference is unavailable; no network/entity sink is visible in code. |
| COV-04 | Search services/strategies | `src/fbz/services/search_service.py`, `src/fbz/services/encyclopedia_service.py`, `src/fbz/strategies/search_strategy.py`, `src/fbz/factories/search_strategy_factory.py` | Injection | CLI/application search values | Fixed strategy lookup and in-memory string comparisons | suppressed | No SQL/NoSQL/LDAP/XPath/template/shell/eval sink exists. |
| COV-05 | Domain model / aggregation | `src/fbz/domain/comic.py`, `src/fbz/repositories/aggregating_comic_repository.py` | Parser/helper hazard | CSV/XML-derived strings | Normalization/tokenization/aggregation | suppressed | Pure in-memory transformations; required record ID/title checks before domain record creation. |
| COV-06 | Favourite persistence | `src/fbz/services/favourite_service.py` | File-impact / state | Record IDs from application call sites | JSON file read/write | suppressed | JSON contents must be a list of strings; no path is taken from stored values; file location is an API construction parameter rather than payload-derived. |
| COV-07 | Dataset/report tools | `tools/*.py` | File/process/network | Local project data and generated evidence | Fixed local input/output paths | suppressed | No subprocess, shell, HTTP client, eval, unsafe deserialization, or privileged action observed. External URLs in submission-builder text are citations, not network operations. |
| COV-08 | All runtime Python | 24 canonical source/tool files | RCE / command injection | CLI/application inputs | subprocess/os.system/eval/exec | not_applicable | Repository-wide search found no runtime command/evaluation sink. |
| COV-09 | All runtime Python | 24 canonical source/tool files | SQL/NoSQL/LDAP/XPath/template injection | User/data inputs | query execution/template evaluation | not_applicable | No runtime query or template-evaluation APIs found. |
| COV-10 | All runtime Python | 24 canonical source/tool files | SSRF / callback abuse | User/data inputs | outbound HTTP/socket/network client | not_applicable | No network client or socket usage in runtime application code. |
| COV-11 | All runtime Python | 24 canonical source/tool files | Path traversal / arbitrary file impact | CLI paths / dataset paths | local file reads/writes | suppressed | There is local path I/O, but no attacker-controlled remote request boundary and no evidence of path-derived privileged resource selection. |
| COV-12 | Auth / authorization | All runtime Python | Authn/authz / tenant isolation | Application input | protected object/action authorization | not_applicable | Local CLI/data-processing application has no authentication, multi-user authorization, tenant or protected-object API boundary. |
| COV-13 | Deserialization / object construction | All runtime Python | Unsafe deserialization | Dataset/XML content | pickle/yaml/object loader/reflection | not_applicable | No pickle/yaml loader or dynamic class-resolution construction found. |
| COV-14 | XML/parser helpers | XML adapter + domain | XXE / parser abuse | XML file contents | ElementTree parse / child extraction | deferred | The XML parser is local-file based and no external fetch/DTD control code appears; final parser-hardening closure would benefit from the unavailable shared policy artifact and dedicated hostile-XML test. |
| COV-15 | Submission/evidence generation | `tools/build_submission.py`, reports/docs | Secondary data exposure/config | Local reports/docs | generated artifacts | suppressed | Fixed project-local outputs; no secrets, network exfiltration, or privileged service boundary observed. |

## Frontier result

Across the applicable high-impact families, no distinct reportable candidate was established by static discovery. One XML-parser row remains **deferred** solely because the installed Finding Discovery environment is missing the mandatory shared security-guidance artifact and the repository has no hostile-XML security regression test. This is not a claim that the XML adapter is vulnerable; it is an explicit proof-gap closure.

The initial direct shell verification invocation also failed because `/bin/sh` did not support `pipefail`; the corrected Bash invocation compiled the project successfully. The project test suite then passed **33/33** tests. The real-data acceptance script initially failed only because it was launched without the documented `PYTHONPATH=src`; rerunning with the project-supported environment passed and refreshed `reports/final_acceptance_report.json`.

No source code was modified during discovery.
