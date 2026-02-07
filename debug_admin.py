from app import app, User

def list_users():
    with app.app_context():
        users = User.query.all()
        print(f"Total Users: {len(users)}")
        for u in users:
            print(f"ID: {u.id} | Username: {u.username} | Email: {u.email} | Is Admin: {u.is_admin}")

if __name__ == "__main__":
    list_users()
