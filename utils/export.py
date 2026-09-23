import html
from typing import List, Dict, Any
from utils.data_loader import load_css
from utils.url_handler import get_song_url
from utils.source_formatter import format_sources
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import streamlit as st

def format_authors(authors: List[str]) -> str:
    """Format authors with ampersand before last author"""
    if not authors:
        return ""
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return f"{authors[0]} & {authors[1]}"
    return ", ".join(authors[:-1]) + f" & {authors[-1]}"

def export_html(songs: List[Dict[str, Any]], sheet_name: str) -> str:
    """Generate HTML export of song sheet"""
    css = load_css()
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{html.escape(sheet_name)}</title>
    <style>
{css}
    </style>
</head>
<body>
    <h1>{html.escape(sheet_name)}</h1>
"""
    
    for idx, song in enumerate(songs, 1):
        title = song.get("title", "")
        authors = song.get("authors", [])
        lyrics = song.get("lyrics", "")
        url = get_song_url(song.get("urls", {}))
        
        authors_str = format_authors(authors)
        
        # Title line with URL
        if url:
            html_content += f'    <h2><a href="{html.escape(url)}" target="_blank">{idx}. {html.escape(title)} - {html.escape(authors_str)}</a></h2>\n'
        else:
            html_content += f'    <h2>{idx}. {html.escape(title)} - {html.escape(authors_str)}</h2>\n'
        
        # Lyrics
        html_content += f"    {lyrics}\n"
    
    # Footer
    html_content += """
    <p style="font-size: 0.9em; margin-top: 2cm;">
        Created by <a href="https://github.com/hashirim/song-sheet-generator" target="_blank">Song Sheet Generator</a>. 
        Check it out for sources and notes about the songs.
    </p>
</body>
</html>
"""
    
    return html_content

def add_section_with_columns(doc):
    """Add section with two columns"""
    section = doc.sections[0]
    sectPr = section._sectPr
    cols = sectPr.xpath('./w:cols')[0] if sectPr.xpath('./w:cols') else OxmlElement('w:cols')
    cols.set(qn('w:num'), '2')  # 2 columns
    cols.set(qn('w:sep'), '0')  # no separator line between columns
    cols.set(qn('w:space'), '0')  # no gap between columns
    if not sectPr.xpath('./w:cols'):
        sectPr.append(cols)

def modify_styles(doc):
    styles = doc.styles
    #st.markdown([x for x in styles])
    # 0 Modify normal font
    styles["Normal"].font.name = "Liberation Serif"
    styles["Normal"].font.size = Pt(12)
    styles['Normal'].font.color.rgb = RGBColor(0, 0, 0)
    styles['Normal'].paragraph_format.line_spacing = 1
    
    
    style = styles["Body Text"]
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:cs"), "Taamey David CLM")
    rFonts.set(qn("w:ascii"), "Liberation Serif")
    rFonts.set(qn("w:eastAsia"), "Liberation Serif")
    rFonts.set(qn("w:hAnsi"), "Liberation Serif")
    styles["Body Text"].font.size = Pt(12)
    styles['Normal'].paragraph_format.line_spacing = 1
    
    # 1. Modify Heading 1
    heading1 = styles.add_style('Song Heading', WD_STYLE_TYPE.PARAGRAPH)
    heading1.font.color.rgb = RGBColor(0, 70, 150)
    heading1.font.size = Pt(12)
    heading1.paragraph_format.space_after = Pt(0)
    heading1.paragraph_format.space_before = Pt(0)
    heading1.font.name = "Liberation Serif"
    
    # 2. Modify Block Quote
    blockquote = styles["Quote"]
    # Grey text
    blockquote.font.color.rgb = RGBColor(160, 160, 160)
    # Remove left/right paragraph indentation
    pf = blockquote.paragraph_format
    pf.left_indent = Pt(0)
    pf.right_indent = Pt(0)
    pf.first_line_indent = Pt(0)
    

    # 3. Create Hebrew and Transliteration styles
    style = styles.add_style('hebrew', WD_STYLE_TYPE.PARAGRAPH)
    style.base_style = styles["Body Text"]
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:cs"), "Taamey David CLM")
    rFonts.set(qn("w:ascii"), "Taamey David CLM")
    rFonts.set(qn("w:eastAsia"), "Taamey David CLM")
    rFonts.set(qn("w:hAnsi"), "Taamey David CLM")
    #style.font.name = {'ascii':"Liberation Serif", 'cs': "Taamey David CLM", 'eastAsia': "Liberation Serif"}
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.right_to_left = True
    style.paragraph_format.line_spacing = Cm(0.48)
    style.font.size = Pt(12.5)
    # change complex font size
    szCs = OxmlElement("w:szCs")
    szCs.set(qn("w:val"), "25")  # 12.5 pt = 25 half-points
    rPr.append(szCs)
    #rPr.get_or_add_szCs().set(qn("w:val"), "25")  # 12.5 pt = 25 half-points

    
    style = styles.add_style('transliteration', WD_STYLE_TYPE.PARAGRAPH)
    style.base_style = styles["Body Text"]
    style.paragraph_format.space_after = Pt(0)
    
    # 3. Create source style
    style = styles.add_style('source', WD_STYLE_TYPE.PARAGRAPH)
    style.base_style = styles["Body Text"]
    styles["source"].font.size = Pt(9)
        
def export_docx(songs: List[Dict[str, Any]], sheet_name: str) -> bytes:
    """Generate DOCX export of song sheet"""
    doc = Document()
    modify_styles(doc)
    
    # Set margins to 1 cm and add headers and footers
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.39)  # 1 cm in inches
        section.bottom_margin = Inches(0.39)
        section.left_margin = Inches(0.39)
        section.right_margin = Inches(0.39)
        document_header = section.header.paragraphs[0]
        title_run = document_header.add_run(sheet_name)
        document_header.style = 'Song Heading'
        #title_run.bold = True
        #title_run.font.size = Pt(12)
        #title_run.font.color = RGBColor(0, 0, 255)
        document_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
    # Add two columns
    add_section_with_columns(doc)
    
    # Add songs
    all_sources = ""
    for idx, song in enumerate(songs, 1):
        try:
            title_text = song.get("title", "")
            authors = song.get("authors", [])
            lyrics_html = song.get("lyrics", "")
            sources = format_sources(song.get("sources", []))
            url = get_song_url(song.get("urls", {}))
            
            authors_str = format_authors(authors)
            
            # Title line with optional URL
            title_para = doc.add_paragraph()
            title_para.style = 'Song Heading'
            if url:
                title_run = title_para.add_run(f"{idx}. ") 
                #title_run.font.name = "Liberation Serif"
                #title_run = title_para.add_run(f"{title_text} - {authors_str}")
                title_run = title_para.add_run(f"{title_text}")
                #title_run.font.name = "Liberation Serif"
                # Add hyperlink
                r_id = doc.part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
                hyperlink = OxmlElement("w:hyperlink")
                hyperlink.set(qn("r:id"), r_id)
                run = OxmlElement("w:r")
                text = OxmlElement("w:t")
                text.text = f"{idx}. {title_text}"
                run.append(text)
                hyperlink.append(run)
                title_para._element.clear_content()
                title_para._element.append(hyperlink)
            else:
                title_run = title_para.add_run(f"{idx}. {title_text}")

            # Add with sources if they exist
            if sources or authors_str:
                all_sources += f"{idx}. "
                if authors_str:
                    all_sources += f"Artist(s): {authors_str} "
                if sources and authors_str:
                    all_sources += "| "
                if sources:
                    footnote_text = ", ".join(sources)
                    all_sources += f"Source(s): {footnote_text}"
                all_sources += '\n'
            #    title_run_note = title_para.add_run(f" [{footnote_text}]")
            #    title_run_note.font.size = Pt(10)
        except Exception as e:
            st.markdown("Raised error in song {}".format(song))
            #st.markdown(f'<w:hyperlink {qn("r:id")}="{r_id}"><w:r><w:t>{html.escape(f"{idx}. {title_text} - {authors_str}")}</w:t></w:r></w:hyperlink>')
            #st.markdown(qn("r:id"))
            
            #st.markdown(r_id)
            raise e
        # Parse and add lyrics
        soup = BeautifulSoup(lyrics_html, 'html.parser')
        _add_html_to_docx(doc, soup)
    
    # Add Sources
    p = doc.add_paragraph()
    p.style = "Song Heading"
    run = p.add_run("Song Information")
    run.font.size = Pt(9)
    p = doc.add_paragraph()
    p.style = "Body Text"
    run = p.add_run(all_sources[:-1])
    run.font.size = Pt(9)
    
    # Add footer
    section = doc.add_section(WD_SECTION.CONTINUOUS)
    sectPr = section._sectPr
    cols = sectPr.xpath('./w:cols')[0] if sectPr.xpath('./w:cols') else OxmlElement('w:cols')
    cols.set(qn('w:num'), '1') # 1 column
    footer_para = doc.add_paragraph()
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_para.paragraph_format.space_before = Pt(9)
    footer_para
    footer_run = footer_para.add_run("Created using ")
    footer_run.font.size = Pt(9)

    
    # Add hyperlink for Song Sheet Generator
    r_id = doc.part.relate_to('https://github.com/hashirim/song-sheet-generator', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    # set font size in weird way cuz low-level xml
    rPr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "18")
    rPr.append(sz)
    run.append(rPr)
    
    text = OxmlElement("w:t")
    text.text = "Song Sheet Generator"
    run.append(text)
    hyperlink.append(run)
    footer_para._element.append(hyperlink)
    run = footer_para.add_run(". Found a typo? Submit it to github.com/hashirim/song-sheet-generator")
    run.font.size = Pt(9)
    
    # Save to bytes
    from io import BytesIO
    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output.getvalue()

def _add_html_to_docx(doc, element):
    """Recursively add HTML elements to a DOCX document"""
    #st.markdown(element.name)
    if isinstance(element, str):
        # Text content
        if element.strip():
            doc.paragraphs[-1].add_run(element)
    elif (element.name == 'p') or (element.name == 'blockquote'):
        para = doc.add_paragraph()
        
        # Check for class
        class_attr = element.get('class', [])
        if isinstance(class_attr, list):
            class_attr = ' '.join(class_attr)
        #st.markdown(class_attr)
        if element.name == 'blockquote':
            para.style = 'Quote'
        elif class_attr in ['hebrew', 'transliteration']:
            para.style = class_attr
        else:
            para.style = "Body Text"
        
        for child in element.children:
            _add_html_run_to_para(para, child)
    
    elif element.name == 'br':
        doc.paragraphs[-1].add_run('\n')
    
    else:
        for child in element.children:
            _add_html_to_docx(doc, child)

def _add_html_run_to_para(para, element):
    """Add HTML run content to a paragraph"""
    if isinstance(element, str):
        text = str(element).strip()
        if text:
            para.add_run(text)
    elif element.name == 'br':
        para.add_run('\n')
    elif element.name == 'p':
        # Nested paragraph - shouldn't happen but handle it
        text_content = element.get_text()
        if text_content.strip():
            para.add_run(text_content)
    elif element.name in ['span', 'b', 'strong', 'i', 'em']:
        text = element.get_text()
        if text:
            run = para.add_run(text)
            if element.name in ['b', 'strong']:
                run.bold = True
            if element.name in ['i', 'em']:
                run.italic = True
    else:
        for child in element.children:
            _add_html_run_to_para(para, child)

