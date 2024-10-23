from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# PostgreSQL connection
try:
    conn = psycopg2.connect(
        dbname="Housedb",
        user="postgres",
        password="mamun2483asif",
        host="localhost",
        port="5432"
    )
    print("Database connected successfully!")
except Exception as e:
    print(f"Failed to connect to the database: {e}")

# Route for login page
@app.route('/')
def login():
    return render_template('login.html')

# Handle login logic
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    # Query the user from the database
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user:
        # If the stored password is hashed, use check_password_hash
        stored_password = user[2]  # Assuming user[2] contains the stored password
        try:
            # If the password is already hashed
            if check_password_hash(stored_password, password):
                flash('Logged in successfully!', 'success')
                return redirect('/')
            else:
                flash('Invalid password.', 'error')
                return redirect('/')
        except ValueError:
            # If check_password_hash throws a ValueError, assume the password is in plain text
            if stored_password == password:
                # Hash the plain text password and update the database
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                cur = conn.cursor()
                cur.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_password, username))
                conn.commit()
                cur.close()
                flash('Logged in successfully and password updated!', 'success')
                return redirect('/')
            else:
                flash('Login failed. Check your credentials.', 'error')
                return redirect('/')
    else:
        flash('Username not found.', 'error')
        return redirect('/')

# Route for signup page
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Handle signup logic
@app.route('/signup', methods=['POST'])
def signup_post():
    # Get form data (username and password)
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        # Handle missing input here
        return "Please provide both username and password."

    # Hash the password using pbkdf2:sha256
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Check if user already exists
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    if user:
        flash('Username already exists. Please log in.', 'error')
        cur.close()
        return redirect('/')

    # Insert the new user into the database
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    cur.close()

    flash('Account created successfully!', 'success')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)