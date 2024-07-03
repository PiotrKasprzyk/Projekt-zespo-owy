import sqlite3

def check_db_structure():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("PRAGMA table_info(books)")
    books_columns = c.fetchall()

    c.execute("PRAGMA table_info(users)")
    users_columns = c.fetchall()

    c.execute("PRAGMA table_info(reviews)")
    reviews_columns = c.fetchall()

    conn.close()
    return books_columns, users_columns, reviews_columns

if __name__ == '__main__':
    books_columns, users_columns, reviews_columns = check_db_structure()

    print("Books Table Columns:")
    for column in books_columns:
        print(column)

    print("\nUsers Table Columns:")
    for column in users_columns:
        print(column)

    print("\nReviews Table Columns:")
    for column in reviews_columns:
        print(column)
