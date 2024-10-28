from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import bcrypt  # For hashing passwords

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Database connection
def create_connection():
    return mysql.connector.connect(
        host='localhost',  # Change if using a different server
        database='blood_bank',
        user='your_mysql_username',
        password='your_mysql_password'
    )

# Route for rendering the login page
@app.route('/')
def index():
    return render_template('login.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    # Check if the user exists in the database
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        session['username'] = user['username']
        return jsonify({'message': 'Login successful', 'redirect': '/dashboard'})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Dashboard route for authenticated users
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))

    return render_template('dashboard.html', username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)
