import sqlite3

#connection = sqlite3.connect('SBD.db')

def _create_table():
    global connection
    connection.execute('''
    CREATE TABLE users(user_name text, pass text,pk text)
    ''')
    connection.commit()

def _insert_data(con,user,passw,pk):
    con.execute('''INSERT INTO users VALUES(?,?,?)''',(user,passw,pk))
    con.commit()

def _retrive_data():
    for x in connection.execute('SELECT * FROM users'):
        print(x)  # x[0]

def _clear_db(conn):
        conn.execute('delete from users')
        conn.commit()


#_retrive_data()