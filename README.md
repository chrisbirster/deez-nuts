# deez-nuts

Public `.nut` deck content published for Deez.

This repository contains author-owned source content. The public catalog and registry live separately in [`chrisbirster/deez-run`](https://github.com/chrisbirster/deez-run).

## Layout

Each deck lives under:

```text
nuts/<slug>/<slug>.nut
```

`.nut` files are Deez's human-readable, shareable NDJSON deck format. Registry releases pin an immutable Git commit and SHA-256 checksum rather than downloading from a mutable branch.

## Published nuts

- `zig-basics` — introductory Zig concepts

## Relationship to deez.run

`deez.run` owns discovery metadata, validation, generated search indexes, and safe previews. This repository owns the actual deck bytes.
