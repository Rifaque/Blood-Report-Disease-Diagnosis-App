from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import sqlite3

app = Flask(__name__)
app.secret_key = 'Hub_Zero'

# Load the main dataset
df_main = pd.read_csv("Training.csv")

# Diseases
disease = {0: 'Anemia', 1: 'Polycythemia', 2: 'Leukocytosis', 3: 'Leukopenia', 4: 'Thrombocytopenia',
           5: 'Thrombocytosis', 6: 'Neutropenia', 7: 'Neutrophilia', 8: 'Lymphocytopenia', 9: 'Lymphocytosis',
           10: 'Monocytes high', 11: 'Eosinophil high', 12: 'Basophil high', 13: 'Normal'}

# Causes
Rea = {0: [' - Anemia due to blood loss \n'
            ' - Bone marrow disorders \n'
            ' - Nutritional deficiency \n'
            ' - Chronic Kidney disease  \n'
            ' - Chronic inflammatory disease \n'],
       1: ['- Dehydration, such as from severe diarrhea \n'
           '- tumours \n'
           '- Lung diseases \n'
           '- Smoking \n'
           '- Polycythemia vera \n'],
       2: ['- Infection \n'
           '- Leukemia \n'
           '- Inflammation \n'
           '- Stress, allergies, asthma \n'],
       3: ['- Viral infection \n'
           '- Severe bacterial infection \n'
           '- Bone marrow disorders \n'
           '- Autoimmune conditions \n'
           '- Lymphoma \n'
           '- Dietary deficiencies \n'],
       4: ['- Cancer, such as leukemia or lymphoma \n'
           '- Autoimmune diseases \n'
           '- Bacterial infection \n'
           '- Viral infection like dengue \n'
           '- Chemotherapy or radiation therapy \n'
           '- Certain drugs, such as nonsteroidal anti-inflammatory drugs (NSAIDs) \n'],
       5: ['- Bone marrow disorders \n'
           '- Essential thrombocythemia \n'
           '- Anemia \n'
           '- Infection \n'
           '- Surgical removal of the spleen \n'
           '- Polycythemia vera \n'
           '- Some types of leukemia \n'],
       6: ['- Severe infection \n'
           '- Immunodeficiency \n'
           '- Autoimmune disorders \n'
           '- Dietary deficiencies \n'
           '- Reaction to drugs \n'
           '- Bone marrow damage \n'],
       7: ['- Acute bacterial infections \n'
           '- Inflammation \n'
           '- Stress, Trauma \n'
           '- Certain leukemias \n'],
       8: ['- Autoimmune disorders \n'
           '- Infections \n'
           '- Bone marrow damage \n'
           '- Corticosteroids \n'],
       9: ['- Acute viral infections \n'
           '- Certain bacterial infections \n'
           '- Chronic inflammatory disorder \n'
           '- Lymphocytic leukemia, lymphoma \n'
           '- Acute stress \n'],
       10: ['- Chronic infections \n'
            '- Infection within the heart \n'
            '- Collagen vascular diseases \n'
            '- Monocytic or myelomonocytic leukemia \n'],
       11: ['- Asthma, allergies such as hay fever \n'
            '- Drug reactions \n'
            '- Parasitic infections \n'
            '- Inflammatory disorders \n'
            '- Some cancers, leukemias or lymphomas \n'],
       12: ['- Rare allergic reactions \n'
            '- Inflammation \n'
            '- Some leukemias \n'
            '- Uremia \n'],
       13: ['- Normal \n']}

# Function to train and predict using RandomForestClassifier
def rf(W, R, H, P, N, L, M, E, B):
    # Load the dataset and split into features and target variable
    x = df_main.drop(columns=['Disease'], axis=1)
    y = df_main['Disease']

    # Split the dataset into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=40)

    # Initialize and train the RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(x_train, y_train)

    # Prepare input data as numpy array
    t = np.array([W, R, H, P, N, L, M, E, B]).reshape(1, -1)

    # Predict using the trained model
    res = clf.predict(t)[0]
    return res

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        W = float(request.form['WBC'])
        R = float(request.form['RBC'])
        H = float(request.form['HGB'])
        P = float(request.form['PLT'])
        N = float(request.form['NEUT'])
        L = float(request.form['LYMPH'])
        M = float(request.form['MONO'])
        E = float(request.form['EO'])
        B = float(request.form['BASO'])

        # Call the RandomForestClassifier function
        result = rf(W, R, H, P, N, L, M, E, B)

        # Get the cause of the disease
        cause = Rea[result][0]

        # Render result template
        return render_template('result.html', disease=disease[result], cause=cause)

    return render_template('index.html')

# Route for saving the data without displaying the result
@app.route('/save_data', methods=['POST'])
def save_data():
    if request.method == 'POST':
        W = float(request.form['WBC'])
        R = float(request.form['RBC'])
        H = float(request.form['HGB'])
        P = float(request.form['PLT'])
        N = float(request.form['NEUT'])
        L = float(request.form['LYMPH'])
        M = float(request.form['MONO'])
        E = float(request.form['EO'])
        B = float(request.form['BASO'])
        
        print("Received data:", W, R, H, P, N, L, M, E, B)  # Add this line for debugging

        # Call the RandomForestClassifier function
        result = rf(W, R, H, P, N, L, M, E, B)

        # Get the user ID of the currently logged-in user
        user_id = session.get('user_id')

        # Save the data to the user history table
        insert_user_history(user_id, W, R, H, P, N, L, M, E, B, result)

        # Show success message
        return "Data saved successfully"



# Routes for login and register
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/result')
def result():
    # Your logic for handling the result page goes here
    return render_template('result.html')


@app.route('/afterlogin', methods=['GET', 'POST'])
def afterlogin():
    if request.method == 'POST':
        # Process form submission
        W = float(request.form['WBC'])
        R = float(request.form['RBC'])
        H = float(request.form['HGB'])
        P = float(request.form['PLT'])
        N = float(request.form['NEUT'])
        L = float(request.form['LYMPH'])
        M = float(request.form['MONO'])
        E = float(request.form['EO'])
        B = float(request.form['BASO'])

        # Call the RandomForestClassifier function
        result = rf(W, R, H, P, N, L, M, E, B)

        # Get the cause of the disease
        cause = Rea[result][0]

        # Render result template
        return render_template('resultafter.html', disease=disease[result], cause=cause)  # Redirect to the desired page after form submission
    else:
        # Handle GET request
        return render_template('afterlogin.html')


# Route for logging out
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('index'))

# Function to create a connection to the database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create the user table if it doesn't exist
def create_user_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

# Function to create the user history table if it doesn't exist
def create_user_history_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            WBC REAL,
            RBC REAL,
            HGB REAL,
            PLT REAL,
            NEUT REAL,
            LYMPH REAL,
            MONO REAL,
            EO REAL,
            BASO REAL,
            result INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')
    conn.commit()
    conn.close()

# Check if the user table exists, if not, create it
create_user_table()
create_user_history_table()

# Function to insert user history into the user_history table
def insert_user_history(user_id, WBC, RBC, HGB, PLT, NEUT, LYMPH, MONO, EO, BASO, result):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO user_history (user_id, WBC, RBC, HGB, PLT, NEUT, LYMPH, MONO, EO, BASO, result) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, WBC, RBC, HGB, PLT, NEUT, LYMPH, MONO, EO, BASO, result))
    conn.commit()
    conn.close()

# Function to get user history based on user ID
def get_user_history(user_id):
    conn = get_db_connection()
    cursor = conn.execute('''
        SELECT * FROM user_history WHERE user_id = ?
    ''', (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history

# Function to get user ID based on email
def get_user_id(email):
    conn = get_db_connection()
    cursor = conn.execute('''
        SELECT id FROM users WHERE email = ?
    ''', (email,))
    user = cursor.fetchone()
    conn.close()
    return user['id'] if user else None

    
# Route for registering a new user
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']
        
        # Insert user data into the database
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO users (name, email, password, age, gender)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, password, age, gender))
        conn.commit()
        conn.close()
        
        # Redirect to login page after successful registration
        return redirect(url_for('login')) 
    
    # Render the registration form
    return render_template('register.html')

# Route for logging in
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate user credentials
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE name = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Store user information in session
            session['user_id'] = user['id']
            session['username'] = user['name']
            # Redirect to home page or any other page after successful login
            return redirect(url_for('afterlogin'))
        else:
            error_message = "Invalid username or password. Please try again."
            return render_template('login.html', error_message=error_message)

    # Render the login form
    return render_template('login.html')

# Route for viewing user history

@app.route('/view_history')
def view_history():
    # Logic to retrieve user history from the database
    # Assuming you have a function to get user history data
    history_data = get_user_history(session.get('user_id'))
    return render_template('history.html', history=history_data)


if __name__ == '__main__':
    app.run(debug=True)
