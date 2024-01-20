import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import numpy as np
import colibri
import st_utility as ut
#App config
st.set_page_config(page_title='Colibri', page_icon=':black_nib:', layout="wide")
#Read imagetracer.js
jsColibri, jsImageTracer, css = ut.read(['colibri.js', 'imagetracer.js', 'style.css'])
#Style CSS
st.markdown('<style>{}</style>'.format(css), unsafe_allow_html=True)
ut.num_spectrum_colors = 7
ut.show_spectrum()
ut.set_colors([[2,3,8,8,8],[2,-1]])
ut.show_colors()
#Read .clb file
book = colibri.ColibriBook()
book.init('static/clb/', 'teonaht')
book.run()
#Navigation tabs
with st.container():
  arrTab = ['font', 'phone', 'graph', 'adjust', 'profile']
  fontTab, graphTab, phoneTab, adjustTab, accountTab = st.tabs(arrTab)
##########################################
# Main UI
##########################################
#function font_text_area_callback():
with fontTab:
  font_text_area = st.text_input(
    "glyph code",
    label_visibility='collapsed',
    #height=400,
    #on_change=font_text_area_callback,
    value='\n'.join(book.font['arrGlyphCode']))
  #HTML component
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
