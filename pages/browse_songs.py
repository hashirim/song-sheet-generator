import streamlit as st
import pandas as pd
from utils.data_loader import (
    load_songs, get_all_authors, get_all_languages,
    get_service_tags, get_theme_tags, get_other_tags,
    get_all_books, get_chapters_for_book, get_verses_for_book_chapter
)
from utils.filters import (
    filter_songs, count_author_songs, count_language_songs,
    count_tag_songs, count_book_songs, count_chapter_songs, count_verse_songs
)
from utils.url_handler import get_song_url
from utils.source_formatter import format_sources

def show():
    #st.title("Browse Songs")
    
    songs = load_songs()
    
    # Initialize session state for filters
    if "selected_authors" not in st.session_state:
        st.session_state.selected_authors = []
    if "selected_languages" not in st.session_state:
        st.session_state.selected_languages = []
    if "selected_service_tags" not in st.session_state:
        st.session_state.selected_service_tags = []
    if "selected_theme_tags" not in st.session_state:
        st.session_state.selected_theme_tags = []
    if "selected_other_tags" not in st.session_state:
        st.session_state.selected_other_tags = []
    if "selected_book" not in st.session_state:
        st.session_state.selected_book = None
    if "selected_chapter" not in st.session_state:
        st.session_state.selected_chapter = None
    if "selected_verse" not in st.session_state:
        st.session_state.selected_verse = None
    if "lyrics_search" not in st.session_state:
        st.session_state.lyrics_search = ""
    if "selected_song_index" not in st.session_state:
        st.session_state.selected_song_index = None
    
    # Cache for display options - these are created once and updated with new counts
    if "author_display_cache" not in st.session_state:
        st.session_state.author_display_cache = {}
    if "language_display_cache" not in st.session_state:
        st.session_state.language_display_cache = {}
    if "service_display_cache" not in st.session_state:
        st.session_state.service_display_cache = {}
    if "theme_display_cache" not in st.session_state:
        st.session_state.theme_display_cache = {}
    if "other_display_cache" not in st.session_state:
        st.session_state.other_display_cache = {}
    if "book_display_cache" not in st.session_state:
        st.session_state.book_display_cache = {}
    if "chapter_display_cache" not in st.session_state:
        st.session_state.chapter_display_cache = {}
    if "verse_display_cache" not in st.session_state:
        st.session_state.verse_display_cache = {}
    
    # Filters section
    st.subheader("Filters")
    
    col1, col2, col3 = st.columns(3)
    
    # Author filter
    with col1:
        authors = get_all_authors(songs)
        current_filtered = filter_songs(
            songs,
            languages=st.session_state.selected_languages if st.session_state.selected_languages else None,
            service_tags=st.session_state.selected_service_tags if st.session_state.selected_service_tags else None,
            theme_tags=st.session_state.selected_theme_tags if st.session_state.selected_theme_tags else None,
            other_tags=st.session_state.selected_other_tags if st.session_state.selected_other_tags else None,
            book=st.session_state.selected_book,
            chapter=st.session_state.selected_chapter,
            verse=st.session_state.selected_verse,
            lyrics_search=st.session_state.lyrics_search if st.session_state.lyrics_search else None
        )
        
        # Update cache with new counts and build display options
        author_options = []
        author_value_map = {}
        for author in authors:
            count = count_author_songs(current_filtered, author)
            # Only show if count > 0 or if already selected
            if count > 0 or author in st.session_state.selected_authors:
                # Always update cache with current count
                display = f"{author} ({count})"
                st.session_state.author_display_cache[author] = display
                author_options.append(display)
                author_value_map[display] = author
        
        # Build default selections using updated cache
        default_options = []
        for author in st.session_state.selected_authors:
            if author in st.session_state.author_display_cache:
                default_options.append(st.session_state.author_display_cache[author])
        
        selected_author_options = st.multiselect(
            "Artist/Author",
            options=author_options,
            default=default_options,
            key="author_multiselect"
        )
        st.session_state.selected_authors = [author_value_map[opt] for opt in selected_author_options]
    
    # Language filter
    with col2:
        languages = get_all_languages(songs)
        current_filtered = filter_songs(
            songs,
            authors=st.session_state.selected_authors if st.session_state.selected_authors else None,
            service_tags=st.session_state.selected_service_tags if st.session_state.selected_service_tags else None,
            theme_tags=st.session_state.selected_theme_tags if st.session_state.selected_theme_tags else None,
            other_tags=st.session_state.selected_other_tags if st.session_state.selected_other_tags else None,
            book=st.session_state.selected_book,
            chapter=st.session_state.selected_chapter,
            verse=st.session_state.selected_verse,
            lyrics_search=st.session_state.lyrics_search if st.session_state.lyrics_search else None
        )
        
        language_options = []
        language_value_map = {}
        for language in languages:
            count = count_language_songs(current_filtered, language)
            if count > 0 or language in st.session_state.selected_languages:
                display = f"{language} ({count})"
                st.session_state.language_display_cache[language] = display
                language_options.append(display)
                language_value_map[display] = language
        
        default_options = []
        for language in st.session_state.selected_languages:
            if language in st.session_state.language_display_cache:
                default_options.append(st.session_state.language_display_cache[language])
        
        selected_language_options = st.multiselect(
            "Language",
            options=language_options,
            default=default_options,
            key="language_multiselect"
        )
        st.session_state.selected_languages = [language_value_map[opt] for opt in selected_language_options]
    
    # Service & Holiday tags filter
    with col3:
        service_tags = get_service_tags(songs)
        current_filtered = filter_songs(
            songs,
            authors=st.session_state.selected_authors if st.session_state.selected_authors else None,
            languages=st.session_state.selected_languages if st.session_state.selected_languages else None,
            theme_tags=st.session_state.selected_theme_tags if st.session_state.selected_theme_tags else None,
            other_tags=st.session_state.selected_other_tags if st.session_state.selected_other_tags else None,
            book=st.session_state.selected_book,
            chapter=st.session_state.selected_chapter,
            verse=st.session_state.selected_verse,
            lyrics_search=st.session_state.lyrics_search if st.session_state.lyrics_search else None
        )
        
        service_options = []
        service_value_map = {}
        for tag in service_tags:
            count = count_tag_songs(current_filtered, tag)
            if count > 0 or tag in st.session_state.selected_service_tags:
                display = f"{tag} ({count})"
                st.session_state.service_display_cache[tag] = display
                service_options.append(display)
                service_value_map[display] = tag
        
        default_options = []
        for tag in st.session_state.selected_service_tags:
            if tag in st.session_state.service_display_cache:
                default_options.append(st.session_state.service_display_cache[tag])
        
        selected_service_options = st.multiselect(
            "Service & Holiday",
            options=service_options,
            default=default_options,
            key="service_multiselect"
        )
        st.session_state.selected_service_tags = [service_value_map[opt] for opt in selected_service_options]
    
    col4, col5, col6 = st.columns(3)
    
    # Theme tags filter
    with col4:
        theme_tags = get_theme_tags(songs)
        current_filtered = filter_songs(
            songs,
            authors=st.session_state.selected_authors if st.session_state.selected_authors else None,
            languages=st.session_state.selected_languages if st.session_state.selected_languages else None,
            service_tags=st.session_state.selected_service_tags if st.session_state.selected_service_tags else None,
            other_tags=st.session_state.selected_other_tags if st.session_state.selected_other_tags else None,
            book=st.session_state.selected_book,
            chapter=st.session_state.selected_chapter,
            verse=st.session_state.selected_verse,
            lyrics_search=st.session_state.lyrics_search if st.session_state.lyrics_search else None
        )
        
        theme_options = []
        theme_value_map = {}
        for tag in theme_tags:
            count = count_tag_songs(current_filtered, tag)
            if count > 0 or tag in st.session_state.selected_theme_tags:
                display = f"{tag} ({count})"
                st.session_state.theme_display_cache[tag] = display
                theme_options.append(display)
                theme_value_map[display] = tag
        
        default_options = []
        for tag in st.session_state.selected_theme_tags:
            if tag in st.session_state.theme_display_cache:
                default_options.append(st.session_state.theme_display_cache[tag])
        
        selected_theme_options = st.multiselect(
            "Theme Tags",
            options=theme_options,
            default=default_options,
            key="theme_multiselect"
        )
        st.session_state.selected_theme_tags = [theme_value_map[opt] for opt in selected_theme_options]
    
    # Other tags filter
    with col5:
        other_tags = get_other_tags(songs)
        current_filtered = filter_songs(
            songs,
            authors=st.session_state.selected_authors if st.session_state.selected_authors else None,
            languages=st.session_state.selected_languages if st.session_state.selected_languages else None,
            service_tags=st.session_state.selected_service_tags if st.session_state.selected_service_tags else None,
            theme_tags=st.session_state.selected_theme_tags if st.session_state.selected_theme_tags else None,
            book=st.session_state.selected_book,
            chapter=st.session_state.selected_chapter,
            verse=st.session_state.selected_verse,
            lyrics_search=st.session_state.lyrics_search if st.session_state.lyrics_search else None
        )
        
        other_options = []
        other_value_map = {}
        for tag in other_tags:
            count = count_tag_songs(current_filtered, tag)
            if count > 0 or tag in st.session_state.selected_other_tags:
                display = f"{tag} ({count})"
                st.session_state.other_display_cache[tag] = display
                other_options.append(display)
                other_value_map[display] = tag
        
        default_options = []
        for tag in st.session_state.selected_other_tags:
            if tag in st.session_state.other_display_cache:
                default_options.append(st.session_state.other_display_cache[tag])
        
        selected_other_options = st.multiselect(
            "Additional Tags",
            options=other_options,
            default=default_options,
            key="other_multiselect"
        )
        st.session_state.selected_other_tags = [other_value_map[opt] for opt in selected_other_options]
    
    # Lyrics search
    with col6:
        st.session_state.lyrics_search = st.text_input(
            "Search Lyrics",
            value=st.session_state.lyrics_search
        )
    
    # Source filter
    st.subheader("Source Filter")
    
    source_col1, source_col2, source_col3 = st.columns(3)
    
    with source_col1:
        books = get_all_books(songs)
        current_filtered = filter_songs(
            songs,
            authors=st.session_state.selected_authors if st.session_state.selected_authors else None,
            languages=st.session_state.selected_languages if st.session_state.selected_languages else None,
            service_tags=st.session_state.selected_service_tags if st.session_state.selected_service_tags else None,
            theme_tags=st.session_state.selected_theme_tags if st.session_state.selected_theme_tags else None,
            other_tags=st.session_state.selected_other_tags if st.session_state.selected_other_tags else None,
            chapter=st.session_state.selected_chapter,
            verse=st.session_state.selected_verse,
            lyrics_search=st.session_state.lyrics_search if st.session_state.lyrics_search else None
        )
        
        book_options = ["All Books"]
        book_value_map = {"All Books": ""}
        for book in books:
            count = count_book_songs(current_filtered, book)
            if count > 0 or book == st.session_state.selected_book:
                display = f"{book} ({count})"
                st.session_state.book_display_cache[book] = display
                book_options.append(display)
                book_value_map[display] = book
        
        if st.session_state.selected_book and st.session_state.selected_book in st.session_state.book_display_cache:
            default_display = st.session_state.book_display_cache[st.session_state.selected_book]
            default_index = book_options.index(default_display) if default_display in book_options else 0
        else:
            default_index = 0
        
        selected_book_display = st.selectbox(
            "Book",
            options=book_options,
            index=default_index,
            key="book_select"
        )
        st.session_state.selected_book = book_value_map[selected_book_display]
        
        if not st.session_state.selected_book:
            st.session_state.selected_chapter = None
            st.session_state.selected_verse = None
    
    with source_col2:
        if st.session_state.selected_book:
            chapters = get_chapters_for_book(songs, st.session_state.selected_book)
            current_filtered = filter_songs(
                songs,
                authors=st.session_state.selected_authors if st.session_state.selected_authors else None,
                languages=st.session_state.selected_languages if st.session_state.selected_languages else None,
                service_tags=st.session_state.selected_service_tags if st.session_state.selected_service_tags else None,
                theme_tags=st.session_state.selected_theme_tags if st.session_state.selected_theme_tags else None,
                other_tags=st.session_state.selected_other_tags if st.session_state.selected_other_tags else None,
                book=st.session_state.selected_book,
                verse=st.session_state.selected_verse,
                lyrics_search=st.session_state.lyrics_search if st.session_state.lyrics_search else None
            )
            
            chapter_options = ["All Chapters"]
            chapter_value_map = {"All Chapters": ""}
            for chapter in chapters:
                count = count_chapter_songs(current_filtered, st.session_state.selected_book, chapter)
                if count > 0 or chapter == st.session_state.selected_chapter:
                    cache_key = f"{st.session_state.selected_book}_{chapter}"
                    display = f"{chapter} ({count})"
                    st.session_state.chapter_display_cache[cache_key] = display
                    chapter_options.append(display)
                    chapter_value_map[display] = chapter
            
            if st.session_state.selected_chapter:
                cache_key = f"{st.session_state.selected_book}_{st.session_state.selected_chapter}"
                default_display = st.session_state.chapter_display_cache.get(cache_key, "")
                default_index = chapter_options.index(default_display) if default_display in chapter_options else 0
            else:
                default_index = 0
            
            selected_chapter_display = st.selectbox(
                "Chapter",
                options=chapter_options,
                index=default_index,
                key="chapter_select"
            )
            st.session_state.selected_chapter = chapter_value_map[selected_chapter_display]
            
            if not st.session_state.selected_chapter:
                st.session_state.selected_verse = None
        else:
            st.selectbox("Chapter", options=[], disabled=True, key="chapter_select_disabled")
    
    with source_col3:
        if st.session_state.selected_book and st.session_state.selected_chapter:
            verses = get_verses_for_book_chapter(songs, st.session_state.selected_book, st.session_state.selected_chapter)
            current_filtered = filter_songs(
                songs,
                authors=st.session_state.selected_authors if st.session_state.selected_authors else None,
                languages=st.session_state.selected_languages if st.session_state.selected_languages else None,
                service_tags=st.session_state.selected_service_tags if st.session_state.selected_service_tags else None,
                theme_tags=st.session_state.selected_theme_tags if st.session_state.selected_theme_tags else None,
                other_tags=st.session_state.selected_other_tags if st.session_state.selected_other_tags else None,
                book=st.session_state.selected_book,
                chapter=st.session_state.selected_chapter,
                lyrics_search=st.session_state.lyrics_search if st.session_state.lyrics_search else None
            )
            
            verse_options = ["All Verses"]
            verse_value_map = {"All Verses": ""}
            for verse in verses:
                count = count_verse_songs(current_filtered, st.session_state.selected_book, st.session_state.selected_chapter, verse)
                if count > 0 or verse == st.session_state.selected_verse:
                    cache_key = f"{st.session_state.selected_book}_{st.session_state.selected_chapter}_{verse}"
                    display = f"{verse} ({count})"
                    st.session_state.verse_display_cache[cache_key] = display
                    verse_options.append(display)
                    verse_value_map[display] = verse
            
            if st.session_state.selected_verse:
                cache_key = f"{st.session_state.selected_book}_{st.session_state.selected_chapter}_{st.session_state.selected_verse}"
                default_display = st.session_state.verse_display_cache.get(cache_key, "")
                default_index = verse_options.index(default_display) if default_display in verse_options else 0
            else:
                default_index = 0
            
            selected_verse_display = st.selectbox(
                "Verse",
                options=verse_options,
                index=default_index,
                key="verse_select"
            )
            st.session_state.selected_verse = verse_value_map[selected_verse_display]
        else:
            st.selectbox("Verse", options=[], disabled=True, key="verse_select_disabled")
    
    # Apply filters
    filtered_songs = filter_songs(
        songs,
        authors=st.session_state.selected_authors if st.session_state.selected_authors else None,
        languages=st.session_state.selected_languages if st.session_state.selected_languages else None,
        service_tags=st.session_state.selected_service_tags if st.session_state.selected_service_tags else None,
        theme_tags=st.session_state.selected_theme_tags if st.session_state.selected_theme_tags else None,
        other_tags=st.session_state.selected_other_tags if st.session_state.selected_other_tags else None,
        book=st.session_state.selected_book,
        chapter=st.session_state.selected_chapter,
        verse=st.session_state.selected_verse,
        lyrics_search=st.session_state.lyrics_search if st.session_state.lyrics_search else None
    )
    
    col1, col2 = st.columns(2)
    
    # Display songs table
    with col1:
        st.subheader(f"Songs ({len(filtered_songs)})")
        st.markdown("Select songs to include in the song sheet")
        for idx, song in enumerate(filtered_songs):
            col_check, col_title, col_authors, col_details = st.columns([1, 3, 2, 2])
            
            with col_check:
                # Find if song is already selected
                song_in_selected = False
                for selected in st.session_state.selected_songs:
                    if selected['title'] == song['title'] and selected['authors'] == song['authors']:
                        song_in_selected = True
                        break
                
                if st.checkbox(
                    "Add to database",
                    value=song_in_selected,
                    key=f"song_check_{idx}_{song['title']}",
                    label_visibility='hidden'
                ):
                    # Add to selected if not already there
                    if not song_in_selected:
                        st.session_state.selected_songs.append(song)
                else:
                    # Remove from selected if unchecked
                    st.session_state.selected_songs = [
                        s for s in st.session_state.selected_songs 
                        if not (s['title'] == song['title'] and s['authors'] == song['authors'])
                    ]
            
            with col_title:
                url = get_song_url(song.get("urls", {}))
                if url:
                    st.markdown(f"[{song['title']}]({url})")
                else:
                    st.write(song['title'])
            
            with col_authors:
                authors_str = ", ".join(song.get("authors", []))
                st.write(authors_str)
            
            # Allow selecting a song row
            with col_details:
                if st.button(f"Details", key=f"details_{idx}_{song['title']}"):
                    st.session_state.selected_song_index = idx
    
    # Display selected song details
    with col2:
        st.subheader("Song Details")
        if st.session_state.selected_song_index is not None and st.session_state.selected_song_index < len(filtered_songs):
            
            selected_song = filtered_songs[st.session_state.selected_song_index]
            
            # Title and authors
            authors_str = ", ".join(selected_song.get("authors", []))
            st.markdown(f"### {selected_song['title']}")
            st.write(f"**Authors:** {authors_str}")
            
            # Lyrics (render as HTML)
            st.markdown("#### Lyrics")
            lyrics_html = selected_song.get("lyrics", "")
            st.markdown(lyrics_html, unsafe_allow_html=True)
            
            # Notes
            if selected_song.get("notes"):
                st.markdown("#### Notes")
                st.write(selected_song.get("notes"))
            
            # Sources
            sources = format_sources(selected_song.get("sources", []))
            if sources:
                st.markdown("#### Sources")
                for source in sources:
                    st.write(source)
            # tags
            tags = selected_song.get("tags", [])
            if tags:
                st.markdown("#### Tags")
                for tag in tags:
                    st.write(tag)
        else:
            st.markdown("Select 'view details' to see song lyrics.")
