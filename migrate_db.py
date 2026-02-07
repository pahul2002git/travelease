from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        # Create new tables if they don't exist
        db.create_all()
        
        # Add columns to packages table
        columns_to_add_packages = [
            ('hotel_details', 'TEXT'),
            ('sightseeing', 'TEXT'),
            ('popular_places', 'TEXT'),
            ('flight_details', 'TEXT'),
            ('itinerary', 'TEXT'),
            ('hotel_amenities', 'TEXT'),
            ('discount_percentage', 'FLOAT DEFAULT 0.0'),
            ('special_offer_text', 'VARCHAR(200)'),
            ('is_featured', 'BOOLEAN DEFAULT FALSE'),
            ('images', 'TEXT'),
            ('flight_economy_price', 'FLOAT DEFAULT 0.0'),
            ('flight_premium_economy_price', 'FLOAT DEFAULT 0.0'),
            ('flight_business_price', 'FLOAT DEFAULT 0.0'),
            ('flight_first_class_price', 'FLOAT DEFAULT 0.0')
        ]

        for col_name, col_type in columns_to_add_packages:
            try:
                db.session.execute(text(f"ALTER TABLE packages ADD COLUMN {col_name} {col_type}"))
                db.session.commit()
                print(f"Added column {col_name} to packages")
            except Exception as e:
                db.session.rollback()
                if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                    pass
                else:
                    print(f"Error adding column {col_name} to packages: {str(e)}")

        # Create new tables (Flight and FlightBooking)
        db.create_all()
        print("Ensured all tables exist (Flight, FlightBooking, etc.)")

        # Add columns to bookings table
        columns_to_add_bookings = [
            ('selected_flight_class', 'VARCHAR(50)'),
            ('flight_price_at_booking', 'FLOAT DEFAULT 0.0'),
            ('flight_booking_id', 'INTEGER')
        ]
        
        for col_name, col_type in columns_to_add_bookings:
            try:
                db.session.execute(text(f"ALTER TABLE bookings ADD COLUMN {col_name} {col_type}"))
                db.session.commit()
                print(f"Added column {col_name} to bookings")
            except Exception as e:
                db.session.rollback()
                if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                    pass
                else:
                    print(f"Error adding column {col_name} to bookings: {str(e)}")

        # Add status column to contact_us table
        try:
            db.session.execute(text("ALTER TABLE contact_us ADD COLUMN status VARCHAR(50) DEFAULT 'Pending'"))
            db.session.commit()
            print("Added column status to contact_us")
        except Exception as e:
            db.session.rollback()
            if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                pass
            else:
                print(f"Error adding column status to contact_us: {str(e)}")

        # Add num_travellers to flight_bookings table
        try:
            db.session.execute(text("ALTER TABLE flight_bookings ADD COLUMN num_travellers INTEGER DEFAULT 1"))
            db.session.commit()
            print("Added column num_travellers to flight_bookings")
        except Exception as e:
            db.session.rollback()
            if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                pass
            else:
                print(f"Error adding column num_travellers to flight_bookings: {str(e)}")

        # Ensure Review and Wishlist tables exist
        db.create_all()
        print("Ensured Review and Wishlist tables exist")

    print("Migration complete!")

if __name__ == "__main__":
    migrate()
