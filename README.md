# Bierkroeg Service
Een bierkroeg service waarbij bestellingen gemaakt en gevolgd kunnen worden.

### Quick Start

1) In terminal: git clone https://github.com/MattiasDC/BierkroegService.git
2) Run initDb.py script to setup a database
3) Fill in db environment variables and docker secrets (by providing an alternative docker-compose)\
Environment variables to set:
    - db_driver(e.g. 'ODBC Driver 17 for SQL Server')
    - db_server
    - db_port
    - db_database
    - db_username
4) In terminal: python dc.py --build --user mdc (user is used for docker-compose)
6) Open web browser at localhost:5004
