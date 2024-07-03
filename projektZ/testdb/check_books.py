import sqlite3

def check_books():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books')
    books = c.fetchall()
    conn.close()
    return books

if __name__ == '__main__':
    books = check_books()
    for book in books:
        print(book)
