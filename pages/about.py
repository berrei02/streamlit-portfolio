import streamlit as st

st.set_page_config(page_title="About Stefan")

about_md = open('pages/texts/about.md', 'r').read()
st.write(about_md)