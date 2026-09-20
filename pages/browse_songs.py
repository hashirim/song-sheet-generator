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
    
    # Filters section
    st.subheader("Filters")
    
    col1, col2, col3 = st.columns(3)
    
    # Author filter
    with col1:
        authors = get_all_authors(songs)
        author_options = [f"{author} ({count_author_songs(songs, author)})" for author in authors]
        author_labels = {opt: author for opt, author in zip(author_options, authors)}
        
        selected_author_options = st.multiselect(
            "Artist/Author",
            options=author_options,
            default=[opt for opt in author_options if author_labels[opt] in st.session_state.selected_authors],
            key="author_multiselect"
        )
        st.session_state.selected_authors = [author_labels[opt] for opt in selected_author_options]
    
    # Language filter
    with col2:
        languages = get_all_languages(songs)
        language_options = [f"{lang} ({count_language_songs(songs, lang)})" for lang in languages]
        language_labels = {opt: lang for opt, lang in zip(language_options, languages)}
        
        selected_language_options = st.multiselect(
            "Language",
            options=language_options,
            default=[opt for opt in language_options if language_labels[opt] in st.session_state.selected_languages],
            key="language_multiselect"
        )
        st.session_state.selected_languages = [language_labels[opt] for opt in selected_language_options]
    
    # Service & Holiday tags filter
    with col3:
        service_tags = get_service_tags(songs)
        service_options = [f"{tag} ({count_tag_songs(songs, tag)})" for tag in service_tags]
        service_labels = {opt: tag for opt, tag in zip(service_options, service_tags)}
        
        selected_service_options = st.multiselect(
            "Service & Holiday",
            options=service_options,
            default=[opt for opt in service_options if service_labels[opt] in st.session_state.selected_service_tags],
            key="service_multiselect"
        )
        st.session_state.selected_service_tags = [service_labels[opt] for opt in selected_service_options]
    
    col4, col5, col6 = st.columns(3)
    
    # Theme tags filter
    with col4:
        theme_tags = get_theme_tags(songs)
        theme_options = [f"{tag} ({count_tag_songs(songs, tag)})" for tag in theme_tags]
        theme_labels = {opt: tag for opt, tag in zip(theme_options, theme_tags)}
        
        selected_theme_options = st.multiselect(
            "Theme Tags",
            options=theme_options,
            default=[opt for opt in theme_options if theme_labels[opt] in st.session_state.selected_theme_tags],
            key="theme_multiselect"
        )
        st.session_state.selected_theme_tags = [theme_labels[opt] for opt in selected_theme_options]
    
    # Other tags filter
    with col5:
        other_tags = get_other_tags(songs)
        other_options = [f"{tag} ({count_tag_songs(songs, tag)})" for tag in other_tags]
        other_labels = {opt: tag for opt, tag in zip(other_options, other_tags)}
        
        selected_other_options = st.multiselect(
            "Additional Tags",
            options=other_options,
            default=[opt for opt in other_options if other_labels[opt] in st.session_state.selected_other_tags],
            key="other_multiselect"
        )
        st.session_state.selected_other_tags = [other_labels[opt] for opt in selected_other_options]
    
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
        book_options = [""] + books
        book_display = ["All Books"] + [f"{book} ({count_book_songs(songs, book)})" for book in books]
        book_mapping = {display: book for display, book in zip(book_display, book_options)}
        
        # Find the index safely
        selected_index = 0
        if st.session_state.selected_book:
            for i, display in enumerate(book_display):
                if book_mapping[display] == st.session_state.selected_book:
                    selected_index = i
                    break
        
        selected_book_display = st.selectbox(
            "Book",
            options=book_display,
            index=selected_index,
            key="book_select"
        )
        st.session_state.selected_book = book_mapping[selected_book_display]
        
        if not st.session_state.selected_book:
            st.session_state.selected_chapter = None
            st.session_state.selected_verse = None
    
    with source_col2:
        if st.session_state.selected_book:
            chapters = get_chapters_for_book(songs, st.session_state.selected_book)
            chapter_options = [""] + chapters
            chapter_display = ["All Chapters"] + [
                f"{chapter} ({count_chapter_songs(songs, st.session_state.selected_book, chapter)})" 
                for chapter in chapters
            ]
            chapter_mapping = {display: chapter for display, chapter in zip(chapter_display, chapter_options)}
            
            # Find the index safely
            selected_index = 0
            if st.session_state.selected_chapter:
                for i, display in enumerate(chapter_display):
                    if chapter_mapping[display] == st.session_state.selected_chapter:
                        selected_index = i
                        break
            
            selected_chapter_display = st.selectbox(
                "Chapter",
                options=chapter_display,
                index=selected_index,
                key="chapter_select"
            )
            st.session_state.selected_chapter = chapter_mapping[selected_chapter_display]
            
            if not st.session_state.selected_chapter:
                st.session_state.selected_verse = None
        else:
            st.selectbox("Chapter", options=[], disabled=True, key="chapter_select_disabled")
    
    with source_col3:
        if st.session_state.selected_book and st.session_state.selected_chapter:
            verses = get_verses_for_book_chapter(songs, st.session_state.selected_book, st.session_state.selected_chapter)
            verse_options = [""] + verses
            verse_display = ["All Verses"] + [
                f"{verse} ({count_verse_songs(songs, st.session_state.selected_book, st.session_state.selected_chapter, verse)})"
                for verse in verses
            ]
            verse_mapping = {display: verse for display, verse in zip(verse_display, verse_options)}
            
            # Find the index safely
            selected_index = 0
            if st.session_state.selected_verse:
                for i, display in enumerate(verse_display):
                    if verse_mapping[display] == st.session_state.selected_verse:
                        selected_index = i
                        break
            
            selected_verse_display = st.selectbox(
                "Verse",
                options=verse_display,
                index=selected_index,
                key="verse_select"
            )
            st.session_state.selected_verse = verse_mapping[selected_verse_display]
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
                    "",
                    value=song_in_selected,
                    key=f"song_check_{idx}_{song['title']}"
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
        else:
            st.markdown("Select 'view details' to see song lyrics.")

