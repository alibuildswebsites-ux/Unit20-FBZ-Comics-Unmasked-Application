# Evaluation and Higher-Grade Analysis

## M3 — Effectiveness of SOLID, clean coding and patterns

SOLID is effective in FBZ because the application has multiple reasons to change: source format, search algorithms, presentation behaviour and domain rules. Dependency inversion allows tests to use an in-memory repository without rewriting search logic. Strategy isolates search algorithms, while the repository boundary isolates storage. The trade-off is additional classes and indirection; for a one-off script this would be unnecessary overhead. For FBZ, the requirement for multiple search behaviours and automated testing makes the boundaries useful.

Clean coding is effective because it makes the algorithmic pipeline explicit: parse → map → aggregate → filter → sort → present. This allows complexity to be discussed accurately and makes failures easier to localise. The immutable `Comic` model also reduces accidental mutation while a search session is running.

Patterns are effective when they address actual variation. Strategy is directly justified by four search behaviours. The simple factory centralises strategy construction. Repository supports alternate source implementations. Adding additional patterns solely to increase the pattern count would create pattern overload and weaken maintainability.

## D1 — Impact of SOLID on OOP development

The most important impact is the movement of change boundaries into explicit abstractions. A new search strategy does not require rewriting existing strategies. A new repository implementation can satisfy the same contract. This reduces the blast radius of change and improves unit-test isolation. The cost is that a developer must understand more classes and interfaces before tracing a request. The design therefore benefits an evolving application more than a tiny disposable script.

The real dataset also exposed a design issue that SOLID alone would not solve: role relationships must be preserved. The refined `Contributor` model demonstrates that good OOP design combines principles with domain understanding. A perfectly abstract architecture can still be semantically wrong if it flattens relationships in the source data.

## D2 — Automated testing across applications

Automated testing is strongest where workflows are repeatable, data-intensive, regression-prone or frequently executed. FBZ is a strong candidate because the same CSV parsing, filtering, sorting and search operations must work repeatedly over a large dataset. Unit tests provide fast feedback, integration tests validate boundaries, and end-to-end tests validate user-visible behaviour. Real-data acceptance tests then verify assumptions that synthetic fixtures cannot establish.

Automation is not universally sufficient. Exploratory usability, visual presentation and ambiguous human judgement still benefit from manual testing. End-to-end/UI automation can also be slow and brittle; the Test Pyramid therefore supports keeping focused tests as the larger base (Fowler, 2012). SmartBear (n.d.) similarly notes that automation frameworks improve repeatability and maintenance when designed appropriately, while record/playback approaches can become costly when applications change.

## Evidence-based conclusion

The project should be judged by traceability rather than by isolated metrics: each requirement maps to an implementation point, a test, and a report/presentation evidence point. The final acceptance run verifies the actual British Library dataset, not a synthetic substitute. This is stronger evidence than reporting coverage alone.

## References

Chebanyuk, E. and Markov, K. (2016) ‘An Approach to Class Diagrams Verification According to SOLID Design Principles’, *Proceedings of MODELSWARD 2016*, pp. 435–441. doi: 10.5220/0005830104350441.

Fowler, M. (2012) ‘Test Pyramid’, Martin Fowler. Available at: https://martinfowler.com/bliki/TestPyramid.html (Accessed: 28 August 2026).

Refactoring.Guru (n.d.) *Design Patterns*. Available at: https://refactoring.guru/design-patterns (Accessed: 28 August 2026).

SmartBear (n.d.) *Test Automation Frameworks*. Available at: https://smartbear.com/learn/automated-testing/test-automation-frameworks/ (Accessed: 28 August 2026).

Subburaj, R., Jekese, G. and Hwata, C. (2015) ‘Impact of Object Oriented Design Patterns on Software Development’, *International Journal of Scientific & Engineering Research*, 6(2), pp. 961–966.
