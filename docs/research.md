# Research Record — Unit 20 FBZ Application

## Primary sources

1. **British Library — Collection Metadata Services / Researcher Format datasets.** The project uses the British Library's Comics Unmasked Researcher Format package specified by the assignment. The exact 2022 ZIP referenced by the brief was recovered from an Internet Archive snapshot of the original British Library download URL because the historical direct path now returns 404. The current British Library repository record is discoverable through DOI `10.23636/jyxw-xa90`, titled *Researcher Format Datasets from Collection Metadata*.
2. **Python `csv` documentation.** The implementation uses `csv.DictReader` so quoted fields, commas and newline behaviour are handled by the standard parser instead of manual string splitting.
3. **pytest documentation.** pytest supports test discovery, fixtures, assertion introspection and plugin-based reporting; it is used for the automated test regime.
4. **Refactoring.Guru Strategy catalogue.** Strategy is a behavioural pattern for encapsulating interchangeable algorithms; this directly maps to the application's title/author/genre/year search algorithms.
5. **Refactoring.Guru pattern catalogue.** The catalogue is used to classify patterns into creational, structural and behavioural families and to explain why patterns should be selected for concrete design problems.

## Dataset-specific findings

The supplied package contains exactly five CSV views: records, names, titles, topics and classification. The project verified their actual row/column counts and found that every observed BL record ID begins with a leading zero. The names view has 117,873 rows but only 54,147 unique record IDs, confirming that facet rows must be aggregated for a single-record encyclopedia display.

Observed exact genre counts in the aggregated names view are Fantasy 4,793, Horror 1,929 and Science Fiction 9,356. These values are generated from the integrated dataset and saved in `reports/real_dataset_analysis.json`.

## Design conclusions

- Strategy is the natural fit for interchangeable search algorithms.
- A simple factory keeps construction out of the application service.
- Repository abstraction supports dependency inversion and testing with in-memory data.
- Aggregating repository behaviour preserves the source views while satisfying the user-facing “one record entry” requirement.
- CSV identifiers remain strings to preserve leading zeroes.
