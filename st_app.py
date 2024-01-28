import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import numpy as np
import colibri
import time
import st_utility as ut
try:
  from st_font_tool import font_tool
except:
  from st_font_tool.st_font_tool import font_tool #Dev mode sees it as this path
# State init
if 'font_glyph_code' not in st.session_state:
  st.session_state.font_glyph_code = ''
if 'selected_char' not in st.session_state:
  st.session_state.selected_char = ''
# State update callback
def callbk(attrib, key):
  st.session_state[attrib] = st.session_state[key]
#App config
st.set_page_config(page_title='Colibri', page_icon=':book:', layout="wide")
st.markdown(f'<style>{ut.read("style.css")}</style>', unsafe_allow_html=True)
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
  with st.expander('character', expanded=True):
    st.session_state.selected_char
    char_block_index = st.select_slider('character block', options=range(0, 6), value=1)
    arr_ignore_char_index = [0x20, 0x2b, 0x2d, 0x5c, 0x5f, 0x7c, 0x7f, 0xa0, 0xad,
                             0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87,
                             0x88, 0x89, 0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f,
                             0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97,
                             0x98, 0x99, 0x9a, 0x9b, 0x9c, 0x9d, 0x9e, 0x9f]
    arr_first_char_index_in_block = [ 0x20, 0x40, 0x60, 0xa0, 0xc0, 0xe0 ]
    click = {}
    first_char_index = arr_first_char_index_in_block[char_block_index]
    for i_begin in range(first_char_index, first_char_index + 32, 8):
      i = i_begin
      for col in st.columns([1,1,1,1,1,1,1,1]):
        if i not in arr_ignore_char_index:
          c = ut.char(i)
          key = 'character ' + c
          click[key] = col.button(c, type=('primary' if 'character ' + ut.char(i) == st.session_state.selected_char else 'secondary'), on_click=callbk, args=['selected_char', key], key=key)
        i += 1
    for key in click:
      if click[key]:
        st.session_state.selected_char = key
        st.session_state.font_glyph_code = book.font['arrGlyphCode'][ut.asc(key)]
  with st.container(border=True):
    st.text_input('glyph code', value=st.session_state.font_glyph_code or '', on_change=callbk, args=['font_glyph_code', 'font_glyph_code_text_input_key'], key='font_glyph_code_text_input_key')
    temp = font_tool(fontGlyphCode = st.session_state.font_glyph_code or '')
    st.markdown('You clicked! ' + temp)
