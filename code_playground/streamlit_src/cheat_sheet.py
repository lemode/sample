import streamlit as st


def write():

    col1, col2 = st.beta_columns(2)

    col1.subheader("Streamlit")
    col1.markdown(
        "> [Streamlit Cheat Sheet](https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py)"
    )

    col1.subheader("VS Code")
    col1.markdown(
        """
        > **Open/close side bar** `Ctrl+ b`
        > **Go to specific line** `Ctrl + g`
        > **Duplicate line** `Ctrl + Shift + d`
        > **Create ipython cell** `# %%`
        > **Clear terminal** `Ctrl + l`
        """
    )
    col1.markdown(
        "> [VS Code](https://medium.com/better-programming/20-vs-code-shortcuts-for-fast-coding-cheatsheet-10b0e72fd5d)"
    )

    col1.subheader("ipython")
    col1.markdown(
        """
        > **Clear variable with no user confirmation** `%reset -f>`  
        """
    )
    col1.markdown(
        "> [ipython](https://www.delftstack.com/howto/python/how-to-clear-variables-in-ipython/)"
    )

    col1.subheader("Command Line")
    col1.markdown(
        """
        > **Move down directory** `cd <folder name/partial folder name*>`  
        > **Move up directory** `cd ..`  
        > **View files and folders in directory** `ls`  
        > **Get current directory** `cd "%~dp0"`  
        """
    )

    col2.subheader("Python Environment Setup")
    col2.markdown(
        """
        > **Create virtual environment** `python -m venv .venv`  
        > **Activate virtual environment** `.venv\\Scripts\\activate`  
        > **Install requirements** `python -m pip install -r requirements.txt`  
        > **Deactivate environment** `deactivate`  
        > **Remove virtual environment** `rm -r .venv`  
    """
    )

    col2.subheader("Docker")
    col2.markdown(
        """
        > **Create folder directory** `<folder directorybuild\html>`  
        > **Build an image from a Dockerfile** `docker build . -t <name:tag>`  
    """
    )
