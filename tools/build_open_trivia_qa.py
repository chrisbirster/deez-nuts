#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import urllib.request
from pathlib import Path

SOURCE_OWNER = "uberspot"
SOURCE_REPO = "OpenTriviaQA"
SOURCE_COMMIT = "dcc1cdf36c2985ed5c849d1f2265c5041ffcdfb9"
SOURCE_BASE = f"https://raw.githubusercontent.com/{SOURCE_OWNER}/{SOURCE_REPO}/{SOURCE_COMMIT}/categories"
SOURCE_HOME = f"https://github.com/{SOURCE_OWNER}/{SOURCE_REPO}"
LICENSE = "CC-BY-SA-4.0"
MAX_NOTES_PER_DECK = 500

# OpenTriviaQA also includes `newest` and `rated`, which are aggregate views and
# duplicate questions from the canonical categories. Excluding those gives us
# one archival pass over the 20 canonical category files.
CATEGORIES = {
    "animals": "Animals",
    "brain-teasers": "Brain Teasers",
    "celebrities": "Celebrities",
    "entertainment": "Entertainment",
    "for-kids": "For Kids",
    "general": "General Knowledge",
    "geography": "Geography",
    "history": "History",
    "hobbies": "Hobbies",
    "humanities": "Humanities",
    "literature": "Literature",
    "movies": "Movies",
    "music": "Music",
    "people": "People",
    "religion-faith": "Religion & Faith",
    "science-technology": "Science & Technology",
    "sports": "Sports",
    "television": "Television",
    "video-games": "Video Games",
    "world": "World",
}

ROOT = Path(__file__).resolve().parents[1]
NUTS = ROOT / "nuts"
SOURCES = ROOT / "sources"
GENERATED_MARKER = ".open-trivia-qa-generated"


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "deez-nuts-builder/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        raw = response.read()
    return raw.decode("utf-8", errors="replace")


def clean_text(value: str) -> str:
    value = html.unescape(value.strip())
    if any(token in value for token in ("â€", "â€™", "â€œ", "â€\u009d", "Â")):
        try:
            value = value.encode("latin-1").decode("utf-8")
        except UnicodeError:
            pass
    return re.sub(r"\s+", " ", value).strip()


def parse_questions(text: str) -> list[tuple[str, str]]:
    questions: list[tuple[str, str]] = []
    current_question: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("#Q "):
            current_question = clean_text(line[3:])
        elif line.startswith("^ ") and current_question:
            answer = clean_text(line[2:])
            if current_question and answer:
                questions.append((current_question, answer))
            current_question = None
    return questions


def dedupe(questions: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    output: list[tuple[str, str]] = []
    for question, answer in questions:
        key = (question.casefold(), answer.casefold())
        if key in seen:
            continue
        seen.add(key)
        output.append((question, answer))
    return output


def chunks(items: list[tuple[str, str]], size: int):
    for start in range(0, len(items), size):
        yield items[start : start + size]


def json_line(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def write_nut(path: Path, name: str, category: str, questions: list[tuple[str, str]]) -> str:
    tags = ["trivia", category, "source:open-trivia-qa", "license:cc-by-sa-4.0"]
    lines = [json_line({"kind": "deck", "format": "deez.nut", "version": 2, "name": name})]
    for question, answer in questions:
        lines.append(
            json_line(
                {
                    "kind": "note",
                    "note_type": "basic",
                    "fields": [question, answer],
                    "tags_json": json.dumps(tags, ensure_ascii=False, separators=(",", ":")),
                }
            )
        )
    body = "\n".join(lines) + "\n"
    path.write_text(body, encoding="utf-8")
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def remove_old_generated_decks() -> None:
    if not NUTS.exists():
        return
    for child in NUTS.iterdir():
        if child.is_dir() and (child / GENERATED_MARKER).exists():
            shutil.rmtree(child)


def source_notice(display_name: str, category: str, volume: int, count: int) -> str:
    return f"""# Source and license\n\nThis deck is an adaptation of **OpenTriviaQA** by its contributors.\n\n- Source: {SOURCE_HOME}\n- Source category: `{category}`\n- Pinned source commit: `{SOURCE_COMMIT}`\n- Deck: {display_name} v{volume}\n- Notes in this volume: {count}\n- License: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)\n\nThe source question/answer material was transformed into Deez `.nut` v2 NDJSON and split into volumes of at most {MAX_NOTES_PER_DECK} notes. This derivative deck is distributed under CC BY-SA 4.0.\n"""


def main() -> None:
    NUTS.mkdir(parents=True, exist_ok=True)
    SOURCES.mkdir(parents=True, exist_ok=True)
    remove_old_generated_decks()

    catalog: list[dict] = []
    summary_rows: list[tuple[str, int, int]] = []
    grand_total = 0

    for category, display_name in CATEGORIES.items():
        url = f"{SOURCE_BASE}/{category}"
        parsed = parse_questions(fetch_text(url))
        questions = dedupe(parsed)
        grand_total += len(questions)
        volumes = list(chunks(questions, MAX_NOTES_PER_DECK))
        summary_rows.append((display_name, len(questions), len(volumes)))

        for index, volume_questions in enumerate(volumes, start=1):
            slug = f"{category}-v{index}"
            deck_name = f"{display_name} v{index}"
            deck_dir = NUTS / slug
            deck_dir.mkdir(parents=True, exist_ok=True)
            (deck_dir / GENERATED_MARKER).write_text("generated by tools/build_open_trivia_qa.py\n", encoding="utf-8")
            nut_path = deck_dir / f"{slug}.nut"
            digest = write_nut(nut_path, deck_name, category, volume_questions)
            (deck_dir / "SOURCE.md").write_text(
                source_notice(display_name, category, index, len(volume_questions)),
                encoding="utf-8",
            )
            catalog.append(
                {
                    "slug": slug,
                    "name": deck_name,
                    "category": category,
                    "volume": index,
                    "notes": len(volume_questions),
                    "sha256": digest,
                    "path": str(nut_path.relative_to(ROOT)),
                    "source": SOURCE_HOME,
                    "source_commit": SOURCE_COMMIT,
                    "license": LICENSE,
                }
            )

    (SOURCES / "open-trivia-qa-catalog.json").write_text(
        json.dumps({"source": SOURCE_HOME, "source_commit": SOURCE_COMMIT, "decks": catalog}, indent=2) + "\n",
        encoding="utf-8",
    )

    rows = [
        "# OpenTriviaQA generated deck summary",
        "",
        f"Pinned source commit: `{SOURCE_COMMIT}`",
        f"Maximum notes per deck: {MAX_NOTES_PER_DECK}",
        f"Total unique logical notes: {grand_total}",
        f"Total `.nut` volumes: {len(catalog)}",
        "",
        "| Category | Notes | Volumes |",
        "| --- | ---: | ---: |",
    ]
    rows.extend(f"| {name} | {count} | {volumes} |" for name, count, volumes in summary_rows)
    rows.extend(["", "See `sources/open-trivia-qa.md` for attribution and licensing.", ""])
    (SOURCES / "open-trivia-qa-summary.md").write_text("\n".join(rows), encoding="utf-8")

    print(f"generated {len(catalog)} decks from {grand_total} unique questions")


if __name__ == "__main__":
    main()
