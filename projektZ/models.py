import sqlite3
from datetime import datetime

def get_genres():
    genres = [
        'Romans', 'Fantastyka i Science Fiction', 'Powieść historyczna', 'Horror',
        'Kryminał i Thriller', 'Biografia i reportaż', 'Książki dla młodzieży'
    ]
    return genres

def get_categories():
    categories = [
        'powieść', 'bajka', 'ballada', 'poemat', 'dziennik', 'elegia', 'epos',
        'esej', 'fraszka', 'kazanie', 'list', 'oda', 'opowiadanie', 'pamiętnik',
        'pieśń', 'psalm', 'satyra', 'sielanka', 'sonet', 'tren', 'hymn'
    ]
    return categories
def get_books(query=None, genre=None, category=None):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    query_conditions = []
    query_params = []

    if query:
        query_conditions.append("(title LIKE ? OR author LIKE ? OR genre LIKE ? OR category LIKE ?)")
        query_params.extend([f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'])

    if genre:
        query_conditions.append("genre = ?")
        query_params.append(genre)

    if category:
        query_conditions.append("category = ?")
        query_params.append(category)

    query_conditions = " AND ".join(query_conditions)
    query_string = f"SELECT id, title, author, genre, category, description, publish_date, rating FROM books WHERE {query_conditions}" if query_conditions else "SELECT id, title, author, genre, category, description, publish_date, rating FROM books"

    c.execute(query_string, query_params)
    books = c.fetchall()
    conn.close()
    return books



def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            description TEXT,
            publish_date TEXT,
            rating REAL,
            category TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            first_name TEXT,
            last_name TEXT,
            phone_number TEXT,
            email TEXT,
            address TEXT
        )
    ''')
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
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            content TEXT,
            likes INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
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
    c.execute('''
        CREATE TABLE IF NOT EXISTS post_likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS comment_likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (comment_id) REFERENCES comments(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
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
    conn.commit()
    conn.close()

def add_book(title, author, genre, description, publish_date, rating, category):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO books (title, author, genre, description, publish_date, rating, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, author, genre, description, publish_date, rating, category))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_user(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def get_recommendations():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books ORDER BY RANDOM() LIMIT 5')
    books = c.fetchall()
    conn.close()
    return books

def get_book_rankings():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT id, title, author, genre, publish_date, description, rating, category FROM books ORDER BY rating DESC')
    books = c.fetchall()
    conn.close()
    return books


def add_post(user_id, title, content):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)', (user_id, title, content))
    conn.commit()
    conn.close()

def get_posts():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT posts.id, users.username, posts.title, posts.content, posts.likes FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.id DESC')
    posts = c.fetchall()
    conn.close()
    return posts

def add_comment(post_id, user_id, content, parent_id=None):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO comments (post_id, user_id, content, parent_id) VALUES (?, ?, ?, ?)', (post_id, user_id, content, parent_id))
    conn.commit()
    conn.close()

def get_comments(post_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT comments.id, users.username, comments.content, comments.likes, comments.parent_id FROM comments JOIN users ON comments.user_id = users.id WHERE comments.post_id = ? ORDER BY comments.id ASC', (post_id,))
    comments = c.fetchall()
    conn.close()

    comment_tree = build_comment_tree(comments)
    return comment_tree

def build_comment_tree(comments):
    comment_dict = {comment[0]: list(comment) for comment in comments}
    tree = []
    for comment in comments:
        comment_id, username, content, likes, parent_id = comment
        if parent_id is None:
            tree.append(comment_dict[comment_id])
        else:
            parent = comment_dict.get(parent_id)
            if parent is not None:
                if len(parent) == 5:
                    parent.append([])
                parent[5].append(comment_dict[comment_id])
    return tree

def like_post(post_id, user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM post_likes WHERE post_id = ? AND user_id = ?', (post_id, user_id))
    if not c.fetchone():
        c.execute('UPDATE posts SET likes = likes + 1 WHERE id = ?', (post_id,))
        c.execute('INSERT INTO post_likes (post_id, user_id) VALUES (?, ?)', (post_id, user_id))
    conn.commit()
    conn.close()

def unlike_post(post_id, user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM post_likes WHERE post_id = ? AND user_id = ?', (post_id, user_id))
    if c.fetchone():
        c.execute('UPDATE posts SET likes = likes - 1 WHERE id = ? AND likes > 0', (post_id,))
        c.execute('DELETE FROM post_likes WHERE post_id = ? AND user_id = ?', (post_id, user_id))
    conn.commit()
    conn.close()

def like_comment(comment_id, user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM comment_likes WHERE comment_id = ? AND user_id = ?', (comment_id, user_id))
    if not c.fetchone():
        c.execute('UPDATE comments SET likes = likes + 1 WHERE id = ?', (comment_id,))
        c.execute('INSERT INTO comment_likes (comment_id, user_id) VALUES (?, ?)', (comment_id, user_id))
    conn.commit()
    conn.close()

def unlike_comment(comment_id, user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM comment_likes WHERE comment_id = ? AND user_id = ?', (comment_id, user_id))
    if c.fetchone():
        c.execute('UPDATE comments SET likes = likes - 1 WHERE id = ? AND likes > 0', (comment_id,))
        c.execute('DELETE FROM comment_likes WHERE comment_id = ? AND user_id = ?', (comment_id, user_id))
    conn.commit()
    conn.close()
def add_review(book_id, user_id, rating, opinion):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    print(f"Adding review: book_id={book_id}, user_id={user_id}, rating={rating}, opinion={opinion}")
    c.execute('''
        INSERT INTO reviews (book_id, user_id, rating, opinion)
        VALUES (?, ?, ?, ?)
    ''', (book_id, user_id, rating, opinion))
    conn.commit()
    update_book_rating(book_id)
    conn.close()
def get_reviews(book_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        SELECT reviews.rating, reviews.opinion, users.username
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        WHERE reviews.book_id = ?
    ''', (book_id,))
    reviews = c.fetchall()
    print(f"Fetched reviews for book_id={book_id}: {reviews}")
    conn.close()
    return reviews


def update_book_rating(book_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT AVG(rating) FROM reviews WHERE book_id = ?', (book_id,))
    avg_rating = c.fetchone()[0]
    c.execute('UPDATE books SET rating = ? WHERE id = ?', (avg_rating, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

def add_loan(user_id, book_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
    INSERT INTO loans (user_id, book_id, loan_date)
    VALUES (?, ?, ?)
    ''', (user_id, book_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def get_loans_by_user(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
    SELECT books.id, books.title, books.author, loans.loan_date
    FROM books
    JOIN loans ON books.id = loans.book_id
    WHERE loans.user_id = ? AND loans.return_date IS NULL
    ''', (user_id,))
    loans = c.fetchall()
    conn.close()
    return loans

def return_book(user_id, book_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
    UPDATE loans
    SET return_date = ?
    WHERE user_id = ? AND book_id = ? AND return_date IS NULL
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id, book_id))
    conn.commit()
    conn.close()

def get_user_info(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user
def update_user_info(user_id, first_name, last_name, phone_number, email, address):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
    UPDATE users
    SET first_name = ?, last_name = ?, phone_number = ?, email = ?, address = ?
    WHERE id = ?
    ''', (first_name, last_name, phone_number, email, address, user_id))
    conn.commit()
    conn.close()
