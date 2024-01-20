import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import numpy as np
import colibri
import st_utility as ut
#App config
st.set_page_config(page_title='Colibri', page_icon=':book:', layout="wide")
#Read imagetracer.js
jsColibri, jsImageTracer, css = ut.read(['colibri.js', 'imagetracer.js', 'style.css'])
#Style CSS
st.markdown('<style>{}</style>'.format(css), unsafe_allow_html=True)
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
# Main UI
##########################################
#function font_text_area_callback():
with fontTab:
  #Glyph drawing component
  html("""
    <style>
      body {{ margin:0; background-color:#444; }}
      #scratch-img, #scratch-canvas {{ display:none }}
      #font-canvas {{
        background-color:lemonchiffon;
        transform:scaleY(-1);
        width:100%;
        height:100%;
        object-fit:contain;
        object-position:center;
      }}
    </style>
    <canvas id='scratch-canvas' width='500' height='500'></canvas>
    <canvas id='font-canvas' width='500' height='500'></canvas>
    <img id="scratch-img" alt="scratch">
    <script>
      {jsImageTracer}
      {jsColibri}
      var canvas = document.getElementById('font-canvas');
      var ctx = canvas.getContext('2d');
      (async () => {{
        const svgStrGrid = "data:image/svg+xml;base64," + btoa(ColibriConst.svgStrGrid);
        document.getElementById('font-canvas').style.backgroundImage = "url(" + svgStrGrid + ")";
        const res = await ColibriDraw.drawImageAndGetSVG_isValid(ctx, "a/h");
      }})();
    </script>
  """.format(jsImageTracer=jsImageTracer, jsColibri=jsColibri),
  width=500,
  height=500)
  #font_text_input = st.text_input(
  #  "glyph code",
  #  label_visibility='collapsed',
  #  #height=400,
  #  #on_change=font_text_area_callback,
  #  value=book.font['arrGlyphCode'][0])
  #def get_glyph_callback():
  #  font_text_input.value = 'hi'
  placeholder = st.empty()
  input = placeholder.text_input('glyph code', value='click a character')
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
        input = placeholder.text_input('glyph code', value=book.font['arrGlyphCode'][i])
