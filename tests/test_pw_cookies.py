# PLAYWRIGHT - ODKLIKNUTÍ COOKIES (přijetí či odmítnutí)
# Způsoby zpracování cookies:
# 1) Zpracování cookies přímo v testovací funkci;
# 2) Zpracování cookies v pomocné funkci;
# 3) Zpracování cookies pomocí fixture

from playwright.sync_api import Page                    # import třídy Page z knihovny Playwright kvůli nápovědám metod objektu page

# 1 a) ZPRACOVÁNÍ COOKIES PŘÍMO V TESTOVACÍ FUNKCI
# test odmítnutí cookies - Google (kliknutí na tlačítko "Odmítnout vše", cookie lišta zmizí);
# zpracování cookies přímo v testovací funkci je vhodné pro jednoduché testy nebo rychlou demonstraci, kdy se tento krok neopakuje;
# nevýhoda: kód se musí kopírovat do každého testu, který cookies pro danou webovou stránku řeší;
# proměnné a f-string:
# f-string umožňuje vložit hodnotu proměnné přímo do textu CSS selektoru;
# následující zápisy jsou totožné: f"button#{id_button_refuse}" = "button#" + id_button_refuse

def test_refuse_cookies(page: Page):                                
 page.goto("https://www.google.com/")                # přechod na testovanou stránku, Google zobrazí úvodní lištu s výzvou k přijetí cookies
 id_cookie_bar = "CXQnmb"                                      # selektor z DevTools pro cookies lištu
 id_button_refuse = "W0wltc"                                   # selektor z DevTools pro tlačítko "Odmítnout vše"

 refuse_button = page.locator(f"button#{id_button_refuse}")    # vyhledání tlačítka "Odmítnout vše" pomocí CSS selektoru
 refuse_button.click()                                         # kliknutí na tlačítko "Odmítnout vše"

 cookie_bar = page.locator(f"div#{id_cookie_bar}")             # vyhledání cookies lišty pomocí CSS selektoru
 assert not cookie_bar.is_visible()                            # ověření, že cookie lišta zmizela
 # assert cookie_bar.is_visible() == False                     # jiný způsob ověření, že cookie lišta zmizela, méně doporučovaný

 # možnost doplnění hlášek o úspěchu či neúspěchu testu, pro vytištění hlášek spustit příkazem: pytest -s
 if not cookie_bar.is_visible():
    print("Cookie lišta úspěšně zmizela.")                     
 else:
    raise AssertionError("Cookie lišta nezmizela, stále je viditelná.")

#################################################################################################################################################
# 1 b) ZPRACOVÁNÍ COOKIES PŘÍMO V TESTOVACÍ FUNKCI
# test přijetí cookies ("Povolit vše") - Knihy Dobrovský

def test_accept_all_cookies(page: Page):
    page.goto("https://www.knihydobrovsky.cz/")            # přechod na domovskou stránku (režim incognito)
    cookies_bar_loc = "#ch2-dialog"                        # CSS selektor pro cookies lištu
    button_allow_loc = "#ch2-dialog >> .ch2-allow-all-btn" # CSS selektor pro tlačítko "Povolit vše"

    button_allow = page.locator(button_allow_loc)   # vyhledání tlačítka "Povolit vše" pomocí CSS selektoru
    button_allow.click()                            # kliknutí na tlačitko "Povolit vše"

    cookies_bar = page.locator(cookies_bar_loc)     # vyhledání cookies lišty pomocí CSS selektoru
    assert cookies_bar.is_visible() == False        # ověření, že cookie lišta zmizela

#################################################################################################################################################
# 2) ZPRACOVÁNÍ COOKIES V POMOCNÉ FUNKCI
# test odmítnutí cookies - ENGETO (synchronizace - vynucené čekání Playwrightu na zmizení tlačítka pro odmítnutí cookies);
# zpracování cookies v samostatné pomocné funkci refuse_cookies();
# výhody: možnost volat pomocnou funkci v různých testech pro tu samou webovou stránku, přehlednější testy;
# nevýhoda: testy musí pořád ručně volat danou pomocnou funkci

# definice pomocné funkce pro odmítnutí cookies                  
def refuse_cookies(page: Page):                                  
    btn_refuse = page.locator("#cookiescript_reject")   # vyhledání tlačítka pro odmítnutí cookies přes CSS lokátor (ID)

    if btn_refuse.is_visible():                         # pokud je tlačítko pro odmítnutí cookies viditelné,
        btn_refuse.click()                              # kliknutí na něj

# definice testovací funkce pro stránku Egeta s voláním dříve definované funkce pro odmítnutí cookies
def test_cookies(page: Page):                                      # definice funkce pro test cookies
    page.goto("https://engeto.cz/")                                # otevření domovské stránky Engeta
    refuse_cookies(page)                                           # volání dříve definované funkce pro odmítnutí cookies
    page.wait_for_selector("#cookiescript_reject", state="hidden") # čekání, dokud tlačítko pro odmítnutí cookies nezmizí (bude skryté)
    assert not page.locator("#cookiescript_reject").is_visible()   # ověření, že tlačítko pro odmítnutí cookies není vidět


##################################################################################################################################################
# 3) ZPRACOVÁNÍ COOKIES POMOCÍ FIXTURE
# test názvu webové stránky Knihy Dobrovský s využitím fixture pro zpracování cookies (page_cookies_engeto);
# testovací funkce volá fixture pro cookies spojenou s konkrétní URL, fixture pro cookies volá fixture page a ta volá fixture browser (a vestavěnou context);
# testovací funkce používá fixture page_cookies_dobrovsky, která je definována v souboru conftest.py;
# tato fixture nejprve zavolá fixture 'page', která zavolá fixture 'browser' (a interně i 'context');
# výsledkem řetězce browser → context → page → page_cookies_dobrovsky je plně připravená stránka s otevřenou URL a již odkliknutými cookies;
# výhoda: nejčistší přístup, doporučený pro větší projekty, fixture je možno používat napříč testy bez duplikace kódu

def test_dobrovsky_title(page_cookies_dobrovsky: Page):                 # parametrem je fixture page_cookies_dobrovsky z conftest.py
    title = page_cookies_dobrovsky.title()                              # získání názvu (title) aktuálně otevřené webové stránky
    assert title == "Knihy Dobrovský | Vaše (nejen) online knihkupectví s tradicí" # ověření, že název stránky odpovídá očekávané hodnotě