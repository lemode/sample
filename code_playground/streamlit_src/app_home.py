"""Home page shown when the user enters the application"""
import streamlit as st

import code_playground.streamlit_src.webpage as webpage


def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Home ..."):
        webpage.webpage_title("")
        st.write(
            """
             #### The Magic of the Quick Commands
            ---
            This application's **purpose** is to provide:
            - a **Cheat Sheet** of quick commands that have been amazed from different places.
            - Easily recall common commands for coding, shipping and owning a pipeline
            
            """
        )
