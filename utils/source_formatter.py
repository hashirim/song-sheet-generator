from typing import List, Dict, Any

def format_sources(sources: List[Dict[str, Any]]) -> List[str]:
    """Format sources for display, merging adjacent verses"""
    if not sources:
        return []
    
    formatted = []
    grouped = {}
    
    # Group by book and chapter
    for source in sources:
        book = source.get("book", "")
        chapter = source.get("chapter", "")
        verse = source.get("verse", "")
        
        key = (book, chapter)
        if key not in grouped:
            grouped[key] = []
        if verse:
            grouped[key].append(verse)
    
    # Format each group
    for (book, chapter), verses in sorted(grouped.items()):
        verses = sorted(set(verses), key=lambda x: (not x[0].isdigit(), x))
        
        if not chapter and not verses:
            # Just the book
            formatted.append(book)
        elif not verses:
            # Book and chapter only
            formatted.append(f"{book} {chapter}")
        else:
            # Format with verses
            merged_verses = _merge_numeric_ranges(verses)
            formatted.append(f"{book} {chapter}:{merged_verses}")
    
    return formatted

def _merge_numeric_ranges(verses: List[str]) -> str:
    """Merge numeric verses into ranges, e.g., 2,3,4 -> 2-4"""
    if not verses:
        return ""
    
    # Try to parse as numbers first
    numeric_verses = []
    non_numeric = []
    
    for v in verses:
        try:
            numeric_verses.append((int(v), v))
        except ValueError:
            non_numeric.append(v)
    
    if not numeric_verses:
        return ", ".join(verses)
    
    # Sort numeric verses
    numeric_verses.sort()
    
    # Merge ranges
    merged = []
    start = numeric_verses[0][0]
    end = numeric_verses[0][0]
    
    for i in range(1, len(numeric_verses)):
        current = numeric_verses[i][0]
        if current == end + 1:
            end = current
        else:
            # Close the range
            if start == end:
                merged.append(str(start))
            else:
                merged.append(f"{start}-{end}")
            start = current
            end = current
    
    # Close the last range
    if start == end:
        merged.append(str(start))
    else:
        merged.append(f"{start}-{end}")
    
    # Combine with non-numeric verses
    result = merged + non_numeric
    return ", ".join(result)

