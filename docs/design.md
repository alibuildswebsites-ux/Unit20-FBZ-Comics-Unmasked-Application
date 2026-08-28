# Design and Implementation — Unit 20 FBZ Application

## 1. Scenario and requirements

Fantasy Bazaar needs a maintainable application around the British Library Comics Unmasked metadata. The implementation loads the real five-view CSV package, supports the required genre browse/search workflow, preserves catalogue identifiers and multi-value metadata, and provides the advanced search, in-memory search list and popularity-reporting behaviour specified by the brief.

## 2. Architecture

The application is divided into presentation, application services, domain, strategy/factory and repository layers. `CsvComicRepository` owns CSV I/O. `AggregatingComicRepository` converts the names facet view into one user-facing record per BL record ID. `Comic` and `Contributor` model domain data. `EncyclopediaService` coordinates the scenario-specific workflow, while `SearchService` demonstrates the strategy/factory search abstraction. The CLI is responsible only for input/output and delegates business decisions to services.

## 3. OOP relationships

`Comic` encapsulates record state and domain operations such as multi-value tokenisation and author extraction. `Contributor` represents a name/role relationship. `ComicRepository` is an abstraction implemented by CSV, in-memory and XML repositories. `SearchStrategy` is an abstraction implemented by title, author, genre and year strategies. These relationships demonstrate inheritance for substitutable contracts, association/dependency injection between services and repositories, and composition of repository state from domain objects.

## 4. SOLID design

**Single Responsibility:** each major class has a focused reason to change. **Open/Closed:** new search strategies can be added without rewriting the service. **Liskov Substitution:** repository and strategy implementations honour their contracts. **Interface Segregation:** contracts are small and focused. **Dependency Inversion:** services depend on the repository abstraction rather than CSV implementation.

The design was refined after inspecting the real names view: multiple rows can associate different roles with the same record. A flat `name` field is therefore insufficient for an author-specific search. `Contributor(name, role)` preserves the relationship, and `Comic.authors()` filters explicit author/writer roles. This prevents a user searching for an author from receiving records solely because the same person was an editor or illustrator.

## 5. Clean coding, data structures and algorithms

The implementation uses descriptive names, type hints, immutable dataclasses, small methods, early validation, explicit exceptions and separated I/O/business logic. Records are held as immutable tuples after loading. Basic filtering/search is O(n); alphabetical sorting is O(n log n); token frequency aggregation is O(n) expected over the observed token stream. The design deliberately favours deterministic linear scans because the assignment asks for an in-memory educational application. A database index or inverted search index would become preferable for much larger or frequently changing collections.

Clean coding directly improves algorithmic reasoning. A monolithic function would combine parsing, aggregation, filtering, sorting and presentation, making both correctness and complexity difficult to inspect. Separating those operations means each algorithm has a clear input/output contract and can be tested independently.

## 6. Design patterns

The project uses Strategy for interchangeable search algorithms, a simple Factory for strategy construction, and Repository as a structural/architectural boundary around storage. The patterns were selected because the application actually has multiple search behaviours and multiple source representations. The project deliberately avoids claiming the simple factory is the formal GoF Factory Method.

## 7. Dataset integration

The real 2022 package is retained under `data/raw/`. The five extracted views are independently loadable. The names view contains 117,873 rows and 54,147 unique BL record IDs. The aggregation repository collapses 63,726 repeated facet rows while retaining multi-value fields and contributor role relationships. The raw source is never overwritten.

## 8. Functional implementation

The application provides Fantasy/Horror/Science Fiction filtering, author/year grouping, A–Z/Z–A sorting, title search, Unicode-safe handling, repeated-value tokenisation, missing ISBN display, multi-title aggregation, an in-memory search list, advanced author/year/genre/edition/language/name-type/title search, classification/names/titles/topics searches, XML adaptation, top-10 query/result reporting and >100-result threshold notification.

## 9. Testing design

The test suite is layered: unit tests cover domain and strategy behaviour; integration tests cover CSV/service boundaries and real five-view loading; CLI/end-to-end tests cover user-visible results/no-results and ordering. A real-data acceptance script checks the official row counts, leading-zero IDs, genre counts, author-role search, Unicode title search, missing ISBN, multi-value metadata, aggregation, ordering and the >100 notification.

## 10. Evaluation

The final design is more maintainable and testable than a procedural alternative because change boundaries are explicit. Its trade-off is additional abstraction and indirection. Strategy is justified by multiple search behaviours; Repository is justified by multiple source representations; aggregation is justified by the facet-row structure of the real dataset. The result is not “SOLID for its own sake”; each abstraction is connected to an identified requirement or data characteristic.
