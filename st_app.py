import json
import os
import streamlit as st
from streamlit import session_state as state
from streamlit.components.v1 import html
import pandas as pd
import numpy as np
import colibri
import st_utility as ut
from st_supabase import db
from streamlit_shortcuts import add_keyboard_shortcuts
try: from st_font_tool import font_tool
except: from st_font_tool.st_font_tool import font_tool
##########################################
# INIT
##########################################
#App config
if 'bool_configured' not in state:
  st.set_page_config(page_title='Colibri', page_icon=':book:', layout="wide")
  state.bool_configured = True
st.markdown(f'<style>{ut.read("style.css")}</style>', unsafe_allow_html=True)
#Book state variable
if 'book' not in state:
  state.book = colibri.Book()
  state.book.init('static/clb/ignota.clb')
  state.book.update()
  state.book.run()
#Other state variables
def init_app_state(bool_overwrite=False):
  ut.init_state({
    'num_runs': 0,
    'bool_saved': False,
    'autosave_interval_sec': 20,
    'font_char_selected': '',
    'library': sorted(os.listdir('static/clb/')),
    'phone_script_text_area_wkey': state.book.source['phone_replace'],
    'phone_original_text_area_wkey': state.book.source['arr_book_page'][0],
    'graph_script_text_area_wkey': state.book.source['graph_replace'],
    'graph_original_text_area_wkey': state.book.source['arr_book_page'][0],
  }, bool_overwrite=bool_overwrite)
  state.num_runs += 1
init_app_state()
with st.expander('{} runs'.format(state.num_runs)):
  state.book
#Set some color names
#ut.num_spectrum_colors = 30
#ut.set_colors({ 'gold': [2,3,8,8,8], 'brown': [2,-1] })
#ut.show_colors()
#Save button and hotkey
with st.expander(':green[saved]' if state.bool_saved else ':orange[unsaved (alt+enter)]', expanded=True):
  def save():
    db.table('colibri_source').insert(
      [{'colibri_source': state.book.source}]
    ).execute()
    state.bool_saved = True
  col0, col1 = st.columns([1,1])
  col0.write('{}'.format(state.book.source['title']))
  col1.button('save', on_click=save)
  add_keyboard_shortcuts({
    'Alt+Enter': 'save',
  })
#arr_source = db.query("*", table="colibri_source").execute()
#state.book.source
#Navigation tabs
arr_tab = [
  ':bust_in_silhouette:',
  ':lower_left_fountain_pen:',
  ':ear:',
  ':eye:',
  ':scroll:']
account_tab, font_tab, phone_tab, graph_tab, adjust_tab = st.tabs(arr_tab)
##########################################
with account_tab:
##########################################
  def select_from_library():
    state.book.init('static/clb/' + state.account_library_text_input_wkey)
    state.book.update()
    state.book.run()
    init_app_state(bool_overwrite=True)
  with st.expander('language', expanded=True):
    st.selectbox(
      label='your projects',
      options=['english', 'russian'],
      key='account_your_projects_text_input_wkey')
    st.selectbox(
      label='library',
      options=state.library,
      on_change=select_from_library,
      key='account_library_text_input_wkey')
  with st.expander('profile', expanded=True):
    st.text_input(
      label='name',
      key='account_username_text_input_wkey')
    st.radio(
      label='mode',
      options=['create','read','chat'],
      key='account_mode_toggle_wkey')
##########################################
with font_tab:
##########################################
  with st.expander(state.font_char_selected or 'select a character', expanded=True):
    char_block_index = st.select_slider('block', label_visibility='collapsed', options=range(0, 6), value=2, key='character_expander_wkey')
    arr_ignore_char_index = [
      0x20, 0x2b, 0x2d, 0x5c, 0x5f, 0x7c, 0x7f, 0xa0, 0xad,
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
            type='primary' if c == state.font_char_selected else 'secondary',
            on_click=lambda c=c: state.update(font_char_selected=c),
            key=c)
        i += 1
  ##########################################
  with st.container(border=True):
    c_sel = state.font_char_selected
    if c_sel:
      i_sel = ut.asc(c_sel) - 33 #First 33 are ascii control characters not included in list
      g_sel = state.book.font['arr_glyph_code'][i_sel]
      st.text_input(
        label='glyph code',
        label_visibility='collapsed',
        placeholder='glyph code',
        value=g_sel,
        on_change=lambda g_sel=g_sel: state.update(font_glyph_code=g_sel),
        key='font_glyph_text_input_wkey')
      font_tool(
        font_glyph_code=g_sel,
        key='font_tool_wkey')
##########################################
with phone_tab:
##########################################
  def update_phone_script():
    ut.set_state_from_wkey(['book','source','phone_replace'], 'phone_script_text_area_wkey')
    state.book.update()
    state.book.run()
  def update_phone_original():
    ut.set_state_from_wkey(['book','source','arr_book_page',0], 'phone_original_text_area_wkey')
    state.book.update()
    state.book.run()
  st.expander('phoneme script', expanded=True).text_area(
      label='script',
      label_visibility='collapsed',
      placeholder='example:\nii,i i,I a,e',
      height=600,
      on_change=update_phone_script,
      key='phone_script_text_area_wkey')
  left, right = st.columns([1,1])
  left.text_area(
    label='original',
    label_visibility='collapsed',
    height=600,
    on_change=update_phone_original,
    key='phone_original_text_area_wkey')
  with right:
    html('<body style="background-color: #f0ead6"><span style="white-space: pre-line; font-family: monospace; color: charcoal">{}</span>'.format(state.book.phone['text'][0]), height=600)
##########################################
with graph_tab:
##########################################
  def update_graph_script():
    ut.set_state_from_wkey(['book','source','graph_replace'], 'graph_script_text_area_wkey')
    state.book.update()
    state.book.run()
  def update_graph_original():
    ut.set_state_from_wkey(['book','source','arr_book_page',0], 'graph_original_text_area_wkey')
    state.book.update()
    state.book.run()
  st.expander('grapheme script', expanded=True).text_area(
      label='script',
      label_visibility='collapsed',
      placeholder='example:\nii,i i,I a,e',
      height=600,
      on_change=update_graph_script,
      key='graph_script_text_area_wkey')
  left, right = st.columns([1,1])
  left.text_area(
    label='original',
    label_visibility='collapsed',
    height=600,
    on_change=update_graph_original,
    key='graph_original_text_area_wkey')
  with right:
    html('<body style="background-color: #f0ead6"><span style="white-space: pre-line; font-family: monospace; color: charcoal">{}</span>'.format(state.book.graph['text'][0]), height=600)
##########################################
with adjust_tab:
##########################################
  with st.expander('options', expanded=True):
    st.selectbox(
      label='size',
      options=[
        'small',
        'large'],
      key='adjust_size_select_box_wkey')
    st.selectbox(
      label='weight',
      options=[
        'light',
        'bold'],
      key='adjust_style_select_box_wkey')
    st.selectbox(
      label='pen',
      options=[
        'round',
        'medium',
        'sharp'],
      key='adjust_pen_select_box_wkey')
    st.selectbox(
      label='direction',
      options=[
        'right-down',
        'left-down'],
      key='adjust_direction_select_box_wkey')
    st.selectbox(
      label='theme',
      options=[
        'plain',
        'dark',
        'illuminated',
        'terminal',
        'papyrus',
        'fire',
        'stone',
        'stitch',
        'splotch',
        'shadow'],
      key='adjust_theme_select_box_wkey')
    st.select_slider(
      label='space',
      options=np.arange(0, 2.1, 0.1),
      value=.5,
      format_func=lambda x: '0.5 (default)' if x==.5 else "{:.1f}".format(x),
      key='adjust_space_number_input_wkey')
  with st.expander('kerning', expanded=True):
    left, right = st.columns([1,1])
    left.text_area(
      label='kerning script',
      label_visibility='collapsed',
      placeholder='example:\n0x30<<0x48',
      height=400,
      key='kern_text_area_wkey')
    right.image(
      image='static/img/bkg/shadow.jpg')
  with st.container(border=True):
    st.markdown('###### page', unsafe_allow_html=True)
