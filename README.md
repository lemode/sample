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

### Run and Test Points
To run data and application using `main.py` and the following command.
Data will print for simplicity of review
```
python points\main.py
```

Tests can be run from the command line using the following commands
```
python -m unittest points\tests/test_order.py
```
---- 

