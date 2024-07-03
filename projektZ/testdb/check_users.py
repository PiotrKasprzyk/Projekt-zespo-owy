import sqlite3

def check_users():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return users

if __name__ == '__main__':
    users = check_users()
    for user in users:
        print(user)
