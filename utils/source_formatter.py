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

        # 1) skip unknown entries
        if any("unknown" in value.lower() for value in (book, chapter, verse) if value):
            continue

        key = (book, chapter)
        if key not in grouped:
            grouped[key] = {"book": book, "chapter": chapter, "verses": []}

        if verse:
            grouped[key]["verses"].append(verse)

    formatted = []

    for (book, chapter), data in sorted(grouped.items()):
        verses = sorted(set(data["verses"]), key=_sort_verse_values)

        # 3) lowercase book
        if book and book[:1].islower():
            if not chapter and not verses:
                continue

            # no dash if only one side is there
            if chapter and verses:
                verse_text = _format_verse_list(verses)
                formatted.append(f"{chapter} - {verse_text}")
            elif chapter:
                formatted.append(chapter)
            elif verses:
                formatted.append(_format_verse_list(verses))
            continue

        # 4) uppercase book
        if not verses:
            if book and chapter:
                formatted.append(f"{book} {chapter}".strip())
            elif book:
                formatted.append(book)
            elif chapter:
                formatted.append(chapter)
            continue

        # 2) numeric verse handling
        if all(v.isdigit() for v in verses):
            merged_verses = _merge_numeric_ranges(verses)
            if book and chapter:
                formatted.append(f"{book} {chapter}:{merged_verses}")
            elif book:
                formatted.append(f"{book}:{merged_verses}")
            elif chapter:
                formatted.append(f"{chapter}:{merged_verses}")
            else:
                formatted.append(merged_verses)
            continue

        # non-numeric verse(s)
        verse_text = _format_verse_list(verses)
        if book and chapter:
            formatted.append(f"{book} {chapter} {verse_text}".strip())
        elif book:
            formatted.append(f"{book} {verse_text}".strip())
        elif chapter:
            formatted.append(f"{chapter} {verse_text}".strip())
        else:
            formatted.append(verse_text)

    return formatted

def _sort_verse_values(value: str):
    """Sort numeric verses before non-numeric ones, while preserving natural order."""
    if value.isdigit():
        return (0, int(value))
    return (1, value)


def _format_verse_list(verses: List[str]) -> str:
    """Format a list of unique verses without trailing spaces."""
    if not verses:
        return ""

    numeric = [v for v in verses if v.isdigit()]
    non_numeric = [v for v in verses if not v.isdigit()]

    if numeric:
        merged = _merge_numeric_ranges(sorted(set(numeric), key=int))
        if non_numeric:
            return f"{merged}, {', '.join(sorted(set(non_numeric)))}"
        return merged

    return ", ".join(sorted(set(non_numeric)))


def _merge_numeric_ranges(verses: List[str]) -> str:
    """Merge numeric verses into ranges, e.g., 2,3,4 -> 2-4."""
    if not verses:
        return ""

    numeric_verses = sorted(set(int(v) for v in verses if str(v).isdigit()))
    if not numeric_verses:
        return ", ".join(verses)

    merged = []
    start = numeric_verses[0]
    end = numeric_verses[0]

    for current in numeric_verses[1:]:
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

    return ", ".join(merged)
