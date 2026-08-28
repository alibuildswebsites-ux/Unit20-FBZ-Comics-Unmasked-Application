# Research Record — Unit 20 FBZ Application

**Research basis:** the supplied Unit 20 assignment brief, the links/references named in its recommended-resources section, the current British Library collection-metadata service, official Python/pytest documentation, and the cited academic/design-pattern sources. Access date for web sources: 28 August 2026.

## 1. Assignment requirements used as the design baseline

The brief requires an OOP/SOLID investigation, a large dataset-processing application, clean coding, one or more design patterns, and an automated testing regime. The application scenario requires the Comics Unmasked data to be loaded into memory, restricted to Fantasy/Horror/Science Fiction for the initial browse flow, grouped by author or publication year, sorted A–Z/Z–A, searched by title, robust to special characters/missing values/repeated values/multiple titles, and supported by an in-memory search list and advanced multi-criteria search. The later scenario also requires top-10 search reporting and a notification when a comic appears in more than 100 search results.

## 2. Dataset research

The brief identifies the British Library Comics Unmasked Researcher Format package and describes five CSV views: records, names, titles, topics and classification. The current British Library collection metadata service states that Researcher Format CSV datasets are now available through the British Library Research Repository (British Library, n.d.). The project therefore keeps the exact 2022 archive referenced by the brief under `data/raw/` and the five extracted views under `data/raw/extracted/`.

The real package was inspected rather than replaced with a synthetic dataset. The observed views are: records.csv 57,746 rows; names.csv 117,873; titles.csv 77,280; topics.csv 77,919; classification.csv 57,844. Every observed BL record ID begins with a leading zero. The names view contains 117,873 facet rows but only 54,147 unique record IDs, so the user-facing encyclopedia must aggregate repeated facet rows without changing the raw source views.

The assignment annex explains that repeated values may be separated by semicolons and that multiple facet values can occur within one record. The implementation therefore keeps source values as strings, tokenises multi-value fields at the domain boundary, and uses a repository decorator to collapse repeated BL record IDs into one user-facing record.

## 3. OOP relationships research

Khan (2023) distinguishes inheritance, association, composition and aggregation. The project uses inheritance where a common behavioural contract is meaningful (`ComicRepository` and `SearchStrategy`), association/dependency where application services receive repository abstractions, and composition where a repository contains a cached sequence of domain objects. The design intentionally avoids forcing inheritance into the domain model merely for reuse. This supports the brief's requirement to investigate class relationships rather than merely list OOP vocabulary.

## 4. Clean-code research

Mark (2023) describes clean code as readable, understandable and modifiable and emphasises meaningful naming, focused functions and maintainability. freeCodeCamp's 2023 clean-code handbook also connects clean code with effectiveness, efficiency, simplicity, modularisation, naming and algorithmic complexity (Cocca, 2023). These sources influenced the implementation's explicit names, type hints, small service methods, validation at input boundaries, immutable domain records and separated presentation/data-access layers.

The important application-specific conclusion is that clean coding is not just formatting. In FBZ, a single large procedure could parse CSV, aggregate records, filter genres, sort titles and print the CLI. That design would mix I/O, business rules and presentation. The final design separates these concerns, which makes the data structures and algorithms independently testable and makes their complexity easier to reason about.

## 5. SOLID research

Chebanyuk and Markov (2016) examine ways of checking class diagrams against the five SOLID principles: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation and Dependency Inversion. The project applies these principles as design constraints rather than as labels added after implementation.

- **SRP:** CSV parsing, domain modelling, searching, favourites and presentation have separate responsibilities.
- **OCP:** new search algorithms can be added through `SearchStrategy` implementations.
- **LSP:** concrete repositories and search strategies satisfy their abstract contracts.
- **ISP:** the repository and strategy contracts are deliberately small.
- **DIP:** services depend on `ComicRepository`, not `CsvComicRepository`.

The research also supports a critical conclusion: SOLID is useful when it creates meaningful change boundaries, but abstraction has a cost. A tiny one-off script could be shorter without repositories and strategies. FBZ has several search behaviours, multiple data views and a testing requirement, so the additional indirection has a defensible purpose.

## 6. Design-pattern research

Refactoring.Guru classifies patterns into creational, structural and behavioural families and describes Strategy as a behavioural pattern for interchangeable algorithms (Refactoring.Guru, n.d.). Tutorialspoint similarly describes the three broad categories and stresses programming to an interface rather than an implementation (Tutorialspoint, n.d.).

The project uses three pattern/architecture techniques for concrete problems:

1. **Strategy — behavioural:** title, author, genre and year searches are interchangeable algorithms.
2. **Simple Factory — creational technique:** `SearchStrategyFactory` centralises selection/construction of a strategy. It is documented as a simple factory, not incorrectly claimed to be the formal GoF Factory Method.
3. **Repository — structural/architectural technique:** storage concerns are separated from application services; an XML repository can satisfy the same repository contract.

Subburaj, Jekese and Hwata (2015) identify benefits such as reuse, flexibility and extensibility but also warn against inappropriate pattern use and pattern overload. That evidence directly supports the project's restraint: the application does not add patterns merely to increase the pattern count.

## 7. Automated-testing research

The brief asks for different automated-testing methods, developer-produced versus vendor-provided tools, and benefits/drawbacks. pytest documentation describes fixtures as explicit, modular and scalable, supporting reusable test contexts (pytest, n.d.). Katalon (2022) describes linear, modular, library-architecture, data-driven, keyword-driven and hybrid automation frameworks. SmartBear (n.d.) likewise describes common framework styles and notes that record-and-playback approaches can be easy to start but costly to maintain. Fowler's Test Pyramid argues for a larger base of fast, focused tests and fewer expensive broad-stack/UI tests (Fowler, 2012).

The FBZ test regime therefore uses unit tests as the broad base, integration tests for repository/service boundaries, CLI/end-to-end tests for user-visible flows, and real-data acceptance tests for the official five-view dataset. Coverage is treated as a diagnostic rather than as proof of correctness.

## 8. Research-to-implementation conclusions

The research produced four concrete implementation decisions. First, preserve the dataset's string identifiers and repeated-value semantics. Second, preserve name/role relationships so an author search cannot accidentally return an editor or illustrator. Third, use Strategy/Factory/Repository only where they solve actual variation. Fourth, verify requirements with layered tests and real data instead of declaring success because the application starts.

## References

British Library (n.d.) *Collection metadata services*. Available at: https://www.bl.uk/services/collection-metadata-services (Accessed: 28 August 2026).

Chebanyuk, E. and Markov, K. (2016) ‘An Approach to Class Diagrams Verification According to SOLID Design Principles’, *Proceedings of MODELSWARD 2016*, pp. 435–441. doi: 10.5220/0005830104350441.

Cocca, G. (2023) ‘How to Write Clean Code – Tips and Best Practices (Full Handbook)’, freeCodeCamp, 15 May. Available at: https://www.freecodecamp.org/news/how-to-write-clean-code/ (Accessed: 28 August 2026).

Fowler, M. (2012) ‘Test Pyramid’, Martin Fowler, 1 May. Available at: https://martinfowler.com/bliki/TestPyramid.html (Accessed: 28 August 2026).

Katalon (2022) ‘Software Test Automation Frameworks | 6 Common Types’, 28 November. Available at: https://medium.com/@katalon/test-automation-framework-e4e6cc09ea6d (Accessed: 28 August 2026).

Khan, M.H. (2023) ‘Understanding Object-Oriented Relationships: Inheritance, Association, Composition, and Aggregation’, Medium, 14 October. Available at: https://medium.com/@humzakhalid94/understanding-object-oriented-relationships-inheritance-association-composition-and-aggregation-4d298494ac1c (Accessed: 28 August 2026).

Mark, M. (2023) ‘Writing Clean Code: Best Practices and Principles’, DEV Community, 16 September. Available at: https://dev.to/favourmark05/writing-clean-code-best-practices-and-principles-3amh (Accessed: 28 August 2026).

pytest (n.d.) *About fixtures*. Available at: https://docs.pytest.org/en/latest/explanation/fixtures.html (Accessed: 28 August 2026).

Refactoring.Guru (n.d.) *Design Patterns*. Available at: https://refactoring.guru/design-patterns (Accessed: 28 August 2026).

SmartBear (n.d.) *Test Automation Frameworks*. Available at: https://smartbear.com/learn/automated-testing/test-automation-frameworks/ (Accessed: 28 August 2026).

Subburaj, R., Jekese, G. and Hwata, C. (2015) ‘Impact of Object Oriented Design Patterns on Software Development’, *International Journal of Scientific & Engineering Research*, 6(2), pp. 961–966.

Tutorialspoint (n.d.) *Design Patterns – Overview*. Available at: https://www.tutorialspoint.com/design_pattern/design_pattern_overview.htm (Accessed: 28 August 2026).
