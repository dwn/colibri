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
# INIT APP
##########################################
#App config
st.set_page_config(page_title='Colibri', page_icon=':book:', layout="wide")
st.markdown(f'<style>{ut.read("style.css")}</style>', unsafe_allow_html=True)
##########################################
# LOGIN
##########################################
#db.auth.sign_up(dict(email='danwnielsen@gmail.com', password='password', options=dict(data=dict(fname='dan',attribution='developing'))))
db.auth.sign_in_with_password(dict(email='danwnielsen@gmail.com', password='password'))
#st_supabase.auth.sign_out()
##########################################
# INIT STATE
##########################################
#Book state variable
if 'book' not in state:
  state.book = colibri.Book()
  state.book.init('static/clb/ignota.clb')
  state.book.update()
  state.book.run()
#Other state variables
def init_app_state(bool_overwrite=False):
  ut.init_state({
    'user': db.auth.get_user().user,
    'session': db.auth.get_session(),
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
ut.num_spectrum_colors = 12
#ut.set_colors({ 'gold': [2,3,8,8,8], 'brown': [2,-1] })
ut.set_colors({
  'red': [1],
  'orange': [3],
  'amber': [4],
  'green': [6],
  'sky': [8],
  'blue': [9],
  'purple': [11],
})
ut.show_colors()
#Save button and hotkey
with st.expander(':green[saved]' if state.bool_saved else ':orange[unsaved (alt+enter)]', expanded=True):
  def save():
    db.table('colibri_source').insert(
      [{'colibri_source': state.book.source}]
    ).execute()
    state.bool_saved = True
  state.user
  col0, col1 = st.columns([1,1])
  col0.write(state.book.source['title'])
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
    st.button('create new project')
    st.file_uploader('upload project', type=['clb'])
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
      options=['create', 'use'],
      key='account_mode_toggle_wkey')
