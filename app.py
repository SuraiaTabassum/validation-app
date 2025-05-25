
from flask import Flask, request, redirect
import psycopg2

app = Flask(__name__)

# PostgreSQL DB connection
conn = psycopg2.connect(
    host="dpg-d0pano3e5dus73dk7a8g-a.oregon-postgres.render.com",
    port=5432,
    dbname="flask_app_6750",
    user="flask_app_6750_user",
    password="zIZIoLGRzsPYY5P4EKRHKmowP3gsDkXh"
)

# Home route shows Register link
@app.route('/')
def home():
    return '''
        <h2>Welcome!</h2>
        <a href="/register">Register</a><br>
        <a href="/login">Login</a>
    '''

# Registration form
@app.route('/register', methods=['GET'])
def show_register():
    return '''
        <h2>Register</h2>
        <form method="post" action="/register">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Register">
        </form>
    '''

# Handle registration data
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cur.close()

    return redirect('/login')

# Login form
@app.route('/login', methods=['GET'])
def show_login():
    return '''
        <h2>Login</h2>
        <form method="post" action="/login">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# Handle login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()

    if user:
        return f"<h3>Welcome, {username}!</h3>"
    else:
        return "<h3>Invalid username or password</h3>"

if __name__ == '__main__':
    app.run(debug=True)
