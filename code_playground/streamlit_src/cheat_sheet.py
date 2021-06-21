import streamlit as st


def write():

    col1, col2 = st.beta_columns(2)

    col1.subheader("Streamlit")
    col1.markdown(
        "##### [Streamlit Cheat Sheet commands](https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py)"
    )

    col1.subheader("Visual Studio Code")
    col1.markdown(
        "##### More commands [here](https://medium.com/better-programming/20-vs-code-shortcuts-for-fast-coding-cheatsheet-10b0e72fd5d)"
    )
    col1.code(
        """
> Open/close side bar `Ctrl+ b`
> Go to specific line `Ctrl + g`
> Duplicate line `Ctrl + Shift + d`
> Create ipython cell `# %%`
> Clear terminal `Ctrl + l`
"""
    )

    col1.subheader("Command Line")
    col1.code(
        """
> Move down directory `cd <folder name/partial folder name*>`
> Move up directory `cd ..`
> View files and folders in directory `ls`
> Get current directory `cd "%~dp0"`
> Get list of active ports `netstat -ano"`
> Get list of active tasks `tasklist`
> Kill by forcefully terminating process using pid `taskkill /PID <pid> /F`
> Keep bat file open after script runs `pause`
> Copy recursively one folder to another location `cp -r ./etl .fin/etl`
"""
    )

    col1.subheader("Powershell")
    col1.code(
        """
> Keep powershell file open after script runs `Start-Sleep -Seconds 30`
> Run psql command line script on server where postgres is installed `psql -h hostname -d database_name -U user_name -p 5432 -a -q -f filepath`
"""
    )

    col1.subheader("SSH")
    col1.markdown(
        """
    ##### [Generate SSH directory and config file for the first time](https://superuser.com/questions/1256286/missing-ssh-folder-in-macos-high-sierra/1256291)`ssh-keygen`
    ##### [Copy contents of public ssh key](https://stackoverflow.com/questions/3828164/how-do-i-access-my-ssh-public-key)`pbcopy < ~/.ssh/id_rsa.pub`
    """
    )
    
    col2.subheader("Python")
    col2.markdown(
        "##### [Python Cheat Sheet commands](https://github.com/gto76/python-cheatsheet)"
    )

    col2.subheader("Python Environment Setup")
    col2.markdown(
        "##### [Rebuild virtual environment on Mac](https://help.pythonanywhere.com/pages/RebuildingVirtualenvs/)"
    )
    col2.code(
        """
> Create virtual environment on Windows `python -m venv .venv`
> Update python version in virtual environment on Mac `virtualenv -p <location of python intepreter ie. /home/username/opt/python-3.6.2/bin/python3> .venv`
> Activate virtual environment on Mac  `source .venv/bin/activate`
> Activate virtual environment on Windows  `.venv\\Scripts\\activate`
> Install requirements `python -m pip install -r requirements.txt`
> Deactivate environment `deactivate`
> Find out which python is being used on Mac `which python` OR `which python3`
> Update the link from Mac default to python installed from python website `ls -al /usr/local/bin/python3`
"""
    )
    col2.markdown(
        """
    ##### [Force remove virtual environment](https://www.macworld.com/article/222596/master-the-command-line-deleting-files-and-folders.html#:~:text=the%20way%20down.-,When%20you%20run%20the%20rm%20%2DR%20command%20on%20a%20folder,folders%2C%20all%20the%20way%20down.&text=This%20will%20ask%20you%20to%20confirm%20the%20deletion%20of%20each%20item.)`rm -rf .venv`
    ##### [Clear pip cache](https://stackoverflow.com/questions/9510474/removing-pips-cache)`pip cache purge`
    ##### [Check sudo password on Mac (should be local machine password)](https://superuser.com/questions/553932/how-to-check-if-i-have-sudo-access)`sudo -v`
    ##### [Reset python location](https://stackoverflow.com/questions/6819661/python-location-on-mac-osx)
   """
    )

    col2.write("")
    col2.subheader("Docker")
    col2.markdown(
        "##### [Rebuild docker compase container](https://stackoverflow.com/questions/36884991/how-to-rebuild-docker-container-in-docker-compose-yml)"
    )
    col2.code(
        """
> Create folder directory `<folder directorybuild\html>`
> Build an image from a Dockerfile in a Git Hub repo `docker build . -t <name:tag>`
> Run docker file to set up container `docker run - p <local machine port>:<container port> <name:tag>`
> List containers using docker imaage `docker container ls <name:tag>`
> List all running docker containers `docker ps -a>`
> Copy files and directory from docker container to local machine root file/directory called __.__ (run from local machine) `docker cp <container id>:/<container file/directory> .`
"""
    )

    col2.subheader("ipython")
    col2.markdown(
        """
    ##### More commands [here](https://ipython.readthedocs.io/en/stable/interactive/magics.html)
    """
    )
    col2.code(
        """
> Clear variable with no user confirmation `%reset -f`
"""
    )
    

    col2.subheader("Typescript")
    col2.code(
        """
> Run typescript test using jest `npx jest`
> Convert typescript files to javascript 'gulp` or `tsc -w`
"""
    )    
    
