# Playwright – ukázkový soubor pro výuku načítání a čekání v Pytestu
# 1) metoda page.wait_for_load_state()
# 2) metoda page.wait_for_selector()
# 3) metoda page.wait_for_timeout() 
# 4) parametr slow_mo

##################################################################################################################
from playwright.sync_api import Page                    # import třídy Page z knihovny Playwright kvůli nápovědám metod objektu page

# 1) Metoda page.wait_for_load_state()
# wait_for_load_state() je metoda objektu page a slouží k explicitnímu čekání, než se stránka zcela načte;
# parametr "networkidle" znamená, že test počká, dokud nejsou aktivní žádné síťové požadavky (např. AJAX),
# nebo dokud neuplyne daný časový limit v milisekundách (timeout)
def test_slow_load(page: Page):
 page.goto("http://www.uitestingplayground.com/loaddelay")   # otevření cílové webové stránky
 page.wait_for_load_state("networkidle", timeout=60000)      # čekání na úplné načtení stránky (max. 60 s / 1 min)

 btn = page.locator('button:has-text("Button Appearing After Delay")') # lokalizace tlačítka, které se na stránce objeví až po určité prodlevě
 btn.click()                                                 # kliknutí na tlačítko, jakmile je dostupné

##################################################################################################################
# 2) Metoda page.wait_for_selector()
# wait_for_selector() je metoda objektu page a slouží k explicitnímu čekání na zobrazení konkrétního prvku na stránce;
# test pokračuje teprve tehdy, když je prvek nalezen a viditelný, nebo když uplyne stanovený časový limit (timeout);
# tato metoda se používá v případech, kdy se prvky načítají se zpožděním (např. dynamicky po načtení stránky)
def test_slow_selector(page: Page):
 page.goto("http://www.uitestingplayground.com/loaddelay") # otevření cílové webové stránky

 # čekání, dokud se na stránce neobjeví tlačítko s daným textem (maximálně 6 sekund)
 btn = page.wait_for_selector('button:has-text("Button Appearing After Delay")', timeout=6000)  
 btn.click()                                               # kliknutí na tlačítko, jakmile je dostupné

##################################################################################################################
# 3) Metoda page.wait_for_timeout()
# wait_for_timeout() je metoda objektu page, která dočasně zastaví běh testu na zadaný čas (v milisekundách);
# využívá se např. pro krátkou prodlevu mezi akcí a následnou kontrolou (assertem), aby se stránka stihla aktualizovat po kliknutí nebo jiné akci;
# příkaz pro zpomalení: # page.wait_for_timeout(počet_ms)

# Příklad: Odmítnutí cookies na domovské stránce českého webu Ikea
# cílem je ověřit, že po kliknutí na tlačítko „Odmítnout všechna volitelná cookies“ zmizí cookie lišta

def test_cookies_slow(page: Page):
    page.goto("https://www.ikea.com/cz/cs/")                  # otevření domovské stránky IKEA

    # akce s tlačítkem "Odmítnout všechna volitelná cookies"
    button = page.locator("#onetrust-reject-all-handler")     # vyhledání tlačítka dle CSS lokátoru (id)
    button.click()                                            # kliknutí na tlačítko

    # krátká prodleva pro jistotu, že se stránka stihne aktualizovat
    page.wait_for_timeout(1000)                               # pauza 1000 ms = 1 sekunda

    # kontrola, že cookie lišta zmizela
    cookie_bar = page.locator("#onetrust-banner-sdk")         # vyhledání prvku cookie lišty
    assert cookie_bar.is_visible() == False                   # ověření, že cookie lišta není viditelná

##################################################################################################################
# 4) Parametr slow_mo
# test názvu webu Googlu;
# test využívající fixtures pro spuštění prohlížeče a vytvoření nové stránky;
# parametr slow_mo je nastaven ve fixture fix_browser (v souboru conftest.py);
# parametr slow_mo zpomaluje běh testu (v milisekundách mezi jednotlivými akcemi);
# díky zpomalení lze snadno sledovat, co test v prohlížeči právě dělá;
# test působí přirozeněji (jako lidská činnost) a snižuje riziko blokace vůči botům
def test_slow_mo(page: Page):                   # používá stránku (page) vytvořenou vlastní fixture 'page' z conftest.py
 page.goto("https://www.google.com/")     # přechod na testovanou stránku
 title = page.locator("title")            # vyhledání názvu webu pomocí textového selektoru
 assert title.inner_text() == "Google"    # název webu z DevTools pouze v režimu incognito, jinak je "New Tab"

##################################################################################################################
