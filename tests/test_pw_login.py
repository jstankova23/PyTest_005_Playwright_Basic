# Test přihlášení na stránce https://demoqa.com/login a přesměrování na cílovou stránku https://demoqa.com/profile
# testovací funkce volá fixture page z conftest.py, která je univerzální - není spjata s žádnou URL;
# přechod na požadovanou stránku je tedy součástí samotné testovací funkce
from playwright.sync_api import Page, expect

def test_login(page: Page):
    # 1) otevření login stránky
    page.goto("https://demoqa.com/login")

    # 2) vyplnění přihlašovacích údajů
    page.get_by_placeholder("UserName").fill("TestUser")
    page.get_by_placeholder("Password").fill("TestPassword123!")

    # 3) kliknutí na tlačítko Login
    page.get_by_role("button", name="Login").click()

    # 4) ověření přesměrování na cílovou URL
    expect(page).to_have_url("https://demoqa.com/profile")

    # 5) ověření, že se na stránce zobrazuje jméno přihlášeného uživatele
    username_label = page.locator("#userName-value")
    expect(username_label).to_be_visible()
    assert username_label.inner_text() == "TestUser"

