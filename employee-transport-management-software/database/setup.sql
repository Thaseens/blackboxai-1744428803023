-- SQL script to set up the database for ARS Travels and Logistics Pvt Ltd

CREATE DATABASE ars_travels;

USE ars_travels;

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(50) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL
);

CREATE TABLE transports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_type VARCHAR(50) NOT NULL,
    license_plate VARCHAR(20) NOT NULL,
    driver_id INT,
    FOREIGN KEY (driver_id) REFERENCES employees(id)
);

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    date DATE,
    status ENUM('present', 'absent') NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE fuel_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transport_id INT,
    fuel_amount DECIMAL(10, 2) NOT NULL,
    request_date DATE,
    FOREIGN KEY (transport_id) REFERENCES transports(id)
);

CREATE TABLE service_expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transport_id INT,
    expense_amount DECIMAL(10, 2) NOT NULL,
    description VARCHAR(255),
    expense_date DATE,
    FOREIGN KEY (transport_id) REFERENCES transports(id)
);

CREATE TABLE scheduled_trips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transport_id INT,
    trip_date DATE,
    start_time TIME,
    end_time TIME,
    FOREIGN KEY (transport_id) REFERENCES transports(id)
);

CREATE TABLE dynamic_trips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transport_id INT,
    trip_date DATE,
    pickup_location VARCHAR(255),
    dropoff_location VARCHAR(255),
    FOREIGN KEY (transport_id) REFERENCES transports(id)
);
