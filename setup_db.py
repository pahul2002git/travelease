from app import app, db, User, Package, Flight, Train, Bus, Cab
from werkzeug.security import generate_password_hash

def setup_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created.")

        # Create Admin User
        admin_email = 'admin@travelease.com'
        admin_user = User.query.filter_by(email=admin_email).first()

        if not admin_user:
            hashed_password = generate_password_hash('admin123', method='scrypt')
            new_admin = User(
                username='Admin',
                email=admin_email,
                password=hashed_password,
                is_admin=True
            )
            db.session.add(new_admin)
            print(f"Admin user created: Email: {admin_email}, Password: admin123")
        else:
            print("Admin user already exists.")

        # Add Sample Packages
        if Package.query.count() == 0:
            sample_packages = [
                Package(
                    name="Bali Bliss Getaway",
                    description="Experience the magic of Bali with this 5-day retreat. Includes villa accommodation, daily breakfast, and guided temple tours.",
                    price=102000.00,
                    duration="5 Days / 4 Nights",
                    image_url="https://images.unsplash.com/photo-1537996194471-e657df975ab4"
                ),
                Package(
                    name="Swiss Alps Adventure",
                    description="Skiing, hiking, and chocolate tasting in the heart of Switzerland. Perfect for adventure seekers.",
                    price=212500.00,
                    duration="7 Days / 6 Nights",
                    image_url="https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99"
                ),
                Package(
                    name="Maldives Luxury Escape",
                    description="Stay in an overwater bungalow and enjoy crystal clear waters. All-inclusive luxury package.",
                    price=297500.00,
                    duration="6 Days / 5 Nights",
                    image_url="https://images.unsplash.com/photo-1514282401047-d79a71a590e8"
                )
            ]
            db.session.add_all(sample_packages)
            print("Sample vacation packages added.")

        # Seed Transport Data
        seed_transport_data()

        db.session.commit()
        print("Database setup complete!")

def seed_transport_data():
    # Seed Flights
    if Flight.query.count() == 0:
        airlines = ["AirAsia", "Etihad Airways", "Emirates", "Vistara", "IndiGo", "Air India", "Qantas", "Air France"]
        routes = [
            ("Delhi", "Mumbai"), ("Delhi", "Dubai"), ("Mumbai", "Dubai"), ("Delhi", "Manali"),
            ("Mumbai", "Jaipur"), ("Delhi", "Kashmir"), ("Delhi", "Sydney"), ("Mumbai", "Paris")
        ]
        for idx, (dep, arr) in enumerate(routes):
            airline = airlines[idx % len(airlines)]
            flight_number = f"{airline[:2].upper()}{idx+101:03d}"
            base_price = 4500 + (idx * 1000)
            db.session.add(Flight(
                airline=airline,
                flight_number=flight_number,
                departure_city=dep,
                arrival_city=arr,
                departure_time="08:00 AM",
                base_price=base_price
            ))
        print("Flights seeded.")

    # Seed Trains
    if Train.query.count() == 0:
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
        print("Trains seeded.")

    # Seed Buses
    if Bus.query.count() == 0:
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
        print("Buses seeded.")

    # Seed Cabs
    if Cab.query.count() == 0:
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
        print("Cabs seeded.")

if __name__ == '__main__':
    setup_database()
