import streamlit as st


def write():

    col1, col2 = st.beta_columns(2)

    # Command Line
    col1.code(
        """
        cd <folder name/partial folder name*>
        """
    )

    # Markdown
    col1.code(
        """
        **bold**
        """
    )

    # Python Environment Setup
    col1.write('Create virtual environment')
    col1.code(
        """
        python -m venv .venv
        """
    )
    col1.write('Activate virtual environment')
    col1.code(
        """
        .venv\\Scripts\\activate
        """
    )
    col1.write('Install requirements')
    col1.code(
        """
        python -m pip install -r requirements.txt
        """
    )
    col1.write('Deactivate environment')
    col1.code(
        """
        deactivate
        """
    )



    col1.write('Remove virtual environment')
    col1.code(
        """
        rm -r .venv
        """
    )
