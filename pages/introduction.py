import streamlit as st

def show():
    st.title("Welcome to Song Sheet Generator")
    
    st.markdown("""
    ## How to Use This App
    
    This application helps you browse our collection of songs and create personalized song sheets that you can export as HTML or Word documents.
    
    ### Getting Started
    
    1. **Browse Songs**: Visit the "Browse Songs" page to explore our song database. You can filter songs by:
       - Artist/Author
       - Language
       - Service & Holiday (shacharit, maariv, shabbat, havdalah, etc.)
       - Thematic tags (love, peace, healing, nature, etc.)
       - Other tags
       - Source materials (Bible books, liturgy, etc.)
       - Lyrics search
    
    2. **Select Songs**: Check the checkbox next to songs you want to include in your song sheet. You'll be able to see full details including lyrics, notes, and sources.
    
    3. **Create Song Sheet**: Go to the "Create Song Sheet" page to:
       - Reorder your selected songs
       - Name your song sheet
       - Export as HTML or Word document
    
    ### Font Installation
    
    After exporting your song sheet, you may need to install the following fonts to ensure proper formatting:
    
    - **Taamey David CLM** - For Hebrew text
    - **Liberation Serif** - For English text
    - **Liberation Serif Bold** - For bold text
    - **Liberation Serif Italics** - For italic text
    
    You can download these fonts from:
    - [Liberation Fonts](https://github.com/liberationfonts/liberation-fonts)
    - [Taamey David CLM](https://github.com/opensiddur/opensiddur-server/wiki/Taamey-David-CLM)
    
    ### Having Questions or Suggestions?
    
    We'd love to hear from you! Please visit our [GitHub repository](https://github.com/hashirim/song-sheet-generator) to:
    - Report issues
    - Suggest new songs
    - Contribute improvements
    
    ### About This Project
    
    Song Sheet Generator is a community tool designed to make it easy to create beautiful, personalized song sheets for services, events, and personal use.
    """)

