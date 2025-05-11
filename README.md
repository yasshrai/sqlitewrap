# User Authentication System 

This is a simple user authentication system implemented in Python using traditional file system specifically csv which stand for Comma sperated values for storing user details and databases. The system allows users to create a new username and password, verify their details, create a new database, change password, and perform other operations.

## Features

- **User authentication:** Users can create a new username and password, and verify their details before performing any operation.
- **Database creation:** Users can create a new database by providing a database name.
- **Password hashing:** User passwords are hashed using hashlib library for security.
- **Error handling:** Custom exceptions are defined for various error scenarios like incorrect password, user not found, database not selected, etc.
- **CSV file handling:** CSV files are used to store user details and database names.

## Usage

1. Import the required libraries: `csv`, `hashlib`, and `os`.
2. Create an instance of the `connect` class by providing username, password, and database name (optional).
3. Use the methods provided by the `connect` class to perform various operations like creating a new username and password, verifying details, creating a new database, changing password, etc.
4. Handle the custom exceptions as needed for error scenarios.

## Example Usage

```python
# Import required libraries
import datacsv 

# Create an instance of connect class
user = datacsv.connect("myuser", "mypassword")

# Create a new username and password
user.CreateUsernamePassword("newuser", "newpassword")

# Verify username and password
user.VerfiyDetails("newuser", "newpassword")

# Create a new database
user.CreateDatabase("mydatabase")

# Change password
user.ChangePassword("newuser", "newpassword", "newpassword2")

# Get current user
current_user = user.CurrentUser()
print(current_user) # Output: User: newuser



Custom Exceptions

UserNotFound: Raised when a user is not found in the user details CSV file.
IncorrectPassword: Raised when an incorrect password is provided.
NouseridPassword: Raised when no username or password is provided.
DatabaseNameNotProvided: Raised when no database name is provided for creating a new database.
UseralreadyExist: Raised when a user already exists in the user details CSV file.
DatabasealreadyExist: Raised when a database with the same name already exists.
NotVerfiedUsernamePassword: Raised when username and password are not verified.
NotValidUsernameAndPassword: Raised when an invalid username or password is provided.
DatabaseNotSelected: Raised when a database is not selected before performing an operation.
SomethingWentWrong: Raised when an unexpected error occurs.

Note: Replace "yourusername" in the License section with your actual username or organization name if you use a different one.
