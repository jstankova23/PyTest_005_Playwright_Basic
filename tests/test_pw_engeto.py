# ZÁKLADNÍ TESTY STRÁNKY ENGETO S VYUŽITÍ FIXTURES A PARAMETRIZACE
# v parametru testovacích funcí je personalizovaná fixture pro zpracování cookies (page_cookies_engeto), nikoliv přímo vestavěná fixture page;
# personalizovaná fixture pro zpracování cookies je spojena s konkrétní URL pro Engeto a jejími specifickými lokátor pro cookie lištu a cookie tlačítka;
# personalizovaná fixture pro cookies volá vestavěnou fixture 'page', ta volá vestavěnou fixture 'context' a ta volá fixture 'browser';
# fixtures jsou definované v souboru conftest.py;

import pytest                           # import kvůli parametrizované testovací funkci test_presmerovani_a_navrat 
from playwright.sync_api import Page

# 1) Test pro ověření viditelnosti zvoleného nadpisu
def test_hlavni_nadpis_je_viditelny(page_cookies_engeto: Page):               
    nadpis = page_cookies_engeto.get_by_text("Děláme IT vzdělávání dostupný")  # vyhledání nadpisu podle funkčního lokátoru (lokátor z Playwright Inspectoru)
    assert nadpis.is_visible()                                  

# 2) Test pro ověření viditelnosti loga v hlavním menu
# selektor s ID #logo z DevTools není příliš flexibilní, v testu je raději uplatněn ručně vytvořený CSS atributový lokátor;
# <img> prvek (tag name), jehož atribut 'src' (třída) obsahuje (*=) slovo "logo";
# operátor *= → obsahuje
def test_viditelnost_loga(page_cookies_engeto: Page):
    logo = page_cookies_engeto.locator("img[src*='logo']")                      # vyhledání loga podle ručně vytvořeného CSS atributového lokátoru
    assert logo.is_visible()      

# 3) Test pro ověření viditelnosti odkazu na Výukový portál z hlavního menu
# selektor z DevTools není příliš flexibilní, v testu je raději uplatněn ručně vytvořený funkční lokátor podle ARIA role;
# ověřeno v DevTools, že link s textem "Výukový portál" je v HTTML struktuře opravdu označen s tag name <a> (anchor/link) s textem "Výukový portál";
def test_viditelnost_linku_vyukovy_portal(page_cookies_engeto: Page):
    link = page_cookies_engeto.get_by_role("link", name="Výukový portál")      # vyhledání odkazu podle ručně vytvořeného funkčního lokátoru podle ARIA role
    assert link.is_visible()  


# 4) Test ověření, že odkaz na Výukový portál v hlavním menu vede na správnou URL - kontrola atributu v HTML struktuře
# test nekontroluje kliknutí, ale z HTML struktury ověřuje, že atribut 'href' obsahuje očekávanou adresu;
# test pracuje s HTML strukturou:
# a) nejprve vyhledá odkaz (tag <a>) pomocí funkčního lokátoru;
# b) poté z tohoto odkazu získá hodnotu atributu 'href';
# c) závěrečný assert ověří, že hodnota atributu 'href' obsahuje očekávanou URL
def test_odkaz_na_spravnou_url(page_cookies_engeto: Page):
    link = page_cookies_engeto.get_by_role("link", name="Výukový portál")       # vyhledání odkazu pomocí funkčního lokátoru podle role 'link'
    href = link.get_attribute("href")                                           # získání hodnoty HTML atributu 'href' přímo z elementu <a> / link (nikoliv page)
    assert "https://portal.engeto.com/" in href                                 # ověření, že atribut 'href' obsahuje správnou cílovou URL


# 5) Test ověření, že odkaz na Výukový portál v hlavním menu vede na správnou URL - kontrola kliknutím
# test využívá vestavěnou funkci url()
def test_klik_na_odkaz(page_cookies_engeto: Page):
    link = page_cookies_engeto.get_by_role("link", name="Výukový portál")       # vyhledání odkazu pomocí funkčního lokátoru podle role 'link'
    link.click()
    assert "portal.engeto.com" in page_cookies_engeto.url, f"Test selhal: aktuální stránka je {page_cookies_engeto.url}"


# 6) Test skrolování myší, kliknutí na link Blog v zápatí domovské stránky a kontrola URL po přesměrování
# test obsahuje 2 části: ověření viditelnosti odkazu před kliknutím a ověření URL po přesměrování
def test_scroll_a_presmerovani_na_blog(page_cookies_engeto: Page):
    page_cookies_engeto.mouse.wheel(0, 5000)             # skrolování myší o 5000 pixelů dolů
    page_cookies_engeto.wait_for_timeout(1000)           # krátká pauza pro stabilizaci stránky (1 sekunda)

    odkazy = page_cookies_engeto.get_by_role("link", name="Blog", exact=True)   # vyhledání všech odkazů obsahujících přesně slovo "Blog"
    odkaz = odkazy.first                                            # výběr prvního nalezeného odkazu

    assert odkaz.is_visible(), f"Odkaz Blog není viditelný"         # kontrola viditelnosti odkazu před kliknutím
    odkaz.click()                                                   # kliknutí na odkaz (první nalezený)

    page_cookies_engeto.wait_for_load_state("networkidle")                         # čekání, dokud neproběhnou všechny síťové požadavky nové stránky
    assert "blog" in page_cookies_engeto.url, f"Skutečná adrese je {page_cookies_engeto.url}"  # ověření, že v názvu aktuální přesměrované url je obsaženo slovo "blog" 


# 7) Parametrizovaný test: kliknutí na odkazy v domovské stránce Engeta, kontrola URL po přesměrování a návrat zpět na domovskou stránku
# parametry definují název odkazu na domovské stránce z jeho zápatí a endpoint názvu URL spojené s daným odkazem;
# odkaz Blog přesměruje na https://engeto.cz/blog/, tzn. odkaz_text = "Blog", ocekavana_url = "blog";
# odkaz Reference přesměruje na https://engeto.cz/absolventi/, tzn. odkaz_text = "Reference", ocekavana_url = "absolventi";
# testovací funkce se spustí tolikrát, kolik dvojic hodnot je uvedeno v parametrize (v tomto případu se spustí 2 testy);
# každý běh testu pracuje s jiným názvem odkazu a jinou očekávanou částí URL
# metoda page.go_back() pro návrat pomocí šipky zpět v prohlížeči 
@pytest.mark.parametrize("odkaz_text, ocekavana_url", [
    ("Blog", "blog"),
    ("Reference", "absolventi")
])
def test_presmerovani_a_navrat(page_cookies_engeto: Page, odkaz_text: str, ocekavana_url: str):  # parametry obsahují proměnné parametrizace s uvedením, že se jedná o string
    # vyhledání prvního odkazu, jehož text obsahuje slovo zadané v parametrizaci pod proměnnou odkaz_test
    odkaz = page_cookies_engeto.get_by_role("link", name=odkaz_text, exact=False).first  # název linku se dotahuje z parametrizace (poprvé "Kariéra", podruhé "Blog")
    assert odkaz.is_visible(), f"Odkaz {odkaz} není viditelný"  # kontrola viditelnosti odkazu před kliknutím
    
    # kliknutí na odkaz a přesměrování na cílovou URL
    odkaz.click()                                               # kliknutí na odkaz (první nalezený)
    page_cookies_engeto.wait_for_load_state("networkidle")      # čekání, dokud neproběhnou všechny síťové požadavky nové stránky
    assert ocekavana_url in page_cookies_engeto.url, f"Skutečná adrese je {page_cookies_engeto.url}" # ověření názvu nové URL podle zadaného parametru pod proměnnou ocekavana_url
    
    # návrat zpět na domovskou stránku 
    page_cookies_engeto.go_back()                               # návrat pomocí šipky zpět v prohlížeči
    page_cookies_engeto.wait_for_load_state("networkidle")      # čekání, dokud neproběhnou všechny síťové požadavky domovské stránky

    # kontrola návratu zpět na domovskou stránku dle jedinečného textu v nadpisu domovské stránky
    hlavicka = page_cookies_engeto.get_by_text("IT vzdělávání", exact=False) 
    assert hlavicka.is_visible()

