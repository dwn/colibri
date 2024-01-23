import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import numpy as np
import colibri
import st_utility as ut
from st_font_tool import font_tool
#App config
st.set_page_config(page_title='Colibri', page_icon=':book:', layout="wide")
st.markdown('<style>{}</style>'.format(ut.read('style.css')), unsafe_allow_html=True)
#ut.num_spectrum_colors = 30
ut.set_colors({
  'gold': [2,3,8,8,8],
  'brown': [2,-1]
})
#ut.show_colors(); ut.show_spectrum()
#Read .clb file
book = colibri.ColibriBook()
book.init('static/clb/', 'teonaht')
book.run()
#Navigation tabs
with st.container():
  arrTab = [
    ':lower_left_fountain_pen:',
    ':ear:',
    ':eye:',
    ':scroll:',
    ':bust_in_silhouette:']
  fontTab, graphTab, phoneTab, adjustTab, accountTab = st.tabs(arrTab)
##########################################
# Font tab
##########################################
with fontTab:
  st.header('Hello World!')
  fontGlyphCodeIn = 'a/j'
  placeholder = st.empty()
  fontGlyphCodeIn = placeholder.text_input('glyph code', value='click a character')
  with st.container():
    ignore_chars = [0x20, 0x2b, 0x2d, 0x5c, 0x5f, 0x7c, 0x7f, 0xa0, 0xad]
    click = {}
    for i_begin in range(32, 255, 8):
      if not i_begin in [0x80, 0x88, 0x90, 0x98]: #Reserved lines of ASCII space
        i = i_begin
        for col in st.columns([1,1,1,1,1,1,1,1]):
          if i not in ignore_chars:
            c = '\\'+chr(i)
            if len(c) > 1 and c != '\\#' and c != '\\*': #Maintains escaping on special markdown characters
              c = c[1]
            click[i] = col.button(c, key=i)
          i += 1
    for i in click:
      if click[i]:
        fontGlyphCodeIn = placeholder.text_input('glyph code', value=book.font['arrGlyphCode'][i])
  fontGlyphCodeOut = font_tool(fontGlyphCode=fontGlyphCodeIn)
  st.markdown('You clicked! '+str(fontGlyphCodeOut))
