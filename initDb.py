import click
import pyodbc
from utils.dbutils import create_mysql_odbc_connection_string


@click.command()
@click.option('--server', prompt='SQL Server URL', default='hobbies-mdc.database.windows.net')
@click.option('--masterlogin', prompt='Master login', default='hobbies-mdc')
@click.option('--masterloginpassword', hide_input=True, prompt='Master login password')
@click.option('--db', prompt='Database name')
@click.option('--newlogin', prompt='Login, User and Schema to create')
@click.option('--newloginpassword', hide_input=True, prompt='Login password')
def initDb(server, masterlogin, masterloginpassword, db, newlogin, newloginpassword):
	driver = 'ODBC Driver 17 for SQL Server'
	port = 1433
	masterDb = 'master'

    # First we create the database and login in the master database if it does not yet exist
	print("Connecting to master database...", flush=True)
	conn = pyodbc.connect(create_mysql_odbc_connection_string(driver, server, port, masterDb, masterlogin, masterloginpassword), autocommit=True)
	cursor = conn.cursor()
	print("Creating database...", flush=True)
	cursor.execute(f"IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = '{db}') EXEC('CREATE DATABASE [{db}]');")
	print("Creating login...", flush=True)
	cursor.execute(f"IF NOT EXISTS(SELECT * FROM sys.sql_logins WHERE name='{newlogin}') EXEC('CREATE LOGIN [{newlogin}] WITH PASSWORD = ''{newloginpassword}''');")
	cursor.close()
	conn.close()

	# Create user and schema for both development and production in new database
	conn = pyodbc.connect(create_mysql_odbc_connection_string(driver, server, port, db, masterlogin, masterloginpassword), autocommit=True)
	cursor = conn.cursor()
	print("Creating user...", flush=True)
	cursor.execute(f"IF NOT EXISTS(SELECT * FROM sys.sysusers WHERE name='{newlogin}') EXEC('CREATE USER [{newlogin}] FROM LOGIN [{newlogin}]');")
	cursor.execute(f"EXEC sp_addrolemember 'db_datareader', '{newlogin}';")
	cursor.execute(f"EXEC sp_addrolemember 'db_datawriter', '{newlogin}';")
	cursor.execute(f"EXEC sp_addrolemember 'db_ddladmin', '{newlogin}'")
	print("Creating schemas...", flush=True)
	cursor.execute(f"IF NOT EXISTS(SELECT * FROM sys.schemas WHERE name='{newlogin}') EXEC('CREATE SCHEMA [{newlogin}] AUTHORIZATION [{newlogin}]');")
	cursor.execute(f"IF NOT EXISTS(SELECT * FROM sys.schemas WHERE name='{newlogin}-dev') EXEC('CREATE SCHEMA [{newlogin}-dev] AUTHORIZATION [{newlogin}]');")

if __name__ == '__main__':
    initDb()