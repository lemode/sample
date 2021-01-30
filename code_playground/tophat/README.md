## Setup
This app was built with python 3.7.4 
Install requirements with
Open zip file and in root folder run the following commands
```
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Credentials
update `constants.py` file with credentials 

```
class TopHatAnalyticsConfig:
    DB_USER = "XXXXX"
    DB_PASSWORD = "XXXXX"
    DB_HOST = "XXXXX"
    DB_PORT = "XXXXX"
    DB_DATABASE = "XXXXX"
    DB_SCHEMA = "XXXXX"
```

## Run Code
To run and load application perform the following:  
navigate to root folder and run `python tophat.py`
