import streamlit as st
import json
import os
from typing import List, Dict, Any
from urllib.parse import urlparse

# Set page config
st.set_page_config(page_title="Song Editor", layout="wide")

# File path
JSON_FILE = "songs.json"

def load_songs() -> Dict[str, Any]:
    """Load songs from JSON file."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"songs": []}

def save_songs(data: Dict[str, Any]) -> None:
    """Save songs to JSON file."""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def format_song_display(song: Dict[str, Any]) -> str:
    """Format song for display in selection box."""
    title = song.get('title', 'Untitled')
    authors = ', '.join(song.get('authors', []))
    if authors:
        return f"{title} - {authors}"
    return title

def get_sorted_songs(songs: List[Dict[str, Any]]) -> List[int]:
    """Get indices of songs sorted alphabetically by title."""
    indexed_songs = [(i, song.get('title', '')) for i, song in enumerate(songs)]
    indexed_songs.sort(key=lambda x: x[1].lower())
    return [i for i, _ in indexed_songs]

def parse_sources_display(sources: List[Dict[str, str]]) -> str:
    """Convert sources list to editable string format (book,chapter,verse;book2,chapter2,verse2)."""
    source_strings = []
    for source in sources:
        book = source.get('book', '')
        chapter = source.get('chapter', '')
        verse = source.get('verse', '')
        source_strings.append(f"{book},{chapter},{verse}")
    return ";".join(source_strings)

def parse_sources_input(sources_str: str) -> List[Dict[str, str]]:
    """Convert editable string format to sources list."""
    if not sources_str.strip():
        return []
    
    sources = []
    source_items = sources_str.split(';')
    
    for item in source_items:
        item = item.strip()
        if not item:
            continue
        
        parts = [p.strip() for p in item.split(',')]
        source = {
            'book': parts[0] if len(parts) > 0 else '',
            'chapter': parts[1] if len(parts) > 1 else '',
            'verse': parts[2] if len(parts) > 2 else ''
        }
        sources.append(source)
    
    return sources

def get_domain(url: str) -> str:
    """Extract domain name from URL."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        domain_parts = domain.split('.')
        if len(domain_parts) > 1:
            return domain_parts[-2]
        return domain
    except:
        return 'unknown'


def parse_urls_display(urls: Dict[str, str]) -> str:
    """Convert URLs dict to editable string format (one URL per line)."""
    url_strings = []
    for key, url in urls.items():
        url_strings.append(url)
    return "\n".join(url_strings)

def parse_urls_input(urls_str: str) -> Dict[str, str]:
    """Convert editable string format to URLs dict."""
    if not urls_str.strip():
        return {}
    
    urls = {}
    url_lines = urls_str.strip().split('\n')
    
    for line in url_lines:
        url = line.strip()
        if not url:
            continue
        
        # Extract service name from URL
        service_name = get_domain(url)
        urls[service_name] = url
    
    return urls

def create_new_song() -> Dict[str, Any]:
    """Create a new song with default structure."""
    return {
        "title": "",
        "authors": [],
        "sources": [],
        "urls": {},
        "tags": [],
        "lyrics": "",
        "notes": "",
        "language": ""
    }

def main():
    st.title("🎵 Song Editor")
    
    # Load songs
    data = load_songs()
    songs = data.get('songs', [])
    
    # Add new song button at the top
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("➕ Add New Song", use_container_width=True):
            new_song = create_new_song()
            songs.append(new_song)
            data['songs'] = songs
            save_songs(data)
            st.success("✅ New song created!")
            st.rerun()
    
    if not songs:
        st.error("No songs found in songs.json")
        return
    
    # Get sorted song indices
    sorted_indices = get_sorted_songs(songs)
    
    # Create song selection
    st.subheader("Select a Song")
    song_options = [format_song_display(songs[i]) for i in sorted_indices]
    
    selected_display = st.selectbox(
        "Songs",
        options=song_options,
        label_visibility="collapsed"
    )
    
    # Get the index of the selected song
    selected_idx_in_options = song_options.index(selected_display)
    selected_idx = sorted_indices[selected_idx_in_options]
    selected_song = songs[selected_idx]
    
    # Display editable fields
    st.subheader(f"Editing: {selected_song.get('title', 'Untitled')}")
    
    # Create form for editing
    with st.form(key="song_form"):
        # Title
        title = st.text_input(
            "Title",
            value=selected_song.get('title', ''),
            help="Song title"
        )
        
        # Authors
        authors_str = ', '.join(selected_song.get('authors', []))
        authors_input = st.text_input(
            "Authors",
            value=authors_str,
            help="Comma-separated list of authors"
        )
        
        # Language
        language = st.text_input(
            "Language",
            value=selected_song.get('language', ''),
            help="Language of the song"
        )
        
        # Tags
        tags_str = ', '.join(selected_song.get('tags', []))
        tags_input = st.text_input(
            "Tags",
            value=tags_str,
            help="Comma-separated list of tags"
        )
        
        # Sources
        sources_display = parse_sources_display(selected_song.get('sources', []))
        sources_input = st.text_input(
            "Sources",
            value=sources_display,
            help="Format: book,chapter,verse;book2,chapter2,verse2 (semicolon separates multiple sources)"
        )
        
        # Lyrics
        lyrics = st.text_area(
            "Lyrics",
            value=selected_song.get('lyrics', ''),
            height=250,
            help="Song lyrics (HTML formatting preserved)"
        )
        
        # Notes
        notes = st.text_area(
            "Notes",
            value=selected_song.get('notes', ''),
            height=150,
            help="Additional notes about the song"
        )
        
        # URLs
        urls_display = parse_urls_display(selected_song.get('urls', {}))
        urls_input = st.text_area(
            "URLs",
            value=urls_display,
            height=100,
            help="One URL per line (service name will be auto-detected from domain)"
        )
        
        # Save button
        submit_button = st.form_submit_button("💾 Save Changes", use_container_width=True)
        
        if submit_button:
            # Parse inputs
            authors = [a.strip() for a in authors_input.split(',') if a.strip()]
            tags = [t.strip() for t in tags_input.split(',') if t.strip()]
            sources = parse_sources_input(sources_input)
            urls = parse_urls_input(urls_input)
            
            # Update song
            songs[selected_idx].update({
                'title': title,
                'authors': authors,
                'language': language,
                'tags': tags,
                'sources': sources,
                'lyrics': lyrics,
                'notes': notes,
                'urls': urls
            })
            
            # Save to file
            data['songs'] = songs
            save_songs(data)
            
            st.success("✅ Changes saved successfully!")
            st.rerun()

if __name__ == "__main__":
    main()

