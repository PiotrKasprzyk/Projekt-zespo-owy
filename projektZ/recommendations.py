import sqlite3

def get_recommendations():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books ORDER BY RANDOM() LIMIT 5')
    books = c.fetchall()
    conn.close()
    return books
