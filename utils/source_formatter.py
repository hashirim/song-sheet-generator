from typing import List, Dict, Any


def format_sources(sources: List[Dict[str, Any]]) -> List[str]:
    """Format sources for display, merging adjacent numeric verses."""
    if not sources:
        return []

    # Keep numeric verses grouped so that adjacent verses can be merged, while
    # formatting non-numeric verses as individual references.
    grouped = {}
    for source in sources:
        book = str(source.get("book", "") or "")
        chapter = str(source.get("chapter", "") or "")
        verse = str(source.get("verse", "") or "")

        # A source containing an unknown component is not a useful reference.
        if any("unknown" in value.lower() for value in (book, chapter, verse)):
            continue

        key = (book, chapter)
        group = grouped.setdefault(
            key, {"numeric": [], "non_numeric": [], "empty": False}
        )
        if not verse:
            group["empty"] = True
        elif verse.isdigit():
            group["numeric"].append(verse)
        else:
            group["non_numeric"].append(verse)

    formatted = []
    for (book, chapter), group in sorted(grouped.items()):
        numeric_verses = sorted(set(group["numeric"]), key=int)
        if numeric_verses:
            merged_verses = _merge_numeric_ranges(numeric_verses)
            parts = [part for part in (book, chapter) if part]
            prefix = " ".join(parts)
            formatted.append(f"{prefix}:{merged_verses}" if prefix else merged_verses)

        for verse in sorted(set(group["non_numeric"])):
            reference = _format_non_numeric_source(book, chapter, verse)
            if reference:
                formatted.append(reference)

        if group["empty"] and not numeric_verses and not group["non_numeric"]:
            reference = _format_non_numeric_source(book, chapter, "")
            if reference:
                formatted.append(reference)

    return formatted


def _format_non_numeric_source(book: str, chapter: str, verse: str) -> str:
    """Format a source whose verse is not numeric (or is empty)."""
    if book and book[0].islower():
        # Lowercase books are shorthand references: omit the book name.
        if chapter and verse:
            return f"{chapter} - {verse}"
        return chapter or verse

    # Uppercase books use the full reference, without trailing spaces.
    return " ".join(part for part in (book, chapter, verse) if part)


def _merge_numeric_ranges(verses: List[str]) -> str:
    """Merge numeric verses into ranges, e.g., 2,3,4 -> 2-4."""
    if not verses:
        return ""

    numeric_verses = []
    non_numeric = []

    for v in verses:
        try:
            numeric_verses.append((int(v), v))
        except ValueError:
            non_numeric.append(v)

    if not numeric_verses:
        return ", ".join(verses)

    numeric_verses.sort()

    merged = []
    start = numeric_verses[0][0]
    end = numeric_verses[0][0]

    for i in range(1, len(numeric_verses)):
        current = numeric_verses[i][0]
        if current == end + 1:
            end = current
        else:
            if start == end:
                merged.append(str(start))
            else:
                merged.append(f"{start}-{end}")
            start = current
            end = current

    if start == end:
        merged.append(str(start))
    else:
        merged.append(f"{start}-{end}")

    result = merged + non_numeric
    return ", ".join(result)
