#!/usr/bin/env python3
"""
One-shot merge: insert the 15 new substack Article objects from
content-drafts/substack-mirror/new-articles.ts into the live
ventureoracle-site/app/data/articles.ts, right before the closing `];`.

Idempotent guard: refuses to run if any of the new slugs already exist
in the target file.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TARGET = Path("/tmp/voracle-substack-integration/ventureoracle-site/app/data/articles.ts")
SOURCE = Path("/Users/yeojooncho/GEOMachine_2604/content-drafts/substack-mirror/new-articles.ts")


def extract_article_objects(source_text: str) -> list[str]:
    """Extract individual Article object blocks (each `{ ... }` at indent 2)
    from new-articles.ts, stripping the import/export wrapper."""
    # Find the start of the array: `[` after `= `
    array_start = source_text.find("[")
    array_end = source_text.rfind("];")
    if array_start == -1 or array_end == -1:
        sys.exit("Could not find array boundaries in source")
    body = source_text[array_start + 1:array_end]

    # Walk character-by-character finding top-level `{ ... }` blocks.
    # Template strings (backticks) can contain braces so we track them.
    objects: list[str] = []
    depth = 0
    start = -1
    in_template = False
    in_string = False
    string_char = ""
    i = 0
    while i < len(body):
        ch = body[i]
        prev = body[i - 1] if i > 0 else ""
        # Toggle template string state
        if not in_string and ch == "`" and prev != "\\":
            in_template = not in_template
        # Toggle regular string state (only if not in template)
        if not in_template and ch in ('"', "'") and prev != "\\":
            if in_string and ch == string_char:
                in_string = False
                string_char = ""
            elif not in_string:
                in_string = True
                string_char = ch
        # Track braces only outside templates and strings
        if not in_template and not in_string:
            if ch == "{":
                if depth == 0:
                    start = i
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0 and start != -1:
                    objects.append(body[start:i + 1])
                    start = -1
        i += 1
    return objects


def extract_existing_slugs(target_text: str) -> set[str]:
    """Pull all `slug: "..."` values out of the target articles.ts."""
    return set(re.findall(r'slug:\s*"([^"]+)"', target_text))


def extract_new_slugs(objects: list[str]) -> list[str]:
    return [
        (re.search(r'slug:\s*"([^"]+)"', obj) or re.search(r"slug:\s*'([^']+)'", obj)).group(1)
        for obj in objects
    ]


def main() -> None:
    target_text = TARGET.read_text(encoding="utf-8")
    source_text = SOURCE.read_text(encoding="utf-8")

    all_objects = extract_article_objects(source_text)
    # Filter out non-article brace blocks (e.g., the `{ Article }` from the
    # `import { Article } from ...` statement that happens to be a top-level
    # brace block but isn't an Article literal).
    new_objects = [obj for obj in all_objects if "slug:" in obj]
    skipped = len(all_objects) - len(new_objects)
    print(f"Extracted {len(new_objects)} article objects from {SOURCE}"
          + (f" (skipped {skipped} non-article brace blocks)" if skipped else ""))

    existing_slugs = extract_existing_slugs(target_text)
    new_slugs = extract_new_slugs(new_objects)
    print(f"Target has {len(existing_slugs)} existing slugs")
    print(f"New slugs: {new_slugs}")

    conflicts = set(new_slugs) & existing_slugs
    if conflicts:
        sys.exit(f"CONFLICT — slugs already present in target: {conflicts}")

    # Locate the closing `];` of the articles array. We want the FIRST
    # `];` after `export const articles` to be safe.
    array_decl = target_text.find("export const articles")
    if array_decl == -1:
        sys.exit("Could not find `export const articles` in target")
    closing_bracket = target_text.find("];", array_decl)
    if closing_bracket == -1:
        sys.exit("Could not find closing `];` for articles array")

    # Walk backwards from closing_bracket to find the last non-whitespace char.
    # After a previous merge it's `},`; on a fresh origin/main file it's `}`.
    # Both are valid. Normalize so we always emit with a trailing comma.
    before_bracket = target_text[:closing_bracket].rstrip()
    if before_bracket.endswith("},"):
        normalized_before = before_bracket  # already has trailing comma
    elif before_bracket.endswith("}"):
        normalized_before = before_bracket + ","
    else:
        sys.exit(
            f"Expected the char before `];` to be `}}` or `}},`, got: "
            f"{before_bracket[-20:]!r}"
        )

    # Compose the insertion: newline + each new object indented with 2 spaces
    # + comma + newline.
    indent = "  "
    insertion_lines = []
    for obj in new_objects:
        # Each object is already a complete `{ ... }` block. Indent it to
        # match the surrounding array (2 spaces) and add a trailing comma.
        indented = indent + obj.replace("\n", "\n").strip() + ","
        insertion_lines.append(indented)

    # New target content:
    #   everything up to and including the last `},`
    #   newline
    #   insertion_lines joined with newlines
    #   newline
    #   `];`
    #   rest of file after `];`
    new_target = (
        normalized_before
        + "\n"
        + "\n".join(insertion_lines)
        + "\n"
        + target_text[closing_bracket:]
    )

    TARGET.write_text(new_target, encoding="utf-8")
    added = len(new_objects)
    lines_before = target_text.count("\n")
    lines_after = new_target.count("\n")
    print(f"Wrote {TARGET}")
    print(f"Lines: {lines_before} → {lines_after} (+{lines_after - lines_before})")
    print(f"Articles added: {added}")


if __name__ == "__main__":
    main()
