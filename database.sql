CREATE DATABASE IF NOT EXISTS holiday_booking;
USE holiday_booking;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(256) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS packages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    price FLOAT NOT NULL,
    duration VARCHAR(50) NOT NULL,
    image_url VARCHAR(500),
    hotel_details TEXT,
    sightseeing TEXT,
    popular_places TEXT,
    flight_details TEXT,
    itinerary TEXT,
    hotel_amenities TEXT,
    discount_percentage FLOAT DEFAULT 0.0,
    special_offer_text VARCHAR(200),
    is_featured BOOLEAN DEFAULT FALSE,
    images TEXT,
    flight_economy_price FLOAT DEFAULT 0.0,
    flight_premium_economy_price FLOAT DEFAULT 0.0,
    flight_business_price FLOAT DEFAULT 0.0,
    flight_first_class_price FLOAT DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    package_id INT NOT NULL,
    booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Confirmed',
    num_members INT DEFAULT 1,
    total_price FLOAT NOT NULL,
    selected_flight_class VARCHAR(50),
    flight_price_at_booking FLOAT DEFAULT 0.0,
    flight_booking_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (package_id) REFERENCES packages(id),
    FOREIGN KEY (flight_booking_id) REFERENCES flight_bookings(id)
);

CREATE TABLE IF NOT EXISTS flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airline VARCHAR(100) NOT NULL,
    flight_number VARCHAR(20) NOT NULL,
    departure_city VARCHAR(100) NOT NULL,
    arrival_city VARCHAR(100) NOT NULL,
    departure_time VARCHAR(50),
    base_price FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS flight_bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_id INT NOT NULL,
    user_id INT NOT NULL,
    departure_date DATETIME NOT NULL,
    selected_class VARCHAR(50) NOT NULL,
    num_travellers INT DEFAULT 1,
    final_price FLOAT NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES flights(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS contact_us (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    subject VARCHAR(256) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    package_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (package_id) REFERENCES packages(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS wishlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    package_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (package_id) REFERENCES packages(id)
);

CREATE TABLE IF NOT EXISTS trains (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operator VARCHAR(120) NOT NULL,
    train_number VARCHAR(30) NOT NULL,
    departure_city VARCHAR(100) NOT NULL,
    arrival_city VARCHAR(100) NOT NULL,
    departure_time VARCHAR(50),
    base_price FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS train_bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    train_id INT NOT NULL,
    user_id INT NOT NULL,
    travel_date DATETIME NOT NULL,
    selected_class VARCHAR(50) NOT NULL,
    num_travellers INT DEFAULT 1,
    final_price FLOAT NOT NULL,
    status VARCHAR(50) DEFAULT 'Confirmed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (train_id) REFERENCES trains(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS buses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operator VARCHAR(120) NOT NULL,
    bus_number VARCHAR(30) NOT NULL,
    departure_city VARCHAR(100) NOT NULL,
    arrival_city VARCHAR(100) NOT NULL,
    departure_time VARCHAR(50),
    base_price FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS bus_bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bus_id INT NOT NULL,
    user_id INT NOT NULL,
    travel_date DATETIME NOT NULL,
    selected_class VARCHAR(50) NOT NULL,
    num_travellers INT DEFAULT 1,
    final_price FLOAT NOT NULL,
    status VARCHAR(50) DEFAULT 'Confirmed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bus_id) REFERENCES buses(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS cabs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    provider VARCHAR(120) NOT NULL,
    cab_type VARCHAR(50) NOT NULL,
    departure_city VARCHAR(100) NOT NULL,
    arrival_city VARCHAR(100) NOT NULL,
    base_price FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS cab_bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cab_id INT NOT NULL,
    user_id INT NOT NULL,
    travel_date DATETIME NOT NULL,
    selected_class VARCHAR(50) NOT NULL,
    num_travellers INT DEFAULT 1,
    final_price FLOAT NOT NULL,
    status VARCHAR(50) DEFAULT 'Confirmed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cab_id) REFERENCES cabs(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
