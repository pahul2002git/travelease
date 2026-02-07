from app import app, db, Package

def seed_packages():
    with app.app_context():
        # Clear existing packages to avoid duplicates if re-running (optional, but good for clean state)
        # Uncomment the next line if you want to wipe old packages:
        # Clear existing packages for a clean state with new fields
        Package.query.delete()
        
        new_packages = [
            Package(
                name="Tokyo Tech & Tradition",
                description="Discover the seamless blend of ultramodern technology and ancient tradition in Tokyo. Perfect for urban explorers and history buffs alike.",
                price=238000.00,
                duration="8 Days / 7 Nights",
                image_url="https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=800",
                hotel_details="🏨 5-Star Park Hyatt Tokyo: Luxury hotel featured in 'Lost in Translation'. | Includes 24/7 concierge & Club on the Park Spa access. | Gourmet breakfast at Girandole included daily. | Floor-to-ceiling Shinjuku sky views in every room.",
                flight_details="✈️ ANA All Nippon Airways: Executive Class Travel. | Direct flight from Mumbai/Delhi (11h 30m). | 30kg check-in baggage + 10kg hand luggage. | Includes 5-course Japanese kaisaki meal & priority boarding.",
                sightseeing="⛩️ Full Day History Tour: Guided visit to Senso-ji Temple & Meiji Jingu. | 🏙️ Tech Night: Akihabara neon tour & Shinjuku Robot Show. | 🗻 Mt. Fuji Day Trip: Luxury coach tour to Lake Kawaguchi with lunch. | 🍣 Tsukiji Workshop: Morning sushi making with a master chef.",
                popular_places="Shibuya Crossing | Akihabara Electric Town | Meiji Jingu Shrine | teamLab Planets | Tsukiji Outer Market",
                flight_economy_price=15000.0,
                flight_premium_economy_price=35000.0,
                flight_business_price=85000.0,
                flight_first_class_price=150000.0
            ),
            Package(
                name="Safari in Serengeti",
                description="Embark on the adventure of a lifetime in the heart of Tanzania's Serengeti National Park. Witness the Great Migration and the Big Five.",
                price=357000.00,
                duration="7 Days / 6 Nights",
                image_url="https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=800",
                hotel_details="🏨 Four Seasons Safari Lodge: Luxury suite with private watering hole view. | All-inclusive fine dining & sunset deck cocktails. | Infinity pool overlooking savannah with visiting elephants. | Luxury spa treatments featuring local botanicals.",
                flight_details="✈️ Ethiopian Airlines: Cloud Nine Business Class experience. | 1 Stop via Addis Ababa with airport lounge access. | 2x 23kg baggage allowance + priority handling. | Multi-cuisine in-flight catering & lie-flat seating.",
                sightseeing="🦁 Great Migration Drive: 4x4 game drives with expert Masai trackers. | 🎈 Hot Air Balloon Safari: Sunrise flight with champagne bush breakfast. | 🌍 Olduvai Gorge: Private tour of the 'Cradle of Mankind'. | 🌅 Sunset Bush Dinner: Traditional Masai dance & feast under the stars.",
                popular_places="Seronera Valley | Ngorongoro Crater | Olduvai Gorge | Masai Village | Grumeti River",
                flight_economy_price=20000.0,
                flight_premium_economy_price=45000.0,
                flight_business_price=110000.0,
                flight_first_class_price=190000.0
            ),
            Package(
                name="Parisian Romance",
                description="Fall in love with the City of Light. A curated experience for couples seeking the ultimate blend of romance, art, and French gastronomy.",
                price=263500.00,
                duration="6 Days / 5 Nights",
                image_url="https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=800",
                hotel_details="🏨 Hôtel Plaza Athénée: Iconic 'Red Awning' luxury on Avenue Montaigne. | Stay in a Prestige Room with direct Eiffel Tower views. | Daily champagne breakfast at Alain Ducasse included. | Dior Institut Spa sessions for two.",
                flight_details="✈️ Air France: Business Class 'The Private Cabin'. | Direct flight with full lie-flat bed comfort. | 2x 32kg baggage + SkyPriority boarding. | Menu designed by Michelin-starred chefs & premium wines.",
                sightseeing="🥂 Seine River Cruise: Sunset private yacht dinner with live violin. | 🎨 Artistic Paris: VIP skip-the-line tour of Louvre & Musee d'Orsay. | 🏰 Versailles: Private tour of the Royal Apartments & Gardens. | 🥖 Macaron Class: Exclusive workshop at Ladurée Paris.",
                popular_places="Eiffel Tower | Montmartre | Palace of Versailles | Notre-Dame | Champs-Élysées",
                flight_economy_price=18000.0,
                flight_premium_economy_price=38000.0,
                flight_business_price=95000.0,
                flight_first_class_price=170000.0
            ),
            Package(
                name="New York City Lights",
                description="Experience the electric energy of the Big Apple. From Broadway's dazzling lights to the serene paths of Central Park.",
                price=204000.00,
                duration="5 Days / 4 Nights",
                image_url="https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=800",
                hotel_details="🏨 The Ritz-Carlton Central Park: Unrivaled location with park-view suites. | Access to the exclusive Club Lounge with culinary presentations. | La Prairie Spa treatments & nightly turndown service. | Traditional afternoon tea for two at the Star Lounge.",
                flight_details="✈️ Delta Airlines: One Delta Business Elite suites. | Direct flight with personalized pillows & Westin Heavenly bedding. | 2x 23kg baggage + Delta Sky Club lounge access. | In-flight WiFi, TUMI amenity kits & curated chef-crafted meals.",
                sightseeing="🎭 Broadway Night: Premium orchestra seats for a top-rated show. | 🚁 Helicopter Tour: 15-minute 'Ultimate Manhattan' flight. | 🗽 Statue of Liberty: VIP ferry access & pedestal entry. | 🍽️ Michelin Dining: 3-course dinner at a top Manhattan restaurant.",
                popular_places="Times Square | Central Park | Empire State Building | 9/11 Memorial | The High Line",
                flight_economy_price=25000.0,
                flight_premium_economy_price=55000.0,
                flight_business_price=130000.0,
                flight_first_class_price=220000.0
            ),
            Package(
                name="Santorini Sunset Bliss",
                description="Relax on the breathtaking cliffs of Santorini. Famous for its blue-domed churches, volcanic beaches, and world-class sunsets.",
                price=306000.00,
                duration="6 Days / 5 Nights",
                image_url="https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?auto=format&fit=crop&w=800",
                hotel_details="🏨 Canaves Oia Luxury Suites: Cave suite with private infinity plunge pool. | Daily Greek gourmet breakfast served on your private balcony. | Sunset wine tasting session with an expert sommelier. | Luxury round-trip airport & port transfers included.",
                flight_details="✈️ Aegean Airlines: Business Class seating from Athens. | Priority baggage handling & lounge access in Athens/Santorini. | High-speed ferry business class tickets (Athens to Oia). | Complimentary Greek snacks & premium beverages onboard.",
                sightseeing="⛵ Private Catamaran: Caldera cruise with cliffside snorkeling & BBQ. | 🍷 Volcanic Vineyards: Private tour of 3 ancient wineries. | 🚶 Oia Heritage: Guided sunset walking tour of the village. | 📸 Professional Shoot: 1-hour vacation photo session in Oia.",
                popular_places="Oia Village | Red Beach | Akrotiri Ruins | Amoudi Bay | Fira Town",
                flight_economy_price=12000.0,
                flight_premium_economy_price=28000.0,
                flight_business_price=70000.0,
                flight_first_class_price=125000.0
            ),
            Package(
                name="Royal Jaipur",
                description="Experience the majesty of the Pink City. Live like a Maharaja in heritage palaces and explore centuries-old Rajput history.",
                price=153000.00,
                duration="5 Days / 4 Nights",
                image_url="https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800",
                hotel_details="🏨 Rambagh Palace: Known as the 'Jewel of Jaipur'. | Stay in a Royal Suite within the former Maharajas residence. | Ceremonial welcome with traditional lamps & heritage walk. | Peacock garden dining experience with live folk music.",
                flight_details="✈️ IndiGo: 6E Prime service with extra legroom & priority check-in. | Direct flight from major Indian metros (Mumbai/Delhi/Bangalore). | 25kg check-in baggage + 7kg hand luggage. | Gourmet food box & beverages included during flight.",
                sightseeing="🏰 Fort & Palaces: Elephant or Jeep ride to Amer Fort summit. | 🛍️ Artisan Shopping: Private guided walk through Johari Bazaar. | 🔭 Astronomy Tour: Guided visit to Jantar Mantar observatory. | 🍲 Chokhi Dhani: Traditional Rajasthani cultural evening & dinner.",
                popular_places="Hawa Mahal | Amer Fort | City Palace | Nahargarh Fort | Jal Mahal",
                flight_economy_price=4500.0,
                flight_premium_economy_price=8500.0,
                flight_business_price=18000.0,
                flight_first_class_price=35000.0
            ),
            Package(
                name="Magical Manali",
                description="Snow-capped Himalayan peaks, lush cedar forests, and the sparkling Beas River. The ultimate mountain getaway for soul-seekers.",
                price=127500.00,
                duration="5 Days / 4 Nights",
                image_url="https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?q=80&w=2000&auto=format&fit=crop",
                hotel_details="🏨 Span Resort and Spa: 12-acre riverside park property. | Premium cottage with private fireplace & snow-peak views. | Riverside morning yoga & meditation sessions included. | Luxury L’Occitane spa credits & mountain herb high tea.",
                flight_details="✈️ Vistara: Club Vistara Premium Economy experience. | 1 Stop via Chandigarh with priority check-in & boarding. | 20kg baggage + priority handling for sports gear. | Luxury 4x4 SUV transfers from airport to Manali resort.",
                sightseeing="⛷️ Rohtang Pass: Full day snow point excursion with activities. | 🪂 Solang Adventure: Paragliding, zorbing & quad biking sessions. | 🕍 Old Manali Walk: Guided Hadimba Temple & river trail tour. | 🍎 Orchard Picnic: Lunch at a private apple orchard with local cider.",
                popular_places="Solang Valley | Rohtang Pass | Mall Road | Vashisht Springs | Jogini Falls",
                flight_economy_price=5500.0,
                flight_premium_economy_price=10500.0,
                flight_business_price=22000.0,
                flight_first_class_price=42000.0
            ),
            Package(
                name="Australian Adventure",
                description="From the iconic Sydney Opera House to the vibrant Great Barrier Reef. A diverse journey across the Land Down Under.",
                price=382500.00,
                duration="10 Days / 9 Nights",
                image_url="https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?q=80&w=2000&auto=format&fit=crop",
                hotel_details="🏨 5-Star Double Stay: Sydney Harbour & Port Douglas Beachfront. | Opera House view suites & private garden villas. | Inter-city luxury flights & private chauffeur transfers. | All-inclusive breakfasts & premium cocktail hours.",
                flight_details="✈️ Qantas: Spirit of Australia Business Class experience. | 14-hour premium flight with Neil Perry signature dining. | 2x 32kg baggage + dedicated premium check-in lane. | In-flight lie-flat beds & luxury Sheridan bedding sets.",
                sightseeing="🪸 Great Barrier Reef: Luxury catamaran snorkeling & diving. | 🌉 Sydney Bridge: Private 'BridgeClimb' at sunset. | 🐨 Wildlife Park: VIP koala encounter & kangaroo feeding. | 🛳️ Harbour Cruise: Private sunset yacht dinner for two.",
                popular_places="Sydney Opera House | Great Barrier Reef | Bondi Beach | Twelve Apostles | Blue Mountains",
                flight_economy_price=35000.0,
                flight_premium_economy_price=75000.0,
                flight_business_price=160000.0,
                flight_first_class_price=280000.0
            ),
            Package(
                name="Dubai Skyline & Desert",
                description="Witness the record-breaking architecture and luxurious desert lifestyle. From the tallest building to the smoothest dunes.",
                price=185000.00,
                duration="6 Days / 5 Nights",
                image_url="https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=800",
                hotel_details="🏨 Burj Al Arab Jumeirah: The world's only 7-star luxury stay. | 24-hour private butler service & Hermès bath amenities. | Unlimited access to Wild Wadi & private beach club. | Gold-plated elevator access & marina-view suites.",
                flight_details="✈️ Emirates: Fly the flagship A380 in Business Class. | Direct flight with onboard lounge & social area access. | 35kg baggage + chauffeur-drive service from your home. | Multi-course gourmet meals served on Royal Doulton bone china.",
                sightseeing="🏢 Burj Khalifa: 'At The Top' SKY entry (148th floor). | 🏎️ Platinum Safari: Luxury dune bashing with private desert camp. | 🚤 Marina Cruise: 2-hour private yacht tour with light snacks. | ⛲ Fountain Show: VIP dinner seating at a Burj-view terrace.",
                popular_places="Burj Khalifa | Palm Jumeirah | Dubai Mall | Gold Souk | Museum of the Future",
                flight_economy_price=11000.0,
                flight_premium_economy_price=25000.0,
                flight_business_price=65000.0,
                flight_first_class_price=115000.0
            ),
            Package(
                name="Mystical Mexico",
                description="Discover the white sand beaches of Tulum, the ancient Mayan wonders of Chichén Itzá, and the vibrant culture of Mexico.",
                price=215000.00,
                duration="7 Days / 6 Nights",
                image_url="https://images.unsplash.com/photo-1512813195386-6cf811ad3542?auto=format&fit=crop&w=800",
                hotel_details="🏨 Azulik Tulum: Architectural masterpiece treehouse suites. | Morning meditation & organic farm-to-table dining included. | Ancient Maya-inspired spa ritual & sound healing. | Eco-luxury beach club access with private cabanas.",
                flight_details="✈️ Aeroméxico: Clase Premier experience with 1 stop. | Full access to Salon Premier lounge at Mexico City airport. | 2x 23kg baggage allowance & priority baggage tag. | Premium Mexican fusion menu served at 35,000 feet.",
                sightseeing="🗿 Chichén Itzá VIP: Early sunrise access to Mayan ruins. | 🏊 Cenote Private: Swimming at Ik Kil before the crowds. | 🐢 Akumal Snorkel: Swim with giant sea turtles in the wild. | 🌮 Culinary Tour: Private tequila tasting & street food walk.",
                popular_places="Tulum Beach | Chichén Itzá | Cozumel Island | Playa del Carmen | Xcaret Park",
                flight_economy_price=22000.0,
                flight_premium_economy_price=48000.0,
                flight_business_price=115000.0,
                flight_first_class_price=200000.0
            ),
            Package(
                name="California Dreamin'",
                description="The ultimate West Coast road trip. From the glam of Hollywood to the tech hubs of Silicon Valley and the majesty of Yosemite.",
                price=289000.00,
                duration="9 Days / 8 Nights",
                image_url="https://images.unsplash.com/photo-1449034446853-66c86144b0ad?auto=format&fit=crop&w=800",
                hotel_details="🏨 Beverly Hills Hotel: Iconic 'Pink Palace' heritage bungalows. | Private patio stay with poolside cabana rental included. | Daily breakfast at the legendary Polo Lounge. | 24-hour personal shopper & stylist service available.",
                flight_details="✈️ United Airlines: Polaris Business Class direct flight. | Saks Fifth Avenue bedding & cooling gel-foam pillows. | 2x 32kg baggage + access to United Polaris luxury lounges. | Personalized in-flight sundae cart & multi-course dining.",
                sightseeing="🎬 Warner Bros: VIP behind-the-scenes studio backlot tour. | 🌉 SF Experience: Private Golden Gate & Alcatraz night tour. | 🌲 Yosemite Trek: Guided hike to Glacier Point summit. | 🍷 Napa Elite: Private vineyard tour & 5-course wine dinner.",
                popular_places="Hollywood Sign | Santa Monica Pier | Golden Gate Bridge | Yosemite Park | Napa Valley",
                flight_economy_price=28000.0,
                flight_premium_economy_price=60000.0,
                flight_business_price=145000.0,
                flight_first_class_price=250000.0
            ),
            Package(
                name="Heavenly Kashmir",
                description="Explore the 'Paradise on Earth'. Serene shikara rides, snow-clad peaks of Gulmarg, and the vibrant Mughal Gardens.",
                price=95000.00,
                duration="6 Days / 5 Nights",
                image_url="/static/images/kashmir.png",
                hotel_details="🏨 The Khyber Himalayan Resort: Gulmarg luxury at 8,825 feet. | Luxury room stay with panoramic Mount Affarwat views. | Heated indoor pool access & Himalayan herbal tea service. | Private butler for organizing ski gear & trek planning.",
                flight_details="✈️ Air India: Maharaja Business Class comfort seating. | Direct flight or 1 stop with priority check-in/lounge. | 35kg baggage + special handling for ski/golf equipment. | Authentic Wazwan Kashmiri cuisine served during flight.",
                sightseeing="🛶 Dal Lake: Exclusive sunset shikara ride with local snacks. | 🚠 Gondola VIP: Phase 1 & 2 tickets with skip-the-line access. | 🌷 Mughal Gardens: Private guided tour of Shalimar & Nishat. | 🧶 Artisan Walk: Visit to master weavers for Pashmina shawls.",
                popular_places="Dal Lake | Gulmarg Gondola | Betaab Valley | Sonamarg | Shankaracharya Temple",
                flight_economy_price=3500.0,
                flight_premium_economy_price=7500.0,
                flight_business_price=15000.0,
                flight_first_class_price=28000.0
            )
        ]
        
        for p in new_packages:
            db.session.add(p)
        
        db.session.commit()
        print(f"Successfully re-seeded {len(new_packages)} packages with flight pricing!")

def seed_flights():
    from models import Flight
    with app.app_context():
        # Clear existing flights
        Flight.query.delete()

        new_flights = [
            Flight(airline="AirAsia", flight_number="AA101", departure_city="Delhi", arrival_city="Mumbai", departure_time="08:00 AM", base_price=4500.0),
            Flight(airline="Etihad Airways", flight_number="EY202", departure_city="Delhi", arrival_city="Dubai", departure_time="10:30 AM", base_price=12000.0),
            Flight(airline="Emirates", flight_number="EK303", departure_city="Mumbai", arrival_city="Dubai", departure_time="02:00 PM", base_price=13500.0),
            Flight(airline="Vistara", flight_number="UK404", departure_city="Delhi", arrival_city="Manali", departure_time="06:00 AM", base_price=5500.0),
            Flight(airline="IndiGo", flight_number="6E505", departure_city="Mumbai", arrival_city="Jaipur", departure_time="09:15 AM", base_price=4800.0),
            Flight(airline="Air India", flight_number="AI606", departure_city="Delhi", arrival_city="Kashmir", departure_time="07:45 AM", base_price=6000.0),
            Flight(airline="Qantas", flight_number="QF707", departure_city="Delhi", arrival_city="Sydney", departure_time="11:30 PM", base_price=45000.0),
            Flight(airline="Air France", flight_number="AF808", departure_city="Mumbai", arrival_city="Paris", departure_time="12:15 AM", base_price=38000.0)
        ]

        for f in new_flights:
            db.session.add(f)
        
        db.session.commit()
        print(f"Successfully seeded {len(new_flights)} flight options!")

if __name__ == '__main__':
    seed_packages()
    seed_flights()
