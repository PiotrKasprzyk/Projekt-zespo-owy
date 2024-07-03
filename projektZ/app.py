from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import init_db, add_book, get_books, add_user, get_user, get_recommendations, get_book_rankings, add_post, get_posts, add_comment, get_comments, like_post, unlike_post, like_comment, unlike_comment, get_genres, get_categories, add_review, get_reviews, get_loans_by_user, get_user_info, delete_book, return_book, add_loan, update_user_info
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def check_admin():
    return 'username' in session and session['username'] == 'admin'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    books = get_books()
    return render_template('index.html', books=books)

@app.route('/search', methods=['GET', 'POST'])
def search():
    genres = get_genres()
    categories = get_categories()
    query = request.form.get('query')
    genre = request.form.get('genre')
    category = request.form.get('category')
    
    books = get_books(query, genre, category)
    
    return render_template('search.html', books=books, genres=genres, categories=categories)

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    genres = get_genres()
    categories = get_categories()
    books = get_recommendations()
    if request.method == 'POST':
        genre = request.form.get('genre', '')
        category = request.form.get('category', '')
        books = get_books(genre=genre, category=category)
    return render_template('recommendations.html', books=books, genres=genres, categories=categories)

@app.route('/rankings')
def rankings():
    books = get_book_rankings()
    return render_template('rankings.html', books=books)
@app.route('/reviews/<int:book_id>', methods=['GET', 'POST'])
def reviews(book_id):
    if request.method == 'POST':
        rating = request.form.get('rating')
        opinion = request.form.get('opinion')
        user_id = session.get('user_id')
        print(f"user_id: {user_id}, book_id: {book_id}, rating: {rating}, opinion: {opinion}")  # Debugowanie
        if user_id:
            add_review(book_id, user_id, rating, opinion)
            flash('Recenzja dodana pomyślnie', 'success')
        else:
            flash('Musisz być zalogowany, aby dodać recenzję', 'danger')
    reviews = get_reviews(book_id)
    return render_template('reviews.html', reviews=reviews, book_id=book_id)


@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        if 'username' not in session:
            flash('You must be logged in to create a post.', 'danger')
            return redirect(url_for('login'))

        title = request.form['title']
        content = request.form['content']
        user = get_user(session['username'])
        add_post(user[0], title, content)
        flash('Post created successfully!', 'success')
        return redirect(url_for('forum'))

    posts = get_posts()
    return render_template('forum.html', posts=posts)

@app.route('/forum/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    if request.method == 'POST':
        if 'username' not in session:
            flash('You must be logged in to comment.', 'danger')
            return redirect(url_for('login'))

        content = request.form['content']
        user = get_user(session['username'])
        parent_id = request.form.get('parent_id')
        add_comment(post_id, user[0], content, parent_id)
        flash('Comment added successfully!', 'success')
        return redirect(url_for('post', post_id=post_id))

    post_data = [post for post in get_posts() if post[0] == post_id][0]
    comments = get_comments(post_id)
    return render_template('post.html', post=post_data, comments=comments)

@app.route('/forum/like/<int:post_id>')
def like(post_id):
    if 'username' not in session:
        flash('You must be logged in to like a post.', 'danger')
        return redirect(url_for('login'))

    user_id = get_user(session['username'])[0]
    like_post(post_id, user_id)
    return redirect(request.referrer)

@app.route('/forum/unlike/<int:post_id>')
def unlike(post_id):
    if 'username' not in session:
        flash('You must be logged in to unlike a post.', 'danger')
        return redirect(url_for('login'))

    user_id = get_user(session['username'])[0]
    unlike_post(post_id, user_id)
    return redirect(request.referrer)

@app.route('/forum/comment/like/<int:comment_id>')
def like_comment_route(comment_id):
    if 'username' not in session:
        flash('You must be logged in to like a comment.', 'danger')
        return redirect(url_for('login'))

    user_id = get_user(session['username'])[0]
    like_comment(comment_id, user_id)
    return redirect(request.referrer)

@app.route('/forum/comment/unlike/<int:comment_id>')
def unlike_comment_route(comment_id):
    if 'username' not in session:
        flash('You must be logged in to unlike a comment.', 'danger')
        return redirect(url_for('login'))

    user_id = get_user(session['username'])[0]
    unlike_comment(comment_id, user_id)
    return redirect(request.referrer)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        try:
            add_user(username, hashed_password)
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except:
            flash('Username already exists', 'danger')
            return render_template('register.html')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            session['user_id'] = user[0]  # Ustawienie user_id w sesji

            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    flash('Your message has been sent successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not check_admin():
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        category = request.form.get('category')
        description = request.form.get('description')
        publish_date = request.form.get('publish_date')
        rating = request.form.get('rating')
        add_book(title, author, genre, category, description, publish_date, rating)
        flash('Book added successfully', 'success')

    genres = get_genres()
    categories = get_categories()
    books = get_books()
    return render_template('admin.html', genres=genres, categories=categories, books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book_route():
    if not check_admin():
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        category = request.form.get('category')
        description = request.form.get('description')
        publish_date = request.form.get('publish_date')
        rating = request.form.get('rating')
        add_book(title, author, genre, category, description, publish_date, rating)
        flash('Book added successfully', 'success')
        return redirect(url_for('add_book_route'))

    genres = get_genres()
    categories = get_categories()
    return render_template('add_book.html', genres=genres, categories=categories)

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book_route(book_id):
    if not check_admin():
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('index'))

    delete_book(book_id)
    flash('Book deleted successfully', 'success')
    return redirect(url_for('admin'))

@app.route('/reader', methods=['GET', 'POST'])
@login_required
def reader_panel():
    username = session.get('username')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        address = request.form.get('address')

        print("Received data from form:")
        print(f"first_name: {first_name}")
        print(f"last_name: {last_name}")
        print(f"phone_number: {phone_number}")
        print(f"email: {email}")
        print(f"address: {address}")

        c.execute('''
        UPDATE users
        SET first_name = ?, last_name = ?, phone_number = ?, email = ?, address = ?
        WHERE username = ?
        ''', (first_name, last_name, phone_number, email, address, username))

        conn.commit()
        flash('Information updated successfully!', 'success')

    c.execute('SELECT id, first_name, last_name, phone_number, email, address FROM users WHERE username = ?', (username,))
    user_info = c.fetchone()

    if user_info:
        user_id = user_info[0]
        c.execute('''
        SELECT books.id, books.title, books.author, loans.loan_date
        FROM books
        JOIN loans ON books.id = loans.book_id
        WHERE loans.user_id = ? AND loans.return_date IS NULL
        ''', (user_id,))
        loans = c.fetchall()
        print("Borrowed books: ", loans)
    else:
        loans = []

    conn.close()

    return render_template('reader.html', user_info=user_info, loans=loans)
@app.route('/update_reader_info', methods=['POST'])
@login_required
def update_reader_info():
    user_id = session.get('user_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    address = request.form.get('address')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
    UPDATE users
    SET first_name = ?, last_name = ?, phone_number = ?, email = ?, address = ?
    WHERE id = ?
    ''', (first_name, last_name, phone_number, email, address, user_id))

    conn.commit()
    conn.close()
    flash('Information updated successfully!', 'success')
    return redirect(url_for('reader_panel'))


@app.route('/return_book/<int:book_id>', methods=['POST'])
@login_required
def return_book_route(book_id):
    username = session.get('username')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute('SELECT id FROM users WHERE username = ?', (username,))
    user_id = c.fetchone()[0]

    return_book(user_id, book_id)
    
    flash('Book returned successfully!', 'success')
    return redirect(url_for('reader_panel'))

@app.route('/borrow_book/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    username = session.get('username')
    if not username:
        flash('Musisz być zalogowany, aby wypożyczyć książkę', 'danger')
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Pobierz user_id na podstawie username
    c.execute('SELECT id FROM users WHERE username = ?', (username,))
    user_id = c.fetchone()[0]

    c.execute('''
    INSERT INTO loans (user_id, book_id, loan_date)
    VALUES (?, ?, ?)
    ''', (user_id, book_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    conn.commit()
    conn.close()
    flash('Książka została wypożyczona!', 'success')
    return redirect(url_for('search'))
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
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
