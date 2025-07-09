from flask import Flask, render_template, request, redirect, session
import sqlite3

from config import SECRET_KEY, ENCRYPTION_KEY
from encryption.aes_utils import encrypt_data, decrypt_data
from access.capability_token import generate_token, validate_token

app = Flask(__name__)
app.secret_key = SECRET_KEY

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return "Go to /register or /login"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        encrypted_password = encrypt_data(ENCRYPTION_KEY, password)

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                         (username, encrypted_password))
            conn.commit()
        except Exception as e:
            return f"Registration error: {e}"
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", 
                            (username,)).fetchone()
        conn.close()

        if user:
            try:
                decrypted = decrypt_data(ENCRYPTION_KEY, user['password'])
                if decrypted == password_input:
                    token = generate_token(user['id'])
                    session['token'] = token
                    return f"Welcome {username}!<br>Capability Token: {token}"
            except:
                return "Decryption error. Possible tampered data."
        return "Invalid credentials"
    return render_template('login.html')

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=5000)