# ARS Travels and Logistics Pvt Ltd - Employee & Transport Management Software

A comprehensive software solution for managing employees, vehicles, trips, attendance, and expenses for transport companies.

## Features

### 1. Employee Management
- Employee database management
- Attendance tracking
- Leave management
- Performance monitoring

### 2. Transport Management
- Vehicle fleet management
- Fuel request handling
- Service and maintenance tracking
- Vehicle assignment

### 3. Trip Management
- Scheduled trips (School bus routes)
- Dynamic trips (On-demand transport)
- Route planning
- Trip status tracking

### 4. Attendance System
- Daily attendance tracking
- Leave request management
- Attendance reports
- Late arrival monitoring

### 5. Expense Management
- Fuel expenses
- Service expenses
- Trip-related expenses
- Financial reporting

## Technology Stack

- Frontend: HTML, Tailwind CSS, JavaScript
- Backend: Python (Flask)
- Database: MySQL
- Icons: Font Awesome
- Fonts: Google Fonts (Poppins)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/ars-travels-management.git
cd ars-travels-management
```

2. Set up the Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the MySQL database:
```bash
mysql -u your_username -p < database/setup.sql
```

5. Configure the database connection in `backend/app.py`:
```python
connection = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='ars_travels'
)
```

## Running the Application

1. Start the backend server:
```bash
cd backend
python app.py
```

2. Open the frontend in a web browser:
```bash
cd frontend
python -m http.server 8000
```

3. Access the application at `http://localhost:8000`

## Usage Guide

### Employee Management
- Add new employees through the Employees page
- Track attendance and manage leave requests
- View employee performance and attendance statistics

### Transport Management
- Add and manage vehicles in the fleet
- Track fuel consumption and service history
- Assign vehicles to specific routes or trips

### Trip Management
- Create and manage scheduled school bus routes
- Handle dynamic trip requests
- Monitor ongoing trips and track completion

### Attendance System
- Mark daily attendance for employees
- Process leave requests
- Generate attendance reports

### Expense Management
- Track and manage all expenses
- Process fuel requests
- Monitor service expenses
- Generate financial reports

## Security

- User authentication required for accessing the system
- Role-based access control
- Secure database connections
- Input validation and sanitization

## Support

For any issues or questions, please contact:
- Email: support@arstravels.com
- Phone: +91-XXXXXXXXXX

## License

Copyright © 2023 ARS Travels and Logistics Pvt Ltd. All rights reserved.
