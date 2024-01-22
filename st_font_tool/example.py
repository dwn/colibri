import streamlit as st
from st_font_tool import font_tool

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/example.py`

num_clicks = font_tool('ag')
st.markdown("You've clicked %s times!" % int(num_clicks))
