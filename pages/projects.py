import streamlit as st

st.set_page_config(page_title="Projects")

projects_md = open('pages/texts/projects.md', 'r').read()
st.write(projects_md)