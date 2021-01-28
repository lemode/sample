Pandas Pivot Table with Subtotals
https://stackoverflow.com/questions/53266032/adding-a-grand-total-to-a-pandas-pivot-table

SQL Analytics Windows Functions
https://docs.oracle.com/cd/B19306_01/server.102/b14200/functions001.htm

Markdown
https://support.discord.com/hc/en-us/articles/210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline-

Writing Postgres Functions and Stored Procedures
http://sqlines.com/postgresql/how-to/return_result_set_from_stored_procedure
http://sqlines.com/postgresql/stored_procedures_functions
Add Defaults to Functions: https://stackoverflow.com/questions/39896329/how-to-write-function-for-optional-parameters-in-postgresql


Download and Setup Postgres
Download Postgres: https://www.postgresql.org/download/
Change postgres password: https://www.postgresqltutorial.com/postgresql-reset-password/
Create user no password: https://www.postgresql.org/docs/8.0/sql-createuser.html 
```CREATE <user>; GRANT ALL PRIVILEGES ON DATABASE lemode to <user>;```
Create psql for windows (add to environment variables): https://stackoverflow.com/questions/30401460/postgres-psql-not-recognized-as-an-internal-or-external-command 
Run sql script using postgres: ```psql -h hostname -d database_name -U user_name -p 5432 -a -q -f filepath```