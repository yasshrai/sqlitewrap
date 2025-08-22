# sqlitewrap

`sqlitewrap` is a Python library for user authentication and database management using SQLite. It provides a class-based API to securely manage users, create databases and tables, and perform CRUD operations, all with error handling and password hashing.

## Features

- User registration and authentication (with SHA-256 password hashing)
- Create, select, and remove databases
- Create, update, and remove tables
- Insert and fetch table data
- Change user passwords
- Connect and compare tables
- Custom error classes for robust exception handling

## Installation

Clone the repository and install dependencies (if any):

```bash
git clone https://github.com/yasshrai/sqlitewrap.git

```

## Usage

Import the `connect` class from `sqlitewrap.py` and use its methods for user and database management:

```python
from sqlitewrap import connect

# Register a new user
c = connect()
c.CreateUsernamePassword('username', 'password')

# Authenticate user
c = connect('username', 'password')

# Create a new database
c.CreateDatabase('mydb')

# Select a database
c.UseDatabase('mydb')

# Create a table
c.CreateTable('mytable')

# Insert data into table
c.InsertIntoTable('mytable', ['value1', 'value2'])

# Fetch data from table
for row in c.FetchTable('mytable'):
	print(row)

# Change password
c.ChangePassword('username', 'oldpassword', 'newpassword')
```

All operations raise custom exceptions for error handling (see `sqlitewrap.py`).

## Project Structure

- `sqlitewrap.py`: Main library with the `connect` class and helper functions
- `pyproject.toml`: Project metadata
- `README.md`: Project documentation


## Contributing

Pull requests and issues are welcome!
