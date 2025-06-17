import sqlite3

def create_table():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    print("Table created succefully")
    conn.close()

def creat_user(un, pw):
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("INSERT INTO users(username, password) VALUES(?,?)", (un, pw))
        conn.commit()
        print("User added")
    except Exception as e:
        conn.rollback()
        print("Error in INSERT: {e}")
        raise
    finally:
        conn.close()

def query(command, params=()):
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute(command, params)
        data = c.fetchall()
        conn.commit()
        return data
    except Exception as e:
        conn.rollback()
        print(f"Error in {command}: {e}")
        return None
    finally:
        conn.close()




        

