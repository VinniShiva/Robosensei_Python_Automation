import re
from playwright.sync_api import Page, expect
class RegisterPage:

    def __init__(
        self,
        page: Page,
        base_url: str,
        login_path: str,
        profile_path: str,
        first_name: str,
        last_name: str
    ):
        self.page = page
        # Application URLs
        self.base_url = base_url.rstrip("/")
        self.login_url = f"{self.base_url}/{login_path.lstrip('/')}"
        self.profile_url = f"{self.base_url}/{profile_path.lstrip('/')}"
        # Registration locators
        self.register_link = page.get_by_test_id("layout-register-link")
        self.first_name = page.get_by_test_id("register-firstname")
        self.last_name = page.get_by_test_id("register-lastname")
        self.email = page.get_by_test_id("register-email")
        self.country = page.get_by_test_id("register-country")
        self.password = page.get_by_test_id("register-password")
        self.confirm_password = page.get_by_test_id(
            "register-confirm-password"
        )
        self.register_button = page.get_by_test_id(
            "register-submit-button"
        )
        # Login locators
        self.sign_in_button = page.get_by_test_id("login-signin-button")
        self.login_email = page.get_by_test_id("login-email")
        self.login_password = page.get_by_test_id("login-password")
        self.login_button = page.get_by_test_id("login-submit-button")
        # User profile locator
        full_name = f"{first_name} {last_name}"
        self.user_profile = page.get_by_role(
            "link",
            name=full_name
        ).first
        # Logout locator
        self.logout_button = page.get_by_text("Logout", exact=True)
    def verify_dashboard(self):
        expect(self.page).to_have_url(
            f"{self.base_url}/",
            timeout=20000
        )
    def click_user_profile(self):
        expect(self.user_profile).to_be_visible(timeout=20000)
        self.user_profile.click()

        expect(self.page).to_have_url(
            re.compile(rf"^{re.escape(self.profile_url)}/?$"),
            timeout=20000
        )
    def click_logout(self):
        expect(self.logout_button).to_be_visible(timeout=20000)
        self.logout_button.click()
        # Allow query parameters such as ReturnUrl after logout
        expect(self.page).to_have_url(
            re.compile(
                rf"^{re.escape(self.login_url)}(?:\?.*)?$"
            ),
            timeout=30000
        )
