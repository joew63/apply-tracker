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
    print(contains)   
    if contains.fetchone() is None:
        cursor.execute("""
            INSERT INTO companies (name) VALUES (?)
        """, (name,))

def add_application(name):
    contains = cursor.execute("SELECT name FROM companies WHERE name = ?", (name,))    
    if contains.fetchone() is None:
        print("add company first")
    else:
        id = cursor.execute("SELECT company_id FROM companies WHERE name = ?", (name,))
    cursor.execute(f"""
        INSERT INTO applications (name) VALUES (?)
    """, (name,))

app_create()
add_company("Microsoft")
add_company("Amazon")
add_company("Microsoft")
add_company("Microsoft")
add_company("Microsoft")
connect.commit()