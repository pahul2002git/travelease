from app import app, db, User, Package
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
        
        db.session.commit()
        print("Database setup complete!")

if __name__ == '__main__':
    setup_database()
