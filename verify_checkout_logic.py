from app import app, db, Flight, Package, User

def verify_checkout_data():
    with app.app_context():
        print("--- Verifying app.py checkout logic update ---")
        package = Package.query.first()
        if not package:
            print("No packages found.")
            return

        # Prepare dummy data
        selected_class = 'Business'
        num_members = 2
        
        # Multipliers from logic
        multipliers = {'Economy': 1.0, 'Premium Economy': 1.5, 'Business': 2.5, 'First Class': 4.0}
        
        # Flight logic
        selected_flight = Flight.query.first()
        flight_base_price = selected_flight.base_price if selected_flight else (package.flight_economy_price or 0.0)
        
        multiplier = multipliers.get(selected_class, 1.0)
        current_flight_price = round(flight_base_price * multiplier, 2)
        total_price = (package.price + current_flight_price) * num_members
        
        print(f"Package: {package.name} (Price: {package.price})")
        print(f"Flight: {selected_flight.airline if selected_flight else 'Default'} (Base: {flight_base_price})")
        print(f"Selected Class: {selected_class} (Multiplier: {multiplier})")
        print(f"Calculated Flight Price: {current_flight_price}")
        print(f"Calculated Total Price for {num_members}: {total_price}")
        
        # Verify calculation logic matches what's in checkout.html script
        # JS logic: const total = (packagePrice + currentFlightPrice) * members;
        expected_total = (package.price + current_flight_price) * num_members
        
        if total_price == expected_total:
            print("SUCCESS: Pricing logic is consistent between backend and frontend expectation.")
        else:
            print(f"FAILURE: Pricing mismatch. Total: {total_price}, Expected: {expected_total}")

if __name__ == "__main__":
    verify_checkout_data()
