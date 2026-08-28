# Unit 20 — SOLID Development Principles in OOP

## Slide 1 — FBZ problem and objective
**On slide**
- Fantasy Bazaar needs a maintainable application for Comics Unmasked metadata.
- Goal: useful data processing + sound OOP design.

**Speaker notes**
The scenario is a comic-book shop that needs an encyclopedia around the British Library Comics Unmasked metadata. The important point is that this is not only a search script: the assignment evaluates how the application is designed, implemented and tested. The solution therefore separates the domain model, data access, application services and presentation. We use the real five-view dataset rather than a toy dataset, and the final evidence is generated from that data. This gives us a concrete way to demonstrate SOLID, clean coding, design patterns and automated testing rather than discussing them as isolated theory.

## Slide 2 — OOP foundations
**On slide**
- Encapsulation
- Abstraction
- Inheritance
- Polymorphism

**Speaker notes**
Encapsulation is visible in `Comic`, which owns catalogue state and operations such as tokenisation and author extraction. Abstraction is visible in `ComicRepository` and `SearchStrategy`, because callers use a small contract rather than depending on implementation details. Inheritance is used only where substitutability is meaningful: CSV, in-memory and XML repositories satisfy the repository contract, while concrete search strategies satisfy the strategy contract. Polymorphism then allows the same search service to work with title, author, genre or year strategies. The design avoids unnecessary domain inheritance because composition and dependency injection are more appropriate for the catalogue records.

## Slide 3 — Class relationships
**On slide**
- Services depend on repository abstractions.
- Strategies share a common contract.
- `Comic` contains contributor relationships.

**Speaker notes**
There are several relationships to distinguish. A service has a dependency on a repository because it needs data but should not care whether that data comes from CSV, XML or memory. The repository contains a sequence of `Comic` objects, which is a composition of application state. The most important domain refinement is `Contributor`: the real names view has a person together with a role such as author, artist or editor. Earlier flattening of these values could make an author search return an editor. The final model preserves name and role together and derives `Comic.authors()` from explicit author or writer roles.

## Slide 4 — SOLID in FBZ
**On slide**
- SRP
- OCP
- LSP
- ISP
- DIP

**Speaker notes**
Single Responsibility is demonstrated by keeping CSV parsing, domain modelling, search, favourites and presentation separate. Open/Closed is demonstrated by adding search algorithms as new Strategy implementations rather than modifying the existing service. Liskov Substitution means concrete repositories and strategies can be substituted wherever their contracts are expected. Interface Segregation is achieved with small repository and strategy contracts instead of one large interface. Dependency Inversion is especially valuable: services depend on `ComicRepository`, so tests can inject an in-memory repository. Chebanyuk and Markov's work supports treating these principles as structural design constraints rather than decorative terminology.

## Slide 5 — Clean coding
**On slide**
- Explicit names and types
- Focused methods
- Validation at boundaries
- Immutable domain state
- Separated I/O and business logic

**Speaker notes**
Clean coding is more than formatting. The research describes clean code in terms of readability, maintainability, simplicity and modularisation. In FBZ, a monolithic procedure would parse CSV, aggregate rows, filter genres, sort titles and print output. That would make defects difficult to isolate and algorithmic complexity difficult to explain. Instead, the CSV repository parses, the aggregation repository handles repeated record IDs, the service coordinates business rules, and the CLI handles interaction. This makes each operation easier to test and change. It also keeps data structures visible: tuples hold immutable records, lists hold result sequences, and dictionaries support grouped results.

## Slide 6 — Data structures and algorithms
**On slide**
- Tuple-backed in-memory records
- Linear search: O(n)
- Sorting: O(n log n)
- Token aggregation
- Real names view: 117,873 rows → 54,147 records

**Speaker notes**
The application intentionally loads the dataset into memory as required by the scenario. A tuple gives stable, immutable storage after loading. Filtering and basic search scan the sequence linearly, so their time complexity is O(n). Alphabetical sorting uses Python's stable sort and is O(n log n). Multi-value fields are tokenised so genre and topic operations do not treat the entire semicolon-separated string as one value. The real names view demonstrates why aggregation matters: 117,873 facet rows correspond to only 54,147 unique BL record IDs. We collapse those repeated rows without modifying the original source files.

## Slide 7 — Creational pattern
**On slide**
- `SearchStrategyFactory`
- Centralised strategy construction
- Simple Factory, not formal Factory Method

**Speaker notes**
The creational technique used is a simple factory. The application receives a search type such as title, author, genre or year, and `SearchStrategyFactory` creates the corresponding strategy object. This keeps object-construction decisions out of the caller. It is important to be technically precise: this project calls it a simple factory and does not claim that the implementation is the formal GoF Factory Method pattern. Tutorialspoint describes factory approaches as a way of hiding creation logic behind a common interface. Here the value is modest but concrete: adding another strategy does not require changing every client that constructs searches.

## Slide 8 — Structural / architectural boundary
**On slide**
- Repository abstraction
- CSV source
- In-memory source
- XML adapter

**Speaker notes**
The Repository boundary separates storage from application behaviour. `CsvComicRepository` knows how to open the official CSV and validate its required columns. `InMemoryComicRepository` supports fast isolated tests. `XmlComicRepository` demonstrates that another source can satisfy the same contract. This is useful because the services do not need to know how the data was obtained. The real dataset also justified an aggregation repository: the names view is a facet view with repeated record IDs, so aggregation is a separate responsibility. This keeps source fidelity and user-facing one-record presentation from becoming tangled.

## Slide 9 — Behavioural pattern
**On slide**
- Strategy pattern
- Title / Author / Genre / Year
- Interchangeable algorithms

**Speaker notes**
Strategy is the clearest behavioural pattern in the application. Title, author, genre and year searches are different algorithms, but the caller needs the same operation: search a sequence of Comics using a query. Each concrete strategy implements that common contract. This reduces a large conditional search method and makes each algorithm independently testable. The author strategy is also a good example of why patterns do not replace domain analysis: the strategy delegates to `Comic.authors()`, which understands the source's name-role relationship. A future ISBN or publisher strategy can be added without rewriting the existing search implementations.

## Slide 10 — Real dataset validation
**On slide**
- records.csv: 57,746
- names.csv: 117,873
- titles.csv: 77,280
- topics.csv: 77,919
- classification.csv: 57,844
- Fantasy 4,793 / Horror 1,929 / Science Fiction 9,356

**Speaker notes**
The final acceptance run uses the actual Comics Unmasked package. All five views match the observed row counts and preserve leading-zero BL record IDs. The aggregated names view has 54,147 unique records. Exact genre filtering produces 4,793 Fantasy records, 1,929 Horror records and 9,356 Science Fiction records. The acceptance run also checks a real author-role search, a title containing Unicode characters, universal missing-value display, a missing ISBN, consistent multi-value metadata display and both title-order directions. This is important evidence because synthetic fixtures can prove algorithmic behaviour but cannot prove that our assumptions match the supplied dataset.

## Slide 11 — Automated testing
**On slide**
- 33 automated tests pass
- Unit
- Integration
- CLI / E2E
- Real-data acceptance
- >100 notification verified

**Speaker notes**
The current automated suite has 33 passing tests. Unit tests focus on domain and strategy behaviour. Integration tests verify CSV-to-service boundaries and all five official views. End-to-end tests verify user-visible no-result and ordering behaviour. The real-data acceptance script checks the actual dataset and writes a machine-readable report. The >100 requirement is demonstrated deterministically by running the same real Comic through 101 search inclusions and verifying that the notification is triggered. Coverage is useful as a diagnostic, but it is not treated as proof of correctness. pytest fixtures provide reusable test contexts, while the test-pyramid idea supports keeping fast focused tests as the larger base.

## Slide 12 — Evaluation and conclusion
**On slide**
- SOLID improves change isolation.
- Patterns solve concrete variation.
- Automation reduces regression risk.
- Abstraction has a cost.

**Speaker notes**
The final evaluation is deliberately balanced. SOLID improves testability and limits the blast radius of changes, but it adds indirection and learning cost. Strategy is justified by multiple search behaviours, Repository by multiple data sources, and aggregation by the real facet structure. Design patterns are not automatically good; using them without a problem can create unnecessary complexity, which is why the project uses only patterns with a clear purpose. Automated testing is valuable because this application repeats data-heavy workflows, but broad UI automation would be more expensive and brittle. The final result is therefore traceable from requirement to design, implementation, test and evidence.
