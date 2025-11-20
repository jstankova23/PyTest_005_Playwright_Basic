# Test ověřuje, že odkaz „Výukový portál“ je viditelný na stránce Engeto při spuštění v různých webových prohlížečích
# testovací funkce používá fixture 'browser_page', která volá parametrizovanou fixture 'browser_type';
# fixture 'browser_page' je parametrizovaná — test se spustí zvlášť v Chromiu, WebKitu a Firefoxu;
# definice fixtures jsou uvedeny v souboru conftest.py

from playwright.sync_api import Page

def test_browser_kompatibilita(browser_page: Page):
    link = browser_page.get_by_role("link", name="Výukový portál")  # vyhledání linku pomocí funkčního lokátoru
    assert link.is_visible()                                        # kontrola viditelnosti linku
