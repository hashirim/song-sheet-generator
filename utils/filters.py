import unicodedata
from typing import List, Dict, Any, Optional
from utils.data_loader import load_songs

def remove_diacritics(text: str) -> str:
    """Remove diacritical marks from text"""
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def filter_songs(
    songs: List[Dict[str, Any]],
    authors: List[str] = None,
    languages: List[str] = None,
    service_tags: List[str] = None,
    theme_tags: List[str] = None,
    other_tags: List[str] = None,
    book: Optional[str] = None,
    chapter: Optional[str] = None,
    verse: Optional[str] = None,
    lyrics_search: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Filter songs based on all criteria"""
    
    filtered = songs
    
    # Author filter
    if authors:
        filtered = [s for s in filtered if any(author in authors for author in s.get("authors", []))]
    
    # Language filter
    if languages:
        filtered = [s for s in filtered if s.get("language", "") in languages]
    
    # Service tags filter
    if service_tags:
        filtered = [s for s in filtered if any(
            tag.lower() in [st.lower() for st in service_tags] 
            for tag in s.get("tags", [])
        )]
    
    # Theme tags filter
    if theme_tags:
        filtered = [s for s in filtered if any(
            tag.lower() in [tt.lower() for tt in theme_tags] 
            for tag in s.get("tags", [])
        )]
    
    # Other tags filter
    if other_tags:
        filtered = [s for s in filtered if any(
            tag in other_tags 
            for tag in s.get("tags", [])
        )]
    
    # Source filter
    if book:
        filtered = [s for s in filtered if any(
            source.get("book") == book and 
            (not chapter or source.get("chapter") == chapter) and
            (not verse or source.get("verse") == verse)
            for source in s.get("sources", [])
        )]
    
    # Lyrics search filter
    if lyrics_search:
        search_normalized = remove_diacritics(lyrics_search.lower())
        filtered = [s for s in filtered if search_normalized in remove_diacritics(s.get("lyrics", "").lower())]
    
    return filtered

def count_author_songs(songs: List[Dict[str, Any]], author: str) -> int:
    """Count songs by a specific author"""
    return sum(1 for s in songs if author in s.get("authors", []))

def count_language_songs(songs: List[Dict[str, Any]], language: str) -> int:
    """Count songs with a specific language"""
    return sum(1 for s in songs if s.get("language", "") == language)

def count_tag_songs(songs: List[Dict[str, Any]], tag: str) -> int:
    """Count songs with a specific tag"""
    return sum(1 for s in songs if tag.lower() in [t.lower() for t in s.get("tags", [])])

def count_book_songs(songs: List[Dict[str, Any]], book: str) -> int:
    """Count songs with a specific book source"""
    return sum(1 for s in songs if any(source.get("book") == book for source in s.get("sources", [])))

def count_chapter_songs(songs: List[Dict[str, Any]], book: str, chapter: str) -> int:
    """Count songs with a specific book and chapter"""
    return sum(1 for s in songs if any(
        source.get("book") == book and source.get("chapter") == chapter 
        for source in s.get("sources", [])
    ))

def count_verse_songs(songs: List[Dict[str, Any]], book: str, chapter: str, verse: str) -> int:
    """Count songs with a specific book, chapter, and verse"""
    return sum(1 for s in songs if any(
        source.get("book") == book and source.get("chapter") == chapter and source.get("verse") == verse
        for source in s.get("sources", [])
    ))

