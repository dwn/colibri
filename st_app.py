import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import numpy as np
import colibri
import st_utility as ut
try: from st_font_tool import font_tool
except: from st_font_tool.st_font_tool import font_tool
#App config
st.set_page_config(page_title='Colibri', page_icon=':book:', layout="wide")
st.markdown(f'<style>{ut.read("style.css")}</style>', unsafe_allow_html=True)
#ut.num_spectrum_colors = 30
ut.set_colors({
  'gold': [2,3,8,8,8],
  'brown': [2,-1]
})
#ut.show_colors()
#Init state
ut.init_state({
  'font_char_selected': ''
})
if 'book' not in st.session_state:
  st.session_state.book = colibri.Book()
  st.session_state.book.init('static/clb/', 'cyrillic')
  st.session_state.book.run()
#Navigation tabs
with st.container():
  arr_tab = [
    ':lower_left_fountain_pen:',
    ':ear:',
    ':eye:',
    ':scroll:',
    ':bust_in_silhouette:']
  font_tab, graph_tab, phone_tab, adjust_tab, account_tab = st.tabs(arr_tab)
##########################################
with font_tab:
##########################################
  with st.expander(st.session_state.font_char_selected if st.session_state.font_char_selected else 'character block', expanded=True):
    char_block_index = st.select_slider('block', label_visibility='collapsed', options=range(0, 6), value=1, key='character_expander_wkey')
    arr_ignore_char_index = [0x20, 0x2b, 0x2d, 0x5c, 0x5f, 0x7c, 0x7f, 0xa0, 0xad,
                             0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87,
                             0x88, 0x89, 0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f,
                             0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97,
                             0x98, 0x99, 0x9a, 0x9b, 0x9c, 0x9d, 0x9e, 0x9f]
    arr_first_char_index_in_block = [ 0x20, 0x40, 0x60, 0xa0, 0xc0, 0xe0 ]
    first_char_index = arr_first_char_index_in_block[char_block_index]
    for i_begin in range(first_char_index, first_char_index + 32, 8):
      i = i_begin
      for col in st.columns([1,1,1,1,1,1,1,1]):
        if i not in arr_ignore_char_index:
          c = ut.char(i)
          col.button(
            label=c,
            type='primary' if c == st.session_state.font_char_selected else 'secondary',
            on_click=ut.set_state_from_val,
            args=['font_char_selected', c],
            key=c)
        i += 1
  ##########################################
  with st.container(border=True):
    c = st.session_state.font_char_selected
    if c:
      asc = ut.asc(c)
      st.text_input(
        label='glyph code',
        label_visibility='collapsed',
        placeholder='glyph code',
        value=st.session_state.book.font['arr_glyph_code'][asc],
        on_change=ut.set_state_from_wkey,
        args=[['book', 'font', 'arr_glyph_code', asc], 'font_glyph_text_input_wkey'],
        key='font_glyph_text_input_wkey')
      font_tool(font_glyph_code=st.session_state.book.font['arr_glyph_code'][asc], key='font_tool_wkey')
      st.session_state.book.font['arr_glyph_code']
