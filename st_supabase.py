import streamlit as st
from st_supabase_connection import SupabaseConnection
##########################################
# SUPABASE DATA TABLE AND AUTH FUNCTIONS
##########################################
db = st.connection(
  name="colibri_connection",
  type=SupabaseConnection,
  ttl=None,
  url='https://tjkknwkdcgqcjozcdvwf.supabase.co',
  key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRqa2tud2tkY2dxY2pvemNkdndmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc1MTYxMDEsImV4cCI6MjAyMzA5MjEwMX0.RtE5f--zm2zw4Z2GVWSDW7Z8fkGjDeRWHvHM3PiXvWc',
)
