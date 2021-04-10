## Setup
This app was built with python 3.7.4
Install requirements with
```
git clone https://github.com/lemode/code_playground
```

Open cloned sample and run the following commands
```
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Credentials
Create file called `secrets.py` placed in root folder with classes of credentials and its environment

```
class DatabaseEnvironmentConfig:
    DB_DATABASE = "XXXXX"
    DB_USER = "XXXXX"
    DB_PASSWORD = "XXXXX"
    DB_HOST = "XXXXX"
    DB_PORT = "XXXXX"
```

## Run App

To run and load application perform the following:
**Run** `app.bat` or in root folder. To run on Windows use `streamlit run app.py` and to run on Mac `streamlit run ./app.py`

### Run and test folder applications
To run data and application use the below command. Data will print for simplicity of review. Tests can be run from the command line


**Points Application**
Enabled using `python code_playground\points\main.py`

**Points Tests**
Enabled using `python -m unittest code_playground\points\tests\test_order.py`

**Streamlit Application**
Enabled using `streamlit run code_playground\streamlit_src\app.py`


