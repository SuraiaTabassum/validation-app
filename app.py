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

# Create 'users' table if it doesn't exist
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100),
            password VARCHAR(100)
        );
    """)
    conn.commit()

@app.route('/')
def index():
    return '''
        <h2>Login</h2>
        <form method="post" action="/login">
            Username: <input type="text" name="username" /><br>
            Password: <input type="password" name="password" /><br>
            <input type="submit" value="Login" />
        </form>
        <p>Don't have an account? <a href="/register">Register here</a></p>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()

    if user:
        return f"<h3>Welcome, {username}!</h3>"
    else:
        return "<h3>Invalid username or password</h3>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()

        return redirect('/')  # Redirect to login after registration
    return '''
        <h2>Register</h2>
        <form method="post">
            Username: <input type="text" name="username" /><br>
            Password: <input type="password" name="password" /><br>
            <input type="submit" value="Register" />
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
