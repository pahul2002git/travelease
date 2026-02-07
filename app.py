import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Package, Booking, Contact, Flight, FlightBooking, Review, Wishlist, Train, TrainBooking, Bus, BusBooking, Cab, CabBooking
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Context Processor to inject current year or other globals
@app.context_processor
def inject_now():
    from datetime import datetime
    return {'year': datetime.utcnow().year}

def ensure_admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('Access denied.', 'danger')
        return False
    return True

def seed_transport_data():
    if Train.query.first() is None:
        operators = ["Vande Bharat", "Rajdhani Express", "Duronto", "Shatabdi"]
        routes = [("Delhi", "Mumbai"), ("Delhi", "Jaipur"), ("Bangalore", "Chennai"), ("Hyderabad", "Pune")]
        for idx, (dep, arr) in enumerate(routes, start=1):
            for op in operators:
                db.session.add(Train(
                    operator=op,
                    train_number=f"TR{idx:03d}",
                    departure_city=dep,
                    arrival_city=arr,
                    departure_time="06:30 AM",
                    base_price=1200 + (idx * 150)
                ))
    if Bus.query.first() is None:
        operators = ["RedBus Prime", "Volvo Express", "Intercity", "Night Rider"]
        routes = [("Mumbai", "Pune"), ("Chennai", "Bangalore"), ("Delhi", "Agra"), ("Kolkata", "Siliguri")]
        for idx, (dep, arr) in enumerate(routes, start=1):
            for op in operators:
                db.session.add(Bus(
                    operator=op,
                    bus_number=f"BS{idx:03d}",
                    departure_city=dep,
                    arrival_city=arr,
                    departure_time="09:15 PM",
                    base_price=600 + (idx * 80)
                ))
    if Cab.query.first() is None:
        providers = ["TravelEase Cabs", "CityLux", "RapidGo"]
        routes = [("Delhi", "Agra"), ("Mumbai", "Lonavala"), ("Bangalore", "Mysore"), ("Chennai", "Pondicherry")]
        for idx, (dep, arr) in enumerate(routes, start=1):
            for provider in providers:
                db.session.add(Cab(
                    provider=provider,
                    cab_type="Sedan",
                    departure_city=dep,
                    arrival_city=arr,
                    base_price=1800 + (idx * 200)
                ))
    db.session.commit()

def compute_price(base_price, travel_class, travellers):
    multipliers = {
        "Economy": 1.0,
        "Premium": 1.4,
        "Business": 2.2,
        "Standard": 1.0,
        "Comfort": 1.3,
        "Luxury": 1.8
    }
    multiplier = multipliers.get(travel_class, 1.0)
    per_person = round(base_price * multiplier, 2)
    total = round(per_person * travellers, 2)
    return per_person, total

# Routes
@app.route('/')
def index():
    packages = Package.query.all()
    return render_template('index.html', packages=packages)

@app.route('/checkout/<int:package_id>', methods=['GET'])
@login_required
def checkout(package_id):
    package = Package.query.get_or_404(package_id)
    num_members = int(session.get('search_travellers') or '1')
    return render_template('checkout.html', package=package, num_members=num_members)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered.', 'warning')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('Error creating account.', 'danger')
            
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/package/<int:package_id>')
def package_details(package_id):
    package = Package.query.get_or_404(package_id)
    reviews = Review.query.filter_by(package_id=package_id).order_by(Review.created_at.desc()).all()
    
    # Calculate average rating
    avg_rating = 0
    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
    
    # Check if user has this in wishlist
    in_wishlist = False
    if current_user.is_authenticated:
        in_wishlist = Wishlist.query.filter_by(user_id=current_user.id, package_id=package_id).first() is not None
    
    return render_template('package_details.html', 
                          package=package, 
                          reviews=reviews,
                          avg_rating=avg_rating,
                          review_count=len(reviews),
                          in_wishlist=in_wishlist)



@app.route('/pay', methods=['POST'])
@login_required
def pay():
    package_id = request.form.get('package_id')
    num_members = int(request.form.get('num_members', 1))
    
    package = Package.query.get_or_404(package_id)
    total_price = package.price * num_members
    
    # Simulate Banking Gateway Logic
    card_number = request.form.get('card_number')
    cvv = request.form.get('cvv')
    
    if not card_number or not cvv:
        flash('Payment failed: Invalid card details.', 'danger')
        return redirect(url_for('checkout', package_id=package_id))
    
    # Create main booking
    new_booking = Booking(
        user_id=current_user.id,
        package_id=package.id,
        total_price=total_price,
        num_members=num_members,
        status='Confirmed'
    )
    
    try:
        db.session.add(new_booking)
        db.session.commit()
        
        # Clear any residual flight session data
        session.pop('selected_flight_id', None)
        session.pop('selected_flight_date', None)
        session.pop('selected_flight_travellers', None)
        session.pop('selected_flight_class', None)
        
        flash('Payment Successful! Booking Confirmed.', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred during booking processing.', 'danger')
        return redirect(url_for('checkout', package_id=package_id))

@app.route('/dashboard')
@login_required
def dashboard():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    train_bookings = TrainBooking.query.filter_by(user_id=current_user.id).order_by(TrainBooking.created_at.desc()).all()
    bus_bookings = BusBooking.query.filter_by(user_id=current_user.id).order_by(BusBooking.created_at.desc()).all()
    cab_bookings = CabBooking.query.filter_by(user_id=current_user.id).order_by(CabBooking.created_at.desc()).all()
    return render_template(
        'dashboard.html',
        bookings=bookings,
        train_bookings=train_bookings,
        bus_bookings=bus_bookings,
        cab_bookings=cab_bookings
    )

# Admin Routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if not ensure_admin():
        return redirect(url_for('index'))
    
    packages = Package.query.all()
    bookings = Booking.query.all()
    train_bookings = TrainBooking.query.order_by(TrainBooking.created_at.desc()).all()
    bus_bookings = BusBooking.query.order_by(BusBooking.created_at.desc()).all()
    cab_bookings = CabBooking.query.order_by(CabBooking.created_at.desc()).all()
    return render_template(
        'admin_dashboard.html',
        packages=packages,
        bookings=bookings,
        train_bookings=train_bookings,
        bus_bookings=bus_bookings,
        cab_bookings=cab_bookings
    )

@app.route('/admin/add', methods=['POST'])
@login_required
def add_package():
    if not ensure_admin():
        return redirect(url_for('index'))
        
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    duration = request.form.get('duration')
    image_url = request.form.get('image_url')
    hotel_details = request.form.get('hotel_details')
    sightseeing = request.form.get('sightseeing')
    popular_places = request.form.get('popular_places')
    itinerary = request.form.get('itinerary')
    hotel_amenities = request.form.get('hotel_amenities')
    discount_percentage = float(request.form.get('discount_percentage', 0))
    images = request.form.get('images', '')

    
    new_package = Package(
        name=name, 
        description=description, 
        price=price, 
        duration=duration, 
        image_url=image_url,
        hotel_details=hotel_details,
        sightseeing=sightseeing,
        popular_places=popular_places,
        itinerary=itinerary,
        hotel_amenities=hotel_amenities,
        discount_percentage=discount_percentage,
        images=images if images else None
    )
    db.session.add(new_package)
    db.session.commit()
    flash('Package added successfully.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<int:package_id>')
@login_required
def delete_package(package_id):
    if not ensure_admin():
        return redirect(url_for('index'))
        
    package = Package.query.get_or_404(package_id)
    db.session.delete(package)
    db.session.commit()
    flash('Package deleted.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/booking/edit/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def edit_booking(booking_id):
    if not ensure_admin():
        return redirect(url_for('index'))
    
    booking = Booking.query.get_or_404(booking_id)
    
    if request.method == 'POST':
        try:
            num_members = int(request.form.get('num_members', booking.num_members))
            status = request.form.get('status', booking.status)
            
            if num_members < 1:
                flash('Number of members must be at least 1.', 'warning')
                return redirect(url_for('edit_booking', booking_id=booking_id))
            
            # Update fields
            booking.num_members = num_members
            booking.status = status
            
            # Recalculate total price
            booking.total_price = booking.package.price * num_members
            
            db.session.commit()
            flash(f'Booking #{booking_id} updated successfully.', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating booking: {str(e)}', 'danger')
            return redirect(url_for('edit_booking', booking_id=booking_id))
            
    return render_template('edit_booking.html', booking=booking)

@app.route('/contact', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not name or not email or not message:
            flash('Please fill in all required fields.', 'warning')
            return redirect(url_for('contact_us'))
            
        new_contact = Contact(name=name, email=email, subject=subject, message=message)
        try:
            db.session.add(new_contact)
            db.session.commit()
            flash('Your message has been sent! We will get back to you soon.', 'success')
            return redirect(url_for('contact_us'))
        except:
            db.session.rollback()
            flash('Error sending message. Please try again.', 'danger')
            
    return render_template('contact.html')

@app.route('/admin/inquiries')
@login_required
def admin_inquiries():
    if not ensure_admin():
        return redirect(url_for('index'))
    
    inquiries = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin_inquiries.html', inquiries=inquiries)

@app.route('/admin/inquiries/acknowledge/<int:contact_id>', methods=['POST'])
@login_required
def acknowledge_inquiry(contact_id):
    if not ensure_admin():
        return redirect(url_for('index'))
        
    inquiry = Contact.query.get_or_404(contact_id)
    try:
        inquiry.status = 'Acknowledged'
        db.session.commit()
        flash('Inquiry marked as acknowledged.', 'success')
    except:
        db.session.rollback()
        flash('Error updating inquiry.', 'danger')
        
    return redirect(url_for('admin_inquiries'))

# Admin Transport Management
@app.route('/admin/trains')
@login_required
def admin_trains():
    if not ensure_admin():
        return redirect(url_for('index'))
    trains = Train.query.order_by(Train.id.desc()).all()
    return render_template('admin_trains.html', trains=trains)

@app.route('/admin/trains/add', methods=['POST'])
@login_required
def admin_trains_add():
    if not ensure_admin():
        return redirect(url_for('index'))
    train = Train(
        operator=request.form.get('operator'),
        train_number=request.form.get('train_number'),
        departure_city=request.form.get('departure_city'),
        arrival_city=request.form.get('arrival_city'),
        departure_time=request.form.get('departure_time'),
        base_price=float(request.form.get('base_price', 0))
    )
    try:
        db.session.add(train)
        db.session.commit()
        flash('Train added successfully.', 'success')
    except:
        db.session.rollback()
        flash('Error adding train.', 'danger')
    return redirect(url_for('admin_trains'))

@app.route('/admin/trains/delete/<int:train_id>', methods=['POST'])
@login_required
def admin_trains_delete(train_id):
    if not ensure_admin():
        return redirect(url_for('index'))
    train = Train.query.get_or_404(train_id)
    try:
        db.session.delete(train)
        db.session.commit()
        flash('Train deleted.', 'success')
    except:
        db.session.rollback()
        flash('Error deleting train.', 'danger')
    return redirect(url_for('admin_trains'))

@app.route('/admin/trains/edit/<int:train_id>', methods=['GET', 'POST'])
@login_required
def admin_trains_edit(train_id):
    if not ensure_admin():
        return redirect(url_for('index'))
    train = Train.query.get_or_404(train_id)
    if request.method == 'POST':
        train.operator = request.form.get('operator')
        train.train_number = request.form.get('train_number')
        train.departure_city = request.form.get('departure_city')
        train.arrival_city = request.form.get('arrival_city')
        train.departure_time = request.form.get('departure_time')
        train.base_price = float(request.form.get('base_price', train.base_price))
        try:
            db.session.commit()
            flash('Train updated successfully.', 'success')
            return redirect(url_for('admin_trains'))
        except:
            db.session.rollback()
            flash('Error updating train.', 'danger')
    return render_template('admin_train_edit.html', train=train)

@app.route('/admin/buses')
@login_required
def admin_buses():
    if not ensure_admin():
        return redirect(url_for('index'))
    buses = Bus.query.order_by(Bus.id.desc()).all()
    return render_template('admin_buses.html', buses=buses)

@app.route('/admin/buses/add', methods=['POST'])
@login_required
def admin_buses_add():
    if not ensure_admin():
        return redirect(url_for('index'))
    bus = Bus(
        operator=request.form.get('operator'),
        bus_number=request.form.get('bus_number'),
        departure_city=request.form.get('departure_city'),
        arrival_city=request.form.get('arrival_city'),
        departure_time=request.form.get('departure_time'),
        base_price=float(request.form.get('base_price', 0))
    )
    try:
        db.session.add(bus)
        db.session.commit()
        flash('Bus added successfully.', 'success')
    except:
        db.session.rollback()
        flash('Error adding bus.', 'danger')
    return redirect(url_for('admin_buses'))

@app.route('/admin/buses/delete/<int:bus_id>', methods=['POST'])
@login_required
def admin_buses_delete(bus_id):
    if not ensure_admin():
        return redirect(url_for('index'))
    bus = Bus.query.get_or_404(bus_id)
    try:
        db.session.delete(bus)
        db.session.commit()
        flash('Bus deleted.', 'success')
    except:
        db.session.rollback()
        flash('Error deleting bus.', 'danger')
    return redirect(url_for('admin_buses'))

@app.route('/admin/buses/edit/<int:bus_id>', methods=['GET', 'POST'])
@login_required
def admin_buses_edit(bus_id):
    if not ensure_admin():
        return redirect(url_for('index'))
    bus = Bus.query.get_or_404(bus_id)
    if request.method == 'POST':
        bus.operator = request.form.get('operator')
        bus.bus_number = request.form.get('bus_number')
        bus.departure_city = request.form.get('departure_city')
        bus.arrival_city = request.form.get('arrival_city')
        bus.departure_time = request.form.get('departure_time')
        bus.base_price = float(request.form.get('base_price', bus.base_price))
        try:
            db.session.commit()
            flash('Bus updated successfully.', 'success')
            return redirect(url_for('admin_buses'))
        except:
            db.session.rollback()
            flash('Error updating bus.', 'danger')
    return render_template('admin_bus_edit.html', bus=bus)

@app.route('/admin/cabs')
@login_required
def admin_cabs():
    if not ensure_admin():
        return redirect(url_for('index'))
    cabs = Cab.query.order_by(Cab.id.desc()).all()
    return render_template('admin_cabs.html', cabs=cabs)

@app.route('/admin/cabs/add', methods=['POST'])
@login_required
def admin_cabs_add():
    if not ensure_admin():
        return redirect(url_for('index'))
    cab = Cab(
        provider=request.form.get('provider'),
        cab_type=request.form.get('cab_type'),
        departure_city=request.form.get('departure_city'),
        arrival_city=request.form.get('arrival_city'),
        base_price=float(request.form.get('base_price', 0))
    )
    try:
        db.session.add(cab)
        db.session.commit()
        flash('Cab added successfully.', 'success')
    except:
        db.session.rollback()
        flash('Error adding cab.', 'danger')
    return redirect(url_for('admin_cabs'))

@app.route('/admin/cabs/delete/<int:cab_id>', methods=['POST'])
@login_required
def admin_cabs_delete(cab_id):
    if not ensure_admin():
        return redirect(url_for('index'))
    cab = Cab.query.get_or_404(cab_id)
    try:
        db.session.delete(cab)
        db.session.commit()
        flash('Cab deleted.', 'success')
    except:
        db.session.rollback()
        flash('Error deleting cab.', 'danger')
    return redirect(url_for('admin_cabs'))

@app.route('/admin/cabs/edit/<int:cab_id>', methods=['GET', 'POST'])
@login_required
def admin_cabs_edit(cab_id):
    if not ensure_admin():
        return redirect(url_for('index'))
    cab = Cab.query.get_or_404(cab_id)
    if request.method == 'POST':
        cab.provider = request.form.get('provider')
        cab.cab_type = request.form.get('cab_type')
        cab.departure_city = request.form.get('departure_city')
        cab.arrival_city = request.form.get('arrival_city')
        cab.base_price = float(request.form.get('base_price', cab.base_price))
        try:
            db.session.commit()
            flash('Cab updated successfully.', 'success')
            return redirect(url_for('admin_cabs'))
        except:
            db.session.rollback()
            flash('Error updating cab.', 'danger')
    return render_template('admin_cab_edit.html', cab=cab)

# Review Routes
@app.route('/package/<int:package_id>/review', methods=['POST'])
@login_required
def submit_review(package_id):
    package = Package.query.get_or_404(package_id)
    rating = int(request.form.get('rating', 0))
    comment = request.form.get('comment', '').strip()
    
    if rating < 1 or rating > 5:
        flash('Invalid rating. Please select 1-5 stars.', 'danger')
        return redirect(url_for('package_details', package_id=package_id))
    
    # Check if user already reviewed
    existing_review = Review.query.filter_by(user_id=current_user.id, package_id=package_id).first()
    if existing_review:
        flash('You have already reviewed this package.', 'warning')
        return redirect(url_for('package_details', package_id=package_id))
    
    new_review = Review(
        package_id=package_id,
        user_id=current_user.id,
        rating=rating,
        comment=comment
    )
    
    try:
        db.session.add(new_review)
        db.session.commit()
        flash('Thank you for your review!', 'success')
    except:
        db.session.rollback()
        flash('Error submitting review.', 'danger')
    
    return redirect(url_for('package_details', package_id=package_id))

# Wishlist Routes
@app.route('/wishlist/add/<int:package_id>', methods=['POST'])
@login_required
def add_to_wishlist(package_id):
    package = Package.query.get_or_404(package_id)
    
    # Check if already in wishlist
    existing = Wishlist.query.filter_by(user_id=current_user.id, package_id=package_id).first()
    if existing:
        flash('Package is already in your wishlist.', 'info')
        return redirect(request.referrer or url_for('index'))
    
    wishlist_item = Wishlist(user_id=current_user.id, package_id=package_id)
    try:
        db.session.add(wishlist_item)
        db.session.commit()
        flash(f'{package.name} added to your wishlist!', 'success')
    except:
        db.session.rollback()
        flash('Error adding to wishlist.', 'danger')
    
    return redirect(request.referrer or url_for('index'))

@app.route('/wishlist/remove/<int:package_id>', methods=['POST'])
@login_required
def remove_from_wishlist(package_id):
    wishlist_item = Wishlist.query.filter_by(user_id=current_user.id, package_id=package_id).first()
    if wishlist_item:
        try:
            db.session.delete(wishlist_item)
            db.session.commit()
            flash('Removed from wishlist.', 'success')
        except:
            db.session.rollback()
            flash('Error removing from wishlist.', 'danger')
    
    return redirect(request.referrer or url_for('index'))

@app.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    packages = [item.package for item in wishlist_items]
    return render_template('wishlist.html', packages=packages)

# Search and Filter
@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort = request.args.get('sort', 'newest')
    
    packages_query = Package.query
    
    # Text search
    if query:
        packages_query = packages_query.filter(
            (Package.name.contains(query)) | 
            (Package.description.contains(query))
        )
    
    # Price filter
    if min_price is not None:
        packages_query = packages_query.filter(Package.price >= min_price)
    if max_price is not None:
        packages_query = packages_query.filter(Package.price <= max_price)
    
    # Sorting
    if sort == 'price_low':
        packages_query = packages_query.order_by(Package.price.asc())
    elif sort == 'price_high':
        packages_query = packages_query.order_by(Package.price.desc())
    else:  # newest
        packages_query = packages_query.order_by(Package.created_at.desc())
    
    packages = packages_query.all()
    
    return render_template('search_results.html', 
                          packages=packages, 
                          query=query,
                          min_price=min_price,
                          max_price=max_price,
                          sort=sort)

# Train Routes
@app.route('/trains', methods=['GET', 'POST'])
def trains():
    seed_transport_data()
    trains_data = []
    from_city = to_city = travel_date = travel_class = ''
    travellers = 1

    if request.method == 'POST':
        from_city = request.form.get('from_city', '').strip()
        to_city = request.form.get('to_city', '').strip()
        travel_date = request.form.get('travel_date', '').strip()
        travel_class = request.form.get('travel_class', 'Economy')
        travellers = int(request.form.get('travellers', 1))

        query = Train.query
        if from_city:
            query = query.filter(Train.departure_city.contains(from_city))
        if to_city:
            query = query.filter(Train.arrival_city.contains(to_city))
        trains_list = query.all()

        for train in trains_list:
            per_person, total = compute_price(train.base_price, travel_class, travellers)
            trains_data.append({
                "train": train,
                "per_person": per_person,
                "total": total
            })

    departure_cities = [c[0] for c in db.session.query(Train.departure_city).distinct().all()]
    arrival_cities = [c[0] for c in db.session.query(Train.arrival_city).distinct().all()]
    return render_template(
        'trains.html',
        trains=trains_data,
        from_city=from_city,
        to_city=to_city,
        travel_date=travel_date,
        travel_class=travel_class,
        travellers=travellers,
        searched=request.method == 'POST',
        departure_cities=departure_cities,
        arrival_cities=arrival_cities
    )

@app.route('/trains/checkout/<int:train_id>')
@login_required
def train_checkout(train_id):
    train = Train.query.get_or_404(train_id)
    travel_date = request.args.get('date', '') or datetime.utcnow().strftime('%Y-%m-%d')
    travellers = int(request.args.get('travellers', 1))
    travel_class = request.args.get('travel_class', 'Economy')
    per_person, total = compute_price(train.base_price, travel_class, travellers)
    return render_template(
        'train_checkout.html',
        train=train,
        travel_date=travel_date,
        travellers=travellers,
        travel_class=travel_class,
        per_person=per_person,
        total=total
    )

@app.route('/trains/pay', methods=['POST'])
@login_required
def train_pay():
    train_id = request.form.get('train_id')
    travel_date = request.form.get('travel_date', '') or datetime.utcnow().strftime('%Y-%m-%d')
    travellers = int(request.form.get('travellers', 1))
    travel_class = request.form.get('travel_class', 'Economy')
    card_number = request.form.get('card_number')
    cvv = request.form.get('cvv')
    confirm_details = request.form.get('confirm_details')

    if not confirm_details:
        flash('Please confirm the booking details before payment.', 'warning')
        return redirect(url_for('train_checkout', train_id=train_id, date=travel_date, travellers=travellers, travel_class=travel_class))

    if not card_number or not cvv:
        flash('Payment failed: Invalid card details.', 'danger')
        return redirect(url_for('train_checkout', train_id=train_id, date=travel_date, travellers=travellers, travel_class=travel_class))

    train = Train.query.get_or_404(train_id)
    per_person, total = compute_price(train.base_price, travel_class, travellers)
    booking = TrainBooking(
        train_id=train.id,
        user_id=current_user.id,
        travel_date=datetime.strptime(travel_date, '%Y-%m-%d'),
        selected_class=travel_class,
        num_travellers=travellers,
        final_price=total
    )
    try:
        db.session.add(booking)
        db.session.commit()
        flash('Train booking confirmed!', 'success')
    except:
        db.session.rollback()
        flash('Error processing train booking.', 'danger')
    return redirect(url_for('dashboard'))

# Bus Routes
@app.route('/buses', methods=['GET', 'POST'])
def buses():
    seed_transport_data()
    buses_data = []
    from_city = to_city = travel_date = travel_class = ''
    travellers = 1

    if request.method == 'POST':
        from_city = request.form.get('from_city', '').strip()
        to_city = request.form.get('to_city', '').strip()
        travel_date = request.form.get('travel_date', '').strip()
        travel_class = request.form.get('travel_class', 'Economy')
        travellers = int(request.form.get('travellers', 1))

        query = Bus.query
        if from_city:
            query = query.filter(Bus.departure_city.contains(from_city))
        if to_city:
            query = query.filter(Bus.arrival_city.contains(to_city))
        buses_list = query.all()

        for bus in buses_list:
            per_person, total = compute_price(bus.base_price, travel_class, travellers)
            buses_data.append({
                "bus": bus,
                "per_person": per_person,
                "total": total
            })

    departure_cities = [c[0] for c in db.session.query(Bus.departure_city).distinct().all()]
    arrival_cities = [c[0] for c in db.session.query(Bus.arrival_city).distinct().all()]
    return render_template(
        'buses.html',
        buses=buses_data,
        from_city=from_city,
        to_city=to_city,
        travel_date=travel_date,
        travel_class=travel_class,
        travellers=travellers,
        searched=request.method == 'POST',
        departure_cities=departure_cities,
        arrival_cities=arrival_cities
    )

@app.route('/buses/checkout/<int:bus_id>')
@login_required
def bus_checkout(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    travel_date = request.args.get('date', '') or datetime.utcnow().strftime('%Y-%m-%d')
    travellers = int(request.args.get('travellers', 1))
    travel_class = request.args.get('travel_class', 'Economy')
    per_person, total = compute_price(bus.base_price, travel_class, travellers)
    return render_template(
        'bus_checkout.html',
        bus=bus,
        travel_date=travel_date,
        travellers=travellers,
        travel_class=travel_class,
        per_person=per_person,
        total=total
    )

@app.route('/buses/pay', methods=['POST'])
@login_required
def bus_pay():
    bus_id = request.form.get('bus_id')
    travel_date = request.form.get('travel_date', '') or datetime.utcnow().strftime('%Y-%m-%d')
    travellers = int(request.form.get('travellers', 1))
    travel_class = request.form.get('travel_class', 'Economy')
    card_number = request.form.get('card_number')
    cvv = request.form.get('cvv')
    confirm_details = request.form.get('confirm_details')

    if not confirm_details:
        flash('Please confirm the booking details before payment.', 'warning')
        return redirect(url_for('bus_checkout', bus_id=bus_id, date=travel_date, travellers=travellers, travel_class=travel_class))

    if not card_number or not cvv:
        flash('Payment failed: Invalid card details.', 'danger')
        return redirect(url_for('bus_checkout', bus_id=bus_id, date=travel_date, travellers=travellers, travel_class=travel_class))

    bus = Bus.query.get_or_404(bus_id)
    per_person, total = compute_price(bus.base_price, travel_class, travellers)
    booking = BusBooking(
        bus_id=bus.id,
        user_id=current_user.id,
        travel_date=datetime.strptime(travel_date, '%Y-%m-%d'),
        selected_class=travel_class,
        num_travellers=travellers,
        final_price=total
    )
    try:
        db.session.add(booking)
        db.session.commit()
        flash('Bus booking confirmed!', 'success')
    except:
        db.session.rollback()
        flash('Error processing bus booking.', 'danger')
    return redirect(url_for('dashboard'))

# Cab Routes
@app.route('/cabs', methods=['GET', 'POST'])
def cabs():
    seed_transport_data()
    cabs_data = []
    from_city = to_city = travel_date = travel_class = ''
    travellers = 1

    if request.method == 'POST':
        from_city = request.form.get('from_city', '').strip()
        to_city = request.form.get('to_city', '').strip()
        travel_date = request.form.get('travel_date', '').strip()
        travel_class = request.form.get('travel_class', 'Standard')
        travellers = int(request.form.get('travellers', 1))

        query = Cab.query
        if from_city:
            query = query.filter(Cab.departure_city.contains(from_city))
        if to_city:
            query = query.filter(Cab.arrival_city.contains(to_city))
        cabs_list = query.all()

        for cab in cabs_list:
            per_person, total = compute_price(cab.base_price, travel_class, travellers)
            cabs_data.append({
                "cab": cab,
                "per_person": per_person,
                "total": total
            })

    departure_cities = [c[0] for c in db.session.query(Cab.departure_city).distinct().all()]
    arrival_cities = [c[0] for c in db.session.query(Cab.arrival_city).distinct().all()]
    return render_template(
        'cabs.html',
        cabs=cabs_data,
        from_city=from_city,
        to_city=to_city,
        travel_date=travel_date,
        travel_class=travel_class,
        travellers=travellers,
        searched=request.method == 'POST',
        departure_cities=departure_cities,
        arrival_cities=arrival_cities
    )

@app.route('/cabs/checkout/<int:cab_id>')
@login_required
def cab_checkout(cab_id):
    cab = Cab.query.get_or_404(cab_id)
    travel_date = request.args.get('date', '') or datetime.utcnow().strftime('%Y-%m-%d')
    travellers = int(request.args.get('travellers', 1))
    travel_class = request.args.get('travel_class', 'Standard')
    per_person, total = compute_price(cab.base_price, travel_class, travellers)
    return render_template(
        'cab_checkout.html',
        cab=cab,
        travel_date=travel_date,
        travellers=travellers,
        travel_class=travel_class,
        per_person=per_person,
        total=total
    )

@app.route('/cabs/pay', methods=['POST'])
@login_required
def cab_pay():
    cab_id = request.form.get('cab_id')
    travel_date = request.form.get('travel_date', '') or datetime.utcnow().strftime('%Y-%m-%d')
    travellers = int(request.form.get('travellers', 1))
    travel_class = request.form.get('travel_class', 'Standard')
    card_number = request.form.get('card_number')
    cvv = request.form.get('cvv')
    confirm_details = request.form.get('confirm_details')

    if not confirm_details:
        flash('Please confirm the booking details before payment.', 'warning')
        return redirect(url_for('cab_checkout', cab_id=cab_id, date=travel_date, travellers=travellers, travel_class=travel_class))

    if not card_number or not cvv:
        flash('Payment failed: Invalid card details.', 'danger')
        return redirect(url_for('cab_checkout', cab_id=cab_id, date=travel_date, travellers=travellers, travel_class=travel_class))

    cab = Cab.query.get_or_404(cab_id)
    per_person, total = compute_price(cab.base_price, travel_class, travellers)
    booking = CabBooking(
        cab_id=cab.id,
        user_id=current_user.id,
        travel_date=datetime.strptime(travel_date, '%Y-%m-%d'),
        selected_class=travel_class,
        num_travellers=travellers,
        final_price=total
    )
    try:
        db.session.add(booking)
        db.session.commit()
        flash('Cab booking confirmed!', 'success')
    except:
        db.session.rollback()
        flash('Error processing cab booking.', 'danger')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Initialize DB (Note: In production with MySQL, tables should be created externally or via migrations)
    # with app.app_context():
    #     db.create_all()
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '5000'))
    app.run(host=host, port=port, debug=True)
