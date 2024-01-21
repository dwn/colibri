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
    ├── setup.py                <- name="X"
    └── streamlit_custom_slider <- folder name
        ├── __init__.py         <- make changes
        └── frontend            <- run `npm install` here
            ├── package.json    <- "name": "X"
            ├── public/
            ├── src/            <- filename X.tsx
            ├── .env
            ├── .prettierc
            ├── package-lock.json
            ├── node_modules
            └── tsconfig.json
