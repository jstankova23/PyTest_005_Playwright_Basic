# TESTOVÁNÍ MOBILNÍCH ZAŘÍZENÍ

# Test přesměrování kliknutím na link "Výukový portál" po otevření hlavního menu přes ikonku hamburger menu ve vybraných typech mobilů
# přesné názvy vestavěných mobilních zařízení lze zjistit z devices.py;
# testovací funkce používá fixture 'mobile_page', která volá parametrizovanou fixture 'mobile_device';
# definice fixtures jsou uvedeny v souboru conftest.py

from playwright.sync_api import Page

def test_mobile_menu(mobile_page: Page):
    hamburger_menu = mobile_page.locator("#main-header label").nth(4) # vyhledání ikonky hamburger menu dle lokátoru z Playwright Inspectoru

    if hamburger_menu.is_visible():                         # pokud je ikonka menu v mobilu viditelná,
        hamburger_menu.click()                              # otevřít hamburger menu kliknutím
        mobile_page.wait_for_timeout(500)                   # krátká pauza pro stabilizaci nové nabídky

    link = mobile_page.get_by_role("link", name="Výukový portál") # vyhledání odkazu pomocí funkčního lokátoru podle role 'link'

    assert link.is_visible(), "Chyba"  # kontrola viditelnosti linku a případná chybová hláška










