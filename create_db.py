import sqlite3

def create_employee_table():
    con = sqlite3.connect(r'ims.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS employee (
            emp_id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            dob TEXT,
            doj TEXT,
            pass TEXT,
            utype TEXT,
            address TEXT
        )
    ''')
    con.commit()
    con.close()

create_employee_table()
