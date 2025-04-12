from flask import Flask, jsonify, request, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Database setup
def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'ars_travels.db')
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

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

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
    app.run(debug=True, port=8000)
