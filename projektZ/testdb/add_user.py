from models import add_user

def add_sample_user():
    add_user("testuser", "testpassword")

if __name__ == '__main__':
    add_sample_user()
    print("Sample user added.")
