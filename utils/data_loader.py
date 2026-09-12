import json
import os
from typing import List, Dict, Any

def load_songs() -> List[Dict[str, Any]]:
    """Load songs from songs.json"""
    songs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "songs.json")
    with open(songs_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get("songs", [])

def load_css() -> str:
    """Load CSS from style.css"""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
    with open(css_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_all_authors(songs: List[Dict[str, Any]]) -> List[str]:
    """Get all unique authors sorted alphabetically"""
    authors = set()
    for song in songs:
        for author in song.get("authors", []):
            if author and author.strip():
                authors.add(author)
    return sorted(list(authors))

def get_all_languages(songs: List[Dict[str, Any]]) -> List[str]:
    """Get all unique languages in desired order"""
    languages = set()
    for song in songs:
        lang = song.get("language", "").strip()
        if lang:
            languages.add(lang)
    
    # Define desired order
    ordered = ['english', 'hebrew', 'english and hebrew']
    result = [lang for lang in ordered if lang in languages]
    result.extend(sorted([lang for lang in languages if lang not in ordered]))
    return result

def get_service_tags(songs: List[Dict[str, Any]]) -> List[str]:
    """Get service/holiday tags in desired order"""
    service_tags = {
        'maariv', 'shacharit', 'mincha', 'hallel', 'shabbat', 'havdalah',
        'rosh chodesh', 'rosh hashanah', 'yom kippur', 'sukkot', 'shmini atzeret',
        'simchat torah', 'chanukah', 'purim', 'pesach', 'omer', 'lag b\'omer',
        'shavuot', 'tu b\'av', 'tisha b\'av', 'slichot'
    }
    
    found_tags = set()
    for song in songs:
        for tag in song.get("tags", []):
            if tag.lower() in service_tags:
                found_tags.add(tag.lower())
    
    ordered = [
        'maariv', 'shacharit', 'mincha', 'hallel', 'shabbat', 'havdalah',
        'rosh chodesh', 'rosh hashanah', 'yom kippur', 'sukkot', 'shmini atzeret',
        'simchat torah', 'chanukah', 'tu bishvat', 'purim', 'pesach', 'omer', 'lag b\'omer',
        'shavuot', 'tu b\'av', 'tisha b\'av', 'slichot'
    ]
    
    return [tag for tag in ordered if tag in found_tags]

def get_theme_tags(songs: List[Dict[str, Any]]) -> List[str]:
    """Get thematic tags in desired order"""
    theme_tags = {
        'creation', 'redemption', 'revelation', 'love', 'healing', 'nature',
        'trust', 'gratitude', 'praise', 'celebration', 'mourning', 'justice', 'community',
        'peace', 'protection', 'journey'
    }
    
    found_tags = set()
    for song in songs:
        for tag in song.get("tags", []):
            if tag.lower() in theme_tags:
                found_tags.add(tag.lower())
    
    ordered = [
        'creation', 'redemption', 'revelation', 'love', 'healing', 'nature',
        'trust', 'gratitude', 'celebration', 'mourning', 'yearning', 'justice', 'community',
        'peace', 'protection', 'journey'
    ]
    
    return [tag for tag in ordered if tag in found_tags]

def get_other_tags(songs: List[Dict[str, Any]]) -> List[str]:
    """Get all other tags not in service or theme categories"""
    service_tags = {
        'maariv', 'shacharit', 'mincha', 'hallel', 'shabbat', 'havdalah',
        'rosh chodesh', 'rosh hashanah', 'yom kippur', 'sukkot', 'shmini atzeret',
        'simchat torah', 'chanukah', 'purim', 'pesach', 'omer', 'lag b\'omer',
        'shavuot', 'tu b\'av', 'tisha b\'av', 'slichot'
    }
    
    theme_tags = {
        'creation', 'redemption', 'revelation', 'love', 'healing', 'nature',
        'trust', 'gratitude', 'celebration', 'mourning', 'justice', 'community',
        'peace', 'protection', 'journey'
    }
    
    other_tags = set()
    for song in songs:
        for tag in song.get("tags", []):
            if tag.lower() not in service_tags and tag.lower() not in theme_tags:
                other_tags.add(tag)
    
    return sorted(list(other_tags))

def get_all_books(songs: List[Dict[str, Any]]) -> List[str]:
    """Get all unique book names from sources"""
    books = set()
    for song in songs:
        for source in song.get("sources", []):
            book = source.get("book", "").strip()
            if book:
                books.add(book)
    return sorted(list(books))

def get_chapters_for_book(songs: List[Dict[str, Any]], book: str) -> List[str]:
    """Get all chapters for a specific book"""
    chapters = set()
    for song in songs:
        for source in song.get("sources", []):
            if source.get("book") == book:
                chapter = source.get("chapter", "").strip()
                if chapter:
                    chapters.add(chapter)
    return sorted(list(chapters), key=lambda x: (not x[0].isdigit(), x))

def get_verses_for_book_chapter(songs: List[Dict[str, Any]], book: str, chapter: str) -> List[str]:
    """Get all verses for a specific book and chapter"""
    verses = set()
    for song in songs:
        for source in song.get("sources", []):
            if source.get("book") == book and source.get("chapter") == chapter:
                verse = source.get("verse", "").strip()
                if verse:
                    verses.add(verse)
    return sorted(list(verses), key=lambda x: (not x[0].isdigit(), x))

