import os
import json
import re
import random
from difflib import SequenceMatcher
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from config import Config
from models import db, User, Package, Booking, Contact, Flight, FlightBooking, Review, Wishlist, Train, TrainBooking, Bus, BusBooking, Cab, CabBooking
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)


def _runtime_sqlite_url():
    instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    db_path = os.path.join(instance_dir, 'holiday_booking.db')
    return f"sqlite:///{db_path.replace(os.sep, '/')}"


def _configure_database(flask_app):
    try:
        db.init_app(flask_app)
    except ModuleNotFoundError as exc:
        if exc.name != 'pymysql':
            raise
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = _runtime_sqlite_url()
        flask_app.config['DATABASE_FALLBACK_REASON'] = 'PyMySQL dependency is not installed.'
        db.init_app(flask_app)


def _initialize_database(flask_app):
    with flask_app.app_context():
        try:
            db.create_all()
        except Exception as exc:
            flask_app.logger.error("Database initialization skipped: %s", exc)


_configure_database(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

SPIN_WHEEL_OFFERS = [
    {"id": "offer_5", "label": "5% OFF", "discount": 5, "weight": 24},
    {"id": "offer_10", "label": "10% OFF", "discount": 10, "weight": 20},
    {"id": "offer_0_a", "label": "Try Again", "discount": 0, "weight": 18},
    {"id": "offer_12", "label": "12% OFF", "discount": 12, "weight": 14},
    {"id": "offer_7", "label": "7% OFF", "discount": 7, "weight": 10},
    {"id": "offer_20", "label": "20% OFF", "discount": 20, "weight": 6},
    {"id": "offer_0_b", "label": "No Offer", "discount": 0, "weight": 5},
    {"id": "offer_15", "label": "15% OFF", "discount": 15, "weight": 3},
]


def _today_iso():
    return datetime.now().strftime('%Y-%m-%d')


def _pick_weighted_spin_offer():
    total_weight = sum(item['weight'] for item in SPIN_WHEEL_OFFERS)
    roll = random.uniform(0, total_weight)
    upto = 0.0
    for item in SPIN_WHEEL_OFFERS:
        upto += item['weight']
        if roll <= upto:
            return item
    return SPIN_WHEEL_OFFERS[-1]


def _get_active_spin_offer():
    offer = session.get('spin_wheel_offer')
    if not offer:
        return None
    if offer.get('spin_date') != _today_iso():
        session.pop('spin_wheel_offer', None)
        session.modified = True
        return None
    return offer

fallback_reason = app.config.get('DATABASE_FALLBACK_REASON')
if fallback_reason:
    app.logger.warning("Using SQLite fallback database. Reason: %s", fallback_reason)

_initialize_database(app)

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

# Removed seed_transport_data function as it's now handled in setup_db.py

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

def transport_image_url(kind, item_id, title):
    """Return a local real-photo image matched to title/operator first, then fallback."""
    image_sets = {
        "cab": [
            "images/transport/cabs/cab1.jpg",
            "images/transport/cabs/cab2.jpg",
            "images/transport/cabs/cab3.jpg",
            "images/transport/cabs/cab4.jpg",
            "images/transport/cabs/cab5.jpg",
        ],
        "bus": [
            "images/transport/buses/bus1.jpg",
            "images/transport/buses/bus2.jpg",
            "images/transport/buses/bus3.jpg",
            "images/transport/buses/bus4.jpg",
            "images/transport/buses/bus5.jpg",
        ],
        "train": [
            "images/transport/trains/operators/vande_bharat.jpg",
            "images/transport/trains/operators/rajdhani_express.jpg",
            "images/transport/trains/operators/duronto_express.jpg",
            "images/transport/trains/operators/shatabdi_express.jpg",
            "images/transport/trains/train_try_3.jpg",
        ],
    }

    title_key = (title or "").strip().lower()
    image_by_title = {
        "cab": {
            "travelease cabs": "images/transport/cabs/cab1.jpg",
            "citylux": "images/transport/cabs/cab2.jpg",
            "rapidgo": "images/transport/cabs/cab3.jpg",
        },
        "bus": {
            "redbus prime": "images/transport/buses/bus1.jpg",
            "volvo express": "images/transport/buses/bus2.jpg",
            "intercity": "images/transport/buses/bus3.jpg",
            "night rider": "images/transport/buses/bus4.jpg",
        },
        "train": {
            "vande bharat": "images/transport/trains/operators/vande_bharat.jpg",
            "rajdhani express": "images/transport/trains/operators/rajdhani_express.jpg",
            "duronto": "images/transport/trains/operators/duronto_express.jpg",
            "shatabdi": "images/transport/trains/operators/shatabdi_express.jpg",
        },
    }

    matched = image_by_title.get(kind, {}).get(title_key)
    if matched:
        return url_for("static", filename=matched)

    images = image_sets.get(kind, image_sets["cab"])
    return url_for("static", filename=images[item_id % len(images)])

def _fallback_chat_reply(user_message):
    text = user_message.lower()

    if any(word in text for word in ["book", "booking", "reserve"]):
        return (
            "Here's how to complete your booking on TravelEase:\n"
            "- Browse packages on the **Home** page\n"
            "- Click on a package to view details\n"
            "- Hit **Book Now**, choose travellers & class\n"
            "- Complete payment (card or UPI)\n\n"
            "You'll need to be logged in to proceed. Need help finding a specific destination?"
        )
    if any(word in text for word in ["price", "cost", "budget", "cheap", "expensive"]):
        return (
            "Our packages are priced to suit every budget! 💰\n"
            "- Use the **Home** page to browse and compare packages\n"
            "- Transport fares vary by class (Economy / Premium / Business)\n"
            "- More travellers = better per-person value\n\n"
            "Try asking: *'packages under INR 20,000'* or *'cheapest holiday deals'*"
        )
    if any(word in text for word in ["flight", "train", "bus", "cab", "transport"]):
        return (
            "We offer multiple transport options from the top menu:\n"
            "- **Flights** — domestic routes at competitive fares\n"
            "- **Trains** — Rajdhani, Vande Bharat, Shatabdi & more\n"
            "- **Buses** — Volvo, sleeper, and semi-sleeper options\n"
            "- **Cabs** — city rides and outstation transfers\n\n"
            "Just pick your route, date, class, and number of travellers!"
        )
    if any(word in text for word in ["contact", "support", "help", "agent"]):
        return (
            "Our support team is here for you! \ud83d\ude4c\n"
            "- Visit the **Contact** page and fill in your query\n"
            "- Share your booking ID for faster assistance\n"
            "- We typically respond within 24 hours\n\n"
            "Is there anything specific I can help clarify right now?"
        )
    if any(word in text for word in ["cancel", "change", "edit", "modify"]):
        return (
            "To manage an existing booking:\n"
            "- Go to **My Bookings** from the top navigation\n"
            "- Select the booking you'd like to modify\n"
            "- For cancellations, please contact us via the **Contact** page\n\n"
            "Our support team can assist with any changes or refund queries."
        )
    if any(word in text for word in ["hi", "hello", "hey", "greetings", "good"]):
        return (
            "Hello there! \ud83d\udc4b Welcome to TravelEase!\n\n"
            "I'm your personal travel assistant. I can help you:\n"
            "- Discover the perfect holiday package\n"
            "- Compare transport options and fares\n"
            "- Guide you through the booking process\n\n"
            "What destination are you dreaming of?"
        )

    return (
        "I'm here to make your travel planning effortless! \u2708\ufe0f\n\n"
        "Here are some things you can ask me:\n"
        "- *Show packages for Goa*\n"
        "- *Packages under INR 15,000*\n"
        "- *How do I book for 3 travellers?*\n"
        "- *Cheapest train options*\n\n"
        "What would you like to explore?"
    )

def _extract_budget(user_message):
    text = user_message.lower()
    patterns = [
        r"(?:under|below|less than|within|max(?:imum)?)\s*(?:inr|rs\.?)?\s*([0-9]{3,7})",
        r"(?:inr|rs\.?)\s*([0-9]{3,7})"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
    return None

def _format_package_line(pkg):
    discount = f" \u2022 {int(pkg.discount_percentage)}% OFF" if pkg.discount_percentage else ""
    return f"**{pkg.name}** ({pkg.duration}) \u2014 INR {pkg.price:,.0f}{discount}"

def _format_package_detailed(pkg):
    """Enhanced package formatting with more details for AI context"""
    highlights = ""
    if pkg.popular_places:
        places = [p.strip() for p in pkg.popular_places.split('|')[:3]]
        highlights = " | Top spots: " + ", ".join(places)
    discount = f" | {int(pkg.discount_percentage)}% OFF" if pkg.discount_percentage else ""
    return f"- {pkg.name} | {pkg.duration} | INR {pkg.price:,.0f}{discount}{highlights}"

def _fmt_amount(value):
    return f"{value:.0f}" if value is not None else "0"

def _db_chat_reply(user_message):
    text = (user_message or "").strip().lower()
    if not text:
        return None

    package_count = Package.query.count()
    if package_count == 0:
        return (
            "Our package catalogue is being updated right now. \ud83d\udee0\n"
            "Please check back shortly or contact our support team for immediate assistance!"
        )

    # ── Budget-based search ──────────────────────────────────────
    budget = _extract_budget(text)
    if budget is not None:
        budget_matches = (
            Package.query
            .filter(Package.price <= budget)
            .order_by(Package.price.asc())
            .limit(5)
            .all()
        )
        if budget_matches:
            lines = "\n".join(f"- {_format_package_line(pkg)}" for pkg in budget_matches)
            return (
                f"Great news! Found **{len(budget_matches)} package(s)** within INR {budget:,.0f}:\n\n"
                + lines +
                "\n\nClick any package on the Home page to view full details and book!"
            )
        return (
            f"I couldn't find packages within INR {budget:,.0f} at the moment. \ud83d\ude14\n"
            "Try raising your budget slightly — our packages start from very affordable rates!\n"
            "You can also check for **ongoing discounts** on the Home page."
        )

    # ── Cheapest / most affordable ───────────────────────────────
    if any(word in text for word in ["cheap", "lowest", "affordable", "minimum price", "budget"]):
        cheapest = Package.query.order_by(Package.price.asc()).first()
        if cheapest:
            return (
                f"Our most affordable option right now is:\n\n"
                f"- {_format_package_line(cheapest)}\n\n"
                "Head to the Home page to explore more budget-friendly options!"
            )

    # ── Top / featured / recommended ────────────────────────────
    if any(word in text for word in ["best", "top", "recommended", "featured", "popular"]):
        featured = (
            Package.query
            .order_by(Package.is_featured.desc(), Package.discount_percentage.desc(), Package.created_at.desc())
            .limit(3)
            .all()
        )
        if featured:
            lines = "\n".join(f"- {_format_package_line(pkg)}" for pkg in featured)
            return (
                "Here are our **top-rated packages** right now: \u2b50\n\n"
                + lines +
                "\n\nAll include curated itineraries, hotel stays & sightseeing!"
            )

    # ── Destination / keyword search ─────────────────────────────
    if any(word in text for word in ["show", "list", "packages", "package", "destination", "trip", "holiday"]):
        stop_words = {
            "show", "list", "packages", "package", "for", "from", "with", "trip", "trips", "best",
            "top", "cheap", "budget", "under", "price", "cost", "book", "booking", "travel", "go",
            "suggest", "suggestion", "options", "option", "me", "to", "in", "holiday", "destination"
        }
        keywords = [w for w in re.findall(r"[a-zA-Z]{3,}", text) if w not in stop_words]

        for keyword in keywords:
            city_matches = (
                Package.query
                .filter(
                    or_(
                        Package.name.ilike(f"%{keyword}%"),
                        Package.description.ilike(f"%{keyword}%"),
                        Package.popular_places.ilike(f"%{keyword}%")
                    )
                )
                .order_by(Package.price.asc())
                .limit(4)
                .all()
            )
            if city_matches:
                lines = "\n".join(f"- {_format_package_line(pkg)}" for pkg in city_matches)
                return (
                    f"Here are packages matching **'{keyword.title()}'**: \ud83c\udf0d\n\n"
                    + lines +
                    "\n\nClick a package to view the full itinerary, photos & amenities!"
                )

        # Generic: show all
        all_pkgs = Package.query.order_by(Package.price.asc()).limit(6).all()
        lines = "\n".join(f"- {_format_package_line(pkg)}" for pkg in all_pkgs)
        total = Package.query.count()
        suffix = f" (showing 6 of {total} — browse all on the Home page)" if total > 6 else ""
        return (
            f"Here are our available holiday packages{suffix}:\n\n"
            + lines +
            "\n\nWould you like me to filter by destination or budget?"
        )

    # ── Price range query ────────────────────────────────────────
    if any(word in text for word in ["price", "cost", "range"]):
        cheapest = Package.query.order_by(Package.price.asc()).first()
        costliest = Package.query.order_by(Package.price.desc()).first()
        if cheapest and costliest:
            return (
                f"Our packages range from **INR {cheapest.price:,.0f}** to **INR {costliest.price:,.0f}**.\n\n"
                f"- Most affordable: {cheapest.name}\n"
                f"- Premium pick: {costliest.name}\n\n"
                "You can also tell me your budget and I'll find the best matches!"
            )

    # ── Transport pricing ────────────────────────────────────────
    if any(word in text for word in ["flight", "train", "bus", "cab", "transport", "fare"]):
        flight_min = db.session.query(db.func.min(Flight.base_price)).scalar()
        train_min = db.session.query(db.func.min(Train.base_price)).scalar()
        bus_min = db.session.query(db.func.min(Bus.base_price)).scalar()
        cab_min = db.session.query(db.func.min(Cab.base_price)).scalar()
        return (
            "Here are the current **starting fares** for transport: \u2708\ufe0f\n\n"
            f"- **Flights** — from INR {_fmt_amount(flight_min)}\n"
            f"- **Trains** — from INR {_fmt_amount(train_min)}\n"
            f"- **Buses** — from INR {_fmt_amount(bus_min)}\n"
            f"- **Cabs** — from INR {_fmt_amount(cab_min)}\n\n"
            "Actual fare depends on class, route, and number of travellers. Book from the top menu!"
        )

    # ── Booking guidance ─────────────────────────────────────────
    if any(word in text for word in ["book", "booking", "reserve", "how to"]):
        top = Package.query.order_by(Package.created_at.desc()).limit(3).all()
        lines = "\n".join(f"- {_format_package_line(pkg)}" for pkg in top)
        return (
            "Booking on TravelEase is quick and easy! \ud83d\ude80\n\n"
            "1. Browse packages on the **Home** page\n"
            "2. Click a package to see full details\n"
            "3. Select travellers, class & date\n"
            "4. Proceed to checkout and pay\n\n"
            "Here are some recently added packages:\n" + lines
        )

    return None

def _openai_chat_reply(user_message):
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    model = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini").strip() or "gpt-4.1-mini"
    if not api_key:
        return None

    packages = Package.query.order_by(Package.price.asc()).all()
    package_lines = [_format_package_detailed(pkg) for pkg in packages]
    package_context = "\n".join(package_lines) if package_lines else "No packages currently listed."

    system_prompt = (
        "You are a friendly, professional travel assistant for TravelEase — an online holiday booking platform. "
        "Your role is to help users discover packages, understand pricing, navigate the booking process, "
        "and choose the right transport options (flights, trains, buses, cabs).\n\n"
        "Guidelines:\n"
        "- Use a warm, conversational yet professional tone\n"
        "- Format responses with bullet points (- item) for lists\n"
        "- Use **bold** for package names, prices, and important terms\n"
        "- Keep replies concise (max 6 lines), ending with a helpful follow-up question or call-to-action\n"
        "- If asked something unrelated to travel/booking, politely redirect\n"
        "- Always refer to prices in INR format (e.g., INR 12,500)\n\n"
        "Website navigation:\n"
        "- Holiday Packages: Home page -> package card -> Book Now -> checkout -> payment\n"
        "- Transport: top nav (Flights / Trains / Buses / Cabs) -> select route/date/class -> checkout\n"
        "- Account: Login / Register from nav; view history in My Bookings\n"
        "- Support: Contact page for queries and booking assistance\n\n"
        f"Live package catalogue:\n{package_context}"
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.5,
        "max_tokens": 280
    }

    req = Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        method="POST"
    )

    try:
        with urlopen(req, timeout=20) as response:
            body = json.loads(response.read().decode("utf-8"))
            choices = body.get("choices", [])
            if choices:
                message = choices[0].get("message", {}).get("content", "").strip()
                if message:
                    return message
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError):
        return None

    return None

@app.route('/chatbot/ask', methods=['POST'])
def chatbot_ask():
    data = request.get_json(silent=True) or {}
    user_message = (data.get('message') or '').strip()

    if not user_message:
        return jsonify({"reply": "Please type your trip or booking question."}), 400

    if len(user_message) > 800:
        user_message = user_message[:800]

    db_reply = _db_chat_reply(user_message)
    if db_reply:
        return jsonify({"reply": db_reply})

    ai_reply = _openai_chat_reply(user_message)
    reply = ai_reply if ai_reply else _fallback_chat_reply(user_message)
    return jsonify({"reply": reply})

# Routes
@app.route('/')
def index():
    packages = Package.query.order_by(Package.created_at.desc()).all()
    spin_offer = _get_active_spin_offer()
    return render_template('index.html', packages=packages, spin_offer=spin_offer)


@app.route('/offers/spin', methods=['POST'])
def spin_wheel_offer():
    active_offer = _get_active_spin_offer()
    if active_offer:
        return jsonify({
            "status": "ok",
            "already_spun": True,
            "offer_id": active_offer.get('offer_id'),
            "label": active_offer.get('label'),
            "discount": active_offer.get('discount', 0),
            "code": active_offer.get('code'),
            "used": bool(active_offer.get('used', False)),
            "spin_date": active_offer.get('spin_date')
        })

    selected_offer = _pick_weighted_spin_offer()
    code = f"TE{selected_offer['discount']:02d}{random.randint(100, 999)}"
    stored_offer = {
        "offer_id": selected_offer['id'],
        "label": selected_offer['label'],
        "discount": selected_offer['discount'],
        "code": code,
        "used": False,
        "spin_date": _today_iso()
    }
    session['spin_wheel_offer'] = stored_offer
    session.modified = True

    return jsonify({
        "status": "ok",
        "already_spun": False,
        "offer_id": stored_offer['offer_id'],
        "label": stored_offer['label'],
        "discount": stored_offer['discount'],
        "code": stored_offer['code'],
        "used": False,
        "spin_date": stored_offer['spin_date']
    })

@app.route('/checkout/<int:package_id>', methods=['GET'])
@login_required
def checkout(package_id):
    package = Package.query.get_or_404(package_id)
    num_members = int(session.get('search_travellers') or '1')
    offer = _get_active_spin_offer()
    spin_discount = 0
    if offer and not offer.get('used') and offer.get('discount', 0) > 0:
        spin_discount = float(offer['discount'])
    return render_template(
        'checkout.html',
        package=package,
        num_members=num_members,
        spin_offer=offer,
        spin_discount=spin_discount
    )

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
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.filter_by(package_id=package_id).order_by(Review.created_at.desc()).paginate(page=page, per_page=5, error_out=False)

    # Calculate average rating (only for current page reviews for efficiency, but ideally cache or compute once)
    all_reviews = Review.query.filter_by(package_id=package_id).all()
    avg_rating = 0
    if all_reviews:
        avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
    review_count = len(all_reviews)

    # Check if user has this in wishlist
    in_wishlist = False
    if current_user.is_authenticated:
        in_wishlist = Wishlist.query.filter_by(user_id=current_user.id, package_id=package_id).first() is not None

    return render_template('package_details.html',
                          package=package,
                          reviews=reviews,
                          avg_rating=avg_rating,
                          review_count=review_count,
                          in_wishlist=in_wishlist)



@app.route('/pay', methods=['POST'])
@login_required
def pay():
    package_id = request.form.get('package_id')
    num_members = int(request.form.get('num_members', 1))
    
    package = Package.query.get_or_404(package_id)
    subtotal = float(package.price * num_members)
    offer = _get_active_spin_offer()
    spin_discount = 0.0
    if offer and not offer.get('used') and offer.get('discount', 0) > 0:
        spin_discount = float(offer['discount'])
    discount_amount = round(subtotal * (spin_discount / 100.0), 2)
    total_price = round(subtotal - discount_amount, 2)
    
    card_number = request.form.get('card_number', '')
    cvv = request.form.get('cvv', '')
    payment_method = request.form.get('payment_method', 'card')

    if payment_method == 'card' and (not card_number or not cvv):
        flash('Payment failed: Invalid card details.', 'danger')
        return redirect(url_for('checkout', package_id=package_id))
    
    # Create main booking
    new_booking = Booking(
        user_id=current_user.id,
        package_id=package.id,
        package_name=package.name,
        total_price=total_price,
        num_members=num_members,
        status='Confirmed'
    )
    
    try:
        db.session.add(new_booking)
        db.session.commit()

        if offer and spin_discount > 0:
            offer['used'] = True
            offer['used_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            session['spin_wheel_offer'] = offer
            session.modified = True
            flash(f'Spin offer applied: {int(spin_discount)}% OFF. You saved INR {discount_amount:.2f}.', 'success')
        
        # Clear any residual transport session data
        session.pop('selected_flight_id', None)
        session.pop('selected_flight_date', None)
        session.pop('selected_flight_travellers', None)
        session.pop('selected_flight_class', None)
        session.pop('selected_train_id', None)
        session.pop('selected_bus_id', None)
        session.pop('selected_cab_id', None)
        
        flash('Payment Successful! Booking Confirmed.', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred during booking processing.', 'danger')
        return redirect(url_for('checkout', package_id=package_id))

@app.route('/dashboard')
@login_required
def dashboard():
    bookings_page = request.args.get('bookings_page', 1, type=int)
    flight_bookings_page = request.args.get('flight_bookings_page', 1, type=int)
    train_bookings_page = request.args.get('train_bookings_page', 1, type=int)
    bus_bookings_page = request.args.get('bus_bookings_page', 1, type=int)
    cab_bookings_page = request.args.get('cab_bookings_page', 1, type=int)

    bookings = Booking.query.filter_by(user_id=current_user.id).paginate(page=bookings_page, per_page=10, error_out=False)
    flight_bookings = FlightBooking.query.filter_by(user_id=current_user.id).order_by(FlightBooking.departure_date.desc()).paginate(page=flight_bookings_page, per_page=10, error_out=False)
    train_bookings = TrainBooking.query.filter_by(user_id=current_user.id).order_by(TrainBooking.created_at.desc()).paginate(page=train_bookings_page, per_page=10, error_out=False)
    bus_bookings = BusBooking.query.filter_by(user_id=current_user.id).order_by(BusBooking.created_at.desc()).paginate(page=bus_bookings_page, per_page=10, error_out=False)
    cab_bookings = CabBooking.query.filter_by(user_id=current_user.id).order_by(CabBooking.created_at.desc()).paginate(page=cab_bookings_page, per_page=10, error_out=False)
    return render_template(
        'dashboard.html',
        bookings=bookings,
        flight_bookings=flight_bookings,
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

    packages_page = request.args.get('packages_page', 1, type=int)
    bookings_page = request.args.get('bookings_page', 1, type=int)
    trains_page = request.args.get('trains_page', 1, type=int)
    buses_page = request.args.get('buses_page', 1, type=int)
    cabs_page = request.args.get('cabs_page', 1, type=int)
    train_bookings_page = request.args.get('train_bookings_page', 1, type=int)
    bus_bookings_page = request.args.get('bus_bookings_page', 1, type=int)
    cab_bookings_page = request.args.get('cab_bookings_page', 1, type=int)

    packages = Package.query.paginate(page=packages_page, per_page=10, error_out=False)
    bookings = Booking.query.paginate(page=bookings_page, per_page=10, error_out=False)
    trains = Train.query.order_by(Train.id.desc()).paginate(page=trains_page, per_page=10, error_out=False)
    buses = Bus.query.order_by(Bus.id.desc()).paginate(page=buses_page, per_page=10, error_out=False)
    cabs = Cab.query.order_by(Cab.id.desc()).paginate(page=cabs_page, per_page=10, error_out=False)
    train_bookings = TrainBooking.query.order_by(TrainBooking.created_at.desc()).paginate(page=train_bookings_page, per_page=10, error_out=False)
    bus_bookings = BusBooking.query.order_by(BusBooking.created_at.desc()).paginate(page=bus_bookings_page, per_page=10, error_out=False)
    cab_bookings = CabBooking.query.order_by(CabBooking.created_at.desc()).paginate(page=cab_bookings_page, per_page=10, error_out=False)
    return render_template(
        'admin_dashboard.html',
        packages=packages,
        bookings=bookings,
        trains=trains,
        buses=buses,
        cabs=cabs,
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
    page = request.args.get('page', 1, type=int)

    packages_query = Package.query

    # Text search
    if query:
        query_tokens = [token for token in re.split(r'\s+', query) if token]
        text_filter = or_(
            Package.name.ilike(f'%{query}%'),
            Package.description.ilike(f'%{query}%')
        )
        for token in query_tokens:
            text_filter = or_(
                text_filter,
                Package.name.ilike(f'%{token}%'),
                Package.description.ilike(f'%{token}%')
            )
        packages_query = packages_query.filter(
            text_filter
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

    packages = packages_query.paginate(page=page, per_page=10, error_out=False)
    suggested_packages = []
    search_message = None
    did_you_mean_terms = []

    if query and packages.total == 0:
        suggestion_tokens = [token for token in re.split(r'\s+', query) if token]
        base_suggestion_query = Package.query

        if min_price is not None:
            base_suggestion_query = base_suggestion_query.filter(Package.price >= min_price)
        if max_price is not None:
            base_suggestion_query = base_suggestion_query.filter(Package.price <= max_price)

        ranked_suggestions = []

        for token in suggestion_tokens:
            token_matches = (
                base_suggestion_query
                .filter(
                    or_(
                        Package.name.ilike(f'%{token}%'),
                        Package.description.ilike(f'%{token}%')
                    )
                )
                .order_by(Package.discount_percentage.desc(), Package.price.asc())
                .limit(4)
                .all()
            )
            ranked_suggestions.extend(token_matches)

        ranked_suggestions.extend(
            base_suggestion_query
            .order_by(Package.discount_percentage.desc(), Package.price.asc())
            .limit(4)
            .all()
        )
        ranked_suggestions.extend(
            base_suggestion_query
            .order_by(Package.created_at.desc())
            .limit(4)
            .all()
        )

        seen_ids = set()
        for pkg in ranked_suggestions:
            if pkg.id not in seen_ids:
                suggested_packages.append(pkg)
                seen_ids.add(pkg.id)
            if len(suggested_packages) >= 8:
                break

        candidate_packages = (
            base_suggestion_query
            .order_by(Package.created_at.desc())
            .limit(120)
            .all()
        )
        candidate_terms = set()
        for pkg in candidate_packages:
            if pkg.name:
                candidate_terms.add(pkg.name.strip())
            if pkg.popular_places:
                for place in pkg.popular_places.split('|'):
                    place = place.strip()
                    if len(place) >= 3:
                        candidate_terms.add(place)

        query_lower = query.lower()
        query_token_set = {token.lower() for token in suggestion_tokens if len(token) >= 2}
        ranked_terms = []

        for term in candidate_terms:
            clean_term = term.strip()
            if not clean_term:
                continue

            term_lower = clean_term.lower()
            if term_lower == query_lower:
                continue

            score = 0.0
            if query_lower in term_lower:
                score = 3.0
            elif query_token_set and any(token in term_lower for token in query_token_set):
                score = 2.0
            else:
                similarity = SequenceMatcher(None, query_lower, term_lower).ratio()
                if similarity >= 0.55:
                    score = similarity

            if score > 0:
                ranked_terms.append((score, len(clean_term), clean_term))

        ranked_terms.sort(key=lambda item: (-item[0], item[1], item[2].lower()))
        did_you_mean_terms = [item[2] for item in ranked_terms[:5]]

        if not did_you_mean_terms:
            did_you_mean_terms = [pkg.name for pkg in suggested_packages[:5] if pkg.name]

        search_message = f"No exact package match found for '{query}'. Showing suggested options instead."

    return render_template('search_results.html',
                          packages=packages,
                          query=query,
                          min_price=min_price,
                          max_price=max_price,
                          sort=sort,
                          suggested_packages=suggested_packages,
                          search_message=search_message,
                          did_you_mean_terms=did_you_mean_terms)

# Train Routes
@app.route('/trains', methods=['GET', 'POST'])
def trains():
    trains_data = []
    from_city = to_city = travel_date = ''
    travel_class = 'Economy'
    travellers = 1
    page = request.args.get('page', 1, type=int)

    if request.method == 'POST':
        from_city = request.form.get('from_city', '').strip()
        to_city = request.form.get('to_city', '').strip()
        travel_date = request.form.get('travel_date', '').strip()
        travel_class = request.form.get('travel_class', 'Economy')
        travellers = int(request.form.get('travellers', 1))

        # Validate travel date is not in the past
        today_str = datetime.now().strftime('%Y-%m-%d')
        if travel_date and travel_date < today_str:
            flash('Travel date cannot be in the past. Please select today or a future date.', 'danger')
            travel_date = today_str

    query = Train.query.order_by(Train.id.asc())
    if from_city:
        query = query.filter(Train.departure_city.contains(from_city))
    if to_city:
        query = query.filter(Train.arrival_city.contains(to_city))
    trains_list = query.paginate(page=page, per_page=5, error_out=False)

    for idx, train in enumerate(trains_list.items):
        per_person, total = compute_price(train.base_price, travel_class, travellers)
        trains_data.append({
            "train": train,
            "per_person": per_person,
            "total": total,
            "image_url": transport_image_url("train", train.id, train.operator)
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
        arrival_cities=arrival_cities,
        pagination=trains_list if request.method == 'POST' else None
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
    card_number = request.form.get('card_number', '')
    cvv = request.form.get('cvv', '')
    confirm_details = request.form.get('confirm_details')
    payment_method = request.form.get('payment_method', 'card')

    # Validate travel date is not in the past
    today_str = datetime.now().strftime('%Y-%m-%d')
    if travel_date < today_str:
        flash('Travel date cannot be in the past. Please select today or a future date.', 'danger')
        return redirect(url_for('train_checkout', train_id=train_id, date=today_str, travellers=travellers, travel_class=travel_class))

    if not confirm_details:
        flash('Please confirm the booking details before payment.', 'warning')
        return redirect(url_for('train_checkout', train_id=train_id, date=travel_date, travellers=travellers, travel_class=travel_class))

    if payment_method == 'card' and (not card_number or not cvv):
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
    buses_data = []
    from_city = to_city = travel_date = ''
    travel_class = 'Economy'
    travellers = 1

    if request.method == 'POST':
        from_city = request.form.get('from_city', '').strip()
        to_city = request.form.get('to_city', '').strip()
        travel_date = request.form.get('travel_date', '').strip()
        travel_class = request.form.get('travel_class', 'Economy')
        travellers = int(request.form.get('travellers', 1))

        # Validate travel date is not in the past
        today_str = datetime.now().strftime('%Y-%m-%d')
        if travel_date and travel_date < today_str:
            flash('Travel date cannot be in the past. Please select today or a future date.', 'danger')
            travel_date = today_str

    query = Bus.query.order_by(Bus.id.asc())
    if from_city:
        query = query.filter(Bus.departure_city.contains(from_city))
    if to_city:
        query = query.filter(Bus.arrival_city.contains(to_city))
    buses_list = query.limit(5).all()

    for idx, bus in enumerate(buses_list):
        per_person, total = compute_price(bus.base_price, travel_class, travellers)
        buses_data.append({
            "bus": bus,
            "per_person": per_person,
            "total": total,
            "image_url": transport_image_url("bus", bus.id, bus.operator)
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
    card_number = request.form.get('card_number', '')
    cvv = request.form.get('cvv', '')
    confirm_details = request.form.get('confirm_details')
    payment_method = request.form.get('payment_method', 'card')

    # Validate travel date is not in the past
    today_str = datetime.now().strftime('%Y-%m-%d')
    if travel_date < today_str:
        flash('Travel date cannot be in the past. Please select today or a future date.', 'danger')
        return redirect(url_for('bus_checkout', bus_id=bus_id, date=today_str, travellers=travellers, travel_class=travel_class))

    if not confirm_details:
        flash('Please confirm the booking details before payment.', 'warning')
        return redirect(url_for('bus_checkout', bus_id=bus_id, date=travel_date, travellers=travellers, travel_class=travel_class))

    if payment_method == 'card' and (not card_number or not cvv):
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
    cabs_data = []
    from_city = to_city = travel_date = ''
    travel_class = 'Standard'
    travellers = 1
    page = request.args.get('page', 1, type=int)

    if request.method == 'POST':
        from_city = request.form.get('from_city', '').strip()
        to_city = request.form.get('to_city', '').strip()
        travel_date = request.form.get('travel_date', '').strip()
        travel_class = request.form.get('travel_class', 'Standard')
        travellers = int(request.form.get('travellers', 1))

        # Validate travel date is not in the past
        today_str = datetime.now().strftime('%Y-%m-%d')
        if travel_date and travel_date < today_str:
            flash('Travel date cannot be in the past. Please select today or a future date.', 'danger')
            travel_date = today_str

    query = Cab.query.order_by(Cab.id.asc())
    if from_city:
        query = query.filter(Cab.departure_city.contains(from_city))
    if to_city:
        query = query.filter(Cab.arrival_city.contains(to_city))
    cabs_list = query.paginate(page=page, per_page=5, error_out=False)

    for idx, cab in enumerate(cabs_list.items):
        per_person, total = compute_price(cab.base_price, travel_class, travellers)
        cabs_data.append({
            "cab": cab,
            "per_person": per_person,
            "total": total,
            "image_url": transport_image_url("cab", cab.id, cab.provider)
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
        arrival_cities=arrival_cities,
        pagination=cabs_list if request.method == 'POST' else None
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
    card_number = request.form.get('card_number', '')
    cvv = request.form.get('cvv', '')
    confirm_details = request.form.get('confirm_details')
    payment_method = request.form.get('payment_method', 'card')

    # Validate travel date is not in the past
    today_str = datetime.now().strftime('%Y-%m-%d')
    if travel_date < today_str:
        flash('Travel date cannot be in the past. Please select today or a future date.', 'danger')
        return redirect(url_for('cab_checkout', cab_id=cab_id, date=today_str, travellers=travellers, travel_class=travel_class))

    if not confirm_details:
        flash('Please confirm the booking details before payment.', 'warning')
        return redirect(url_for('cab_checkout', cab_id=cab_id, date=travel_date, travellers=travellers, travel_class=travel_class))

    if payment_method == 'card' and (not card_number or not cvv):
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

# Flight Routes
@app.route('/flights', methods=['GET', 'POST'])
def flights():
    flights_data = []
    from_city = to_city = travel_date = travel_class = ''
    travellers = 1
    page = request.args.get('page', 1, type=int)

    if request.method == 'POST':
        from_city = request.form.get('from_city', '').strip()
        to_city = request.form.get('to_city', '').strip()
        travel_date = request.form.get('travel_date', '').strip()
        travel_class = request.form.get('travel_class', 'Economy')
        travellers = int(request.form.get('travellers', 1))

        query = Flight.query
        if from_city:
            query = query.filter(Flight.departure_city.contains(from_city))
        if to_city:
            query = query.filter(Flight.arrival_city.contains(to_city))
        flights_list = query.paginate(page=page, per_page=10, error_out=False)

        for flight in flights_list.items:
            per_person, total = compute_price(flight.base_price, travel_class, travellers)
            flights_data.append({
                "flight": flight,
                "per_person": per_person,
                "total": total
            })

    departure_cities = [c[0] for c in db.session.query(Flight.departure_city).distinct().all()]
    arrival_cities = [c[0] for c in db.session.query(Flight.arrival_city).distinct().all()]
    return render_template(
        'flights.html',
        flights=flights_data,
        from_city=from_city,
        to_city=to_city,
        travel_date=travel_date,
        travel_class=travel_class,
        travellers=travellers,
        searched=request.method == 'POST',
        departure_cities=departure_cities,
        arrival_cities=arrival_cities,
        pagination=flights_list if request.method == 'POST' else None
    )

@app.route('/flights/checkout/<int:flight_id>')
@login_required
def flight_checkout(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    travel_date = request.args.get('date', '') or datetime.utcnow().strftime('%Y-%m-%d')
    travellers = int(request.args.get('travellers', 1))
    travel_class = request.args.get('travel_class', 'Economy')
    per_person, total = compute_price(flight.base_price, travel_class, travellers)
    return render_template(
        'flight_checkout.html',
        flight=flight,
        travel_date=travel_date,
        travellers=travellers,
        travel_class=travel_class,
        per_person=per_person,
        total=total
    )

@app.route('/flights/pay', methods=['POST'])
@login_required
def flight_pay():
    flight_id = request.form.get('flight_id')
    travel_date = request.form.get('travel_date', '') or datetime.utcnow().strftime('%Y-%m-%d')
    travellers = int(request.form.get('travellers', 1))
    travel_class = request.form.get('travel_class', 'Economy')
    card_number = request.form.get('card_number')
    cvv = request.form.get('cvv')
    confirm_details = request.form.get('confirm_details')

    if not confirm_details:
        flash('Please confirm the booking details before payment.', 'warning')
        return redirect(url_for('flight_checkout', flight_id=flight_id, date=travel_date, travellers=travellers, travel_class=travel_class))

    if not card_number or not cvv:
        flash('Payment failed: Invalid card details.', 'danger')
        return redirect(url_for('flight_checkout', flight_id=flight_id, date=travel_date, travellers=travellers, travel_class=travel_class))

    flight = Flight.query.get_or_404(flight_id)
    per_person, total = compute_price(flight.base_price, travel_class, travellers)
    booking = FlightBooking(
        flight_id=flight.id,
        user_id=current_user.id,
        departure_date=datetime.strptime(travel_date, '%Y-%m-%d'),
        selected_class=travel_class,
        num_travellers=travellers,
        final_price=total
    )
    try:
        db.session.add(booking)
        db.session.commit()
        flash('Flight booking confirmed!', 'success')
    except:
        db.session.rollback()
        flash('Error processing flight booking.', 'danger')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Initialize DB (Note: In production with MySQL, tables should be created externally or via migrations)
    # with app.app_context():
    #     db.create_all()
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '5000'))
    app.run(host=host, port=port, debug=True)
