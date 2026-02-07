from app import app, db, User

def fix_admin_email():
    with app.app_context():
        admin = User.query.filter_by(email='admin@dreamvacations.com').first()
        if admin:
            admin.email = 'admin@travelease.com'
            db.session.commit()
            print("Successfully updated admin email to admin@travelease.com")
        else:
            print("Old admin email not found. Checking if correctly already set...")
            new_admin = User.query.filter_by(email='admin@travelease.com').first()
            if new_admin:
                 print("Admin email is already correct.")
            else:
                 print("No admin user found.")

if __name__ == "__main__":
    fix_admin_email()
