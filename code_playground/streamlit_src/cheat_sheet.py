import streamlit as st


def write():

    col1, col2 = st.beta_columns(2)

    col1.subheader("Streamlit")
    col1.markdown(
        "[Streamlit Cheat Sheet](https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py)"
    )

    col1.subheader("Command Line")
    col1.markdown(
        """
        > **Move to directory** `cd <folder name/partial folder name*>`  
        """
    )

    col1.subheader("Python Environment Setup")
    col1.markdown(
        """
        > **Create virtual environment** `python -m venv .venv`  
        > **Activate virtual environment** `.venv\\Scripts\\activate`  
        > **Install requirements** `python -m pip install -r requirements.txt`  
        > **Deactivate environment** `deactivate`  
        > **Remove virtual environment** `rm -r .venv`  
    """
    )
