# Chapter 6: System Design

## 6.1 System Architecture

The TravelEase application follows a **three-tier client-server architecture**. The presentation tier handles all user-facing interaction through HTML, CSS, and JavaScript rendered via Jinja2 templates. The application tier processes business logic through Flask route handlers. The data tier manages persistent storage through SQLAlchemy ORM connected to MySQL (with automatic SQLite fallback).

```mermaid
graph TD
    A["🌐 Browser\n(User / Admin)"] -->|HTTP Request| B

    subgraph APP["Application Tier – Flask (app.py)"]
        B["Route Handler\n(@app.route)"]
        C["Business Logic\n(booking, pricing, validation)"]
        D["Auth Layer\nFlask-Login + Werkzeug"]
        E["Session Manager\n(spin offer, search state)"]
        B --> C
        B --> D
        B --> E
    end

    subgraph FRONT["Presentation Tier"]
        F["Jinja2 Templates\n(HTML + CSS)"]
        G["chatbot.js\n(fetch /chatbot/ask)"]
        H["checkout.js\n(payment validation)"]
    end

    subgraph DATA["Data Tier"]
        I["SQLAlchemy ORM\n(models.py)"]
        J[("MySQL 8.0\n(Primary)")]
        K[("SQLite 3\n(Fallback)")]
        I --> J
        I -.->|"if MySQL unreachable"| K
    end

    subgraph EXT["External Services (Optional)"]
        L["OpenAI API\ngpt-4.1-mini"]
    end

    APP -->|Rendered HTML| FRONT
    C -->|ORM Queries| I
    E -->|Chatbot AI call| L
```

---

## 6.2 Database Design

The database contains **14 tables** mapped to SQLAlchemy model classes in `models.py`. All foreign key relationships enforce referential integrity.

### Table 1 – Database Entity Description

| Table Name | Primary Key | Foreign Keys | Description |
|---|---|---|---|
| `users` | `id` | — | Registered user accounts with hashed passwords and admin flag |
| `packages` | `id` | — | Holiday packages with price, duration, itinerary, hotel, images |
| `bookings` | `id` | `user_id → users`, `package_id → packages` | Package booking records with status, members, and total price |
| `flights` | `id` | — | Flight routes with airline, flight number, cities, and base price |
| `flight_bookings` | `id` | `flight_id → flights`, `user_id → users` | Flight booking records with date, class, travellers, final price |
| `trains` | `id` | — | Train routes with operator, train number, cities, and base price |
| `train_bookings` | `id` | `train_id → trains`, `user_id → users` | Train booking records with date, class, travellers, final price |
| `buses` | `id` | — | Bus routes with operator, bus number, cities, and base price |
| `bus_bookings` | `id` | `bus_id → buses`, `user_id → users` | Bus booking records with date, class, travellers, final price |
| `cabs` | `id` | — | Cab records with provider, cab type, route, and base price |
| `cab_bookings` | `id` | `cab_id → cabs`, `user_id → users` | Cab booking records with date, class, travellers, final price |
| `reviews` | `id` | `user_id → users`, `package_id → packages` | Star ratings (1–5) and text comments per user per package |
| `wishlist` | `id` | `user_id → users`, `package_id → packages` | Saved package associations per user |
| `contact_us` | `id` | — | Customer support inquiries with status tracking |

---

## 6.3 Data Flow Diagram

### DFD Level 0 – Context Diagram

```mermaid
graph LR
    U(["👤 User"])
    A(["🔧 Admin"])
    S(["TravelEase\nSystem"])
    DB[("🗄️ Database")]

    U -->|"Browse, Book, Pay,\nChat, Review"| S
    S -->|"Package Info,\nBooking Confirmation,\nChatbot Reply"| U

    A -->|"Add/Edit/Delete\nPackages and Transport,\nManage Inquiries"| S
    S -->|"Dashboard Data,\nBooking Records,\nInquiry List"| A

    S <-->|"Read / Write\nBooking and User Data"| DB
```

---

### DFD Level 1 – Major Processes

```mermaid
graph TD
    U(["👤 User"])
    A(["🔧 Admin"])
    DB[("🗄️ DB")]

    U -->|"Credentials"| P1["1.0\nUser Authentication"]
    P1 -->|"Session Token"| U
    P1 <-->|"Read/Write User"| DB

    U -->|"Search / Browse"| P2["2.0\nPackage Browsing"]
    P2 -->|"Package List / Details"| U
    P2 <-->|"Read Packages"| DB

    U -->|"Select Package +\nPayment Details"| P3["3.0\nPackage Booking"]
    P3 -->|"Booking Confirmation"| U
    P3 <-->|"Write Booking"| DB

    U -->|"Select Route,\nClass, Date"| P4["4.0\nTransport Booking"]
    P4 -->|"Transport Confirmation"| U
    P4 <-->|"Write Transport Booking"| DB

    U -->|"Query Text"| P5["5.0\nChatbot"]
    P5 -->|"Text Reply"| U
    P5 <-->|"Read Packages and Fares"| DB

    A -->|"Package and Transport\nCRUD Commands"| P6["6.0\nAdmin Management"]
    P6 -->|"Updated Records"| A
    P6 <-->|"Read/Write All Tables"| DB
```

---

### DFD Level 2 – Package Booking Flow

```mermaid
flowchart TD
    A([User Opens Home Page]) --> B["2.1 Fetch Packages\nfrom DB with Pagination"]
    B --> C[Display Package Cards]
    C --> D{User Clicks\nBook Now}
    D --> E["2.2 Retrieve Active\nSpin Offer from Session"]
    E --> F{Offer Valid\nand Unused?}
    F -->|Yes| G[Apply Discount\nto Total]
    F -->|No| H[Use Full Price]
    G --> I["3.1 Checkout Page\ntravellers + payment"]
    H --> I
    I --> J{Payment\nMethod?}
    J -->|Card| K["3.2 Validate Card\nnumber, expiry, CVV"]
    J -->|UPI| L["3.3 Accept UPI ID"]
    K --> M{Valid?}
    M -->|No| N[Flash Error\nRedirect Back]
    M -->|Yes| O["3.4 Create Booking\nRecord in DB"]
    L --> O
    O --> P[Mark Spin\nOffer as Used]
    P --> Q[Flash Confirmation\nRedirect to Dashboard]
```

---

## 6.4 Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    USERS {
        int id PK
        string username
        string email
        string password
        bool is_admin
    }
    PACKAGES {
        int id PK
        string name
        float price
        string duration
        float discount_percentage
        bool is_featured
        text itinerary
        text hotel_details
        datetime created_at
    }
    BOOKINGS {
        int id PK
        int user_id FK
        int package_id FK
        int num_members
        float total_price
        string status
        datetime booking_date
    }
    FLIGHTS {
        int id PK
        string airline
        string flight_number
        string departure_city
        string arrival_city
        float base_price
    }
    FLIGHT_BOOKINGS {
        int id PK
        int flight_id FK
        int user_id FK
        datetime departure_date
        string selected_class
        int num_travellers
        float final_price
    }
    TRAINS {
        int id PK
        string operator
        string train_number
        string departure_city
        string arrival_city
        float base_price
    }
    TRAIN_BOOKINGS {
        int id PK
        int train_id FK
        int user_id FK
        datetime travel_date
        string selected_class
        int num_travellers
        float final_price
        string status
    }
    BUSES {
        int id PK
        string operator
        string bus_number
        string departure_city
        string arrival_city
        float base_price
    }
    BUS_BOOKINGS {
        int id PK
        int bus_id FK
        int user_id FK
        datetime travel_date
        string selected_class
        int num_travellers
        float final_price
        string status
    }
    CABS {
        int id PK
        string provider
        string cab_type
        string departure_city
        string arrival_city
        float base_price
    }
    CAB_BOOKINGS {
        int id PK
        int cab_id FK
        int user_id FK
        datetime travel_date
        string selected_class
        int num_travellers
        float final_price
        string status
    }
    REVIEWS {
        int id PK
        int user_id FK
        int package_id FK
        int rating
        text comment
        datetime created_at
    }
    WISHLIST {
        int id PK
        int user_id FK
        int package_id FK
        datetime created_at
    }
    CONTACT_US {
        int id PK
        string name
        string email
        string subject
        text message
        string status
        datetime created_at
    }

    USERS ||--o{ BOOKINGS : "makes"
    PACKAGES ||--o{ BOOKINGS : "has"
    USERS ||--o{ FLIGHT_BOOKINGS : "makes"
    FLIGHTS ||--o{ FLIGHT_BOOKINGS : "has"
    USERS ||--o{ TRAIN_BOOKINGS : "makes"
    TRAINS ||--o{ TRAIN_BOOKINGS : "has"
    USERS ||--o{ BUS_BOOKINGS : "makes"
    BUSES ||--o{ BUS_BOOKINGS : "has"
    USERS ||--o{ CAB_BOOKINGS : "makes"
    CABS ||--o{ CAB_BOOKINGS : "has"
    USERS ||--o{ REVIEWS : "writes"
    PACKAGES ||--o{ REVIEWS : "receives"
    USERS ||--o{ WISHLIST : "saves"
    PACKAGES ||--o{ WISHLIST : "saved in"
```

---

## 6.5 Flowcharts

### Flowchart 1 – User Registration and Login

```mermaid
flowchart TD
    A([START]) --> B[Visit /register]
    B --> C["Fill Form: username, email, password"]
    C --> D{Email already\nexists in DB?}
    D -->|Yes| E[Flash Warning\nRedirect to /register]
    D -->|No| F["Hash Password (scrypt)"]
    F --> G[Save new User to DB]
    G --> H{DB Commit\nsuccessful?}
    H -->|No| I[Rollback and\nFlash Error]
    H -->|Yes| J[Flash Success\nRedirect to /login]
    J --> K[User enters email + password]
    K --> L{User found\nin DB?}
    L -->|No| M[Flash: Invalid credentials]
    L -->|Yes| N{Password hash\nmatches?}
    N -->|No| M
    N -->|Yes| O[login_user - Create Session]
    O --> P{is_admin = True?}
    P -->|Yes| Q[Redirect to /admin]
    P -->|No| R[Redirect to /dashboard]
    Q --> S([END])
    R --> S
```

---

### Flowchart 2 – Package Booking and Payment

```mermaid
flowchart TD
    A([User logged in]) --> B[Browse Packages on Home Page]
    B --> C[Click Package Card - View Details]
    C --> D[Click Book Now - /checkout/id]
    D --> E{Active spin offer\nin session?}
    E -->|Yes and unused| F[Show discount on checkout]
    E -->|No| G[Show full price]
    F --> H[User fills: Travellers + Payment]
    G --> H
    H --> I{Payment method?}
    I -->|Card| J["Validate: Card No / Expiry / CVV"]
    I -->|UPI| K[Accept UPI ID]
    J --> L{Valid?}
    L -->|No| M[Flash Error - Stay on checkout]
    L -->|Yes| N["Compute Total: price x members x discount"]
    K --> N
    N --> O[Create Booking record in DB]
    O --> P{Commit successful?}
    P -->|No| Q[Rollback and Flash Error]
    P -->|Yes| R[Mark spin offer as used in session]
    R --> S[Flash: Booking Confirmed]
    S --> T[Redirect to /dashboard]
    T --> U([END])
```

---

### Flowchart 3 – Chatbot Response Strategy

```mermaid
flowchart TD
    A([User sends message]) --> B[POST /chatbot/ask]
    B --> C["Strip + lowercase message text"]
    C --> D{Message empty?}
    D -->|Yes| E[Return 400 Bad Request]
    D -->|No| F[Truncate to 800 chars max]
    F --> G["Layer 1: _db_chat_reply()"]
    G --> H{Budget / destination /\ntransport keyword match?}
    H -->|Yes| I[Query live package and transport DB]
    I --> J[Format response with real prices]
    J --> K([Return DB Response])
    H -->|No| L["Layer 2: _openai_chat_reply()"]
    L --> M{OPENAI_API_KEY configured?}
    M -->|No| N["Layer 3: _fallback_chat_reply()"]
    M -->|Yes| O[Build system prompt with package catalogue]
    O --> P[Call OpenAI Chat Completions API]
    P --> Q{API response received?}
    Q -->|Yes| R([Return AI Reply])
    Q -->|No or Error| N
    N --> S[Keyword match for common topics]
    S --> T([Return Structured Fallback Reply])
```

---

### Flowchart 4 – Admin Operations

```mermaid
flowchart TD
    A([Admin Login]) --> B{is_admin = True?}
    B -->|No| C[Flash: Access Denied - Redirect to /]
    B -->|Yes| D[Admin Dashboard /admin]
    D --> E{Select Operation}

    E -->|Add Package| F[Fill Package Form]
    F --> G[POST /admin/add]
    G --> H[Save to packages table]
    H --> I[Flash: Package Added]
    I --> D

    E -->|Edit Package| J[GET /admin/edit/id - Pre-filled form]
    J --> K[POST /admin/edit/id]
    K --> L[Update record in DB]
    L --> M[Flash: Package Updated]
    M --> D

    E -->|Delete Package| N[GET /admin/delete/id]
    N --> O[Delete from packages table]
    O --> P[Flash: Package Deleted]
    P --> D

    E -->|Manage Transport| Q[Trains / Buses / Cabs pages]
    Q --> R[Add / Edit / Delete records]
    R --> D

    E -->|Edit Booking| S[GET /admin/booking/edit/id]
    S --> T[Update members + status]
    T --> U[Recalculate total price]
    U --> D

    E -->|View Inquiries| V[GET /admin/inquiries]
    V --> W[POST acknowledge/id]
    W --> X[Set status to Acknowledged]
    X --> D
```

---

## 6.6 Use Case Diagrams

### Use Case Diagram – Regular User

```mermaid
graph LR
    U(["👤 Regular User"])

    subgraph SYS["TravelEase System"]
        UC1["Register and Login"]
        UC2["Browse and Search Packages"]
        UC3["View Package Details"]
        UC4["Add to Wishlist"]
        UC5["Book Holiday Package"]
        UC6["Apply Spin Wheel Discount"]
        UC7["Book Flight"]
        UC8["Book Train"]
        UC9["Book Bus"]
        UC10["Book Cab"]
        UC11["View Dashboard - Booking History"]
        UC12["Submit Review and Rating"]
        UC13["Contact Support"]
        UC14["Use Chatbot Assistant"]
    end

    U --- UC1
    U --- UC2
    U --- UC3
    U --- UC4
    U --- UC5
    U --- UC6
    U --- UC7
    U --- UC8
    U --- UC9
    U --- UC10
    U --- UC11
    U --- UC12
    U --- UC13
    U --- UC14
```

---

### Use Case Diagram – Admin

```mermaid
graph LR
    A(["🔧 Admin"])

    subgraph ASYS["TravelEase System - Admin Panel"]
        A1["All Regular User Operations"]
        A2["Add New Package"]
        A3["Edit Existing Package"]
        A4["Delete Package"]
        A5["Add / Edit / Delete Trains"]
        A6["Add / Edit / Delete Buses"]
        A7["Add / Edit / Delete Cabs"]
        A8["View All User Bookings"]
        A9["Edit Booking Status and Members"]
        A10["View Customer Inquiries"]
        A11["Acknowledge Inquiry"]
    end

    A --- A1
    A --- A2
    A --- A3
    A --- A4
    A --- A5
    A --- A6
    A --- A7
    A --- A8
    A --- A9
    A --- A10
    A --- A11
```

---

## 6.7 Module Description

### Table 2 – Module Description Summary

| # | Module | Functionality | Key Routes | DB Tables Used |
|---|---|---|---|---|
| 1 | **User Authentication** | Registration, login, logout, session creation, password hashing | `/register`, `/login`, `/logout` | `users` |
| 2 | **Package Management** | Home listing with pagination, keyword/price search, detailed package view | `/`, `/search`, `/package/<id>` | `packages` |
| 3 | **Package Booking** | Checkout, spin discount, payment validation, booking creation | `/checkout/<id>`, `/pay` | `bookings`, `packages` |
| 4 | **Flight Booking** | Route listing, class/date selection, fare computation, booking | `/flights`, `/flight-checkout`, `/flight-pay` | `flights`, `flight_bookings` |
| 5 | **Train Booking** | Train listing, class selection, fare computation, booking | `/trains`, `/train-checkout`, `/train-pay` | `trains`, `train_bookings` |
| 6 | **Bus Booking** | Bus listing, class/date selection, fare computation, booking | `/buses`, `/bus-checkout`, `/bus-pay` | `buses`, `bus_bookings` |
| 7 | **Cab Booking** | Cab listing, provider/route selection, booking | `/cabs`, `/cab-checkout`, `/cab-pay` | `cabs`, `cab_bookings` |
| 8 | **User Dashboard** | Unified booking history — all 5 categories, each paginated | `/dashboard` | All booking tables |
| 9 | **Wishlist** | Add/remove packages, view saved packages | `/wishlist`, `/wishlist/add/<id>` | `wishlist`, `packages` |
| 10 | **Reviews** | Submit star rating (1–5) and comment; one review per user per package | `/package/<id>/review` | `reviews` |
| 11 | **Spin Wheel Offer** | Daily weighted-probability discount generation, session storage | `/offers/spin` | Session only |
| 12 | **Chatbot** | Layer 1: DB-aware intent; Layer 2: OpenAI API; Layer 3: fallback | `/chatbot/ask` | `packages`, transport tables |
| 13 | **Contact Support** | Inquiry submission, status tracking | `/contact` | `contact_us` |
| 14 | **Admin – Packages** | Full CRUD on holiday packages via web forms | `/admin/add`, `/admin/edit/<id>`, `/admin/delete/<id>` | `packages` |
| 15 | **Admin – Transport** | Add, edit, delete train, bus, and cab records | `/admin/trains`, `/admin/buses`, `/admin/cabs` | `trains`, `buses`, `cabs` |
| 16 | **Admin – Bookings** | View all user bookings, update member count and status | `/admin`, `/admin/booking/edit/<id>` | `bookings` |
| 17 | **Admin – Inquiries** | View contact inquiries, mark as acknowledged | `/admin/inquiries` | `contact_us` |

---

### Table 3 – Transport Class Multiplier Table

| Travel Class | Category | Price Multiplier | Example (Base ₹2,000, 2 travellers) |
|---|---|---|---|
| Economy | Flights | 1.0× | ₹2,000 × 1.0 × 2 = **₹4,000** |
| Premium | Flights | 1.4× | ₹2,000 × 1.4 × 2 = **₹5,600** |
| Business | Flights | 2.2× | ₹2,000 × 2.2 × 2 = **₹8,800** |
| Standard | Trains / Buses | 1.0× | ₹800 × 1.0 × 2 = **₹1,600** |
| Comfort | Trains / Buses | 1.3× | ₹800 × 1.3 × 2 = **₹2,080** |
| Luxury | Cabs | 1.8× | ₹1,500 × 1.8 × 2 = **₹5,400** |

**Formula:** `final_price = base_price × class_multiplier × num_travellers`

---

### Table 4 – Spin Wheel Offer Probability Table

| Offer Label | Discount | Weight | Approximate Probability |
|---|---|---|---|
| 5% OFF | 5% | 24 | 24.0% |
| 10% OFF | 10% | 20 | 20.0% |
| Try Again | 0% | 18 | 18.0% |
| 12% OFF | 12% | 14 | 14.0% |
| 7% OFF | 7% | 10 | 10.0% |
| 20% OFF | 20% | 6 | 6.0% |
| No Offer | 0% | 5 | 5.0% |
| 15% OFF | 15% | 3 | 3.0% |
| **Total** | — | **100** | **100%** |

Higher-value discounts carry lower weights. The weighted selection uses `random.uniform(0, total_weight)` and iterates through offers accumulating weights until the roll is exceeded.

---

### Table 5 – Complete Flask API Endpoint Summary

| Method | Endpoint | Description | Auth | Admin |
|---|---|---|---|---|
| GET/POST | `/register` | User registration | No | No |
| GET/POST | `/login` | User login | No | No |
| GET | `/logout` | User logout | Yes | No |
| GET | `/` | Home — package listing with pagination | No | No |
| GET | `/search` | Package search with keyword and price filter | No | No |
| GET | `/package/<id>` | Package detail with reviews and wishlist status | No | No |
| POST | `/package/<id>/review` | Submit star rating and comment | Yes | No |
| GET | `/checkout/<id>` | Package checkout page with spin discount | Yes | No |
| POST | `/pay` | Confirm package booking and payment | Yes | No |
| GET | `/dashboard` | Unified user booking dashboard | Yes | No |
| POST | `/offers/spin` | Generate or retrieve daily spin-wheel offer | No | No |
| POST | `/chatbot/ask` | Chatbot query — DB / AI / fallback pipeline | No | No |
| GET | `/wishlist` | View saved wishlist packages | Yes | No |
| POST | `/wishlist/add/<id>` | Add package to wishlist | Yes | No |
| POST | `/wishlist/remove/<id>` | Remove package from wishlist | Yes | No |
| GET/POST | `/contact` | Contact support inquiry form | No | No |
| GET | `/flights` | Browse available flights | No | No |
| POST | `/flights/book` | Initiate flight booking (store in session) | Yes | No |
| GET | `/flight-checkout` | Flight checkout page | Yes | No |
| POST | `/flight-pay` | Confirm flight booking | Yes | No |
| GET | `/trains` | Browse available trains | No | No |
| POST | `/train/book` | Initiate train booking | Yes | No |
| GET | `/train-checkout` | Train checkout page | Yes | No |
| POST | `/train-pay` | Confirm train booking | Yes | No |
| GET | `/buses` | Browse available buses | No | No |
| POST | `/bus/book` | Initiate bus booking | Yes | No |
| GET | `/bus-checkout` | Bus checkout page | Yes | No |
| POST | `/bus-pay` | Confirm bus booking | Yes | No |
| GET | `/cabs` | Browse available cabs | No | No |
| POST | `/cab/book` | Initiate cab booking | Yes | No |
| GET | `/cab-checkout` | Cab checkout page | Yes | No |
| POST | `/cab-pay` | Confirm cab booking | Yes | No |
| GET | `/admin` | Admin dashboard overview | Yes | Yes |
| POST | `/admin/add` | Add new package | Yes | Yes |
| GET/POST | `/admin/edit/<id>` | Edit existing package | Yes | Yes |
| GET | `/admin/delete/<id>` | Delete package | Yes | Yes |
| GET/POST | `/admin/booking/edit/<id>` | Edit booking status and member count | Yes | Yes |
| GET | `/admin/inquiries` | View all support inquiries | Yes | Yes |
| POST | `/admin/inquiries/acknowledge/<id>` | Mark inquiry as acknowledged | Yes | Yes |
| GET | `/admin/trains` | List all train records | Yes | Yes |
| POST | `/admin/trains/add` | Add new train record | Yes | Yes |
| GET/POST | `/admin/trains/edit/<id>` | Edit train record | Yes | Yes |
| POST | `/admin/trains/delete/<id>` | Delete train record | Yes | Yes |
| GET | `/admin/buses` | List all bus records | Yes | Yes |
| POST | `/admin/buses/add` | Add new bus record | Yes | Yes |
| GET/POST | `/admin/buses/edit/<id>` | Edit bus record | Yes | Yes |
| POST | `/admin/buses/delete/<id>` | Delete bus record | Yes | Yes |
| GET | `/admin/cabs` | List all cab records | Yes | Yes |
| POST | `/admin/cabs/add` | Add new cab record | Yes | Yes |
| GET/POST | `/admin/cabs/edit/<id>` | Edit cab record | Yes | Yes |
| POST | `/admin/cabs/delete/<id>` | Delete cab record | Yes | Yes |
