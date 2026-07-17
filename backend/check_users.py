import sqlite3

def check_users():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # get tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cursor.fetchall()]
    
    if 'users' in tables:
        cursor.execute("SELECT username, email, is_superuser FROM users")
        print("Users Table:", cursor.fetchall())
    elif 'auth_user' in tables:
        cursor.execute("SELECT username, email, is_superuser FROM auth_user")
        print("Auth User Table:", cursor.fetchall())
    else:
        print("Tables:", tables)

if __name__ == '__main__':
    check_users()
