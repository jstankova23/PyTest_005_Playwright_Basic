# PLAYWRIGHT (dle Engeto manuálu) - TEST WEBOVÝCH APLIKACÍ 
# parametr "page": objekt Playwrightu představující otevřenou webovou stránku, pomocí něj můžeme stránku ovládat (navštěvovat URL, klikat, psát atd.)

import pytest
from playwright.sync_api import Page                    # import třídy Page z knihovny Playwright kvůli nápovědám metod objektu page

# 1) METODA CLICK()
# test úspěšného kliknutí na modré tlačítko v testovací aplikaci – po kliknutí tlačítko zezelená;
# po kliknutí se u tlačítka změní třída z .btn-primary na .btn-success;
# modré tlačítko před kliknutím: třída .btn-primary;
# zelené tlačítko po kliknutí: třída .btn-success
def test_click(page: Page):
    page.goto("http://www.uitestingplayground.com/click") # přechod na testovací webovou stránku
    button = page.locator("#badButton") # v DevTools nalezený selektor pro modré tlačítko s ID #badButton; uložíme ho do proměnné
    button.click()                                        # kliknutí na modré tlačítko (pozn.: má třídu .btn-primary)

    # test ověřující, že modré tlačítko po kliknutí změní třídu na .btn-success (zezelená)
    button_success = page.locator(".btn-success")
    assert button_success.is_visible() == True


#################################################################################################################################################
# 2) METODA FILL()

# a) Test změny názvu tlačítka na základě uživatelského vstupu
# 2 elementy: 1) pole (Set New Button Name) pro uživatelský vstup nového názvu, 2) tlačítko určené k přejmenování;
# do pole Set New Button Name se napíše nový název tlačítka a klikne se na dané tlačítko, čímž se změní jeho popisek
def test_text_input(page: Page):
    page.goto("http://www.uitestingplayground.com/textinput")  # přechod na testovací webovou stránku

    text_input = page.locator("#newButtonName")  # vyhledání pole pro zadání nového názvu (pole typu input); selektor z DevTools
    text_input.fill("Nový název")                # vyplnění nového názvu do daného pole

    button = page.locator("#updatingButton")     # vyhledání tlačítka pro potvrzení změny názvu; selektor z DevTools
    button.click()                               # kliknutí na dané tlačítko

    assert button.inner_text() == "Nový název"   # kontrola, že tlačítko má nový název


# b) Pokus o příhlášení k uživatelskému účtu se špatným heslem, kontrola chybové hlášky - negativni test
# ukázka použití metod fill() a press()
def test_login(page: Page): 
    page.goto("https://the-internet.herokuapp.com/login") # otevření testovací stránky s přihlašovacím formulářem
    
    # simulace uživatelského vstupu
    username = "tomsmith"                       # uložení uživatelského jména do proměnné
    passwd = "SuperSecretPassword"              # uložení nesprávného hesla (negativní test) do proměnné

    username_input = page.locator("#username")  # nalezení vstupního pole "Username" podle CSS selektoru (ID)
    password_input = page.locator("#password")  # nalezení vstupního pole "Password" podle CSS selektoru (ID)

    username_input.fill(username)               # vyplnění uživatelského jména (pole Username)
    password_input.fill(passwd)                 # vyplnění hesla (pole Password)

    password_input.press("Enter")               # stisknutí klávesy Enter, odeslání formuláře

    # kontroly výledku testu
    assert page.url == "https://the-internet.herokuapp.com/login" # kontrola, že zůstáváme na stejné URL (přihlášení se nezdařilo)

    error_msg = page.locator("div.flash.error") # nalezení elementu s chybovým hlášením
    assert error_msg.is_visible()               # kontrola, že je chybové hlášení skutečně viditelné   

#################################################################################################################################################
# 3) METODA PRESS()
# test změny názvu tlačítka na základě uživatelského vstupu;
# 2 elementy: 1) pole (Set New Button Name) pro uživatelský vstup nového názvu, 2) tlačítko určené k přejmenování;
# do pole Set New Button Name se napíše nový název tlačítka, přejde se na dané tlačítko a potvrzení se provede stiskem klávesy Enter;
# tento scénář se liší od předchozího s metodou FILL() tím, že na tlačítko k přejmenování se nekliká, ale potvrdí se stiskem klávesy Enter
def test_press_enter(page: Page):
    page.goto("http://www.uitestingplayground.com/textinput")

    text_input = page.locator("#newButtonName")
    text_input.fill("Nový název 2")

    button = page.locator("#updatingButton")
    button.press("Enter")                          # stisknutí klávesy Enter (ne kliknutí)

    assert button.inner_text() == "Nový název 2"

#################################################################################################################################################
# 4) METODA HOVER()
# test změny prvku po najetí myši (změna atributu), úprava DOMu;
# test situace, kdy po najetí myši na odkaz "Click me" se nad ním zobrazí tooltip s textem "Active Link";
# tooltip = "nápovědní bublina", "vyskakovací popisek";
# ve skutečnosti se díky změně atributu původní prvek v DOM nahradí novým;
# ukázka problému „stale element reference“ – odkazu na zastaralý prvek, který může být po akci myší nahrazen nebo upraven

def test_hover(page: Page):
    page.goto("http://www.uitestingplayground.com/mouseover")
    link = page.locator("text=Click me")          # vyhledání odkazu s textem "Click me" pomocí textového selektoru
    link.hover()                                  # simulace najetí myší na daný odkaz

    alert = page.locator("[title='Active Link']") # vyhledání elementu dle CSS selektoru atributu title (tooltip s textem "Active Link")
    assert alert.is_visible() == True             # ověření, že nový element (tooltip) je viditelný


#################################################################################################################################################
# 5) METODA ALL()
# test převodu "víceprvkového lokátoru" na seznam samostatných lokátorů;
# ukázka metody .all() a práce s více prvky najednou;
# metoda all() převede lokátor, který odpovídá více elementům na dané stránce, na seznam samostatných lokátorů, kde každý ukazuje na 1 konkrétní element;
# ná následující testované stránce jsou 2 nadpisy ("Scenario", "Playground") s tagem <h4>

def test_more_h4(page: Page):
 page.goto("http://www.uitestingplayground.com/textinput")
 h4 = page.locator("h4")                        # vyhledání všech elementů s tagem <h4> na dané stránce 

 # převod "víceprvkového lokátoru" na seznam samostatných lokátorů, každý ukazuje na jeden konkrétní <h4> element
 h4_list = h4.all()   

# ověření nalezených elementů dle jejich vnitřního textu
 assert h4_list[0].inner_text() == "Scenario"   
 assert h4_list[1].inner_text() == "Playground" 

#################################################################################################################################################
# 6) METODA DRAG_TO()
# test přetažení objektu (drag & drop) na jiné místo;
# přesun obrázku z <div2> do <div1> (zespoda nahoru na webové stránce)

def test_drag_and_drop(page: Page):
 page.goto("https://seleniumbase.io/other/drag_and_drop")

 img = page.locator("#drag1")           # vyhledání obrázku dle CSS lokátor podle ID, obrázek určený k přetažení na jiné místo
 target = page.locator("#div1")         # vyhledání cílového prvku dle CSS lokátoru podle ID, kam se obrázek přetáhne

 img.drag_to(target)                    # provedení akce přetažení – přesunutí obrázku do cílového elementu

 img_new = page.locator("#div1 > img")  # ověření, že se daný obrázek skutečně nachází uvnitř cílového bloku
 assert img_new.is_visible() == True    # Kontrola, že přetažený obrázek je viditelný (tzn. operace proběhla úspěšně)

 #################################################################################################################################################


