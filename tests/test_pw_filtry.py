# TEST FILTROVÁNÍ AKADEMIÍ NA STRÁNCE ENGETA
# Kurz "Testing Akademie" - prohlížeč Chromium;
# test může občas selhat kvůli problémům s funkčností filtrů na webu Engeto, nikoli kvůli chybě v samotném testu

# cílem testu je ověřit, že po vyfiltrování kurzů podle oblasti a délky se správně zobrazí kurz "Testing Akademie";
# a) otevření úvodní stránky Engeta a odmítnutí cookies;
# b) hover nad tlačítkem "Kurzy" v záhlaví domovské stránky;
# c) kliknutí na tlačítko "Zobrazit termíny kurzů" a tím přechod na další stránku pro termíny kurzů;
# d) zaškrtnutí 2 checkboxů (volba oblasti a délky kurzu);
# e) kontrola, že se správně vybere a zobrazí kurz "Testing akademie" 

from playwright.sync_api import Page                    # import třídy Page z knihovny Playwright kvůli nápovědám metod objektu page

def test_filter(page: Page):                          # definice funkce pro test filtrace Engeto kurzů
    page.goto("https://engeto.cz/")                   # otevření domovské stránky Engeta

# a) odmítnutí cookies
    btn_refuse = page.locator("#cookiescript_reject")   # vyhledání tlačítka pro odmítnutí cookies přes CSS lokátor (ID)
    btn_refuse.click()                                  # kliknutí na něj

# b) zobrazení nabídky "Kurzy" pomocí akce hover
    button_kurzy = page.locator("#top-menu .area-kurzy")   # vyhledání tlačítka "Kurzy" v záhlaví stránky dle CSS lokátoru (ID + třída)
    button_kurzy.hover()                                   # simulace najetí myší na tlačítko "Kurzy" pro zobrazení rozbalovací nabídky kurzů

# c) kliknutí na tlačítko "Zobrazit termíny kurzů"
# vyhledání tlačítka "Zobrazit termíny kurzů" dle manuálně napsaného CSS lokátoru: (2 třídy, tag a atribut);
# po najetí myší (hover) na tlačítko "Kurzy" se zobrazí rozbalovací nabídka (submenu), která obsahuje odkaz "Zobrazit termíny kurzů";
# proto se zde nepracuje přímo s objektem 'page', ale s proměnnou 'button_kurzy', která představuje lokátor oblasti odpovídající tlačítku "Kurzy";
# pomocí button_kurzy.locator(...) je vyhledán vnořený odkaz v submenu a kliknutím na něj se přeujde na stránku s termíny kurzů
    button_terminy = button_kurzy.locator(".sub-menu .menu-buttons a[href='https://www.engeto.cz/terminy']")
    button_terminy.click()                                   # kliknutí na tlačítko "Zobrazit termíny kurzů"

# d) filtrování kurzů – zaškrtnutí 2 checkboxů (volba oblasti a délky kurzu)
    filter_box = page.locator(".block-dates-filter__desktop")               # vyhledání sekce s filtračními možnostmi

    checkbox_testing = filter_box.locator("#technology-testovani-softwaru") # vyhledání 1. checkboxu ve filtrovacím boxu, oblast: Testování softwaru
    checkbox_testing.check()                                                # zaškrtutí 1. checkboxu

    checkbox_academy = filter_box.locator("#type-akademie")                 # vyhledání 2. checkboxu ve filtrovacích boxu, délka kurzu: Akademie
    checkbox_academy.check()                                                # zaškrtutí 2. checkboxu

# e) kontrola, že se správně vybere a zobrazí kurz "Testing akademie" 
    h3_locator = page.locator(".dates-filter-product h3.title") # vyhledání všech nadpisů (h3) s třídou "title" v elementu (odkaz <a>) s třídou .dates-filter-product
    h3_list = h3_locator.all()                                  # vytvoření seznamu všech vyhledaných nadpisů (h3)
    for h3 in h3_list:                                          # procházení seznamem (for in iterace) všech vyhledaných nadpisů kurzů (h3)
        if h3.is_visible():                                     # pokud je nadpis (h3) viditelný, 
            assert h3.inner_text() == "Testing Akademie"        # kontrola, že nějaký vyhledaný nadpis obsahuje text "Testing akademie"



