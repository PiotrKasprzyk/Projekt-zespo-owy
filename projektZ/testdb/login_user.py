from flask import Flask, session
from models import get_user

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/login')
def login():
    user = get_user("testuser")
    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        return "User logged in."
    return "User not found."

if __name__ == '__main__':
    app.run(debug=True)
