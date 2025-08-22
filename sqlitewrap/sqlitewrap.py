import sqlite3
import hashlib
import os



# current path

current_path = os.getcwd()
db_path = os.path.join(current_path, "userdetail.db")

# errors


class UserNotFound(Exception):
    def __init__(self, message='user not found'):
        super().__init__(message)


class IncorrectPassword(Exception):
    def __init__(self, message='incorrect password'):
        super().__init__(message)


class NouseridPassword(Exception):
    def __init__(self, message='No userid password provided'):
        super().__init__(message)


class DatabaseNameNotProvided(Exception):
    def __init__(self, message='Database not provided'):
        super().__init__(message)


class UseralreadyExist(Exception):
    def __init__(self, message='user already exist'):
        super().__init__(message)


class DatabasealreadyExist(Exception):
    def __init__(self, message='database already exist'):
        super().__init__(message)


class NotVerfiedUsernamePassword(Exception):
    def __init__(self, message='not verfied username password'):
        super().__init__(message)


class NotValidUsernameAndPassword(Exception):
    def __init__(self, message='not valid username and password'):
        super().__init__(message)


class DatabaseNotSelected(Exception):
    def __init__(self, message=' database not selected'):
        super().__init__(message)


class SomethingWentWrong(Exception):
    def __init__(self, message='something went wrong'):
        super().__init__(message)

# ----------------connect class----------------
class connect:
    """A class to manage user authentication and database operations using SQLite. """    

    def __init__(self, username=None, password=None, databasename=None):
        self.username = username
        self.password = password
        self.databasename = databasename
        global check
        global databasechecker
        check = False
        databasechecker = False
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._init_db()
        if username is not None and password is not None:
            tempobj = connect()
            tempobj.VerfiyDetails(username, password)

    def _init_db(self):
        # Create users table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )''')
        # Create databases table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS databases (
            name TEXT PRIMARY KEY
        )''')
        self.conn.commit()

    def CreateUsernamePassword(self, newuserid=None, newpassword=None):
        if newuserid is not None and newpassword is not None:
            self.username = newuserid
            self.password = newpassword
        if self.username == '' or self.password == '':
            raise NotValidUsernameAndPassword()
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*',
                   '(', ')', '-', '=', '+', '[', ']', '{', '}', ';', ':', '"', "'", ',', '|']
        for i in symbols:
            if i in self.username:
                raise NotValidUsernameAndPassword()
        # Check if user exists
        self.cursor.execute("SELECT username FROM users WHERE username=?", (self.username,))
        if self.cursor.fetchone():
            raise UseralreadyExist()
        try:
            hasedpass = HashPassword(self.password)
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (self.username, hasedpass))
            self.conn.commit()
            return True
        except Exception as e:
            raise e

    def CreateDatabase(self, newdatabasename=None):
        if check:
            self.databasename = newdatabasename
            try:
                if newdatabasename is None or self.databasename is None:
                    raise DatabaseNameNotProvided()
                elif type(self.databasename) == str:
                    # Check if database exists
                    self.cursor.execute("SELECT name FROM databases WHERE name=?", (self.databasename,))
                    if self.cursor.fetchone():
                        raise DatabasealreadyExist()
                    self.cursor.execute("INSERT INTO databases (name) VALUES (?)", (self.databasename,))
                    self.conn.commit()
            except Exception as e:
                raise e
        else:
            raise NotVerfiedUsernamePassword()

    def VerfiyDetails(self, userid_, password_):
        global check
        self.username = userid_
        self.password = password_
        if self.username == '' or self.password == '':
            raise NotValidUsernameAndPassword()
        try:
            self.cursor.execute("SELECT password FROM users WHERE username=?", (self.username,))
            row = self.cursor.fetchone()
            if row and VerfiyPassword(self.password, row[0]):
                check = True
                return check
            else:
                check = False
                return check
        except Exception as e:
            raise IncorrectPassword(e)

    def CurrentUser(self):
        if check:
            if self.username is None:
                raise NotVerfiedUsernamePassword("not enter username password")
            else:
                return f'User: {self.username}'
        else:
            raise NotVerfiedUsernamePassword()

    def ChangePassword(self, username_, oldpassword, newpassword):
        if check:
            self.cursor.execute("SELECT password FROM users WHERE username=?", (username_,))
            row = self.cursor.fetchone()
            if row and VerfiyPassword(oldpassword, row[0]):
                new_hashed = HashPassword(newpassword)
                self.cursor.execute("UPDATE users SET password=? WHERE username=?", (new_hashed, username_))
                self.conn.commit()
            else:
                raise IncorrectPassword()
        else:
            raise NotVerfiedUsernamePassword()

    def CreateTable(self, tablename):
        if databasechecker and check:
            try:
                # Create a new table for the database
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {tablename} (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT)")
                self.conn.commit()
                return True
            except Exception as e:
                raise SomethingWentWrong(e)
        else:
            if check == False:
                raise NotVerfiedUsernamePassword()
            elif databasechecker == False:
                raise DatabaseNotSelected()

    def RemoveDatabase(self, removedatabasename):
        if check:
            try:
                self.cursor.execute("DELETE FROM databases WHERE name=?", (removedatabasename,))
                self.conn.commit()
                # Optionally drop all tables related to this database
            except Exception as e:
                raise SomethingWentWrong(e)
        else:
            raise NotVerfiedUsernamePassword()

    def RemoveTable(self, databasename, removetablename):
        if check and databasechecker:
            try:
                self.cursor.execute(f"DROP TABLE IF EXISTS {removetablename}")
                self.conn.commit()
            except Exception as e:
                raise SomethingWentWrong(e)
        else:
            if check:
                raise DatabaseNotSelected()
            else:
                raise NotVerfiedUsernamePassword()

    def UpdateTableValues(self, tablename, oldvalue, newvalue):
        if check:
            try:
                self.cursor.execute(f"UPDATE {tablename} SET data=? WHERE data=?", (newvalue, oldvalue))
                self.conn.commit()
            except Exception as e:
                raise SomethingWentWrong(e)
        else:
            if check:
                raise DatabaseNotSelected()
            else:
                raise NotVerfiedUsernamePassword()

    def ConnectTable(self, tablename1, tablename2):
        if databasechecker and check:
            try:
                # Fetch all rows from both tables
                self.cursor.execute(f"SELECT data FROM {tablename1}")
                data1 = [row[0] for row in self.cursor.fetchall()]
                self.cursor.execute(f"SELECT data FROM {tablename2}")
                data2 = [row[0] for row in self.cursor.fetchall()]
                for i in range(min(len(data1), len(data2))):
                    row1 = data1[i]
                    row2 = data2[i]
                    if row1 != row2:
                        yield f"Row {i + 1}: {row1} - {row2}"
            except Exception as e:
                raise SomethingWentWrong(e)
        else:
            if check:
                raise DatabaseNotSelected()
            else:
                raise NotVerfiedUsernamePassword()

    def InsertIntoTable(self, tablename, values=[]):
        if databasechecker and check:
            try:
                # Insert values as a single string (for simplicity)
                self.cursor.execute(f"INSERT INTO {tablename} (data) VALUES (?)", (str(values),))
                self.conn.commit()
            except Exception as e:
                raise SomethingWentWrong(e)
        else:
            if check == False:
                raise NotVerfiedUsernamePassword()
            elif databasechecker == False:
                raise DatabaseNotSelected()

    def FetchTable(self, tablename):
        if databasechecker and check:
            try:
                self.cursor.execute(f"SELECT data FROM {tablename}")
                rows = self.cursor.fetchall()
                for row in rows:
                    yield row[0]
            except Exception as e:
                raise SomethingWentWrong(e)
        else:
            if check == False:
                raise NotVerfiedUsernamePassword()
            elif databasechecker == False:
                raise DatabaseNotSelected()

    def UseDatabase(self, databasen=None):
        global databasechecker
        if databasen is None and self.databasename is None:
            raise DatabaseNameNotProvided()
        elif databasen is not None and self.databasename is None:
            self.databasename = databasen
        self.cursor.execute("SELECT name FROM databases WHERE name=?", (self.databasename,))
        if self.cursor.fetchone():
            databasechecker = True
        else:
            databasechecker = False

# ----------------helper function----------------

def HashPassword(password):
    "return hash value of string or any value"
    try:
        hash_obj = hashlib.sha256((password).encode('utf-8'))
        return hash_obj.hexdigest()
    except Exception as e:
        raise e

def VerfiyPassword(password, stored_password):
    "return True if password match otherwise false"
    try:
        hashed_password = HashPassword(password)
        return hashed_password == stored_password
    except Exception:
        raise Exception
