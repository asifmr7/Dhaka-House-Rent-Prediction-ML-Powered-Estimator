from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import joblib  
import numpy as np
import psycopg2
import os
import pandas as pd
import pickle

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
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




# Load and clean the location data
def get_cleaned_locations():
    csv_file_path = 'C:\\Users\\asifm\\OneDrive\\Desktop\\data\\houserentdhaka.csv'  # Adjust to your file path
    df = pd.read_csv(csv_file_path)
    locations = df['Location'].dropna().unique()
    return sorted([location.strip() for location in locations])





@app.route('/index')
def index():
    # Pass the cleaned locations to the HTML template
    location_suggestions = get_cleaned_locations()
    return render_template('index.html', location_suggestions=location_suggestions)





@app.route('/')
def root():
    # Redirect to the login page by default
   
    return redirect(url_for('login'))

# Route for login page
@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

# Handle login logic
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    
    cur = conn.cursor()
    try:
        cur.execute("SELECT username, password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user:
            stored_password = user[1]
            if check_password_hash(stored_password, password):
                session['username'] = username
                session['logged_in'] = True
                flash('Logged in successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid password.', 'error')
        else:
            flash('Username not found.', 'error')
    except Exception as e:
        flash('An error occurred. Please try again later.', 'error')
        print(e)
    finally:
        cur.close()

    return redirect(url_for('login'))



@app.route('/home')
def home():
    if 'logged_in' in session and session['logged_in']:
        # Pass the cleaned locations to the HTML template
        location_suggestions = get_cleaned_locations()
        return render_template('index.html', location_suggestions=location_suggestions)
    return redirect(url_for('login'))



# Route for signup page
@app.route("/sign-up", methods=["GET"])
def sign_up():
    return render_template("sign-up.html")




# Handle signup logic
@app.route('/signup', methods=['POST'])
def signup_post():
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        flash('Please provide both username and password.', 'error')
        return redirect(url_for('sign_up'))

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    cur = conn.cursor()
    try:
        cur.execute("SELECT username FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user:
            flash('Username already exists. Please log in.', 'error')
            return redirect(url_for('login'))

        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        flash('An error occurred. Please try again.', 'error')
        print(e)
    finally:
        cur.close()

    return redirect(url_for('sign_up'))

@app.route('/signup')
def signup():
    return render_template('signup.html')





# Paths to model and preprocessing files
model_path = 'C:\\Users\\asifm\\OneDrive\\Desktop\\data\\pipeline.pkl'
scaler_path = 'C:\\Users\\asifm\\OneDrive\\Desktop\\data\\scaler.pkl'
label_encoder_path = 'C:\\Users\\asifm\\OneDrive\\Desktop\\data\\label_encode.pkl'

# Load the model and preprocessors
try:
    with open(model_path, 'rb') as file:
        pipeline = pickle.load(file)
    scaler = joblib.load(scaler_path)
    label_encoder = joblib.load(label_encoder_path)
    print("Model and preprocessors loaded successfully!")
except Exception as e:
    pipeline = None
    scaler = None
    label_encoder = None
    print(f"Error loading model or preprocessors: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    if pipeline is None or scaler is None or label_encoder is None:
        return jsonify({'error': 'Model or preprocessors are not available. Please contact the administrator.'})

    try:
        location = request.form['location']
        area = request.form['area']
        bed = int(request.form['bed'])
        bath = int(request.form['bath'])

        try:
            area = float(area)
        except ValueError:
            return jsonify({'error': 'Area must be a numeric value.'})

        if area <= 0 or bed <= 0 or bath <= 0:
            return jsonify({'error': 'Inputs must be positive numbers.'})

        input_data = pd.DataFrame({
            'Area': [area],
            'Bed': [bed],
            'Bath': [bath],
            'Location': [location]
        })

        input_data['Location'] = input_data['Location'].str.strip()

        if location not in label_encoder.classes_:
            label_encoder.classes_ = np.append(label_encoder.classes_, location)
        input_data['Location_encoded'] = label_encoder.transform(input_data['Location'])

        columns_to_normalize = ['Area', 'Bed', 'Bath']
        input_data_scaled = scaler.transform(input_data[columns_to_normalize])

        input_scaled_df = pd.DataFrame(input_data_scaled, columns=columns_to_normalize)
        input_scaled_df['Location_encoded'] = input_data['Location_encoded']

        predicted_price = pipeline.predict(input_scaled_df)[0]
        return jsonify({'predicted_price': round(predicted_price, 2)})

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"})






@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))




if __name__ == "__main__":
    app.run(debug=True)
