# Automated Testing Report — Unit 20 FBZ Application

## 1. Testing strategy

The final regime combines unit, integration, CLI/end-to-end and real-data acceptance testing. The aim is not simply to maximise coverage; it is to verify the behaviour described by the assignment. pytest provides test discovery, assertions and reusable fixtures. The layered approach follows the rationale of the Test Pyramid: fast focused tests form the majority, while broader tests validate integration and user journeys.

## 2. Methods examined

Developer-produced tests contain the FBZ-specific expected behaviour and edge cases. Framework tooling such as pytest provides the execution, fixture and reporting infrastructure. Linear/record-and-playback automation is easy to begin with but is difficult to maintain when the application changes. Data-driven automation is valuable when the same behaviour must be repeated against many datasets; this is particularly relevant to a metadata-processing application. Keyword-driven and hybrid approaches are more useful for larger UI-oriented systems than for this Python CLI application.

## 3. Test matrix

| ID | Requirement | Level | Result |
|---|---|---|---|
| UT-01 | Parse valid record and preserve leading-zero ID | Unit | PASS |
| UT-02 | Reject missing title/required schema | Unit | PASS |
| UT-03 | Tokenise multi-value fields | Unit | PASS |
| UT-04 | Title search | Unit | PASS |
| UT-05 | Author search respects role | Unit | PASS |
| UT-06 | Genre filtering | Unit | PASS |
| UT-07 | Author/year grouping | Unit | PASS |
| UT-08 | A–Z/Z–A ordering | Unit/E2E | PASS |
| UT-09 | Advanced multi-criteria search | Unit | PASS |
| UT-10 | Search list/reset | Unit | PASS |
| UT-11 | >100 notification | Unit/acceptance | PASS |
| IT-01 | CSV → service → favourite flow | Integration | PASS |
| IT-02 | All five official views and row counts | Integration | PASS |
| IT-03 | Real names dataset scale/schema | Integration | PASS |
| E2E-01 | CLI no-result message | E2E | PASS |
| E2E-02 | CLI result display | E2E | PASS |
| E2E-03 | CLI descending order | E2E | PASS |

## 4. Final real-data acceptance

The supplied British Library package was loaded directly. The five views matched the observed acceptance counts: records.csv 57,746; names.csv 117,873; titles.csv 77,280; topics.csv 77,919; classification.csv 57,844. All observed first-record IDs begin with zero and all observed titles are non-empty.

The aggregated names view contains 54,147 unique BL record IDs, meaning 63,726 repeated facet rows are collapsed for the user-facing encyclopedia. Exact genre counts are Fantasy 4,793, Horror 1,929 and Science Fiction 9,356. The final acceptance run also demonstrated an explicit author-role search, a Unicode title, universal missing-value display, missing ISBN display, multi-value genre/name display, both title-order directions and the >100 notification using a real Comic object.

## 5. Results

The current automated suite passes **33 tests**. The final real-data acceptance script exits successfully and writes `reports/final_acceptance_report.json`. The report contains machine-readable evidence for all five views, aggregation, author-role searching, Unicode handling, universal missing-value display, missing ISBN, multi-value data/display, ordering and the threshold notification.

The >100 condition is deliberately exercised 101 times against a real dataset Comic in a deterministic acceptance check. This is stronger than waiting for an uncontrolled demonstration session to happen to cross the threshold. The report records the record ID, count 101 and the notification flag.

## 6. Benefits and drawbacks

Automation gives repeatability, fast regression feedback, consistent edge-case checking and safer refactoring. Its drawbacks are authoring/maintenance cost, execution time as the suite grows, and the risk of false confidence when tests have weak assertions. Unit tests can miss integration defects; integration tests can be slower; end-to-end tests are broader but more fragile. Coverage is therefore treated as a diagnostic indicator, not as a substitute for requirement-based acceptance tests.

## 7. Developer vs vendor/framework tooling

Developer-produced tests encode application semantics: for example, an author search must not return a record solely because the searched person is an editor. pytest supplies the framework mechanics: discovery, fixtures, assertions and reporting. Commercial/vendor frameworks such as TestComplete or Katalon are stronger when teams need visual/UI automation, cross-platform execution, record/playback or enterprise reporting. For this Python CLI, pytest is more proportionate because the dominant risks are parsing, domain logic and service boundaries rather than browser rendering.

## 8. References

Fowler, M. (2012) ‘Test Pyramid’. Available at: https://martinfowler.com/bliki/TestPyramid.html (Accessed: 28 August 2026).

Katalon (2022) ‘Software Test Automation Frameworks | 6 Common Types’. Available at: https://medium.com/@katalon/test-automation-framework-e4e6cc09ea6d (Accessed: 28 August 2026).

pytest (n.d.) *About fixtures*. Available at: https://docs.pytest.org/en/latest/explanation/fixtures.html (Accessed: 28 August 2026).

SmartBear (n.d.) *Test Automation Frameworks*. Available at: https://smartbear.com/learn/automated-testing/test-automation-frameworks/ (Accessed: 28 August 2026).
