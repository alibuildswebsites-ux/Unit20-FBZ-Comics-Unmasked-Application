# Unit 20 — SOLID Development Principles in OOP

## Slide 1 — FBZ Problem and Objective
- Fantasy Bazaar needs a maintainable application for processing Comics Unmasked metadata.
- Goal: combine useful data-processing functionality with sound OOP design.

Speaker notes: The application must load the dataset, provide searching/filtering, support favourites and produce reliable results. The assignment also evaluates the design process, not only whether the program runs.

## Slide 2 — Object-Oriented Programming
- Encapsulation
- Abstraction
- Inheritance
- Polymorphism

Speaker notes: Explain each with a concrete FBZ example: `Comic` encapsulates record data; repository and strategy abstractions hide implementation details; strategies share a common contract; concrete strategies provide polymorphic search behaviour.

## Slide 3 — Relationships Between Classes
```text
SearchService --> ComicRepository
                    ^
                    |
        CsvComicRepository / InMemoryComicRepository

SearchStrategyFactory --> SearchStrategy
                            ^
          +-----------------+----------------+
          |        |         |                |
        Title    Author    Genre             Year
```
Speaker notes: Emphasise composition/dependency injection rather than unnecessary inheritance. Inheritance is used where interchangeable behaviour has a meaningful common contract.

## Slide 4 — SOLID
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

Speaker notes: Connect each principle directly to a module in the application rather than presenting definitions alone.

## Slide 5 — Clean Coding
- Small focused classes
- Explicit names and types
- I/O isolated from business logic
- Clear validation errors
- Immutable domain objects

Speaker notes: Clean code lowers cognitive load and makes the data structures and algorithms easier to verify.

## Slide 6 — Data Structures and Algorithms
- Tuple-backed in-memory repository
- Linear filtering/search: O(n)
- Title sorting: O(n log n)
- `Counter` for frequency summaries

Speaker notes: Discuss why simple linear scans are reasonable for an in-memory assignment application and where indexing/database search would become preferable.

## Slide 7 — Creational Patterns
- Factory techniques separate object construction from use.
- The project uses `SearchStrategyFactory` to select concrete search algorithms.

Speaker notes: Distinguish a simple factory from the formal GoF Factory Method pattern.

## Slide 8 — Structural Patterns
- Repository abstraction separates data access from business logic.
- Alternative repository implementations can be supplied without changing search behaviour.

## Slide 9 — Behavioural Pattern
- Strategy turns title/author/genre/year algorithms into interchangeable objects.
- New strategies can be added without rewriting the service.

## Slide 10 — Application Architecture
- Presentation
- Application services
- Domain model
- Repository/data layer

Speaker notes: Show the flow from CLI → service → repository → CSV and back.

## Slide 11 — Automated Testing
- Unit tests
- Integration tests
- End-to-end acceptance tests
- Coverage as a diagnostic, not a proof of quality

Speaker notes: Explain why the layered testing model catches different classes of failure.

## Slide 12 — Evaluation
- SOLID improves change isolation and testability.
- Patterns help when they solve real variation.
- Abstraction has a maintenance cost.
- Automated testing reduces regression risk but must be maintained.

Speaker notes: Conclude by evaluating trade-offs rather than claiming SOLID or automation is universally best.
