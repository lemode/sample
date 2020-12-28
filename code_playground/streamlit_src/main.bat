:: get current directory
CD "%~dp0" 

:: run app
streamlit run main.py --server.port 8080 --browser.serverPort 8080 
