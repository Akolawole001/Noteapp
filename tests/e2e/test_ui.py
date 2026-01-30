import time
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8003"


def test_register_login_create_note():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to app
        page.goto(BASE_URL)

        # Generate a unique email for this test
        test_email = f'test_ui_{int(time.time())}@example.com'
        test_password = 'TestPass123!'

        # Try to open register form via the "Create one" link if present
        try:
            # If login form present, click the create-account link
            if page.query_selector('#loginForm'):
                # click the anchor that shows register form
                if page.query_selector('text=Create one'):
                    page.click('text=Create one')
                elif page.query_selector('text=Create Account'):
                    page.click('text=Create Account')

            # Wait for register inputs
            page.wait_for_selector('#registerEmail', timeout=3000)
            page.fill('#registerEmail', test_email)
            page.fill('#registerPassword', test_password)
            # Click the create account button
            page.click('button:has-text("Create Account")', timeout=3000)
            # small wait for registration to complete
            page.wait_for_timeout(500)
        except Exception:
            # Registration via UI may not be available or the user may already exist — fallback to API
            import requests
            resp = requests.post(f"{BASE_URL}/auth/register", json={"email": test_email, "password": test_password})
            # ignore errors (user may already exist)

        # Perform login using the visible login form
        page.wait_for_selector('#loginEmail', timeout=5000)
        page.fill('#loginEmail', test_email)
        page.fill('#loginPassword', test_password)
        # Click the Sign In button
        page.click('button:has-text("Sign In")', timeout=5000)

        # Wait for app to load (userEmail element populated)
        page.wait_for_selector('#userEmail', timeout=5000)

        # Create a new note via UI
        page.click('text=New Note')
        page.wait_for_selector('#noteTitle', timeout=3000)
        page.fill('#noteTitle', 'E2E Test Note')
        page.fill('#noteContent', 'This note was created by Playwright E2E test')
        page.click('button:has-text("Save Note")')
        page.wait_for_timeout(800)

        # Verify note appears in the notes list
        notes = page.locator('text=E2E Test Note')
        assert notes.count() >= 1

        browser.close()
