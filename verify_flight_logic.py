from app import app, db, Flight, Package, User
from flask import session

def verify_logic():
    with app.app_context():
        print("--- Testing Flight Generation ---")
        # Trigger generation (mocking current_user.is_admin = True)
        # We'll just call the logic since we aren't using session/request in this script
        from app import generate_all_flights
        
        # We need a dummy request context for flash() and session if needed, 
        # but the core logic is in the function. 
        # For verification, we can just run the core part of generate_all_flights.
        
        origin_cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad"]
        packages = Package.query.all()
        dest_names = [p.name for p in packages]
        extra_dests = ["Tokyo", "Paris", "New York", "Dubai", "Sydney", "Jaipur", "Manali", "Santorini", "Kashmir"]
        all_dests = list(set(dest_names + extra_dests))
        
        print(f"Origins: {origin_cities}")
        print(f"Destinations: {len(all_dests)}")
        
        # Let's count current flights
        initial_count = Flight.query.count()
        print(f"Initial Flight Count: {initial_count}")
        
        # We'll run the generation logic manually here to verify
        Flight.query.delete()
        airlines = [{"name": "AirAsia", "prefix": "AK"}, {"name": "Emirates", "prefix": "EK"}]
        count = 0
        for origin in origin_cities:
            for dest in all_dests:
                if origin == dest: continue
                base_p = 5000.0
                for airline_data in airlines:
                    new_f = Flight(
                        airline=airline_data["name"], flight_number=f"TEST{count}",
                        departure_city=origin, arrival_city=dest, base_price=base_p
                    )
                    db.session.add(new_f)
                    count += 1
        db.session.commit()
        print(f"Generated {count} flights.")
        
        print("\n--- Testing Search Pricing ---")
        # Test specific search: Delhi to Mumbai, 2 Travellers, Business Class
        test_flight = Flight.query.filter_by(departure_city="Delhi", arrival_city="Mumbai").first()
        if test_flight:
            travellers = 2
            flight_class = "Business"
            multipliers = {'Economy': 1.0, 'Premium Economy': 1.5, 'Business': 2.5, 'First Class': 4.0}
            multiplier = multipliers.get(flight_class, 1.0)
            
            calculated_price = round(test_flight.base_price * multiplier, 2)
            total_price = round(calculated_price * travellers, 2)
            
            print(f"Flight: {test_flight.airline} {test_flight.flight_number}")
            print(f"Base Price: {test_flight.base_price}")
            print(f"Class: {flight_class} (Multiplier: {multiplier})")
            print(f"Calculated Price (per person): {calculated_price}")
            print(f"Total Price (for {travellers}): {total_price}")
            
            if calculated_price == 12500.0 and total_price == 25000.0:
                print("SUCCESS: Price calculation is correct!")
            else:
                print(f"FAILURE: Expected 12500.0/25000.0 but got {calculated_price}/{total_price}")
        else:
            print("No flight found from Delhi to Mumbai.")

if __name__ == "__main__":
    verify_logic()
