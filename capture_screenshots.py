import os
import subprocess
import time
from playwright.sync_api import sync_playwright

def run_app_and_capture():
    # Make directory for screenshots
    os.makedirs('screenshots', exist_ok=True)
    
    print("Starting Flask app...")
    # Start flask app - setting environment variables if needed
    env = os.environ.copy()
    env["FLASK_APP"] = "app.py"
    process = subprocess.Popen(["python", "app.py"], env=env)
    
    # Wait for flask to start
    time.sleep(8) 

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={'width': 1440, 'height': 900})
            page = context.new_page()

            def capture(url_path, name):
                try:
                    print(f"Capturing {name}...")
                    page.goto(f"http://127.0.0.1:5000{url_path}")
                    time.sleep(2)
                    page.screenshot(path=f"screenshots/{name}.png")
                except Exception as e:
                    print(f"Failed to capture {name}: {e}")

            capture("/", "home")
            capture("/login", "login")
            capture("/register", "register")
            capture("/contact", "contact")
            
            # Package detail
            capture("/package/1", "package_detail")
            
            # Register test user
            try:
                print("Registering test user...")
                page.goto("http://127.0.0.1:5000/register")
                page.fill("input[name='username']", "PPT_Demo_User")
                page.fill("input[name='email']", "ppt@example.com")
                page.fill("input[name='password']", "password123")
                page.fill("input[name='confirm_password']", "password123")
                page.click("button[type='submit']")
                time.sleep(2)
                
                print("Logging in...")
                page.goto("http://127.0.0.1:5000/login")
                page.fill("input[name='email']", "ppt@example.com")
                page.fill("input[name='password']", "password123")
                page.click("button[type='submit']")
                time.sleep(2)
                
                capture("/dashboard", "dashboard")
                capture("/flights", "flights")
            except Exception as e:
                print(f"Failed to capture user areas: {e}")
            
            browser.close()
    except Exception as e:
        print(f"Error during capturing: {e}")
    finally:
        print("Terminating Flask app...")
        process.terminate()
        process.wait()

if __name__ == "__main__":
    run_app_and_capture()
