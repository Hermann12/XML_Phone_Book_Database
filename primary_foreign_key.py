############################################################
# Primary Key and Foreign Keys from script.sql
# SQLite script "Primary_Foreign_Key.sql"
# Copy the tables and create it abgain with key
#
# XML_Phone_Book_Database
#
## Author (Pseudonym): Hermann12; Date: 10.01.2021
############################################################
import sqlite3

def create_key(db_file):
    # Create Promary Key and Foreign Keys
    connection = sqlite3.connect(db_file)
    print(f"Database connected")
    print(f"Version {sqlite3.version}")
    print(f"SQLITE_VERSION (Library) {sqlite3.sqlite_version}")
    cursor = connection.cursor()
    sql_file = open("Primary_Foreign_Key.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)
    connection.commit()
    print('sql script finished, Primary- and Froreign Key created')
    connection.close()
    print('Database closed.')
       
if __name__ == '__main__':
    """ Input Database file  """
    # create_key("04_Fritz_Phonebook.db")
    print('Finished')