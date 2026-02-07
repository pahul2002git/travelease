# TravelEase - Holiday Booking System

A premium holiday booking website built with Flask, MySQL, and modern HTML/CSS.

## Features
- **User Authentication**: Login and Registration system.
- **Browse Packages**: View holiday packages with details.
- **Booking System**: Book holidays and simulate payments.
- **Admin Panel**: Add and delete packages.
- **User Dashboard**: View booking history.
- **Fake Payment Gateway**: Simulated checkout process.

## Prerequisites
- Python 3.8+
- MySQL Server

## Setup Instructions

### 1. Database Setup
1. Open your MySQL client (e.g., Workbench or Command Line).
2. Create the database:
   ```sql
   CREATE DATABASE holiday_booking;
   ```
3. (Optional) Run the `database.sql` script to create tables manually, though the app can handle this if configured.

### 2. Configuration
1. Open `config.py`.
2. Update the `SQLALCHEMY_DATABASE_URI` with your MySQL credentials:
   ```python
   # Format: mysql+pymysql://username:password@localhost/holiday_booking
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yourpassword@localhost/holiday_booking'
   ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

## Admin Access
To make a user an admin, you currently need to update the database directly:
```sql
UPDATE user SET is_admin = 1 WHERE email = 'your@email.com';
```
Or you can modify `app.py` temporarily to create an admin user.

## Project Structure
- `app.py`: Main application logic.
- `models.py`: Database models.
- `templates/`: HTML files.
- `static/`: CSS and Images.
