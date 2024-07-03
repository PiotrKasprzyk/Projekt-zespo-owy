from models import get_genres, get_categories

print("Testing get_genres:")
genres = get_genres()
print("Genres:", genres)

print("Testing get_categories:")
categories = get_categories()
print("Categories:", categories)
