import streamlit as st
from st_supabase_connection import SupabaseConnection
##########################################
# SUPABASE DATA TABLE AND AUTH FUNCTIONS
##########################################
db = st.connection(
  name="colibri_connection",
  type=SupabaseConnection,
  ttl=None,
  url=st.secrets['SUPABASE_URL'],
  key=st.secrets['SUPABASE_KEY'],
)
