from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    bookings = db.relationship('Booking', backref='user', lazy=True)


class Package(db.Model):
    __tablename__ = 'packages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    hotel_details = db.Column(db.Text, nullable=True)
    sightseeing = db.Column(db.Text, nullable=True)
    popular_places = db.Column(db.Text, nullable=True)
    flight_details = db.Column(db.Text, nullable=True)
    itinerary = db.Column(db.Text, nullable=True)  # Day-by-day travel plan
    hotel_amenities = db.Column(db.Text, nullable=True)  # Hotel facilities and amenities
    
    # Special offers and promotions
    discount_percentage = db.Column(db.Float, default=0.0)
    special_offer_text = db.Column(db.String(200), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    
    # Image gallery (pipe-separated URLs)
    images = db.Column(db.Text, nullable=True)
    
    # Class-based flight prices (base prices that can be added to package price)
    flight_economy_price = db.Column(db.Float, default=0.0)
    flight_premium_economy_price = db.Column(db.Float, default=0.0)
    flight_business_price = db.Column(db.Float, default=0.0)
    flight_first_class_price = db.Column(db.Float, default=0.0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    package_id = db.Column(
        db.Integer,
        db.ForeignKey('packages.id'),
        nullable=False
    )

    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Confirmed')
    num_members = db.Column(db.Integer, default=1, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    
    # Selected flight information
    selected_flight_class = db.Column(db.String(50), nullable=True)
    flight_price_at_booking = db.Column(db.Float, default=0.0)

    package = db.relationship('Package')
    
    # Link to expansion flight booking
    flight_booking_id = db.Column(db.Integer, db.ForeignKey('flight_bookings.id'), nullable=True)
    flight_booking = db.relationship('FlightBooking', backref='main_booking', uselist=False)

class Flight(db.Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(100), nullable=False)
    flight_number = db.Column(db.String(20), nullable=False)
    departure_city = db.Column(db.String(100), nullable=False)
    arrival_city = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.String(50), nullable=True)
    base_price = db.Column(db.Float, nullable=False)

class FlightBooking(db.Model):
    __tablename__ = 'flight_bookings'

    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False)
    selected_class = db.Column(db.String(50), nullable=False)
    num_travellers = db.Column(db.Integer, default=1)
    final_price = db.Column(db.Float, nullable=False)

    flight = db.relationship('Flight')
    user = db.relationship('User')

class Contact(db.Model):
    __tablename__ = 'contact_us'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(256), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    package = db.relationship('Package', backref='reviews')
    user = db.relationship('User', backref='reviews')

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='wishlist_items')
    package = db.relationship('Package', backref='wishlisted_by')

class Train(db.Model):
    __tablename__ = 'trains'

    id = db.Column(db.Integer, primary_key=True)
    operator = db.Column(db.String(120), nullable=False)
    train_number = db.Column(db.String(30), nullable=False)
    departure_city = db.Column(db.String(100), nullable=False)
    arrival_city = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.String(50), nullable=True)
    base_price = db.Column(db.Float, nullable=False)

class TrainBooking(db.Model):
    __tablename__ = 'train_bookings'

    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('trains.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    travel_date = db.Column(db.DateTime, nullable=False)
    selected_class = db.Column(db.String(50), nullable=False)
    num_travellers = db.Column(db.Integer, default=1)
    final_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    train = db.relationship('Train')
    user = db.relationship('User')

class Bus(db.Model):
    __tablename__ = 'buses'

    id = db.Column(db.Integer, primary_key=True)
    operator = db.Column(db.String(120), nullable=False)
    bus_number = db.Column(db.String(30), nullable=False)
    departure_city = db.Column(db.String(100), nullable=False)
    arrival_city = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.String(50), nullable=True)
    base_price = db.Column(db.Float, nullable=False)

class BusBooking(db.Model):
    __tablename__ = 'bus_bookings'

    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    travel_date = db.Column(db.DateTime, nullable=False)
    selected_class = db.Column(db.String(50), nullable=False)
    num_travellers = db.Column(db.Integer, default=1)
    final_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bus = db.relationship('Bus')
    user = db.relationship('User')

class Cab(db.Model):
    __tablename__ = 'cabs'

    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(120), nullable=False)
    cab_type = db.Column(db.String(50), nullable=False)
    departure_city = db.Column(db.String(100), nullable=False)
    arrival_city = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)

class CabBooking(db.Model):
    __tablename__ = 'cab_bookings'

    id = db.Column(db.Integer, primary_key=True)
    cab_id = db.Column(db.Integer, db.ForeignKey('cabs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    travel_date = db.Column(db.DateTime, nullable=False)
    selected_class = db.Column(db.String(50), nullable=False)
    num_travellers = db.Column(db.Integer, default=1)
    final_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cab = db.relationship('Cab')
    user = db.relationship('User')
