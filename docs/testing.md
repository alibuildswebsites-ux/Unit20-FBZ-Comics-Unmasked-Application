# Automated Testing Report

## Testing regime

The application uses a layered test strategy:

- **Unit testing:** validates domain parsing, multi-value handling, factories, search strategies, sorting, statistics and favourites persistence.
- **Integration testing:** validates CSV input through the repository and service layers, including advanced search and favourites persistence.
- **End-to-end acceptance:** final evidence should exercise the CLI with the supplied full dataset and the brief's named use cases.

The selected tooling is pytest with pytest-cov. pytest supports automatic discovery, detailed assertion reporting and modular fixtures; its fixtures provide reusable, isolated test contexts. This makes it appropriate for a small-to-medium Python application and scales better than repetitive setup/teardown as the suite grows. citeturn846938search0turn846938search6

## Test matrix

| ID | Requirement | Expected result | Level |
|---|---|---|---|
| UT-01 | Parse valid record | Domain object created | Unit |
| UT-02 | Preserve leading-zero ID | Identifier remains string | Unit |
| UT-03 | Reject missing title | Clear validation error | Unit |
| UT-04 | Parse multi-value genre | Individual tokens searchable | Unit |
| UT-05 | Title strategy | Matching titles only | Unit |
| UT-06 | Author strategy | Matching author/other-name records | Unit |
| UT-07 | Genre strategy | Matching genre records | Unit |
| UT-08 | Year strategy | Matching publication-year records | Unit |
| UT-09 | Advanced search | Criteria combine correctly | Unit |
| UT-10 | Alphabetical order | Titles ordered consistently | Unit |
| UT-11 | Factory | Valid strategy returned; invalid type rejected | Unit |
| UT-12 | Favourites | Add/remove/persist correctly | Unit |
| IT-01 | CSV to search flow | Full pipeline returns expected records | Integration |
| E2E-01 | CLI normal search | User receives results | End-to-end |
| E2E-02 | CLI no-result search | User receives no-result message | End-to-end |
| E2E-03 | CLI favourite | Favourite persisted | End-to-end |

## Developer-produced vs vendor-supported automated testing

Developer-produced tests are the application-specific assertions and fixtures written by the development team. They encode FBZ business expectations and edge cases. Their main weakness is maintenance cost: the team must keep them aligned with changing requirements.

Vendor/open-source framework tooling such as pytest provides test discovery, assertion introspection, fixture management and plugins. It reduces infrastructure work and supplies mature reporting, but the framework cannot determine whether an FBZ requirement is correct; the project's own tests remain responsible for that domain knowledge. pytest can also run unittest-style suites, allowing gradual adoption when an existing codebase uses the standard library framework. citeturn846938search1

## Benefits and drawbacks

Automated tests give repeatability, regression protection, rapid feedback and safer refactoring. Their drawbacks include initial authoring cost, execution/maintenance overhead, brittle tests when poorly designed, and the risk of false confidence from high coverage with weak assertions. Unit tests are fast and precise but can miss wiring issues; integration tests catch boundary problems but are slower; end-to-end tests provide high business confidence but are usually the most expensive to maintain.

## Verification run

The local suite currently passes all implemented unit/integration tests. Coverage was measured with pytest-cov. Final acceptance requires repeating the same test suite against the complete supplied dataset and recording the actual results in `reports/`.
