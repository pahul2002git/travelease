"""
Quick migration script to populate existing packages with sample itinerary and amenities data.
Run this once after adding the new fields to the database.
"""

from app import app, db
from models import Package

# Sample data templates for different package types
SAMPLE_DATA = {
    'Bali': {
        'itinerary': 'Day 1 - Arrival in Bali, check-in at luxury resort, evening beach walk | Day 2 - Ubud cultural tour, rice terrace visit, traditional dance show | Day 3 - Water sports and beach activities at Nusa Dua | Day 4 - Temple hopping: Tanah Lot and Uluwatu sunset | Day 5 - Leisure day, spa treatments, farewell dinner',
        'hotel_amenities': 'Infinity Pool with Ocean View | 24/7 Concierge Service | Full-Service Spa & Wellness Center | Complimentary Yoga Classes | Private Beach Access | Free High-Speed WiFi | Fine Dining Restaurant | Airport Shuttle Service'
    },
    'Paris': {
        'itinerary': 'Day 1 - Arrival in Paris, Seine River cruise, welcome dinner | Day 2 - Eiffel Tower visit, Champs-Élysées shopping, Louvre Museum | Day 3 - Versailles Palace day trip, gardens tour | Day 4 - Montmartre exploration, Sacré-Cœur visit, French cuisine cooking class | Day 5 - Free day for shopping, departure',
        'hotel_amenities': 'Rooftop Terrace with Eiffel Tower View | Continental Breakfast Buffet | Fitness Center | Business Center | Multi-lingual Staff | In-room Safe | Minibar | Laundry & Dry Cleaning Service'
    },
    'Dubai': {
        'itinerary': 'Day 1 - Arrival, check-in at 5-star hotel, Dubai Marina evening walk | Day 2 - Burj Khalifa visit, Dubai Mall shopping, fountain show | Day 3 - Desert safari with BBQ dinner and cultural show | Day 4 - Palm Jumeirah, Atlantis Aquaventure, beach relaxation | Day 5 - Gold Souk visit, departure',
        'hotel_amenities': 'Temperature-Controlled Swimming Pool | Kids Club & Play Area | Multiple Restaurants & Bars | Valet Parking | Executive Lounge Access | Spa with Sauna & Steam Room | 24-Hour Room Service | Premium Bedding'
    },
    'Tokyo': {
        'itinerary': 'Day 1 - Arrival in Tokyo, Shibuya Crossing, Robot Restaurant dinner | Day 2 - Mount Fuji day trip, traditional tea ceremony | Day 3 - Asakusa Temple, Tokyo Skytree, Akihabara electronics district | Day 4 - Harajuku fashion streets, Meiji Shrine, Tsukiji Fish Market | Day 5 - Last-minute shopping, departure',
        'hotel_amenities': 'Traditional Japanese Bath (Onsen) | Complimentary Green Tea Service | Tatami Room Option | English-Speaking Staff | Currency Exchange | Luggage Storage | Meeting Rooms | USB Charging Ports'
    },
    'default': {
        'itinerary': 'Day 1 - Arrival and hotel check-in, orientation tour, welcome dinner | Day 2 - Full-day sightseeing tour of major attractions | Day 3 - Cultural experience and local market visit | Day 4 - Leisure day with optional activities, spa time | Day 5 - Final shopping, check-out, departure',
        'hotel_amenities': 'Swimming Pool | Fitness Center | Free WiFi | Restaurant & Bar | Room Service | Laundry Service | Tour Desk | Complimentary Breakfast'
    }
}

def get_sample_data(package_name):
    """Get sample data based on package name"""
    for key in SAMPLE_DATA.keys():
        if key.lower() in package_name.lower():
            return SAMPLE_DATA[key]
    return SAMPLE_DATA['default']

def populate_packages():
    """Update all existing packages with sample itinerary and amenities"""
    with app.app_context():
        packages = Package.query.all()
        count = 0
        
        for package in packages:
            # Only update if fields are empty
            if not package.itinerary or not package.hotel_amenities:
                sample = get_sample_data(package.name)
                
                if not package.itinerary:
                    package.itinerary = sample['itinerary']
                
                if not package.hotel_amenities:
                    package.hotel_amenities = sample['hotel_amenities']
                
                count += 1
        
        try:
            db.session.commit()
            print(f"✅ Successfully updated {count} packages with sample data!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    populate_packages()
