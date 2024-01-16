import streamlit as st
import pandas as pd
import numpy as np
import colibri
from streamlit.components.v1 import html
#App config
st.set_page_config(page_title='Colibri', page_icon=':black_nib:', layout="wide")
#Remove padding around app
st.markdown("""
<style>
  .main > div {
    padding:.3rem;
  }
  button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
    font-size:1rem;
  }
  button[data-baseweb="tab"] {
    margin:0;
    width:100%;
  }
  
</style>""", unsafe_allow_html=True)
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
  #Read imagetracer.js
  f = open('imagetracer.js', 'r')
  jsImageTracer = f.read()
  f.close()
  #Read imagetracer.js
  f = open('colibri.js', 'r')
  jsColibri = f.read()
  f.close()
  #HTML component
  html("""
    <style>
      body {{ margin:0 }}
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
