from models import get_reviews

def test_get_reviews(book_id):
    reviews = get_reviews(book_id)
    for review in reviews:
        print(review)

if __name__ == '__main__':
    test_get_reviews(1)  # Zakładając, że book_id to 1
