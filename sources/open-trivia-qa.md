# OpenTriviaQA source and licensing

The generated trivia `.nut` decks in this repository are adapted from [OpenTriviaQA](https://github.com/uberspot/OpenTriviaQA).

## Source pin

- Repository: `uberspot/OpenTriviaQA`
- Commit: `dcc1cdf36c2985ed5c849d1f2265c5041ffcdfb9`
- License: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)

OpenTriviaQA contains 22 category files. The generator intentionally excludes `newest` and `rated` because those are aggregate views that duplicate questions from the canonical categories. The remaining 20 categories are archived into Deez decks.

## Transformation

`tools/build_open_trivia_qa.py`:

1. downloads the 20 canonical OpenTriviaQA category files from the pinned commit;
2. extracts each question and its correct answer;
3. normalizes whitespace/HTML entities and repairs common encoding artifacts;
4. removes exact duplicate question-answer pairs within each category;
5. converts every item to a Deez `.nut` v2 `basic` note;
6. splits each category into numbered volumes containing at most 500 notes;
7. writes SHA-256 hashes and deck metadata to `open-trivia-qa-catalog.json`.

Generated deck directories contain a `SOURCE.md` file carrying the source attribution and CC BY-SA 4.0 notice. The generated deck content itself is distributed under CC BY-SA 4.0.

## J! Archive

J! Archive is not used as a bulk content source by this generator. Its published restrictions prohibit scraping and republication, so this repository does not mirror its clue database.
