import streamlit as st
from utils.export import export_html, export_docx
import pandas as pd
from streamlit_sortables import sort_items

def show():
    st.title("Create Song Sheet")
    
    if not st.session_state.selected_songs:
        st.info("No songs selected. Please go to 'Browse Songs' to select songs for your sheet.")
        return
    
    st.subheader("Selected Songs")
    
    # Create list of song display strings with unique keys
    songs_display = []
    for i, song in enumerate(st.session_state.selected_songs):
        title = song.get("title", "")
        authors = ", ".join(song.get("authors", []))
        display_text = f"{title} - {authors}" if authors else title
        songs_display.append(display_text)
    
    # Use streamlit-sortables for drag-and-drop reordering
    st.info("Drag to reorder songs")
    sort_style = """
.sortable-component {
    font-size: 16px;
    counter-reset: item;
}
.sortable-item {
    background-color: black;
    color: white;
}
.sortable-item, .sortable-item:hover {
    background-color: rgb(62, 95, 92);
    font-color: #FFFFFF;
    font-weight: bold;
}
"""

    sorted_songs = sort_items(songs_display, direction='vertical', custom_style=sort_style)
    
    # Reorder the actual song data based on the sorted display order
    if sorted_songs:
        # Create a mapping of display text to original song data
        display_to_song = {}
        for i, song in enumerate(st.session_state.selected_songs):
            title = song.get("title", "")
            authors = ", ".join(song.get("authors", []))
            display_text = f"{title} - {authors}" if authors else title
            display_to_song[display_text] = song
        
        # Reorder songs based on sorted display order
        reordered_songs = [display_to_song[display] for display in sorted_songs]
        st.session_state.selected_songs = reordered_songs

    # Song sheet name
    st.subheader("Song Sheet Details")
    sheet_name = st.text_input(
        "Song Sheet Name",
        value="My Song Sheet",
        placeholder="Enter the name for your song sheet"
    )
    
    # Export buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export as HTML"):
            html_content = export_html(st.session_state.selected_songs, sheet_name)
            st.download_button(
                label="Download HTML",
                data=html_content,
                file_name=f"{sheet_name.replace(' ', '_')}.html",
                mime="text/html"
            )
            st.success("HTML export ready!")
            _show_font_warning()
    
    with col2:
        if st.button("📝 Export as DOCX"):
            docx_bytes = export_docx(st.session_state.selected_songs, sheet_name)
            st.download_button(
                label="Download DOCX",
                data=docx_bytes,
                file_name=f"{sheet_name.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            st.success("DOCX export ready!")
            _show_font_warning()

def _show_font_warning():
    """Display font installation instructions"""
    st.warning("""
    **Important: Font Installation**
    
    To ensure proper formatting of your exported song sheet, please install the following fonts on your computer:
    
    - **Taamey David CLM** - For Hebrew text
    - **Liberation Serif** - For English text
    - **Liberation Serif Bold** - For bold text
    - **Liberation Serif Italics** - For italic text
    
    Download these fonts from:
    - [Liberation Fonts](https://github.com/liberationfonts/liberation-fonts)
    - [Taamey David CLM](https://github.com/opensiddur/opensiddur-server/wiki/Taamey-David-CLM)
    """)
