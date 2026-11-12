import os
import re
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import Page
from pages.Register import RegisterPage

# Load .env from the project root
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

def get_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Missing environment variable: {key}")
    return value
# Application configuration
BASE_URL = get_env("BASE_URL")
LOGIN_PATH = get_env("LOGIN_PATH")
PROFILE_PATH = get_env("PROFILE_PATH")
# Registration test data
FIRST_NAME = get_env("REGISTER_FIRST_NAME")
LAST_NAME = get_env("REGISTER_LAST_NAME")
EMAIL = get_env("REGISTER_EMAIL")
COUNTRY = get_env("REGISTER_COUNTRY")
PASSWORD = get_env("REGISTER_PASSWORD")
CONFIRM_PASSWORD = get_env("REGISTER_CONFIRM_PASSWORD")

# Build application URLs
LOGIN_URL = f"{BASE_URL.rstrip('/')}/{LOGIN_PATH.lstrip('/')}"
PROFILE_URL = f"{BASE_URL.rstrip('/')}/{PROFILE_PATH.lstrip('/')}"

def test_registration_login_logout(page: Page):
    register = RegisterPage(
        page=page,
        base_url=BASE_URL,
        login_path=LOGIN_PATH,
        profile_path=PROFILE_PATH,
        first_name=FIRST_NAME,
        last_name=LAST_NAME
    )
    # 1. Open Login Page
    page.goto(
        LOGIN_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )
    # 2. Navigate to Registration Page
    register.register_link.click()
    # 3. Fill Registration Details
    register.first_name.fill(FIRST_NAME)
    register.last_name.fill(LAST_NAME)
    register.email.fill(EMAIL)
    register.country.select_option(COUNTRY)
    register.password.fill(PASSWORD)
    register.confirm_password.fill(CONFIRM_PASSWORD)
    # 4. Submit Registration
    register.register_button.click()
    # 5. Verify Sign In Button
    register.sign_in_button.wait_for(
        state="visible",
        timeout=20000
    )
    # 6. Navigate to Sign In
    register.sign_in_button.click()
    # 7. Enter Login Credentials
    register.login_email.fill(EMAIL)
    register.login_password.fill(PASSWORD)
    # 8. Submit Login
    register.login_button.click()
    # 9. Verify Dashboard
    register.verify_dashboard()
    # 10. Open User Profile and verify Profile Page
    register.click_user_profile()
    # 11. Logout and verify Login Page
    register.click_logout()
