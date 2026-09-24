import streamlit as st

def show():
    st.markdown("""
        
    ## About Song Sheet Generator
    
    This program was written and designed Mark Goldman and Molly Fisch-Friedman to help us prepare for our monthly Hadar Rising Song Singing Circle. We are sharing this tool in case others would like to easily make well-formatted and consistent song sheets for their song circles.

    ## How to use this app
    
    ### 1. Browse songs
    
    Visit the "Browse Songs" page to explore our song database. You can filter songs by various categories. You can see each song's details (including lyrics, notes, and sources) by clicking on the 'Details' button. 
    
    ### 2. Select Songs
    
    Check the checkbox next to songs you want to include in your song sheet. 
    
    ### 3. Order Songs
    
     In the "Create Song Sheet" page, drag and drop the songs to the order that you prefer. 
    
    ### 4. Download Song Sheet
    
    In the "Create Song Sheet", click "Export as HTML" or "Export as DOCX". Once you have clicked that, a download button should appear for your to download the file.
    
    ### 5. Install Fonts
    
    The exported documents use open-source fonts which are not installed by default on all operating systems. To ensure proper formatting of your song sheet, you will need to install the following fonts:
    
    - **Taamey David CLM** - For Hebrew text
    - **Liberation Serif** - For English text
    - **Liberation Serif Italics** - For English italic text
    - **Inter SemiBold** - For English headings
    
    You can download these fonts from the [github repository](https://github.com/hashirim/song-sheet-generator/tree/main/fonts) or from these sources:
    - [Liberation Fonts](https://www.dafont.com/liberation-serif.font)
    - [Taamey David CLM](https://opensiddur.org/wp-content/uploads/fonts/TaameyDavidCLM/TaameyDavidCLM.zip)
    - [Inter SemiBold](https://rsms.me/inter/)

    Once you download the fonts, search for how to install fonts on your specific operating system. It is typically pretty simple, though it varies for different operating systems.
    
    ## Frequently asked questions?
    
    ### How did you decide what songs to include?
    
    We chose to include songs that met all the following criteria:
    * Are related to jewish themes
    * Can be sung by a group of people with various backgrounds
    * Are typically not the tunes sung in traditional synagogue services
    
    We also strive to have songs from a variety of artists. 
    
    ### I feel like the database is missing a great song. How can I help get it added?
    
    If there is a song that you think would be great to have here, you can add it in the following way:
    
    1. fill out an [issue on github](https://github.com/hashirim/song-sheet-generator/issues) with the song title, lyrics, and a link to the song.
    2. modify the json file and create a pull request in github (for those who are more tech savy). We have made a separate streamlit app for updating the song database. It is called `streamlit_song_editor.py`. You can download the github repository and run this app locally to modify the database. 
    
    ### How did you decide on the language for God?
    
    We have strived to provide consistent and accurate Hebrew, transliteration, and translation  throughout the database, but we invariably have made a mistake. If you notice anything that can be improved, please submit an [issue](https://github.com/hashirim/song-sheet-generator/issues) on the github page. 

    To avoid accidentally desecrating God's name in printed song sheets, we have replaced God's hebrew name with the yud-yud stand-in, which has been used for hundreds of years as a conservative alternative to make sure God's name is respected.

    In the transliteration of God's name, we have chosen to primarily use Adonai, sometimes even when the artist chose a different term, since this is the most common Hebrew word associated with God for many Jews. We find using Adonai in our songs helps uplift the spirituality and holiness of singing in community.
    
    We recognize that other people have different, perfectly valid practices, and we encourage anyone using this resource to adjust the words to their practice.
    
    ### I found a mistake in a song. How can I help get it fixed?
    
    Fill out an [issue on github](https://github.com/hashirim/song-sheet-generator/issues).
    
    ### The application seems broken. How do help I get it fixed?

    Fill out an [issue on github](https://github.com/hashirim/song-sheet-generator/issues).
    
    ### I have a suggestion to make this even better. How do I let you know?

    Fill out an [issue on github](https://github.com/hashirim/song-sheet-generator/issues).

    ### I am an artist and I don't want my song included here. How do I get you to remove it?
    
    Fill out an [issue on github](https://github.com/hashirim/song-sheet-generator/issues).

    ### I appreciate that you have put this together. How can I show my support?
    
    We have a few ways you can show your support:
    * Share this with your friends and family. 
    * Find a song you would like in the database and create an [issue](https://github.com/hashirim/song-sheet-generator/issues) for that song.
    * Message us to let us know how it has supported you.
    * Star the project on [github](https://github.com/hashirim/song-sheet-generator).
    """)

