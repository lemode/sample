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
        "> [ipython](https://ipython.readthedocs.io/en/stable/interactive/magics.html)"
    )

    col1.subheader("Command Line")
    col1.markdown(
        """
        > **Move down directory** `cd <folder name/partial folder name*>`  
        > **Move up directory** `cd ..`  
        > **View files and folders in directory** `ls`  
        > **Get current directory** `cd "%~dp0"` 
        > **Get list of active ports** `netstat -ano"`
        > **Get list of active tasks** `tasklist`
        > **Kill by forcefully terminating process using pid** `taskkill /PID <pid> /F`  
        > **Keep bat file open after script runs** `pause`
        """
    )

    col2.subheader("Powershell")
    col2.markdown(
        """
        > **Keep powershell file open after script runs** `Start-Sleep -Seconds 30`  
        """
    )

    col2.subheader("Posgres PSQL Powershell")
    col2.markdown(
        """
        > **Run psql command line script** `psql -h hostname -d database_name -U user_name -p 5432 -a -q -f filepath`  
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
        > **Build an image from a Dockerfile in a Git Hub repo** `docker build . -t <name:tag>`  
        > **Run docker file to set up container** `docker run - p <local machine port>:<container port> <name:tag>`  
        > **List containers using docker imaage** `docker container ls <name:tag>`  
        > **List all running docker containers** `docker ps -a>`  
        > **Copy files and directory from docker container to local machine root file/directory called __.__ (run from local machine)** `docker cp <container id>:/<container file/directory> .`
    """
    )
