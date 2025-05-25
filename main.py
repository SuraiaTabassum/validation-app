from flask import Flask, request
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

@app.route('/', methods=['GET'])
def index():
    return '''
        <h2>Login</h2>
        <form method="post" action="/login">
            Username: <input type="text" name="username" /><br>
            Password: <input type="password" name="password" /><br>
            <input type="submit" value="Login" />
        </form>
    '''

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
