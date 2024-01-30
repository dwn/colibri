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
  font_tab, phone_tab, graph_tab, adjust_tab, account_tab = st.tabs(arr_tab)
##########################################
with font_tab:
##########################################
  with st.expander(st.session_state.font_char_selected or 'select a character', expanded=True):
    char_block_index = st.select_slider('block', label_visibility='collapsed', options=range(0, 6), value=2, key='character_expander_wkey')
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
          status = col.button(
            label=c,
            type='primary' if c == st.session_state.font_char_selected else 'secondary',
            key=c)
          if status:
            st.session_state.font_char_selected = c
        i += 1
  ##########################################
  with st.container(border=True):
    c = st.session_state.font_char_selected
    if c:
      i = ut.asc(c) - 33 #First 33 are ascii control characters not included in list
      g = st.session_state.book.font['arr_glyph_code'][i]
      status = st.text_input(
        label='glyph code',
        label_visibility='collapsed',
        placeholder='glyph code',
        value=g,
        key='font_glyph_text_input_wkey')
      if status:
        st.session_state.book.font['arr_glyph_code'][i] = status
      font_tool(
        font_glyph_code=g,
        key='font_tool_wkey')
##########################################
with phone_tab:
##########################################
  with st.expander('phonemes', expanded=True):
    st.text_area(
      label='phonemes',
      label_visibility='collapsed',
      placeholder='example:\nii,i i,I a,e',
      height=600,
      key='phonemes_text_area_wkey')
  left, right = st.columns([1,1])
  left.text_area(
    label='original',
    height=600,
    key='phonemes_original_text_area_wkey')
  right.text_area(
    label='replaced',
    height=600,
    key='phonemes_replaced_text_area_wkey')
##########################################
with graph_tab:
##########################################
  with st.expander('graphemes', expanded=True):
    st.text_area(
      label='graphemes',
      label_visibility='collapsed',
      placeholder='example:\nii,i i,I a,e',
      height=600,
      key='graphemes_text_area_wkey')
  left, right = st.columns([1,1])
  left.text_area(
    label='original',
    height=600,
    key='graphemes_original_text_area_wkey')
  right.text_area(
    label='replaced',
    height=600,
    key='graphemes_replaced_text_area_wkey')
