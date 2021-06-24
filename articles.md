#### Python & Pandas
Pandas pivot table with subtotals: https://stackoverflow.com/questions/53266032/adding-a-grand-total-to-a-pandas-pivot-table <br>
Slow running queries: https://tophat.atlassian.net/wiki/spaces/TOP/pages/1719697419/How+to+Debug+Slow+SQL+Queries <br>
Cron Job Timing: https://crontab.guru/#*/45_*_*_*_* <br>
Add Value from Previous Row: https://stackoverflow.com/questions/19076539/python-pandas-dataframe-add-previous-row-values <br>
Adaptor Pattern: https://bocoup.com/blog/adapter-pattern-a-must-for-vendor-service-integrations <br>
Mocking api calls: https://auth0.com/blog/mocking-api-calls-in-python/ <br>
Mocking api calls with class attributes + full cheat sheet: https://medium.com/@yeraydiazdiaz/what-the-mock-cheatsheet-mocking-in-python-6a71db997832 <br>

#### Timestamp Conversion
[Convert numeric timestamp using Epoch Converter](https://www.epochconverter.com/)

#### SQL
SQL Analytics Windows Functions: https://docs.oracle.com/cd/B19306_01/server.102/b14200/functions001.htm <br>

#### Markdown
Syntax: https://support.discord.com/hc/en-us/articles/210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline-  

#### Postgres Setup
Download Postgres: https://www.postgresql.org/download/ <br>
Change postgres password: https://www.postgresqltutorial.com/postgresql-reset-password/ <br>
Create user no password: https://www.postgresql.org/docs/8.0/sql-createuser.html <br>
```CREATE <user>; GRANT ALL PRIVILEGES ON DATABASE lemode to <user>;``` <br>
Create psql for windows (add to environment variables): https://stackoverflow.com/questions/30401460/postgres-psql-not-recognized-as-an-internal-or-external-command

#### Google App Scripts
https://www.labnol.org/internet/google-apps-script-developers/32305/ <br>

#### Chrome Cast
https://www.youtube.com/watch?v=ZiydI0358s4 <br>

#### Mortgage Calculator
https://www.indeed.com/career-advice/career-development/interest-compounded-semiannually <br>
https://taiheicorp.com/data-science/calculate-loan-payments-using-while-loops-in-python <br>

#### Coverage and Black Library Usage<br>
<br>
coverage - https://pypi.org/project/coverage/<br>
Run all tests in a project:<br>
coverage run --source /Users/tross/repos/codex-local/codex -m unittest discover<br>
Run all tests in a specific test suite file<br>
coverage run --source /Users/tross/repos/codex-local/codex -m unittest codex.module.submodule.tests.test_file OR coverage run  -m unittest discover<br> common/thm_billings/tests/
Run a specific test case<br>
coverage run --source /Users/tross/repos/codex-local/codex -m unittest codex.module.submodule.tests.test_file.TestClass.test_case_method<br>
The --source is so it doesn't look for tests on all the modules in the project, like pandas, without this out coverage would look like 2%, but you'll need to change that location
<br>
<br>
Formatters: <br>
black https://pypi.org/project/black/<br>
isort https://pypi.org/project/isort/<br>
You can setup vscode to run these on save (my settings file below), but you can also just call them from a command line:<br>
black codex/data_objects/travel_advisory_score.py<br>
isort codex/data_objects/travel_advisory_score.py<br>
In general I run black before isort<br>

<br><br>
Linter:<br>
There are lots, you can choose whichever one you like, I use pylint and it's not annoying which is the worst thing about linters<br>
https://pypi.org/project/pylint/<br>
<br>
<br>
Interactive shell<br>
ipython https://pypi.org/project/ipython/<br>
You might already have it via Jupyter, but it's good to know how to use it from a terminal, look up the magic methods for ipython when you have time, there's stuff like save all lines to a python script<br>
pdb docs https://docs.python.org/3.6/library/pdb.html<br>
<br>
My project vscode settings<br>
``` 
{
    "python.pythonPath": "/Users/tross/repos/codex-local/bin/python",
    "python.formatting.provider": "black",
    "python.linting.pylintEnabled": true,
    "python.linting.enabled": true,
    "python.linting.mypyEnabled": false,
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
The bit about
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
is smart enough to use isort if it's installed
If you have issues with black and isort trying to format the same thing, create a file called .isort.cfg in the project root directory and add the following to it:
[settings]
multi_line_output = 3
include_trailing_comma = True
force_grid_wrap = 0
use_parentheses = True
ensure_newline_before_comments = True
line_length = 88
```
That should stop them from fighting with each other
