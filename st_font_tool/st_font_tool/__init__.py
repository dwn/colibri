import os
import shutil
import streamlit.components.v1 as components
#Defaults to production mode
ST_DEV_MODE = os.environ.get('ST_DEV_MODE', '0')
if ST_DEV_MODE == '1':
  _component_func = components.declare_component('font_tool', url='http://localhost:3001')
else:
  parent_dir = os.path.dirname(os.path.abspath(__file__))
  build_dir = os.path.join(parent_dir, 'frontend/build')
  _component_func = components.declare_component('font_tool', path=build_dir)
#Create a wrapper function for the component - an optional best practice allowing us
#to customize our component's API, pre-processing its input args, post-processing its
#output value, and adding a docstring for users
def font_tool(font_glyph_code, key=None):
  '''Create a new instance of 'font tool'
  Parameters
  ----------
  font_glyph_code: str
      a string of characters representing a glyph-drawing code
  key: str or None
      Best to set this to the character, escaped with a prefixed '\\' where needed
  Returns
  -------
  font_glyph_code_out: str
      the edited font glyph code
  '''
  #The 'default' is the initial return value before the user has interacted with it
  component_value = _component_func(font_glyph_code=font_glyph_code, key=key, default='')
  #We could modify the value returned from the component if we wanted
  return component_value
