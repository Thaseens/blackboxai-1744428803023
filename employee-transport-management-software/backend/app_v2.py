from flask import Flask, jsonify, request, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# Database setup
def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'ars_travels.db')
    
    # Delete existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  position TEXT NOT NULL,
                  salary REAL NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS transports
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  vehicle_type TEXT NOT NULL,
                  license_plate TEXT NOT NULL,
                  driver_id INTEGER,
                  FOREIGN KEY (driver_id) REFERENCES employees(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  employee_id INTEGER,
                  date DATE,
                  status TEXT NOT NULL,
                  FOREIGN KEY (employee_id) REFERENCES employees(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user')''')

    # Add default admin and user accounts
    admin_password = generate_password_hash('admin123', method='pbkdf2:sha256')
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
             ('ADMIN001', admin_password, 'admin'))

    user_password = generate_password_hash('user123', method='pbkdf2:sha256')
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
             ('EMP001', user_password, 'user'))

    conn.commit()
    conn.close()

# Database connection
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'ars_travels.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
init_db()

# User Registration Endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                      (username, password, 'user'))
        connection.commit()
    except sqlite3.IntegrityError:
        return jsonify({"message": "Username already exists!"}), 400
    finally:
        cursor.close()
        connection.close()

    return jsonify({"message": "User registered successfully!"}), 201

# User Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid credentials!"}), 401

    token = jwt.encode({
        'user_id': user['id'], 
        'username': user['username'],
        'role': user['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, 'secret_key', algorithm='HS256')
    
    return jsonify({
        "token": token,
        "role": user['role']
    }), 200

# Employee Management Endpoints
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)", 
                   (data['name'], data['position'], data['salary']))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Employee added successfully!"}), 201

@app.route('/employees', methods=['GET'])
def get_employees():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return jsonify(employees)

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE employees SET name = ?, position = ?, salary = ? WHERE id = ?",
                  (data['name'], data['position'], data['salary'], id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Employee updated successfully!"}), 200

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Employee deleted successfully!"}), 200

# Transport Management Endpoints
@app.route('/transports', methods=['POST'])
def add_transport():
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO transports (vehicle_type, license_plate) VALUES (?, ?)", 
                   (data['vehicle_type'], data['license_plate']))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Transport added successfully!"}), 201

@app.route('/transports', methods=['GET'])
def get_transports():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transports")
    transports = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return jsonify(transports)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
