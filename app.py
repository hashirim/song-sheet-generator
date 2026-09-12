import streamlit as st
from pages import introduction, browse_songs, create_song_sheet

# Configure page
st.set_page_config(
    page_title="Song Sheet Generator",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit's automatic page navigation
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "selected_songs" not in st.session_state:
    st.session_state.selected_songs = []

if "song_order" not in st.session_state:
    st.session_state.song_order = []

# Navigation
st.sidebar.title("Song Sheet Generator")
page = st.sidebar.radio(
    "Navigation",
    ["Introduction", "Browse Songs", "Create Song Sheet"],
    index=0
)

# Route to appropriate page
if page == "Introduction":
    introduction.show()
elif page == "Browse Songs":
    browse_songs.show()
elif page == "Create Song Sheet":
    create_song_sheet.show()

