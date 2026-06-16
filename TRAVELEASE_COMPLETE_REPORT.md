# TRAVELEASE: WEB-BASED HOLIDAY AND TRANSPORT BOOKING MANAGEMENT SYSTEM

A Major Project Report submitted in partial fulfillment of the requirements for the award of the degree of
**Master of Computer Applications (MCA)**

Submitted by:
[Your Full Name]
[University Roll Number]
[Enrollment Number]

Under the guidance of:
[Guide Name]
[Designation]

Department of Computer Applications
[College Name]
[University Name]

Academic Session: 2025â€“2026
Submission Date: [DD Month YYYY]

---

## List of Figures

Figure 1 â€“ System Architecture Diagram
Figure 2 â€“ Data Flow Diagram (Level 0 â€“ Context Diagram)
Figure 3 â€“ Data Flow Diagram (Level 1 â€“ Major Processes)
Figure 4 â€“ Data Flow Diagram (Level 2 â€“ Package Booking Flow)
Figure 5 â€“ Entity-Relationship (ER) Diagram
Figure 6 â€“ Use Case Diagram (User)
Figure 7 â€“ Use Case Diagram (Admin)
Figure 8 â€“ User Registration and Login Flowchart
Figure 9 â€“ Package Booking and Payment Flowchart
Figure 10 â€“ Transport Booking Flowchart
Figure 11 â€“ Admin Operations Flowchart
Figure 12 â€“ Chatbot Response Strategy Flowchart
Figure 13 â€“ Spin Wheel Offer Flowchart
Figure 14 â€“ Home Page Screenshot
Figure 15 â€“ Package Details Page Screenshot
Figure 16 â€“ Checkout Page Screenshot
Figure 17 â€“ User Dashboard Screenshot
Figure 18 â€“ Admin Dashboard Screenshot
Figure 19 â€“ Transport Booking Page Screenshot
Figure 20 â€“ Contact Page Screenshot

---

## List of Tables

Table 1 â€“ Stakeholder Summary
Table 2 â€“ Functional Requirements
Table 3 â€“ Non-Functional Requirements
Table 4 â€“ Hardware Requirements
Table 5 â€“ Software Requirements
Table 6 â€“ Feasibility Analysis Summary
Table 7 â€“ Database Entity Description
Table 8 â€“ Module Description Summary
Table 9 â€“ API Endpoint Summary
Table 10 â€“ Test Cases and Results
Table 11 â€“ Bugs Found and Fixed
Table 12 â€“ Project Folder Structure

---

## List of Acronyms and Abbreviations

| Abbreviation | Full Form |
|---|---|
| API | Application Programming Interface |
| CRUD | Create, Read, Update, Delete |
| CSS | Cascading Style Sheets |
| CVV | Card Verification Value |
| DB | Database |
| DFD | Data Flow Diagram |
| ER | Entity Relationship |
| FK | Foreign Key |
| HTML | HyperText Markup Language |
| HTTP | HyperText Transfer Protocol |
| JS | JavaScript |
| JSON | JavaScript Object Notation |
| MCA | Master of Computer Applications |
| NFR | Non-Functional Requirement |
| ORM | Object Relational Mapping |
| PK | Primary Key |
| SDLC | Software Development Life Cycle |
| SQL | Structured Query Language |
| SQLite | Self-Contained SQL Database Engine |
| UI | User Interface |
| UPI | Unified Payments Interface |
| URL | Uniform Resource Locator |
| UX | User Experience |
| WSGI | Web Server Gateway Interface |

---

# Chapter 1: Introduction to the Project

## 1.1 Background

The travel and tourism sector has undergone a significant transformation with the advent of digital platforms. Earlier, booking a holiday required visiting multiple travel agencies, making several phone calls, and coordinating between different service providers for hotels, transport, and sightseeing. The rise of internet-based booking systems has greatly simplified this process, giving travellers direct control over their planning experience.

However, most existing systems either cater exclusively to one mode of transport, or they only list packages without providing an integrated booking workflow. A user wishing to book a complete holidayâ€”including a flight, a hotel-inclusive package, and local transportâ€”is still forced to navigate between multiple websites or applications. This fragmentation leads to inefficiencies, repeated data entry, and difficulty in maintaining a unified record of all bookings.

The TravelEase project was conceived to address this gap. It is a web-based holiday and transport booking management system built using Python and the Flask framework. The platform brings package discovery, transport booking (flights, trains, buses, and cabs), payment simulation, and user account management under a single unified interface. Both travellers and administrators are served through dedicated panels tailored to their respective roles and responsibilities.

## 1.2 Project Overview

TravelEase is a full-stack web application developed as an academic project for the Master of Computer Applications programme. The system follows a client-server architecture where the backend is powered by Flask (a lightweight Python web framework), the data layer is managed using SQLAlchemy ORM with MySQL as the primary database, and the frontend is built using HTML, CSS, JavaScript, and Jinja2 templates.

The application consists of two primary panels:

**User Panel** â€” Registered travellers can browse curated holiday packages, view detailed itineraries and hotel information, add packages to a wishlist, submit ratings and reviews, book packages with class-based pricing, and book individual transport options including flights, trains, buses, and cabs. A personal dashboard allows each user to track all bookings made across every transport category.

**Admin Panel** â€” Administrators have full control over the platform's operational data. They can add, edit, and delete holiday packages; manage transport records for flights, trains, buses, and cabs; view all user bookings; and manage customer support inquiries submitted through the Contact page.

Additional features include a chatbot assistant that answers travel-related queries using live database data, an optional OpenAI-powered response layer, and a daily Spin Wheel discount offer that rewards users with promotional codes redeemable at checkout.

The system also supports Docker-based containerised deployment, enabling straightforward setup in both local development and production-like environments.

## 1.3 Objectives of the Project

The primary objectives of the TravelEase system are as follows:

1. To design and develop an integrated web-based platform that supports end-to-end holiday booking, from package discovery to payment confirmation.

2. To implement a multi-mode transport booking system covering flights, trains, buses, and cabs, each with class-based fare calculation logic.

3. To establish a secure, role-based user management system distinguishing between regular travellers and administrative users.

4. To maintain a consistent and normalised relational database schema using SQLAlchemy ORM, ensuring referential integrity across all booking records.

5. To provide users with supportive tools such as a chatbot assistant, a wishlist feature, a review system, and a daily discount offer to enhance engagement and decision-making.

6. To implement practical deployment support through Docker containerisation and a MySQL-to-SQLite fallback mechanism for resilient local execution.

7. To deliver a maintainable, modular codebase that can be extended with future production features such as real payment gateways, email notifications, and advanced analytics.

## 1.4 Scope of the Project

The scope of TravelEase encompasses the following areas:

**In Scope:**
- User registration, login, and session management with secure password hashing.
- Holiday package listing, search, filtering, and detailed package view with itinerary, hotel details, sightseeing, and image gallery.
- Package booking workflow with support for multiple travellers and class-based pricing, including spin-wheel discount application at checkout.
- Transport booking modules for flights, trains, buses, and cabs with route selection, date selection, class selection, and fare computation.
- User dashboard displaying complete booking history across all booking categories.
- Review and rating system limited to one review per user per package.
- Wishlist management allowing users to save and remove packages.
- Contact and support inquiry form with admin-side acknowledgment workflow.
- Admin panel for complete CRUD operations on packages, transport records, and booking management.
- A chatbot with layered response strategy: database-aware smart replies, optional AI-powered responses via OpenAI, and a structured fallback response system.
- Daily Spin Wheel offer mechanism with session-based discount tracking.
- Docker-based deployment support with automatic database migration and seeding.

**Out of Scope:**
- Live payment gateway integration (Razorpay, Stripe, or PayPal).
- Real-time flight or train availability synchronisation with external providers.
- Email or SMS notification delivery.
- Multi-language support.
- Mobile application interface.

## 1.5 Organisation of the Report

This report is organised into eleven chapters as described below:

- **Chapter 1** introduces the project, its background, objectives, and scope.
- **Chapter 2** identifies the problem statement, existing system shortcomings, and the proposed solution.
- **Chapter 3** provides the theoretical background covering relevant concepts and technologies.
- **Chapter 4** details the requirement gathering process, including functional, non-functional, hardware, and software requirements.
- **Chapter 5** presents the feasibility study examining technical, economic, operational, and schedule dimensions.
- **Chapter 6** covers the complete system design including architecture, database design, DFDs, ER diagram, flowcharts, use case diagrams, and module descriptions.
- **Chapter 7** presents important code snippets with explanations of key implementation decisions.
- **Chapter 8** describes the implementation approach, student and admin panel functionality, test cases, and bugs resolved.
- **Chapter 9** covers building and deployment including installation steps, runtime instructions, and folder structure.
- **Chapter 10** outlines the current limitations of the project across functional, technical, and testing dimensions.
- **Chapter 11** presents the conclusions, key achievements, and planned future enhancements.

---

# Chapter 2: Statement of the Problem

## 2.1 Problem Identification

Travel planning in today's environment, despite the availability of digital tools, remains a fragmented and multi-step process for many users. The following problems have been identified through observation of existing travel booking platforms and user behaviour patterns:

**Fragmented Booking Experience:** A traveller planning a holiday must typically visit separate platforms for package comparison, flight booking, train reservation, hotel selection, and local transport. There is no single platform that integrates all these steps into one cohesive experience.

**Lack of Unified Booking History:** Since bookings are spread across multiple platforms, users have no centralised location to review or manage their complete travel records. This makes tracking, modification, and cancellation unnecessarily complicated.

**Limited Admin Control in Small Systems:** Most lightweight booking portals lack administrative dashboards that allow operational data to be managed without direct database access. Package listings, transport options, and customer inquiries often require manual database updates.

**Insufficient Decision Support Tools:** Many platforms display packages but provide no additional support such as chatbots, review aggregation, wishlists, or price comparison tools to assist users in making informed choices.

**Poor Engagement Mechanisms:** Flat, transactional booking platforms rarely provide any engagement incentives. Without offers, recommendations, or interactive elements, users tend to abandon the platform after a single visit.

**Weak Validation in Payment Flows:** Several academic and small-scale booking systems accept payments without any form of input validation, leading to data integrity issues in booking records.

## 2.2 Proposed Solution â€“ TravelEase

TravelEase proposes a unified web-based holiday and transport booking system that resolves the above challenges through the following design decisions:

**Centralised Platform:** All booking operationsâ€”holiday packages, flights, trains, buses, and cabsâ€”are available through a single web application, eliminating the need to switch between multiple services.

**Unified User Dashboard:** Every booking made by a user across any category is recorded and displayed in a personal dashboard, organised by booking type for clarity.

**Role-Based Admin Panel:** The admin panel provides complete CRUD operations on packages, transport options, and bookings through a structured web interface, eliminating the need for direct database access.

**Decision-Support Features:** The platform includes a chatbot assistant for query resolution, a review and rating system for package evaluation, a wishlist for saving preferred packages, and a price and keyword search filter for refined browsing.

**Engagement Through Offers:** A daily Spin Wheel mechanism generates discount codes with weighted probability, encouraging repeat visits and rewarding users at checkout.

**Validated Checkout Flow:** The payment flow at checkout validates card details (number format, expiry, and CVV) and supports UPI as an alternative payment option, ensuring only valid payment data reaches the booking confirmation stage.

## 2.3 Comparison with the Existing Systems

| Feature | Typical Existing Systems | TravelEase |
|---|---|---|
| Package + Transport in one portal | Rarely | Yes |
| Admin CRUD via web UI | Often absent | Full admin panel |
| User booking history | Single category | All categories |
| Chatbot assistance | Absent or generic | DB-aware + AI fallback |
| Review and wishlist | Rare in small systems | Present |
| Discount engagement | Static codes only | Dynamic Spin Wheel |
| Payment validation | Minimal | Card + UPI validation |
| Docker deployment support | Absent | Present |
| DB fallback mechanism | Absent | MySQL â†’ SQLite fallback |

TravelEase does not claim to replace commercial booking platforms such as MakeMyTrip or IRCTC, but it demonstrates a complete, academic-grade implementation of a multi-category booking system with role-based access, engagement features, and deployment readiness.

---

# Chapter 3: Theoretical Background

## 3.1 Web Application Architecture

A web application follows a client-server model where the client (browser) sends requests over HTTP/HTTPS and the server processes those requests, interacts with the database, and returns responses. TravelEase adopts a three-tier architecture:

- **Presentation Tier:** HTML templates rendered by Jinja2, styled with CSS and JavaScript. This layer handles all user-facing interaction.
- **Application Tier:** Flask routes process incoming HTTP requests, enforce business rules, manage sessions, and coordinate with the data layer.
- **Data Tier:** SQLAlchemy ORM maps Python model classes to relational database tables, providing a clean abstraction over SQL queries.

## 3.2 Flask as a Micro Web Framework

Flask is a lightweight Python web framework that follows the WSGI standard. Unlike full-stack frameworks, Flask gives developers precise control over which extensions to use. Key Flask concepts used in TravelEase include:

- **Routes:** Python functions decorated with `@app.route()` that handle specific URL patterns and HTTP methods.
- **Blueprints (conceptual):** Although not explicitly used as blueprints, the route logic is logically grouped by module (user routes, admin routes, transport routes).
- **Jinja2 Templates:** Flask's integrated templating engine that allows dynamic content insertion, loop rendering, and template inheritance.
- **Session Management:** Flask uses a signed cookie-based session system to persist user state across requests, used here for spin-wheel offer tracking and search preferences.
- **Flash Messages:** Temporary one-time notification messages passed between routes.

## 3.3 Object Relational Mapping with SQLAlchemy

SQLAlchemy is a Python library that provides ORM (Object Relational Mapping) capabilities, allowing relational database tables to be represented as Python classes. In TravelEase, Flask-SQLAlchemy is used as the integration layer.

Each database table has a corresponding model class. Relationships between tables are declared using `db.relationship()` and foreign keys using `db.ForeignKey()`. SQLAlchemy translates Python queries (for example, `Package.query.filter(Package.price <= budget).all()`) into optimised SQL statements without requiring the developer to write raw SQL for most operations.

The system uses MySQL as the primary database in production and Docker environments. When MySQL is unavailable (for example, in a development environment without MySQL installed), the system automatically falls back to a local SQLite database, ensuring uninterrupted development.

## 3.4 Role-Based Access Control

Role-based access control (RBAC) is a security pattern where access to system resources is determined by the role assigned to a user. In TravelEase, two roles are defined:

- **Regular User (is_admin = False):** Can browse packages, make bookings, write reviews, manage wishlist, and contact support.
- **Admin (is_admin = True):** Has all user privileges plus the ability to create, edit, delete packages; manage transport records; view all bookings; and acknowledge customer inquiries.

Admin-protected routes use the `ensure_admin()` helper function that checks `current_user.is_admin` before allowing access. Flask-Login manages authentication state and provides the `@login_required` decorator to protect any route from unauthenticated access.

## 3.5 Chatbot Design and Layered Response Strategy

The TravelEase chatbot is designed with a three-layer response strategy to maximise reliability:

**Layer 1 â€“ Database-Aware Response:** The system first checks if the user query matches known intent patterns such as budget queries, destination searches, or transport fare requests. If a match is found, the system fetches live data from the database and constructs a structured response. This layer ensures replies are always accurate and contextually grounded.

**Layer 2 â€“ AI-Powered Response:** If no database intent match is found, the system attempts to send the query to the OpenAI Chat Completions API (if an API key is configured). The system prompt injects live package data as context, allowing the AI model to produce informed, natural-language responses.

**Layer 3 â€“ Structured Fallback:** If both the database layer and the AI layer fail (for example, due to no API key or a network error), the system uses keyword matching to return a pre-written, informative response covering common topics such as bookings, pricing, transport, and contact support.

## 3.6 Secure Authentication Practices

Password security is implemented using the Werkzeug library's `generate_password_hash()` with the `scrypt` method, which is a modern, memory-intensive hashing algorithm resistant to brute-force attacks. During login, `check_password_hash()` verifies the submitted password against the stored hash without ever decrypting it. Plain-text passwords are never stored.

Flask's session cookie is signed using the application's `SECRET_KEY`, ensuring that session data cannot be tampered with by the client without detection.

---

# Chapter 4: Requirement Gathering and Analysis

## 4.1 Stakeholder Identification

Requirement gathering for TravelEase involved identifying the key stakeholders whose needs the system must satisfy.

**Table 1 â€“ Stakeholder Summary**

| Stakeholder | Role | Primary Needs |
|---|---|---|
| Traveller (End User) | Books packages and transport | Easy browsing, booking, payment, history |
| Administrator | Manages operational data | Package/transport management, inquiry handling |
| Developer/Maintainer | Builds and maintains system | Modular code, clear deployment steps |

## 4.2 Functional Requirements

Functional requirements describe the specific behaviours and operations the system must support.

**Table 2 â€“ Functional Requirements**

| FR No. | Requirement | Module |
|---|---|---|
| FR-01 | The system shall allow new users to register with a username, email, and password. | Authentication |
| FR-02 | The system shall authenticate users via email and password with secure hash comparison. | Authentication |
| FR-03 | The system shall maintain session state to identify logged-in users across requests. | Authentication |
| FR-04 | The system shall display all available holiday packages on the home page with pagination. | Package Management |
| FR-05 | The system shall allow users to search packages by keyword, minimum price, and maximum price. | Package Management |
| FR-06 | The system shall display a detailed package page including description, itinerary, hotel details, sightseeing, image gallery, and reviews. | Package Management |
| FR-07 | The system shall allow authenticated users to book a package by selecting number of travellers and proceeding to checkout. | Booking |
| FR-08 | The system shall compute the total booking amount based on package price, number of travellers, and any applicable spin-wheel discount. | Booking |
| FR-09 | The system shall validate card payment details (number, expiry, CVV) and accept UPI as an alternative. | Payment |
| FR-10 | The system shall allow authenticated users to book flights by selecting route, date, class, and number of travellers. | Flight Booking |
| FR-11 | The system shall allow authenticated users to book trains by selecting operator, route, date, class, and travellers. | Train Booking |
| FR-12 | The system shall allow authenticated users to book buses by selecting operator, route, date, class, and travellers. | Bus Booking |
| FR-13 | The system shall allow authenticated users to book cabs by selecting provider, route, date, and travellers. | Cab Booking |
| FR-14 | The system shall compute transport fares using class-based multipliers applied to the base price. | Pricing |
| FR-15 | The system shall display a personal dashboard showing all bookings across every transport category. | Dashboard |
| FR-16 | The system shall allow users to add and remove packages from a personal wishlist. | Wishlist |
| FR-17 | The system shall allow each user to submit one rating (1â€“5 stars) and comment per package. | Reviews |
| FR-18 | The system shall allow users to submit support inquiries through a contact form. | Support |
| FR-19 | The system shall provide a daily spin-wheel offer that generates a discount code redeemable at package checkout. | Offers |
| FR-20 | The system shall provide a chatbot that responds to travel-related queries using live database data and fallback strategies. | Chatbot |
| FR-21 | The admin shall be able to add, edit, and delete holiday packages through the admin panel. | Admin |
| FR-22 | The admin shall be able to add, edit, and delete train, bus, and cab records. | Admin |
| FR-23 | The admin shall be able to view and update the status of all user bookings. | Admin |
| FR-24 | The admin shall be able to view and acknowledge customer inquiries. | Admin |

## 4.3 Non-Functional Requirements

**Table 3 â€“ Non-Functional Requirements**

| NFR No. | Category | Requirement |
|---|---|---|
| NFR-01 | Security | Passwords shall be stored only as secure hashes (scrypt algorithm). |
| NFR-02 | Security | Admin routes shall be inaccessible to non-admin authenticated users. |
| NFR-03 | Security | Session cookies shall be signed using a server-side secret key. |
| NFR-04 | Performance | Standard page loads and booking operations shall complete within 3 seconds under normal conditions. |
| NFR-05 | Reliability | The system shall fall back to SQLite if MySQL is unreachable, ensuring uninterrupted development. |
| NFR-06 | Usability | The user interface shall provide clear navigation, flash-based feedback messages, and form validation cues. |
| NFR-07 | Maintainability | Route logic, model definitions, and configuration shall be separated into distinct files. |
| NFR-08 | Portability | The application shall be deployable both locally and via Docker containers. |
| NFR-09 | Data Integrity | All booking records shall use foreign keys referencing valid user and package/transport identifiers. |
| NFR-10 | Scalability | The modular route organisation shall permit future expansion with minimal structural changes. |

## 4.4 Hardware Requirements

**Table 4 â€“ Hardware Requirements**

| Component | Minimum Specification |
|---|---|
| Processor | Intel Core i3 (2 GHz) or equivalent |
| RAM | 4 GB (8 GB recommended for Docker) |
| Storage | 2 GB free disk space |
| Network | Active internet connection for OpenAI chatbot (optional) |
| Display | 1280 Ã— 720 resolution minimum |

## 4.5 Software Requirements

**Table 5 â€“ Software Requirements**

| Component | Specification |
|---|---|
| Operating System | Windows 10/11, Ubuntu 20.04+, or macOS 12+ |
| Python | Version 3.9 or later |
| Flask | Latest stable version |
| Flask-SQLAlchemy | Latest stable version |
| Flask-Login | Latest stable version |
| Werkzeug | Latest stable version |
| PyMySQL | Latest stable version (for MySQL connectivity) |
| MySQL | Version 8.0 (or SQLite 3.x as fallback) |
| Docker | Version 20.10+ (optional, for container deployment) |
| Web Browser | Chrome 100+, Firefox 100+, or Edge 100+ |
| Code Editor | VS Code or PyCharm (for development) |

---

# Chapter 5: Feasibility Study

## 5.1 Technical Feasibility

Technical feasibility assesses whether the proposed system can be built using available technology and tools.

TravelEase is built on a mature, well-documented technology stack. Flask is a production-proven Python web framework used by companies of varying sizes worldwide. SQLAlchemy is the most widely adopted Python ORM library, with comprehensive documentation and an active community. MySQL is an industry-standard relational database system, and its Python connector (PyMySQL) is stable and reliable.

The development team has access to all required tools without cost: Flask, SQLAlchemy, Python, and SQLite are all open source. Docker Desktop is freely available for local use. The chatbot's AI layer uses the OpenAI API, which requires an API key, but the system is designed to function fully without it using the database-aware and fallback layers.

The technical architectureâ€”three-tier web application with ORM-driven data access, session management, and role-based access controlâ€”is well-understood and follows established software engineering patterns. The project does not require any experimental or unproven technology.

**Conclusion:** Technically feasible. All required technologies are available, mature, and well-supported.

## 5.2 Economic Feasibility

Economic feasibility examines whether the project can be built and operated within acceptable cost boundaries.

The entire software stack is open source and free to use. Python, Flask, SQLAlchemy, MySQL Community Edition, SQLite, and Docker are all available at no licensing cost. Development is carried out on existing hardware. The optional OpenAI API has a usage-based cost, but this feature is optional and disabled when no API key is configured.

For deployment, the application can be hosted on a low-cost virtual private server (VPS) running Linux, typically available from providers such as DigitalOcean, Linode, or AWS Lightsail at approximately $5â€“$10 per month. The Docker-based deployment model makes setup straightforward and reduces ongoing maintenance effort.

**Conclusion:** Economically feasible. Development and operating costs are minimal, and the project delivers significant learning and practical value relative to the resources invested.

## 5.3 Operational Feasibility

Operational feasibility evaluates whether the system will be accepted and effectively used by its intended users.

The TravelEase interface is designed to be intuitive, with clearly labelled navigation links, descriptive flash messages for every user action, and a logical booking flow from package browsing to confirmation. The admin panel organises management operations under clearly titled sections, minimising the learning curve for administrators.

The system supports both local execution (suitable for academic evaluation) and Docker-based deployment (suitable for demonstration and cloud hosting). No complex configuration is required for local use beyond installing Python packages and setting environment variables.

The chatbot further reduces the need for users to navigate the platform manually by answering common questions such as package prices, booking steps, and transport fare ranges directly in a chat interface.

**Conclusion:** Operationally feasible. The system has a low learning curve and supports multiple deployment modes appropriate for both academic and demonstration contexts.

## 5.4 Schedule Feasibility

Schedule feasibility determines whether the project can be completed within the available academic timeframe.

The project was planned and executed across the standard MCA project timeline. Development was carried out incrementally:

- **Phase 1 â€“ Requirement Analysis and Design:** System requirements, database schema, and architecture diagrams were prepared.
- **Phase 2 â€“ Core Development:** User authentication, package management, and basic booking were implemented first as the foundation.
- **Phase 3 â€“ Transport Modules:** Flight, train, bus, and cab booking modules were added with class-based pricing.
- **Phase 4 â€“ Auxiliary Features:** Chatbot, spin-wheel offer, wishlist, reviews, and contact management were integrated.
- **Phase 5 â€“ Admin Panel:** Full admin CRUD operations were implemented for packages, transport, and inquiries.
- **Phase 6 â€“ Testing and Deployment:** Script-based verification, manual testing, Dockerfile configuration, and documentation were completed.

The modular nature of Flask route development allowed parallel progress on different features, and the use of SQLAlchemy ORM significantly reduced the time required for database operations.

**Conclusion:** Schedule feasibility confirmed. All core modules were completed within the academic project timeline. The phased development approach ensured manageable workloads at each stage.
# Chapter 6: System Design

## 6.1 System Architecture

TravelEase follows a three-tier client-server architecture:

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚              PRESENTATION TIER               â”‚
â”‚   HTML (Jinja2 Templates) + CSS + JavaScript â”‚
â”‚   chatbot.js | checkout.js | search.js       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â”‚ HTTP Request / Response
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚              APPLICATION TIER                â”‚
â”‚         Flask (Python) â€“ app.py              â”‚
â”‚  Route Handlers | Business Logic | Auth      â”‚
â”‚  Flask-Login | Werkzeug | Session Manager    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â”‚ SQLAlchemy ORM
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                  DATA TIER                   â”‚
â”‚     MySQL (Primary) / SQLite (Fallback)      â”‚
â”‚  models.py â€“ User, Package, Booking,         â”‚
â”‚  Flight, Train, Bus, Cab, Review, Wishlist   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**Request Flow:**
1. A user action in the browser (for example, clicking "Book Now") sends an HTTP request to a Flask route.
2. The Flask route handler validates the request, checks authentication, and applies business logic.
3. SQLAlchemy translates Python ORM queries into SQL and retrieves or writes data from/to the database.
4. The Flask handler passes the result data to a Jinja2 template.
5. The rendered HTML is returned to the browser as the HTTP response.

**Key Architectural Decisions:**
- **MySQL-first with SQLite fallback:** The `config.py` file checks MySQL reachability at startup. If MySQL is unavailable, the system transparently switches to a local SQLite database, ensuring uninterrupted development without manual configuration changes.
- **Separation of concerns:** Model definitions (`models.py`), configuration (`config.py`), and route logic (`app.py`) are in separate files, keeping responsibilities clearly divided.
- **Session-based state:** Spin-wheel offer data, search preferences, and selected transport details are stored in the Flask session, eliminating the need for additional database tables for temporary state.

## 6.2 Database Design

The database consists of fourteen tables with clearly defined primary keys, foreign key relationships, and appropriate constraints. The design follows third normal form (3NF) to minimise redundancy and ensure data consistency.

**Table 7 â€“ Database Entity Description**

| Table | Primary Key | Description |
|---|---|---|
| users | id | Stores registered user accounts with hashed passwords and admin flag |
| packages | id | Stores holiday package data including price, duration, itinerary, and amenities |
| bookings | id | Records package bookings linking users and packages with pricing and status |
| flights | id | Stores available flight routes with airline, flight number, and base price |
| flight_bookings | id | Records flight bookings linking users and flights with date, class, and price |
| trains | id | Stores train route records with operator, train number, and base price |
| train_bookings | id | Records train bookings with travel date, class, travellers, and final price |
| buses | id | Stores bus route records with operator, bus number, and base price |
| bus_bookings | id | Records bus bookings with travel date, class, travellers, and final price |
| cabs | id | Stores cab records with provider, cab type, route, and base price |
| cab_bookings | id | Records cab bookings with travel date, class, travellers, and final price |
| reviews | id | Stores user reviews with rating (1â€“5) and comment per package |
| wishlist | id | Records user-package wishlist associations |
| contact_us | id | Stores customer support inquiries with status tracking |

**Key Relationships:**
- `bookings.user_id` â†’ `users.id` (FK)
- `bookings.package_id` â†’ `packages.id` (FK)
- `flight_bookings.flight_id` â†’ `flights.id` (FK)
- `flight_bookings.user_id` â†’ `users.id` (FK)
- `train_bookings.train_id` â†’ `trains.id` (FK)
- `reviews.user_id` â†’ `users.id` (FK), `reviews.package_id` â†’ `packages.id` (FK)
- `wishlist.user_id` â†’ `users.id` (FK), `wishlist.package_id` â†’ `packages.id` (FK)

## 6.3 Data Flow Diagram

### DFD Level 0 â€“ Context Diagram

```
                 â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                 â”‚                     â”‚
  [USER] â”€â”€â”€â”€â”€â”€â”€â–ºâ”‚   TRAVELEASE SYSTEM â”‚â—„â”€â”€â”€â”€â”€â”€â”€ [ADMIN]
         â—„â”€â”€â”€â”€â”€â”€â”€â”‚                     â”‚â”€â”€â”€â”€â”€â”€â”€â”€â–º
                 â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â”‚
                          â–¼
                    [DATABASE]
```

External entities: User, Admin, Database.
The system receives booking requests from users, management instructions from admins, and stores/retrieves data from the database.

### DFD Level 1 â€“ Major Processes

```
[USER] â†’ (1.0 User Auth) â†’ Authenticated Session
[USER] â†’ (2.0 Package Browsing) â†’ Package Data
[USER] â†’ (3.0 Booking Process) â†’ Booking Record
[USER] â†’ (4.0 Transport Booking) â†’ Transport Booking Record
[USER] â†’ (5.0 Chatbot Query) â†’ Chatbot Response
[ADMIN] â†’ (6.0 Admin Management) â†’ Updated Records
```

### DFD Level 2 â€“ Package Booking Flow

```
User Selects Package â†’ (2.1 View Package Details)
â†’ (2.2 Add to Wishlist) [Optional]
â†’ (3.1 Select Travellers & Class)
â†’ (3.2 Apply Spin Discount) [Optional]
â†’ (3.3 Payment Validation)
â†’ (3.4 Booking Confirmation) â†’ Booking Record Written
â†’ (3.5 Dashboard Update) â†’ User Dashboard
```

## 6.4 Entity-Relationship (ER) Diagram

```
USERS â”€â”€â”€â”€< BOOKINGS >â”€â”€â”€â”€ PACKAGES
  â”‚              â”‚
  â”‚          (total_price,
  â”‚           num_members,
  â”‚             status)
  â”‚
  â”œâ”€â”€â”€â”€< FLIGHT_BOOKINGS >â”€â”€â”€â”€ FLIGHTS
  â”‚
  â”œâ”€â”€â”€â”€< TRAIN_BOOKINGS >â”€â”€â”€â”€ TRAINS
  â”‚
  â”œâ”€â”€â”€â”€< BUS_BOOKINGS >â”€â”€â”€â”€ BUSES
  â”‚
  â”œâ”€â”€â”€â”€< CAB_BOOKINGS >â”€â”€â”€â”€ CABS
  â”‚
  â”œâ”€â”€â”€â”€< REVIEWS >â”€â”€â”€â”€ PACKAGES
  â”‚
  â””â”€â”€â”€â”€< WISHLIST >â”€â”€â”€â”€ PACKAGES

CONTACT_US (independent â€“ linked to email only)
```

**Cardinality:**
- One USER can have many BOOKINGS.
- One PACKAGE can have many BOOKINGS.
- One USER can have many REVIEWS but only one per PACKAGE.
- One USER can add many PACKAGES to WISHLIST.
- One USER can make many FLIGHT / TRAIN / BUS / CAB BOOKINGS.

## 6.5 Flowcharts

### User Registration and Login Flowchart

```
START
  â”‚
  â–¼
User visits /register
  â”‚
  â–¼
Fill form (username, email, password)
  â”‚
  â–¼
Email already exists? â”€â”€YESâ”€â”€â–º Flash warning, redirect to /register
  â”‚ NO
  â–¼
Hash password (scrypt)
  â”‚
  â–¼
Save User to DB
  â”‚
  â–¼
Flash success â†’ Redirect to /login
  â”‚
  â–¼
User submits email + password
  â”‚
  â–¼
User found in DB? â”€â”€NOâ”€â”€â–º Flash "Invalid credentials"
  â”‚ YES
  â–¼
Password hash matches? â”€â”€NOâ”€â”€â–º Flash "Invalid credentials"
  â”‚ YES
  â–¼
login_user() called â†’ Session created
  â”‚
  â–¼
is_admin? â”€â”€YESâ”€â”€â–º Redirect to /admin
  â”‚ NO
  â–¼
Redirect to /dashboard
  â”‚
  â–¼
END
```

### Package Booking and Payment Flowchart

```
START
  â”‚
  â–¼
User browses packages â†’ selects one
  â”‚
  â–¼
View package details (/package/<id>)
  â”‚
  â–¼
Click "Book Now" â†’ /checkout/<id>
  â”‚
  â–¼
Active spin offer? â”€â”€YESâ”€â”€â–º Display discount summary
  â”‚ NO
  â–¼
Enter number of travellers + payment details
  â”‚
  â–¼
Payment method = Card?
  â”œâ”€YESâ”€â–º Validate card number, expiry, CVV
  â”‚         Invalid? â”€â”€â–º Flash error, redirect back
  â””â”€NOâ”€â”€â–º UPI selected (no card validation needed)
  â”‚
  â–¼
Compute: total = package.price Ã— travellers Ã— (1 - discount/100)
  â”‚
  â–¼
Create Booking record â†’ Save to DB
  â”‚
  â–¼
Mark spin offer as used
  â”‚
  â–¼
Flash "Booking Confirmed" â†’ Redirect to dashboard
  â”‚
  â–¼
END
```

### Chatbot Response Flowchart

```
START
  â”‚
  â–¼
User sends message via /chatbot/ask
  â”‚
  â–¼
Text pre-processed (lowercase, stripped)
  â”‚
  â–¼
Layer 1: Budget/destination/transport keyword match?
  â”œâ”€YESâ”€â”€â–º Query DB â†’ Return formatted DB response
  â”‚
  â”‚ NO
  â–¼
Layer 2: OPENAI_API_KEY set?
  â”œâ”€YESâ”€â”€â–º Build prompt with package catalogue
  â”‚         Call OpenAI API
  â”‚         Response received? â”€â”€YESâ”€â”€â–º Return AI response
  â”‚                            â”€â”€NOâ”€â”€â–º Fall through
  â”‚ NO
  â–¼
Layer 3: Keyword fallback matching
  â”‚
  â–¼
Return structured fallback response
  â”‚
  â–¼
END
```

## 6.6 Use Case Diagrams

### Use Case â€“ Regular User

```
          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
          â”‚           TravelEase System         â”‚
          â”‚                                    â”‚
          â”‚  â—‹ Register / Login                â”‚
          â”‚  â—‹ Browse Packages                 â”‚
          â”‚  â—‹ Search and Filter Packages      â”‚
          â”‚  â—‹ View Package Details            â”‚
  [USER]â”€â”€â”‚  â—‹ Add / Remove from Wishlist     â”‚
          â”‚  â—‹ Book Package                    â”‚
          â”‚  â—‹ Book Flight / Train / Bus / Cab â”‚
          â”‚  â—‹ Apply Spin Wheel Discount       â”‚
          â”‚  â—‹ Submit Review                   â”‚
          â”‚  â—‹ View Dashboard (My Bookings)    â”‚
          â”‚  â—‹ Submit Contact Inquiry          â”‚
          â”‚  â—‹ Use Chatbot                     â”‚
          â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Use Case â€“ Admin

```
          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
          â”‚           TravelEase System         â”‚
          â”‚                                    â”‚
          â”‚  â—‹ All User Operations             â”‚
          â”‚  â—‹ Add / Edit / Delete Packages    â”‚
  [ADMIN]â”€â”‚  â—‹ Add / Edit / Delete Trains      â”‚
          â”‚  â—‹ Add / Edit / Delete Buses        â”‚
          â”‚  â—‹ Add / Edit / Delete Cabs         â”‚
          â”‚  â—‹ View / Update All Bookings       â”‚
          â”‚  â—‹ View / Acknowledge Inquiries     â”‚
          â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## 6.7 Module Description

**Table 8 â€“ Module Description Summary**

| Module | Description | Key Routes |
|---|---|---|
| Authentication | User registration, login, logout, session management | /register, /login, /logout |
| Package Management | Package listing, search, details, pagination | /, /search, /package/\<id\> |
| Package Booking | Checkout flow, payment validation, booking creation | /checkout/\<id\>, /pay |
| Flight Booking | Flight search, seat class selection, fare computation, booking | /flights, /flights/book, /flight-checkout |
| Train Booking | Train search, class selection, booking | /trains, /train/book, /train-checkout |
| Bus Booking | Bus search, class selection, booking | /buses, /bus/book, /bus-checkout |
| Cab Booking | Cab search, booking | /cabs, /cab/book, /cab-checkout |
| User Dashboard | Unified booking history across all categories | /dashboard |
| Wishlist | Add/remove packages from wishlist, view wishlist | /wishlist, /wishlist/add/\<id\>, /wishlist/remove/\<id\> |
| Reviews | Submit and view star ratings and comments | /package/\<id\>/review |
| Contact Support | Submit inquiries, track status | /contact |
| Spin Wheel Offer | Daily offer generation, session storage, checkout application | /offers/spin |
| Chatbot | Intent detection, DB response, AI response, fallback | /chatbot/ask |
| Admin â€“ Packages | Add, edit, delete holiday packages | /admin/add, /admin/edit/\<id\>, /admin/delete/\<id\> |
| Admin â€“ Transport | Add, edit, delete train, bus, cab records | /admin/trains, /admin/buses, /admin/cabs |
| Admin â€“ Bookings | View and update all booking records | /admin (dashboard), /admin/booking/edit/\<id\> |
| Admin â€“ Inquiries | View and acknowledge contact inquiries | /admin/inquiries, /admin/inquiries/acknowledge/\<id\> |

---

# Chapter 7: Coding â€“ Important Code Snippets

## 7.1 Flask Application Setup and Database Connection

The application is initialised in `app.py`. The configuration is loaded from `config.py`, which contains intelligent database selection logic.

```python
# app.py
app = Flask(__name__)
app.config.from_object(Config)

def _configure_database(flask_app):
    try:
        db.init_app(flask_app)
    except ModuleNotFoundError as exc:
        if exc.name != 'pymysql':
            raise
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = _runtime_sqlite_url()
        db.init_app(flask_app)

_configure_database(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
```

The `_configure_database()` function catches a `ModuleNotFoundError` specifically for `pymysql`. If PyMySQL is not installed, the system switches to SQLite automatically. Similarly, `config.py` checks whether MySQL is reachable on the expected host and port; if not, it sets the SQLite URL before the application even starts.

## 7.2 User Registration Route

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email    = request.form.get('email')
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
```

The `scrypt` hashing method is used because it is deliberately resource-intensive, making dictionary and brute-force attacks significantly harder than MD5 or plain SHA-256. The database session is wrapped in a try-except block to handle unexpected write failures gracefully.

## 7.3 User Login Route

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        user     = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')
```

A deliberate design decision was made to show a single generic error message ("Invalid email or password") rather than separate messages for "email not found" and "wrong password". This approach prevents user enumeration attacks, where an attacker could otherwise determine which email addresses are registered in the system.

## 7.4 Package Checkout Route with Spin Wheel Discount

```python
@app.route('/checkout/<int:package_id>', methods=['GET'])
@login_required
def checkout(package_id):
    package      = Package.query.get_or_404(package_id)
    num_members  = int(session.get('search_travellers') or '1')
    offer        = _get_active_spin_offer()
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
```

The `_get_active_spin_offer()` helper checks the session for a stored offer and validates its date. Offers are valid only for the calendar day on which they were generated. If the stored `spin_date` does not match today's date, the offer is removed from the session automatically.

## 7.5 Chatbot Route with Layered Response

```python
@app.route('/chatbot/ask', methods=['POST'])
def chatbot_ask():
    data         = request.get_json(silent=True) or {}
    user_message = (data.get('message') or '').strip()

    if not user_message:
        return jsonify({"reply": "Please type your trip or booking question."}), 400

    if len(user_message) > 800:
        user_message = user_message[:800]

    db_reply = _db_chat_reply(user_message)
    if db_reply:
        return jsonify({"reply": db_reply})

    ai_reply = _openai_chat_reply(user_message)
    reply    = ai_reply if ai_reply else _fallback_chat_reply(user_message)
    return jsonify({"reply": reply})
```

The message length is capped at 800 characters to prevent abuse or accidental oversized requests. The three-function pipeline (`_db_chat_reply` â†’ `_openai_chat_reply` â†’ `_fallback_chat_reply`) ensures that a response is always returned regardless of database state or network availability.

## 7.6 Admin Routes â€“ Add, Edit, Delete Package

```python
# Add Package
@app.route('/admin/add', methods=['POST'])
@login_required
def add_package():
    if not ensure_admin():
        return redirect(url_for('index'))
    new_package = Package(
        name=request.form.get('name'),
        description=request.form.get('description'),
        price=request.form.get('price'),
        duration=request.form.get('duration'),
        discount_percentage=float(request.form.get('discount_percentage', 0)),
        # ... additional fields
    )
    db.session.add(new_package)
    db.session.commit()
    flash('Package added successfully.', 'success')
    return redirect(url_for('admin_dashboard'))

# Delete Package
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
```

Every admin route calls `ensure_admin()` before performing any operation. This helper function checks both that the user is authenticated (`current_user.is_authenticated`) and that the admin flag is set (`current_user.is_admin`). If either condition fails, the user is redirected to the home page with an "Access denied" message.

## 7.7 Frontend â€“ Sending Query to Flask and Rendering Response

The chatbot JavaScript in `static/js/chatbot.js` sends user messages to the Flask API endpoint and renders the response using lightweight Markdown parsing:

```javascript
async function sendMessage(text) {
    if (!text) return;
    addMessage("user", text);
    showTyping();

    const minDelay = new Promise(res => setTimeout(res, 700));

    try {
        const [response] = await Promise.all([
            fetch("/chatbot/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text }),
            }),
            minDelay,
        ]);
        const data = await response.json();
        hideTyping();
        addMessage("bot", data.reply || "I'm sorry, I couldn't process that.");
    } catch (err) {
        hideTyping();
        addMessage("bot", "Our assistant is temporarily unavailable.");
    }
}
```

`Promise.all()` is used to ensure the typing indicator is visible for at least 700 milliseconds, even if the API responds faster. This prevents the jarring experience of an instantly disappearing indicator. The `formatBotText()` function converts `**bold**`, `*italic*`, and `- bullet` patterns from the Flask response into HTML tags.

## 7.8 Complete Flask API Endpoint Summary

**Table 9 â€“ API Endpoint Summary**

| Method | URL Pattern | Purpose | Auth Required |
|---|---|---|---|
| GET/POST | /register | User registration | No |
| GET/POST | /login | User login | No |
| GET | /logout | User logout | Yes |
| GET | / | Home page â€“ package listing | No |
| GET | /search | Package search with filters | No |
| GET | /package/\<id\> | Package details page | No |
| GET | /checkout/\<id\> | Package checkout page | Yes |
| POST | /pay | Process package booking | Yes |
| GET | /dashboard | User booking dashboard | Yes |
| POST | /offers/spin | Generate spin-wheel offer | No |
| POST | /chatbot/ask | Chatbot message handling | No |
| GET | /flights | Browse flights | No |
| POST | /flights/book | Initiate flight booking | Yes |
| GET | /flight-checkout | Flight checkout page | Yes |
| POST | /flight-pay | Confirm flight booking | Yes |
| GET | /trains | Browse trains | No |
| POST | /train/book | Initiate train booking | Yes |
| GET | /train-checkout | Train checkout page | Yes |
| POST | /train-pay | Confirm train booking | Yes |
| GET | /buses | Browse buses | No |
| POST | /bus/book | Initiate bus booking | Yes |
| GET | /bus-checkout | Bus checkout page | Yes |
| POST | /bus-pay | Confirm bus booking | Yes |
| GET | /cabs | Browse cabs | No |
| POST | /cab/book | Initiate cab booking | Yes |
| GET | /cab-checkout | Cab checkout page | Yes |
| POST | /cab-pay | Confirm cab booking | Yes |
| GET | /wishlist | View wishlist | Yes |
| POST | /wishlist/add/\<id\> | Add to wishlist | Yes |
| POST | /wishlist/remove/\<id\> | Remove from wishlist | Yes |
| POST | /package/\<id\>/review | Submit review | Yes |
| GET/POST | /contact | Contact support form | No |
| GET | /admin | Admin dashboard | Admin |
| POST | /admin/add | Add package | Admin |
| GET/POST | /admin/edit/\<id\> | Edit package | Admin |
| GET | /admin/delete/\<id\> | Delete package | Admin |
| GET/POST | /admin/booking/edit/\<id\> | Edit booking | Admin |
| GET | /admin/inquiries | View inquiries | Admin |
| POST | /admin/inquiries/acknowledge/\<id\> | Acknowledge inquiry | Admin |
| GET, POST | /admin/trains (add, edit, delete) | Train management | Admin |
| GET, POST | /admin/buses (add, edit, delete) | Bus management | Admin |
| GET, POST | /admin/cabs (add, edit, delete) | Cab management | Admin |
# Chapter 8: Implementation and Testing

## 8.1 Implementation Overview

The implementation of TravelEase was carried out in a phased manner, following the planned SDLC approach. The backend was developed using Flask in Python, with SQLAlchemy managing all database interactions. The frontend was built using Jinja2 templates, standard HTML5, CSS3, and JavaScript. No frontend framework was used, keeping the dependency footprint minimal.

The development sequence prioritised foundational modules first:

1. Database schema and model definitions (`models.py`)
2. Application configuration and database fallback logic (`config.py`)
3. User authentication routes (register, login, logout)
4. Package listing, search, and detail view
5. Package checkout and booking flow
6. Transport modules (flight, train, bus, cab)
7. User dashboard
8. Auxiliary features (wishlist, reviews, spin wheel, chatbot)
9. Admin panel routes
10. Contact and inquiry management
11. Docker deployment configuration

## 8.2 Student (User) Panel Implementation

The user panel of TravelEase provides the following implemented features:

**Home Page and Package Browsing**
The home page fetches all packages from the database with pagination (10 per page). Each package card displays the name, image, duration, price, and discount badge if applicable. A spin-wheel offer widget is available on the home page, which generates a daily discount code when clicked.

**Package Details**
Each package has a dedicated detail page showing the full description, day-by-day itinerary, hotel details and amenities, included sightseeing options, popular places, and an image gallery. The average user rating and all approved reviews are displayed below the package information.

**Search and Filter**
The search page accepts a text keyword, minimum price, and maximum price as filters. Results are sorted by newest, cheapest, or most expensive depending on the user's selection. Pagination is applied to search results as well.

**Package Checkout and Payment**
The checkout page pre-fills the number of travellers from session data and displays the total cost including any active spin-wheel discount. Payment accepts credit or debit card details (validated for format, expiry, and CVV) or UPI. On successful validation, a Booking record is created in the database and the user is redirected to the dashboard.

**Transport Booking**
Each transport category (flights, trains, buses, cabs) follows the same pattern: the user selects a route and date on the listing page, chooses a travel class and number of travellers, is redirected to a category-specific checkout page, and completes payment. The class-based multiplier system computes the final fare as follows:

| Class | Multiplier |
|---|---|
| Economy / Standard | 1.0Ã— base price |
| Premium / Comfort | 1.3â€“1.4Ã— base price |
| Business / Luxury | 1.8â€“2.2Ã— base price |

**User Dashboard**
The dashboard displays all booking categories in separate paginated sections: Holiday Packages, Flights, Trains, Buses, and Cabs. Each entry shows booking date, destination/route, class, number of travellers, status, and total amount paid.

**Wishlist and Reviews**
Users can add packages to a wishlist from the detail page. The wishlist page shows saved packages with the option to remove them. The review form on the package detail page allows a single rating and comment per user per package. Duplicate review attempts are blocked with a flash warning.

**Chatbot**
The chatbot widget floats on all pages as a collapsible panel. On opening, suggestion chips are displayed for common queries. The user can type a question or click a chip, and the response is displayed with a realistic typing indicator. Responses support bold, italic, and bullet formatting rendered from the backend Markdown-like syntax.

## 8.3 Admin Panel Implementation

The admin panel is accessible only to users with `is_admin = True`. The admin dashboard consolidates all operational views on a single paginated page.

**Package Management**
Admins can add a new package by filling a form that captures name, description, price, duration, image URL, hotel details, sightseeing, popular places, itinerary, hotel amenities, discount percentage, and additional images. Existing packages can be edited in a pre-filled edit form or deleted. Deletion removes the package from the database; associated bookings reference the package ID and are retained for record purposes.

**Transport Management**
Separate management pages exist for trains, buses, and cabs. Each page lists existing records and provides forms to add new entries. Each record can be edited in an edit form or deleted. Flights are currently managed at the database/seed level and are visible in bookings but do not have a dedicated add/edit admin form in the current version.

**Booking Management**
The admin can view all booking records from all users. Each booking record shows user information, package name, date, number of members, and status. The admin can edit the number of members and update the status of a booking (for example, from Confirmed to Cancelled). The total price is automatically recalculated based on the updated member count.

**Inquiry Management**
The inquiries page lists all contact form submissions in reverse chronological order. Each inquiry shows the sender's name, email, subject, message, and current status. The admin can mark any inquiry as "Acknowledged" to track resolution progress.

## 8.4 Test Cases and Results

**Table 10 â€“ Test Cases and Results**

| TC No. | Module | Test Description | Input | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| TC-01 | Registration | Register with valid details | username, email, password | Account created, redirect to login | Account created, redirected to login | PASS |
| TC-02 | Registration | Register with duplicate email | Existing email | Flash warning shown | Flash warning shown | PASS |
| TC-03 | Login | Login with correct credentials | Valid email + password | Session created, redirect to dashboard | Redirected to dashboard | PASS |
| TC-04 | Login | Login with wrong password | Valid email + wrong password | Flash "Invalid credentials" | Flash shown | PASS |
| TC-05 | Admin Access | Non-admin accessing /admin | Regular user session | Redirect to index with "Access denied" | Redirected | PASS |
| TC-06 | Package Booking | Book a package with 2 members | Package ID, 2 travellers | Booking saved with 2Ã— price | Booking created correctly | PASS |
| TC-07 | Spin Wheel | Spin once and get a discount code | First spin of the day | Discount code generated | Code generated and stored in session | PASS |
| TC-08 | Spin Wheel | Spin twice in the same day | Second spin attempt | Existing offer returned, not re-spun | Existing offer returned | PASS |
| TC-09 | Checkout | Apply spin discount at checkout | Active 10% discount, 2 travellers | 10% deducted from total | Amount correctly reduced | PASS |
| TC-10 | Card Validation | Submit checkout with invalid card | 12-digit card number | Form validation error | Validation error shown | PASS |
| TC-11 | Chatbot | Budget query | "packages under 20000" | List of packages at or below â‚¹20,000 | Correct packages returned | PASS |
| TC-12 | Chatbot | Destination query | "show packages for Goa" | Packages matching "Goa" | Goa packages returned | PASS |
| TC-13 | Wishlist | Add package to wishlist | Click "Add to Wishlist" | Package added, confirmed by flash | Added successfully | PASS |
| TC-14 | Wishlist | Add duplicate | Same package second time | Flash "already in wishlist" | Info message shown | PASS |
| TC-15 | Review | Submit a review | Rating 4, comment text | Review saved, shown on package page | Review saved | PASS |
| TC-16 | Review | Submit duplicate review | Same package, same user | Flash "already reviewed" | Warning shown | PASS |
| TC-17 | Transport | Book a train with Economy class | Train ID, Economy class, 1 traveller | Booking at 1.0Ã— base price | Correct price booked | PASS |
| TC-18 | Transport | Book a bus with Comfort class | Bus ID, Comfort class, 2 travellers | Booking at 1.3Ã— base Ã— 2 | Correct fare computed | PASS |
| TC-19 | Admin â€“ Package | Add a new package | Form data | Package appears in listing | Package added and listed | PASS |
| TC-20 | Admin â€“ Package | Delete a package | Package ID | Package removed from listing | Package deleted | PASS |
| TC-21 | DB Fallback | Start app without MySQL | No MySQL running | App uses SQLite automatically | SQLite selected at startup | PASS |
| TC-22 | Search | Filter by price range | min=5000, max=15000 | Only packages within range shown | Correct results returned | PASS |

## 8.5 Bugs Found and Fixed

**Table 11 â€“ Bugs Found and Fixed**

| Bug No. | Module | Bug Description | Root Cause | Fix Applied |
|---|---|---|---|---|
| BUG-01 | DB Config | App crashed on startup if MySQL was not reachable | Config assumed MySQL was always available | Added `_mysql_reachable()` check in `config.py` with SQLite fallback |
| BUG-02 | Spin Wheel | Offer was not invalidated after midnight (old date still valid) | Date comparison not implemented | Added `spin_date` field and daily date validation in `_get_active_spin_offer()` |
| BUG-03 | Checkout | Spin discount applied twice if page was reloaded | Offer not marked as used immediately | `offer['used'] = True` set in session before redirect after booking |
| BUG-04 | Review | Users could submit multiple reviews for same package | No duplicate check existed | Added `Review.query.filter_by(user_id, package_id).first()` check before saving |
| BUG-05 | Admin | Admin could access other admin routes if `is_admin` was revoked mid-session | Session not invalidated on role change | `ensure_admin()` checks `current_user.is_admin` on every request, not just login |
| BUG-06 | Transport Fare | Fare computed as 0 when class multiplier key not found | Missing fallback for unknown class strings | `multipliers.get(travel_class, 1.0)` default added in `compute_price()` |
| BUG-07 | Chatbot | Bot returned "None" as text when all three layers failed | `reply` variable not guaranteed to be a string | Added `reply = ai_reply if ai_reply else _fallback_chat_reply(user_message)` |
| BUG-08 | Registration | Unhandled exception if DB commit failed | Raw `except:` without rollback | `db.session.rollback()` added in all booking and registration exception handlers |

---

# Chapter 9: Building and Deployment

## 9.1 System Requirements

**For Local Deployment:**
- Python 3.9 or later
- pip (Python package manager)
- MySQL 8.0 (or run without it; SQLite fallback will activate)
- A modern web browser

**For Docker Deployment:**
- Docker Desktop 20.10 or later
- Docker Compose (included in Docker Desktop)

## 9.2 Installation Steps

### Local Installation

**Step 1 â€“ Clone or Copy the Project**

Copy the `holiday_booking` folder to the desired working directory.

**Step 2 â€“ Create a Python Virtual Environment**

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux / macOS
```

**Step 3 â€“ Install Dependencies**

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```
Flask
Flask-SQLAlchemy
Flask-Login
PyMySQL
email_validator
werkzeug
cryptography
```

**Step 4 â€“ Configure Environment Variables**

Create a `.env` file or set the following environment variables:

```
SECRET_KEY=your_secure_secret_key
DATABASE_URL=mysql+pymysql://username:password@localhost/holiday_booking
OPENAI_API_KEY=sk-...  (optional â€“ enables AI chatbot layer)
```

If MySQL is not available, the system will automatically fall back to SQLite. No additional environment variable is needed to enable this.

**Step 5 â€“ Set Up the Database**

```bash
python setup_db.py
python seed_packages.py
python populate_package_details.py
```

These scripts create all tables, insert transport seed data, and populate sample holiday packages.

**Step 6 â€“ Create an Admin Account**

The admin account is set by manually updating a user record's `is_admin` field in the database, or by running:

```bash
python fix_admin.py
```

### Docker Deployment

**Step 1 â€“ Build and Start Containers**

```bash
docker compose up --build
```

This starts two services defined in `compose.yml`:

- `db` â€“ MySQL 8.0 database container
- `web` â€“ Flask application container

**Step 2 â€“ Automatic Initialisation**

The `docker-entrypoint.sh` script runs automatically inside the `web` container. It:

1. Waits for the `db` service to become ready.
2. Runs migration scripts to create tables.
3. Runs seed scripts to populate initial data.
4. Starts the Flask application via the WSGI server.

## 9.3 How to Run the Project

### Local Run

```bash
python app.py
```

The Flask development server starts at `http://127.0.0.1:5000`. Open this URL in a browser to access the application.

### Docker Run

After `docker compose up --build`, the application is accessible at `http://localhost:5000`.

To stop the containers:

```bash
docker compose down
```

To stop and remove all data (including the database volume):

```bash
docker compose down -v
```

## 9.4 Project Folder Structure

**Table 12 â€“ Project Folder Structure**

```
holiday_booking/
â”‚
â”œâ”€â”€ app.py                   # Main Flask application file (routes, chatbot, utils)
â”œâ”€â”€ models.py                # SQLAlchemy model classes
â”œâ”€â”€ config.py                # Application configuration and DB fallback logic
â”œâ”€â”€ database.sql             # SQL schema reference file
â”œâ”€â”€ requirements.txt         # Python package dependencies
â”‚
â”œâ”€â”€ setup_db.py              # Database initialisation script
â”œâ”€â”€ seed_packages.py         # Package seeding script
â”œâ”€â”€ populate_package_details.py  # Detailed package data population
â”œâ”€â”€ migrate_db.py            # Schema migration script
â”œâ”€â”€ fix_admin.py             # Admin account configuration script
â”‚
â”œâ”€â”€ Dockerfile               # Docker image build instructions
â”œâ”€â”€ compose.yml              # Docker Compose service definitions
â”œâ”€â”€ docker-entrypoint.sh     # Container startup and init script
â”‚
â”œâ”€â”€ instance/
â”‚   â””â”€â”€ holiday_booking.db   # SQLite fallback database (auto-created)
â”‚
â”œâ”€â”€ static/
â”‚   â”œâ”€â”€ css/                 # Stylesheets
â”‚   â”œâ”€â”€ js/
â”‚   â”‚   â””â”€â”€ chatbot.js       # Chatbot frontend logic
â”‚   â””â”€â”€ images/
â”‚       â””â”€â”€ transport/       # Transport category images (cabs, buses, trains)
â”‚
â”œâ”€â”€ templates/
â”‚   â”œâ”€â”€ index.html           # Home page
â”‚   â”œâ”€â”€ login.html           # Login page
â”‚   â”œâ”€â”€ register.html        # Registration page
â”‚   â”œâ”€â”€ package_details.html # Package detail page
â”‚   â”œâ”€â”€ checkout.html        # Package checkout page
â”‚   â”œâ”€â”€ dashboard.html       # User booking dashboard
â”‚   â”œâ”€â”€ flights.html         # Flight listing page
â”‚   â”œâ”€â”€ flight_checkout.html # Flight checkout page
â”‚   â”œâ”€â”€ trains.html          # Train listing page
â”‚   â”œâ”€â”€ train_checkout.html  # Train checkout page
â”‚   â”œâ”€â”€ buses.html           # Bus listing page
â”‚   â”œâ”€â”€ bus_checkout.html    # Bus checkout page
â”‚   â”œâ”€â”€ cabs.html            # Cab listing page
â”‚   â”œâ”€â”€ cab_checkout.html    # Cab checkout page
â”‚   â”œâ”€â”€ wishlist.html        # Wishlist page
â”‚   â”œâ”€â”€ contact.html         # Contact/support page
â”‚   â”œâ”€â”€ admin_dashboard.html # Admin overview page
â”‚   â”œâ”€â”€ admin_inquiries.html # Admin inquiry management
â”‚   â”œâ”€â”€ edit_booking.html    # Admin booking edit page
â”‚   â””â”€â”€ ...                  # Additional admin and detail templates
â”‚
â”œâ”€â”€ SYNOPSIS_2.md            # Detailed project synopsis
â”œâ”€â”€ FINAL_REPORT_DRAFT.md    # Report draft reference
â””â”€â”€ README.md                # Quick-start documentation
```

---

# Chapter 10: Limitations of the Project

TravelEase successfully fulfils its academic objectives. However, honest evaluation reveals several boundaries that define where the current implementation ends and where future development should continue.

## 10.1 Functional Limitations

**Payment Processing:** The current checkout flow validates card input fields for format correctness (number length, expiry format, CVV length) and accepts UPI text input, but no actual financial transaction is executed. There is no integration with a real payment gateway such as Razorpay, Stripe, or PayPal. Booking records are created upon validation success, simulating a confirmed payment. For a production system, a real gateway with webhook-based payment status confirmation would be mandatory.

**Cancellation and Refund Workflow:** Once a booking is confirmed, users cannot cancel it themselves. The admin can update the booking status field to "Cancelled", but there is no automated refund calculation, policy enforcement (for example, 48-hour cancellation window), or reversal of payment records. A full cancellation engine is not implemented.

**Booking Modification:** Users cannot reschedule a transport booking or change the number of travellers after confirmation. Self-service modification workflows require significant additional business logic and are beyond the current scope.

**No Email or SMS Notifications:** Booking confirmations, reminders, and support responses are communicated only through on-screen flash messages. No email or SMS delivery is integrated. A production system would typically use a service such as SendGrid or Twilio for transactional communications.

**Static Inventory:** Package and transport data is either seeded from scripts or managed through the admin panel. There is no real-time synchronisation with external providers. Flight availability, for example, is not pulled from any airline API.

## 10.2 Technical Limitations

**Monolithic Route Structure:** All route handlers reside in a single `app.py` file of approximately 1,676 lines. While this is manageable at the current scale and appropriate for academic evaluation, a production application would benefit from Flask Blueprints to separate routes by domain (authentication, booking, admin, transport).

**No Migration Framework:** Database schema changes are managed through custom migration scripts (`migrate_db.py`). A production system would use Flask-Migrate (Alembic) for versioned, rollback-capable schema migrations.

**Chatbot Intelligence:** The chatbot's database-aware layer performs keyword and regex matching, which works well for common queries but cannot understand complex or ambiguous natural-language questions. Advanced intent classification, entity extraction, conversation memory, and multi-turn dialogue are not implemented.

**Two-Tier Role Model:** The system recognises only two roles: regular user and admin. Enterprise platforms typically have more granular roles such as support agent, content manager, or financial auditor, each with different levels of access.

**No Rate Limiting:** The chatbot endpoint (`/chatbot/ask`) and the spin-wheel endpoint (`/offers/spin`) do not have API rate limiting. A malicious actor could potentially flood these endpoints in a production environment.

## 10.3 Testing and Quality Assurance Limitations

**No Automated E2E Tests:** Core booking flows are verified through custom Python scripts (`verify_checkout_logic.py`, `verify_packages.py`) and manual testing. A comprehensive test suite using Pytest with browser automation (for example, Playwright or Selenium) is not yet in place.

**No Security Testing:** Formal penetration testing, OWASP Top 10 vulnerability scanning, and threat-model-driven security reviews have not been carried out. SQL injection protection is inherent in SQLAlchemy's parameterised queries, but other attack vectors have not been systematically validated.

**No CI/CD Pipeline:** There is no continuous integration setup (for example, GitHub Actions) that runs tests automatically on every code commit. Code quality gates, test coverage thresholds, and automated deployment pipelines are outside the current scope.

## 10.4 Operational Limitations

**No Disaster Recovery Plan:** Database backup rotation, restore drills, and replication strategy for high availability are not formalised. The Docker-based deployment does not include automated backup scheduling.

**No Centralised Logging:** Application logs are written to the local server console. There is no integration with a centralised logging platform such as ELK Stack or Datadog, which would be necessary for diagnosing issues in a multi-instance deployment.

**Cloud Deployment Not Hardened:** The application has not been configured for cloud-native production deployment with environment-specific secrets management, HTTPS enforcement, or load balancing.

---

# Chapter 11: Conclusions and Future Work

## 11.1 Conclusions

TravelEase represents a complete, academically rigorous implementation of a web-based holiday and transport booking management system. From user registration and package discovery through to payment simulation, booking history, and administrative oversight, the system demonstrates a coherent full-stack application lifecycle.

The project successfully met every stated objective. An end-to-end booking workflow was delivered supporting multiple transport categories. Secure role-based access control distinguishes user and admin operations. A normalised relational schema maintains data consistency across all booking types. Supplementary featuresâ€”chatbot, wishlist, reviews, and spin-wheel discountsâ€”improve user engagement and reflect practical product thinking beyond a minimal prototype. Docker-based deployment with MySQL-to-SQLite fallback demonstrates deployment awareness and engineering resilience.

From a software engineering perspective, the project establishes clear separation of responsibilities across model, view, and controller layers; maintains consistency in route design; and applies established security practices such as password hashing and session-signed cookies. The codebase is structured to permit incremental feature addition without structural disruption.

TravelEase is not a replacement for commercial booking platforms, but as an academic project it fulfils its purpose: demonstrating mastery of web application development, database design, backend engineering, and end-to-end system thinking within the scope of the Master of Computer Applications programme.

## 11.2 Future Work

The following enhancements are planned for future development phases, ordered by priority and complexity:

**Short-Term Enhancements:**

1. **Real Payment Gateway Integration:** Integration with Razorpay or Stripe with webhook-based payment confirmation, transaction ID storage, and receipt generation. This is the highest-priority production requirement.

2. **Email Notifications:** Booking confirmation emails, cancellation alerts, and inquiry response emails using Flask-Mail with an SMTP provider such as Gmail or SendGrid.

3. **User-Initiated Cancellation:** A self-service cancellation flow with policy-based refund calculation (for example, 100% refund if cancelled 7+ days before travel, 50% within 7 days, and no refund within 24 hours).

4. **Flask Blueprints Refactoring:** Reorganising routes into Blueprint modules (`auth`, `booking`, `transport`, `admin`) for better maintainability as the codebase grows.

**Medium-Term Enhancements:**

5. **Recommendation Engine:** A basic package recommendation system using collaborative filtering on wishlist and booking history data to suggest relevant packages to returning users.

6. **Advanced Analytics Dashboard:** Admin-facing charts displaying booking trends by destination, revenue by transport category, daily active users, and conversion rates from browse to booking.

7. **Automated Testing Suite:** A complete test suite using Pytest for backend unit and integration tests, with Playwright for end-to-end browser automation. CI enforcement through GitHub Actions.

8. **Enhanced Chatbot:** Intent classification using a lightweight NLP model, multi-turn conversation memory, and support for queries in additional Indian languages.

**Long-Term Enhancements:**

9. **Cloud Deployment Architecture:** Containerised deployment on a cloud platform (AWS, GCP, or Azure) with load balancing, auto-scaling, managed MySQL (RDS), centralised logging, and secrets management via environment injection.

10. **Mobile Application:** A responsive progressive web app (PWA) version, or a dedicated React Native mobile application, enabling the complete booking experience from a smartphone with native push notification support.

11. **Multi-Role Access Control:** Expansion of the role model to include support agent (can acknowledge and respond to inquiries), content manager (can manage packages and images), and financial auditor (read-only access to booking and revenue data).

12. **Inventory Synchronisation:** Integration with external flight data APIs (such as Amadeus or Skyscanner API) and Indian Railways data for live availability, pricing, and seat reservation status.

---

# References

## Official Technical Documentation

1. Pallets Projects. (n.d.). *Flask Documentation*. Retrieved from https://flask.palletsprojects.com/

2. Pallets Projects. (n.d.). *Jinja2 Template Engine Documentation*. Retrieved from https://jinja.palletsprojects.com/

3. Flask-Login Contributors. (n.d.). *Flask-Login Documentation*. Retrieved from https://flask-login.readthedocs.io/

4. Flask-SQLAlchemy Contributors. (n.d.). *Flask-SQLAlchemy Documentation*. Retrieved from https://flask-sqlalchemy.palletsprojects.com/

5. SQLAlchemy Team. (n.d.). *SQLAlchemy 2.0 Documentation*. Retrieved from https://docs.sqlalchemy.org/

6. Python Software Foundation. (n.d.). *Python 3 Language Reference*. Retrieved from https://docs.python.org/3/

7. Oracle Corporation. (n.d.). *MySQL 8.0 Reference Manual*. Retrieved from https://dev.mysql.com/doc/

8. SQLite Consortium. (n.d.). *SQLite Documentation*. Retrieved from https://www.sqlite.org/docs.html

9. Docker Inc. (n.d.). *Docker Documentation*. Retrieved from https://docs.docker.com/

10. Werkzeug Contributors. (n.d.). *Werkzeug WSGI Utility Library*. Retrieved from https://werkzeug.palletsprojects.com/

11. OWASP Foundation. (n.d.). *OWASP Authentication Cheat Sheet*. Retrieved from https://cheatsheetseries.owasp.org/

12. OpenAI. (n.d.). *OpenAI API Reference â€“ Chat Completions*. Retrieved from https://platform.openai.com/docs/

## Books and Academic References

13. Grinberg, M. (2018). *Flask Web Development: Developing Web Applications with Python* (2nd ed.). O'Reilly Media.

14. Copeland, R. (2008). *Essential SQLAlchemy*. O'Reilly Media.

15. Pilgrim, M. (2009). *Dive Into Python 3*. Apress.

## Project Source Files (Internal References)

16. Route logic and chatbot implementation: `app.py`

17. Data model definitions: `models.py`

18. Database connection configuration: `config.py`

19. SQL schema reference: `database.sql`

20. Container configuration: `Dockerfile`, `compose.yml`, `docker-entrypoint.sh`

21. Project quick-start guide: `README.md`
