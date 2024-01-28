from pathlib import Path
import setuptools
this_directory = Path(__file__).parent
setuptools.setup(
  name='streamlit-custom-component',
  version='0.0.1',
  author='panteli',
  author_email='danwnielsen@gmail.com',
  description='A font glyph maker for streamlit',
  long_description='''
# Streamlit Custom Component for the creating of font glyphs

This uses a special string of characters that describe strokes of
glyphs. These are associated with characters in the 0x00-0xff ascii range.
''',
  long_description_content_type='text/markdown',
  url='',
  packages=setuptools.find_packages(),
  include_package_data=True,
  classifiers=[],
  python_requires='>=3.7',
  install_requires=[
    'streamlit >= 0.63',
    #List any other component python deps here
  ],
  extras_require={
    'devel': [
      'wheel',
      'pytest==7.4.0',
      'playwright==1.39.0',
      'requests==2.31.0',
      'pytest-playwright-snapshot==1.0',
      'pytest-rerunfailures==12.0',
    ]
  }
)
