# Database server


Server for database management

## What is this server doing?


* It allows users to use the database.
* There is a division into users and admins.

## Development


### System dependencies
* Python 3.X (from version 3.10)

### Modules
* Socket
* sqlite3

## How to start a bot?


1. Change the ip in the CONFIG.py.
2. Run the server.py file first and then the client.py file. For the test, you can use pre-prepared accounts: user and admin (the password is the same as the login).


## Other


The admin user has full access to creating and editing tables, and the user can only view existing data (there is one "users" table: id, login, password)
