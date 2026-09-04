# deez-nuts

Public `.nut` deck content published for Deez.

This repository contains author-owned source content plus properly attributed open-licensed derivative decks. The public catalog and registry live separately in [`chrisbirster/deez-run`](https://github.com/chrisbirster/deez-run).

## Layout

Each deck lives under:

```text
nuts/<slug>/<slug>.nut
```

`.nut` files are Deez's human-readable, shareable NDJSON deck format. Registry releases pin an immutable Git commit and SHA-256 checksum rather than downloading from a mutable branch.

## Published nuts

- `zig-basics` — introductory Zig concepts

## Open trivia archive

Open-licensed trivia is generated from the 20 canonical OpenTriviaQA categories and split into numbered volumes of at most 500 logical notes each, for example:

```text
nuts/sports-v1/sports-v1.nut
nuts/sports-v2/sports-v2.nut
nuts/history-v1/history-v1.nut
```

The two OpenTriviaQA aggregate views, `newest` and `rated`, are intentionally excluded because they duplicate questions already present in the canonical categories.

Run:

```bash
python tools/build_open_trivia_qa.py
```

See [`sources/open-trivia-qa.md`](sources/open-trivia-qa.md) for source pinning, attribution, transformation details, and licensing.

## Licensing

The root repository license applies to author-owned material unless a deck carries a more specific source/license notice. OpenTriviaQA-derived deck content is distributed under CC BY-SA 4.0 and each generated deck directory contains a `SOURCE.md` attribution file.

## Relationship to deez.run

`deez.run` owns discovery metadata, validation, generated search indexes, and safe previews. This repository owns the actual deck bytes.
