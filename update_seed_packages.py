import re

itineraries = {
    "Tokyo Tech & Tradition": "Day 1 - Arrival in Tokyo, airport transfer to Shinjuku hotel, evening free to explore Kabukicho | Day 2 - Full Day History Tour: Senso-ji Temple, Nakamise shopping street, and Meiji Jingu Shrine | Day 3 - Tokyo Skyline & Tech: Tokyo Skytree, Akihabara electronics district, and Shinjuku Robot Show | Day 4 - Mt. Fuji Day Trip: Luxury coach tour to Lake Kawaguchi and Mount Fuji 5th station | Day 5 - Traditional Experiences: Morning sushi making workshop at Tsukiji Outer Market | Day 6 - Shibuya & Harajuku: Shibuya Crossing, Harajuku fashion streets, and Omotesando | Day 7 - Modern Art & Bay Area: teamLab Planets, Odaiba waterfront, and farewell dinner | Day 8 - Morning at leisure, hotel check-out and departure from Narita/Haneda",
    
    "Safari in Serengeti": "Day 1 - Arrival at Kilimanjaro Airport, transfer to Arusha, briefing and evening relaxation | Day 2 - Flight to Serengeti National Park, transfer to luxury lodge, afternoon game drive | Day 3 - Great Migration Drive: Full day 4x4 game drive with expert Masai trackers in Seronera Valley | Day 4 - Hot Air Balloon Safari at sunrise with champagne breakfast, afternoon Grumeti River visit | Day 5 - Drive to Ngorongoro Conservation Area, visit to Olduvai Gorge 'Cradle of Mankind' | Day 6 - Ngorongoro Crater descent for a full day game drive, sunset Masai dance and feast | Day 7 - Morning breakfast, transfer to airstrip for flight back to Kilimanjaro and departure",
    
    "Parisian Romance": "Day 1 - Arrival in Paris, luxury transfer to hotel, evening Seine River Cruise with dinner | Day 2 - Iconic Paris: VIP skip-the-line tour of Louvre and Eiffel Tower visit | Day 3 - Artistic Paris: Musee d'Orsay, Montmartre walking tour, and Sacre-Coeur | Day 4 - Palace of Versailles: Private tour of the Royal Apartments and Gardens | Day 5 - Gastronomy & Shopping: Macaron making class at Laduree, Champs-Elysees shopping | Day 6 - Morning cafe breakfast, hotel check-out and departure",
    
    "New York City Lights": "Day 1 - Arrival in NYC, private transfer to Manhattan hotel, Times Square evening walk | Day 2 - Classic NY: Statue of Liberty VIP ferry, 9/11 Memorial, and Wall Street | Day 3 - Central Park and Museums: MET or MoMA visit, afternoon stroll in Central Park | Day 4 - Skyline & Shows: Helicopter tour of Manhattan, evening Broadway Show with orchestra seats | Day 5 - The High Line walk, last-minute shopping at 5th Avenue, and departure",
    
    "Santorini Sunset Bliss": "Day 1 - Arrival in Santorini, transfer to Oia cave suite, evening sunset viewing | Day 2 - Caldera Cruise: Private catamaran tour with cliffside snorkeling and BBQ | Day 3 - Village Exploration: Guided sunset walking tour of Oia and Fira Town | Day 4 - Volcanic Vineyards: Private tour and tasting at 3 ancient wineries | Day 5 - Beach Day: Visit to Red Beach and Akrotiri Ruins, 1-hour professional photo session | Day 6 - Gourmet Greek breakfast, luxury transfer to airport/port and departure",
    
    "Royal Jaipur": "Day 1 - Arrival in Jaipur, traditional welcome at Rambagh Palace, evening leisure | Day 2 - Forts of Jaipur: Amer Fort summit ride, visit to Jaigarh and Nahargarh Forts | Day 3 - Heritage Walk: City Palace, Hawa Mahal, and Jantar Mantar observatory | Day 4 - Culture & Shopping: Johari Bazaar artisan walk, evening at Chokhi Dhani for Rajasthani dinner | Day 5 - Morning peacock garden breakfast, hotel check-out and departure",
    
    "Magical Manali": "Day 1 - Arrival in Kullu-Manali, 4x4 transfer to riverside resort, evening acclimatization | Day 2 - Snow Excursion: Full day trip to Rohtang Pass or Solang Valley for snow activities | Day 3 - Adventure Day: Paragliding, zorbing, and quad biking in Solang Valley | Day 4 - Old Manali & Culture: Hadimba Temple, Vashisht Springs, and lunch at an apple orchard | Day 5 - Morning riverside yoga, check-out and departure",
    
    "Australian Adventure": "Day 1 - Arrival in Sydney, transfer to Harbour view hotel, evening at leisure | Day 2 - Sydney Highlights: Sydney Opera House tour and Bondi Beach visit | Day 3 - Adventure: Private BridgeClimb at Sydney Harbour Bridge at sunset | Day 4 - Wildlife & Nature: Blue Mountains day trip and VIP koala encounter | Day 5 - Flight to Cairns, transfer to Port Douglas beachfront villa | Day 6 - Great Barrier Reef: Luxury catamaran snorkeling and diving excursion | Day 7 - Daintree Rainforest: Guided walk and Aboriginal cultural experience | Day 8 - Leisure Day: Relax by the beach or explore Port Douglas town | Day 9 - Farewell dinner: Private sunset yacht cruise | Day 10 - Hotel check-out, transfer to Cairns airport and departure",
    
    "Dubai Skyline & Desert": "Day 1 - Arrival in Dubai, chauffeur transfer to Burj Al Arab, evening Marina Cruise | Day 2 - Modern Dubai: Burj Khalifa 'At The Top' SKY entry, Dubai Mall, and Fountain Show | Day 3 - Platinum Desert Safari: Luxury dune bashing, private camp, and traditional dinner | Day 4 - Cultural Dubai: Gold Souk, Spice Souk, and Museum of the Future | Day 5 - Leisure & Waterpark: Wild Wadi access or Palm Jumeirah beach relaxation | Day 6 - Luxury hotel breakfast, chauffeur transfer to airport and departure",
    
    "Mystical Mexico": "Day 1 - Arrival in Cancun, transfer to eco-luxury resort in Tulum, evening beach walk | Day 2 - Mayan Ruins: Early sunrise VIP access to Chichen Itza and Ik Kil Cenote | Day 3 - Tulum & Coba: Explore beachfront ruins and cycle through jungle to Coba pyramids | Day 4 - Marine Life: Snorkel with giant sea turtles in Akumal Bay | Day 5 - Eco-Park Adventure: Full day at Xcaret Park with evening spectacular show | Day 6 - Culinary & Wellness: Ancient Maya spa ritual and private tequila tasting | Day 7 - Morning beach meditation, check-out and departure",
    
    "California Dreamin'": "Day 1 - Arrival in Los Angeles, transfer to Beverly Hills Hotel, evening at Sunset Boulevard | Day 2 - Hollywood Magic: Warner Bros studio backlot tour and Hollywood Walk of Fame | Day 3 - Coastal Drive: Santa Monica Pier to Malibu, evening leisure | Day 4 - Flight or drive to San Francisco, private Golden Gate and Alcatraz night tour | Day 5 - Tech & Wine: Silicon Valley highlights and afternoon transfer to Napa Valley | Day 6 - Napa Elite: Private vineyard tour and 5-course wine pairing dinner | Day 7 - Drive to Yosemite National Park, check-in to lodge, afternoon valley floor tour | Day 8 - Yosemite Trek: Guided hike to Glacier Point summit for panoramic views | Day 9 - Morning nature walk, drive back to SFO and departure",
    
    "Heavenly Kashmir": "Day 1 - Arrival in Srinagar, transfer to luxury houseboat, sunset Dal Lake shikara ride | Day 2 - Mughal Gardens: Private tour of Shalimar, Nishat, and Shankaracharya Temple | Day 3 - Drive to Gulmarg, check-in to Himalayan Resort, afternoon acclimatization | Day 4 - Gondola Adventure: Phase 1 & 2 tickets with skip-the-line access to Mt. Affarwat | Day 5 - Day trip to Pahalgam (Betaab Valley) or Sonamarg, visit to artisan weavers | Day 6 - Authentic Wazwan breakfast, transfer to Srinagar airport and departure",
    
    "Magical Istanbul": "Day 1 - Arrival in Istanbul, airport pickup, hotel check-in, evening free | Day 2 - Hagia Sophia, Blue Mosque, Hippodrome, Grand Bazaar | Day 3 - Bosphorus Cruise, Dolmabahçe Palace, Spice Bazaar | Day 4 - Topkapi Palace, Suleymaniye Mosque, Turkish cultural show | Day 5 - Free day for shopping or optional Princes' Islands tour | Day 6 - Hotel check-out and departure"
}

with open('seed_packages.py', 'r', encoding='utf-8') as f:
    content = f.read()

for name, itinerary in itineraries.items():
    # Find the block for this package
    # Look for name="Package Name",
    pattern = rf'(name="{name}",.*?popular_places=".*?",)'
    replacement = rf'\1\n                itinerary="{itinerary}",'
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('seed_packages.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated seed_packages.py")
