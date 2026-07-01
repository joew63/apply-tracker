import sqlite3

connect = sqlite3.connect("applications.db")

cursor = connect.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

def app_create():
    cursor.execute("DROP TABLE IF EXISTS applications")
    cursor.execute("DROP TABLE IF EXISTS companies")
    cursor.execute("""
        CREATE TABLE companies (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT        
        )
    """)
    cursor.execute("""
        CREATE TABLE applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            role TEXT,
            status TEXT,
            date_applied TEXT,
            notes TEXT,
            FOREIGN KEY (company_id) REFERENCES companies (company_id)
        )
    """)

def add_company(name):
    contains = cursor.execute("SELECT name FROM companies WHERE name = ?", (name,))  
    if contains.fetchone() is None:
        cursor.execute("""
            INSERT INTO companies (name) VALUES (?)
        """, (name,))
        print(f"Inserted {name}")
        connect.commit()

def add_application(name, role, status, date_applied, notes):
    result = cursor.execute("SELECT company_id FROM companies WHERE name = ?", (name,))
    row = result.fetchone()
    if row is None:
        print("add company first")
    else:
        company_id = row[0]
        cursor.execute(f"""
            INSERT INTO applications (company_id, role, status, date_applied, notes) VALUES (?, ?, ?, ?, ?)
        """, (company_id, role, status, date_applied, notes,))
        print(f"Inserted application for {name}")
        connect.commit()