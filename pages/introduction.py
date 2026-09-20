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
    
    Our documents format text using open-source fonts. To ensure proper formatting, you will need to install the following fonts:
    
    - **Taamey David CLM** - For Hebrew text
    - **Liberation Serif** - For English text
    - **Liberation Serif Bold** - For bold text
    - **Liberation Serif Italics** - For italic text
    
    You can download these fonts from:
    - [Liberation Fonts](https://www.dafont.com/liberation-serif.font)
    - [Taamey David CLM](https://opensiddur.org/wp-content/uploads/fonts/TaameyDavidCLM/TaameyDavidCLM.zip)
    
    Once you download the fonts, you can search for how to install fonts on your specific operating system.
    
    ### A note on song selection
    
    
    ### A note on language choice
    
    We have strived to provide consistent and accurate Hebrew, transliteration, and translation  throughout the database, but we invariably have made a mistake. If you notice anything that can be improved, please comment on the github page. 

To avoid accidentally desecrating God's name in printed song sheets, we have replaced God's hebrew name with the yud-yud stand-in, which has been used for hundreds of years as a conservative alternative to make sure God's name is respected.

In the transliteration of God's name, we have chosen to primarily use Adonai, sometimes even when the artist chose a different term, since this is the most common Hebrew word associated with God for many Jews. We find using Adonai in our songs helps uplift the spirituality and holiness of singing in community.

We recognize that other people have different, perfectly valid practices, and we encourage anyone using this resource to adjust the words to their practice.
    
    ### Having Questions or Suggestions?
    
    We'd love to hear from you! Please visit our [GitHub repository](https://github.com/hashirim/song-sheet-generator) to:
    - Report issues
    - Suggest new songs
    - Contribute improvements
    
    ### About This Project
    
    This program was written and designed by AI. No human will answer any of your questions or concerns. Song Sheet Generator is a community tool designed to make it easy to create beautiful, personalized song sheets for services, events, and personal use.
    """)

