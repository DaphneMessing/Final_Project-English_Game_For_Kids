import streamlit as st

# Use Streamlit's set_page_config to hide the sidebar
st.set_page_config(
    page_title="Learning English Game",
    layout="wide",  # This removes the sidebar and uses the full page width
)

st.title('Welcome to the English Learning Game')

st.write("Select a level from the sidebar to start.")
