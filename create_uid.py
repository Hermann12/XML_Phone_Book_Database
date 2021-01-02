import sqlite3

def create_uniqueid(db_file):
    # If the uniqueid is empty, generate one
    connection = sqlite3.connect(db_file)
    print(f"Database connected")
    print(f"Version {sqlite3.version}")
    print(f"SQLITE_VERSION (Library) {sqlite3.sqlite_version}")
    
    connection.row_factory = lambda cursor, row: row[0]
    cursor = connection.cursor()
    
    sql1 = "SELECT uniqueid FROM contacts;"
    unique_id = cursor.execute(sql1).fetchall()
    
    cursor.execute("SELECT count(*) from contacts")
    result = cursor.fetchone()
    print("DB count function:", result)
    
    check_sum = []
    for row in unique_id:
        # print(type(row))
        check_sum.append(row)
        # print("Unique_id:",row)
    # print(check_sum)
    Sum = sum(check_sum)
    print(f'Sum of Check: {Sum}')
    if Sum == 0:
        print(len(check_sum))
        sql2 =('UPDATE contacts SET uniqueid=rowid;')
        cursor.execute(sql2)
        connection.commit()
    else:
        print("Uniqueid is not empty")
    

    cursor.execute('UPDATE numbers SET uniqueid =(SELECT uniqueid FROM contacts WHERE contacts.realName = numbers.realName);')
    connection.commit()
    

    cursor.execute('UPDATE emails SET uniqueid =(SELECT uniqueid FROM contacts WHERE contacts.realName = emails.realName);')
    connection.commit()
    connection.close()
    print('Process finished, database closed!')


if __name__ == '__main__':
    """ Input XML file definition """
    db_file = "04_Fritz_Phonebook.db"
    create_uniqueid(db_file)
    print('Finished')