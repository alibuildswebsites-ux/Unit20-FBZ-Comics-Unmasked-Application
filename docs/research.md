# Research Record — Unit 20 FBZ Application

## Research scope

The assignment brief requires investigation of SOLID development principles in OOP, clean coding, design patterns, data structures/algorithms, and automated testing, followed by design, implementation and testing evidence.

## Sources consulted

1. Python 3.14 `csv` documentation — supports CSV dialect configuration and confirms the standard delimiter is comma unless another dialect/parameter is supplied. This supports using `csv.DictReader` rather than manually splitting rows.
2. pytest documentation — fixtures are explicit, modular and scalable; pytest provides detailed assertion reporting, automatic discovery and fixture support. This supports a fixture-based automated testing regime.
3. Refactoring.Guru Strategy documentation — Strategy separates interchangeable algorithm variants into separate classes behind a common interface. This is directly applicable to title/author/genre/year searching.
4. Refactoring.Guru Factory Method documentation — factories can separate construction from client code and reduce coupling to concrete implementations. The project uses a simple factory for strategy creation and documents the distinction from the formal Factory Method pattern.
5. Refactoring.Guru design-pattern catalogue — patterns are grouped as creational, structural and behavioural; the catalogue provides the classification used in the assessment discussion.

## Research-to-design conclusions

- Search variants are a natural Strategy use case because the application must provide several interchangeable search algorithms.
- A factory is useful at the composition boundary so the service does not depend on concrete search strategy constructors.
- Repository abstraction is appropriate for dependency inversion and enables in-memory repositories for automated tests.
- CSV values are loaded as strings so identifiers can retain leading zeros and so source metadata is not silently coerced into the wrong type.
- pytest fixtures are suitable for repeatable test data and temporary-file scenarios.

## Web citations

Python CSV documentation: https://docs.python.org/3/library/csv.html
pytest documentation: https://docs.pytest.org/en/stable/
Strategy pattern: https://refactoring.guru/design-patterns/strategy
Factory Method: https://refactoring.guru/design-patterns/factory-method
Pattern catalogue: https://refactoring.guru/design-patterns/catalog
