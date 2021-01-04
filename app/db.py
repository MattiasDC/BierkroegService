import urllib

def create_mysql_odbc_connection(driver, server, database, username, password):
	params = urllib.parse.quote_plus(
    	'Driver={%s};' % driver +
    	'Server=tcp:%s,1433;' % server +
    	'Database=%s;' % database +
    	'Uid=%s;' % username +
    	'Pwd={%s};' % password +
    	'Encrypt=yes;' +
    	'TrustServerCertificate=no;' +
    	'Connection Timeout=30;')

	return 'mssql+pyodbc:///?odbc_connect=' + params