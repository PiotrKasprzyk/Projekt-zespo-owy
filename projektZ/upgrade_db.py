import sqlite3
from werkzeug.security import generate_password_hash

def upgrade_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create users table if not exists
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        phone_number TEXT,
        email TEXT,
        address TEXT
    )
    ''')

    # Create books table if not exists
    c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        publish_date DATE,
        rating REAL
    )
    ''')

    # Add missing columns to books table
    c.execute("PRAGMA table_info(books)")
    columns = [column[1] for column in c.fetchall()]
    if 'genre' not in columns:
        c.execute("ALTER TABLE books ADD COLUMN genre TEXT")
    if 'category' not in columns:
        c.execute("ALTER TABLE books ADD COLUMN category TEXT")
    if 'rating' not in columns:
        c.execute("ALTER TABLE books ADD COLUMN rating REAL")

    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            user_id INTEGER,
            rating REAL,
            opinion TEXT,
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Create comments table if not exists with parent_id column
    c.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        user_id INTEGER,
        content TEXT,
        likes INTEGER DEFAULT 0,
        parent_id INTEGER,
        FOREIGN KEY (post_id) REFERENCES posts(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Create posts table if not exists
    c.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        content TEXT,
        likes INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Create post_likes table if not exists
    c.execute('''
    CREATE TABLE IF NOT EXISTS post_likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        user_id INTEGER,
        FOREIGN KEY (post_id) REFERENCES posts(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Create comment_likes table if not exists
    c.execute('''
    CREATE TABLE IF NOT EXISTS comment_likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comment_id INTEGER,
        user_id INTEGER,
        FOREIGN KEY (comment_id) REFERENCES comments(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Create loans table if not exists
    c.execute('''
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        loan_date TEXT,
        return_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
    ''')

    admin_password = generate_password_hash('admin')
    c.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not c.fetchone():
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', admin_password))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    upgrade_db()
    print("Database upgraded successfully.")
