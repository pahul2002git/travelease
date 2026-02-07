from app import app, Package

def verify_packages():
    with app.app_context():
        packages = Package.query.all()
        print(f"Total Packages: {len(packages)}")
        for p in packages:
            print(f"- {p.name} (${p.price}): {p.image_url[:50]}...")

if __name__ == "__main__":
    verify_packages()
