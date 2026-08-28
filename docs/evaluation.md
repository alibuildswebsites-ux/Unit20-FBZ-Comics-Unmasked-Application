# Evaluation and Higher-Grade Analysis

## M3 — Effectiveness of SOLID, clean coding and patterns

SOLID is effective here because each business concern is independently replaceable and testable. Dependency inversion is particularly valuable: search logic can run against an in-memory repository, so tests do not require the real CSV file. Strategy reduces a growing conditional search method into independently testable algorithms. The trade-off is additional classes and abstractions for a relatively small application. The design is therefore more maintainable and extensible, but it has a higher conceptual overhead than a procedural script.

Clean coding improves the predictability of the data structures and algorithms: the domain model is immutable, parsing is isolated, and search operations operate on explicit sequences. This reduces accidental coupling and makes algorithmic complexity easier to reason about.

Patterns are effective when they address actual variation. Strategy directly matches the requirement for multiple search behaviours. The factory centralises strategy construction. Repository separates storage concerns. Adding patterns beyond those justified by actual variation would risk over-engineering.

## D1 — Impact of SOLID on OOP application development

The strongest impact is architectural rather than cosmetic. SOLID moves change boundaries into explicit abstractions. A new storage format can replace the CSV repository while the search service continues to depend on the repository contract. A new search algorithm can be added without changing existing strategies. This reduces the blast radius of change and improves testability. The cost is extra indirection, interfaces/abstract classes, and a learning curve. For a larger or evolving application those costs are justified; for a tiny one-off script they may not be.

## D2 — Automated testing across applications

Automated testing is especially valuable when software has repeated workflows, persistent data, complex business rules, or frequent change. It is less valuable as a sole testing mechanism for highly visual, usability-heavy or exploratory systems where human evaluation remains necessary. Unit tests offer rapid regression feedback; integration tests cover component contracts; end-to-end tests validate user journeys. The highest confidence comes from a layered combination rather than treating one level as sufficient.

Automated testing also introduces maintenance cost. Tests become part of the software system and must evolve with legitimate requirement changes. Poorly isolated end-to-end suites can create slow, flaky pipelines, while over-mocked unit tests can validate test doubles instead of real behaviour. The appropriate balance depends on application risk, change frequency and the cost of failure.

## Pattern research notes

Design patterns are reusable design blueprints, not snippets that should be copied without context. Refactoring.Guru classifies classic patterns as creational, structural and behavioural and describes Strategy as a behavioural pattern for interchangeable algorithms. citeturn838871search6turn838871search4turn838871search2
