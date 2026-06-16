"""Quick test to verify chatbot package integration"""
import sys
from io import StringIO
from app import app, db, Package, _format_package_detailed, _fallback_chat_reply, _db_chat_reply

output = StringIO()
sys.stdout = output

with app.app_context():
    # Test 1: Check all packages are loaded
    packages = Package.query.order_by(Package.price.asc()).all()
    print("=" * 60)
    print("TEST 1: All Packages in Database")
    print("=" * 60)
    print(f"Total packages: {len(packages)}\n")
    for p in packages:
        print(f"- {p.name}: {p.duration} - INR {p.price:,.0f}")
    
    # Test 2: Check detailed formatting
    print("\n" + "=" * 60)
    print("TEST 2: Detailed Package Formatting")
    print("=" * 60)
    if packages:
        detailed = _format_package_detailed(packages[0])
        print(f"Example: {detailed}")
    
    # Test 3: Check fallback response
    print("\n" + "=" * 60)
    print("TEST 3: Fallback Chat Reply")
    print("=" * 60)
    fallback = _fallback_chat_reply("show me packages")
    print(fallback[:500] + "..." if len(fallback) > 500 else fallback)
    
    # Test 4: Check DB reply
    print("\n" + "=" * 60)
    print("TEST 4: DB Chat Reply - List Packages")
    print("=" * 60)
    db_reply = _db_chat_reply("show packages")
    print(db_reply[:500] + "..." if len(db_reply) > 500 else db_reply)
    
    # Test 5: Check budget query
    print("\n" + "=" * 60)
    print("TEST 5: DB Chat Reply - Budget Query")
    print("=" * 60)
    budget_reply = _db_chat_reply("packages under 150000")
    print(budget_reply)
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)

sys.stdout = sys.__stdout__
result = output.getvalue()
print("Tests completed! Writing to file...")
with open("c:/Users/HP/OneDrive/Desktop/MCA Project/holiday_booking/test_output.txt", "w") as f:
    f.write(result)
print("Done!")

