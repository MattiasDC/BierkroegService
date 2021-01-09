import urllib.parse

def create_mysql_odbc_connection_string(driver, server, port, db, username, password):
    return (f'Driver={{{driver}}};'+
        f'Server=tcp:{server},{port};' +
        f'Database={db};' +
        f'Uid={username};' +
        f'Pwd={{{password}}};'+
        'Encrypt=yes;' +
        'TrustServerCertificate=no;' +
        'Connection Timeout=30;')

def create_mysql_odbc_connection_string_url(driver, server, port, db, username, password):
    unquoted = create_mysql_odbc_connection_string(driver, server, port, db, username, password)
    params = urllib.parse.quote_plus(unquoted)
    return 'mssql+pyodbc:///?odbc_connect=' + params