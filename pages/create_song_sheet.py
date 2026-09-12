import streamlit as st
from utils.export import export_html, export_docx
import pandas as pd

def show():
    st.title("Create Song Sheet")
    
    if not st.session_state.selected_songs:
        st.info("No songs selected. Please go to 'Browse Songs' to select songs for your sheet.")
        return
    
    st.subheader("Selected Songs")
    
    # Display selected songs in table
    songs_data = []
    for song in st.session_state.selected_songs:
        songs_data.append({
            "Title": song.get("title", ""),
            "Authors": ", ".join(song.get("authors", []))
        })
    
    df = pd.DataFrame(songs_data)
    st.dataframe(df, use_container_width=True)
    
    st.info(f"{len(st.session_state.selected_songs)} song(s) selected")
    
    # Note: Streamlit doesn't have built-in drag-and-drop sorting for data
    # You can implement manual reordering with buttons or use a third-party library
    
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

