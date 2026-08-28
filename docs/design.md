# Design and Implementation Document

## 1. Scenario

Fantasy Bazaar (FBZ) is a local comic-book shop that wants a data-processing application around the British Library *Comics Unmasked* metadata. The assignment asks for dataset loading, genre and author grouping/filtering, publication-year sorting/filtering, alphabetical title selection, search, favourites, advanced multi-criteria search and specified top-result/search views.

## 2. Functional requirements

1. Load the supplied CSV dataset into application memory.
2. Preserve metadata faithfully, including record identifiers that may contain leading zeroes.
3. Search/filter by title, author, genre and year.
4. Sort records alphabetically by title.
5. Support free-text metadata search.
6. Support advanced searches combining multiple criteria.
7. Display a clear message when no result is found.
8. Save and remove favourites independently of the source dataset.
9. Tokenise multi-value metadata such as Genre and Topics.
10. Provide dataset statistics and top searchable-token summaries to support evidence.

## 3. Non-functional requirements

- Maintainability: responsibilities are separated into domain, repository, service and presentation modules.
- Testability: services depend on abstractions and can be supplied with an in-memory repository.
- Reliability: source parsing validates required columns and reports invalid rows with row numbers.
- Data fidelity: CSV identifiers remain strings and UTF-8 BOMs are supported.
- Extensibility: search variants can be added as new Strategy implementations.

## 4. OOP class relationships

```text
ComicRepository (abstract)
        ▲
        │ implements
CsvComicRepository       InMemoryComicRepository
        │                       │
        └──────────┬────────────┘
                   │ injected into
             SearchService
                   │
                   ├── SearchStrategyFactory
                   │       ├── TitleSearchStrategy
                   │       ├── AuthorSearchStrategy
                   │       ├── GenreSearchStrategy
                   │       └── YearSearchStrategy
                   │
             FavouriteService
```

## 5. SOLID application

### Single Responsibility
`CsvComicRepository` loads CSV records. `Comic` models a catalogue record. `SearchService` coordinates searches. `FavouriteService` owns favourites persistence. Each class therefore has a focused reason to change.

### Open/Closed
New search algorithms can be added as new `SearchStrategy` implementations without rewriting the search service.

### Liskov Substitution
Concrete strategies honour the `SearchStrategy.search` contract and can be substituted by the service/factory without changing the caller's expectations.

### Interface Segregation
The repository abstraction contains only data-access behaviour needed by consumers. Search algorithms depend on a focused strategy contract rather than a large multi-purpose interface.

### Dependency Inversion
`SearchService` depends on `ComicRepository`, not on `CsvComicRepository`. This permits in-memory repositories in tests and alternative data stores later.

## 6. Clean coding

The implementation uses explicit names, small methods, type hints, immutable domain records, early validation and separation of I/O from business logic. Error messages identify the failing row or unsupported search type. No business rules are embedded in the command-line interface.

## 7. Data structures and algorithms

- Records are represented as immutable `Comic` objects in a tuple-backed repository.
- Search scans the in-memory sequence linearly: O(n) for a simple search.
- Alphabetical sorting uses Python's stable Timsort: O(n log n) average/worst case for sorting.
- Advanced search narrows the current result sequence criterion-by-criterion.
- Frequency summaries use `Counter`, giving O(n) expected aggregation over the number of tokens observed.

The design favours clarity and correctness for a dataset-processing assignment. For very large future datasets, indexed dictionaries or database-backed search could reduce repeated linear scans.

## 8. Design patterns

### Strategy — behavioural
Each search algorithm is isolated behind `SearchStrategy`. This makes the algorithms interchangeable and reduces conditional branching in the service.

### Simple Factory — creational technique
`SearchStrategyFactory` centralises creation of the concrete strategy selected by a user's search type. The documentation deliberately calls this a simple factory rather than incorrectly claiming it is the full GoF Factory Method pattern.

### Repository — structural/architectural pattern
`ComicRepository` isolates persistence/data access from application services. The concrete CSV repository can therefore change without rewriting search behaviour.

## 9. Testing design

The project uses unit tests for model, parser, search strategies, factory, statistics and favourites; an integration test covers CSV → repository → search → favourites. pytest fixtures and temporary paths provide repeatable isolated test contexts.

## 10. Implementation evidence

Source code is under `src/fbz/`; automated tests are under `tests/`. The current test run passes all implemented tests. The full supplied dataset must be placed in `data/` before final dataset-specific acceptance evidence can be produced.
