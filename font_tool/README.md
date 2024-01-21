## Installation instructions
```sh
pip install streamlit-custom-component
```

## Usage instructions
```python
import streamlit as st

from my_component import my_component

value = my_component()

st.write(value)
```

# Changes (example name)
    ├── LICENSE
    ├── MANIFEST.in
    ├── setup.py                <- name="streamlit-custom-slider"
    └── streamlit_custom_slider <- folder name
        ├── __init__.py         <- make changes
        └── frontend            <- run `npm install` here
            ├── package.json    <- "name": "streamlit_custom_slider"
            ├── public/
            ├── src/
            ├── .env
            ├── .prettierc
            ├── package-lock.json
            ├── node_modules
            └── tsconfig.json
