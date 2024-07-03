import sqlite3

def check_reviews():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM reviews')
    reviews = c.fetchall()
    conn.close()
    return reviews

if __name__ == '__main__':
    reviews = check_reviews()
    for review in reviews:
        print(review)
