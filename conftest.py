"""
===============================================================================
FIXTURES Z PLUGINU PYTEST-PLAYWRIGHT
===============================================================================
- fixtures 'browser' a 'page' jsou univerzální – nejsou svázané s žádnou konkrétní URL a lze je používat ve všech testech napříč celým projektem;
- naproti tomu fixture pro odkliknutí cookies (např. page_dobrovsky) je vždy specifická pro daný web, protože obsahuje logiku a selektory platné 
  pouze pro tuto konkrétní stránku, každý web má vlastní cookies lištu a proto má mít i vlastní fixture pro zpracování cookies;
- pokud stránka nevyžaduje zpracování cookies, testovací funkce dostane univerzální fixture 'page' bez otevřené URL, v takovém případě je krok 
  'page.goto(...)' pro přechod na požadovanou stránku uveden přímo v testovací funkci;

- fixtures 'page', 'context' a 'browser' jsou již předdefinovány v pluginu 'pytest-playwright';
- vestavěná fixture 'page' spouští řetězově fixture 'context' a ta spouští fixture 'browser';
- Když test používá 'page', pytest-playwright automaticky vytvoří: 
  a) prohlížeč (browser), 
  b) nové okno (context), 
  c) novou kartu (page) 
  a použije k tomu výchozí Chromium v režimu headless=True (bez zobrazení okna).

- fixture 'browser' spouští Playwright interně pomocí volání 'sync_playwright()', čímž vytváří instanci Playwrightu a otevírá příslušný prohlížeč;
- standardně plugin 'pytest-playwright' spouští Chromium prohlížeč v režimu 'headless=True', tzn. okno prohlížeče ani Playwright Inspector se nezobrazují 
  a testy běží na pozadí - pokud je toto default nastavení žádoucí, není nutné fixtures 'browser', 'page' a 'context' vůbec definovat do svého 
  souboru 'conftest.py' – Playwright je má k dispozici automaticky;

- pokud je ale požadováno spuštění pytestu v jiném prohlížečí, či ve viditelném a zpomaleném režimu (např. pro účely výuky nebo manuálního zásahu testera),
  je nutné předefinovat fixture browser ve vlastním souboru conftest.py s jiným nastavením než má výchozí plugin:
  a) jiný prohlížeč než Chromium;
  b) viditelné okno prohlížeče – 'headless=False';
  c) zpomalené provádění testovacích kroků (v milisekundách) – 'slow_mo';
- v případě vlastní definice fixture 'browser' je nutné definovat i vlastní fixture 'page';  

- plugin 'pytest-playwright' při spuštění testů automaticky inicializuje Playwright prostřednictvím své vestavěné fixture 'browser', 
  tím je Playwright spuštěn v každém běhu pytestu, i když tuto fixture přímo program nevolá.
  není tedy možné v jednom projektu současně používat vestavěné fixtures z pluginu ('browser', 'page', 'context') a zároveň definovat vlastní fixture, 
  která znovu spouští Playwright voláním 'sync_playwright()' - při hromadném spuštění všech testů projektu by došlo by k pokusu o paralelní inicializaci 
  více instancí Playwrightu, což vede k chybě "Sync API inside asyncio loop" (konflikt běžících smyček Playwrightu);

  Pokud je v projektu nainstalován plugin 'pytest-playwright', je doporučeno:
  - buď plně využívat jeho vestavěné fixtures ('browser', 'context', 'page') a případě potřeby změnit jejich parametry (viditelné okno prohlížeče, zpomalení),
    což vyžaduje jejich předefinování v souboru conftest.py se zachováním původního jména názvu fixture ('browser', 'context', 'page')
  - nebo si vytvořit své vlastní fixtures otvírající Playwright a plugin při testování vypnout parametrem příkazové řádky: pytest -p no:pytest_playwright

Shrnutí:
Plugin 'pytest-playwright' obsahuje základní fixtures pro práci s Playwrightem a automaticky spouští Playwright.
V testech tohoto projektu je ale účelem vidět průběh testů v reálném prohlížeči ve zpomaleném režimu, fixture 'browser' byla tedy záměrně předefinována 
v 'conftest.py' s parametry 'headless=False' a 'slow_mo'. Fixture 'page' si ponechává default nastavení a je zde uvedena jen pro pochopení provázanosti
s fixture browser.
===============================================================================
"""

import pytest
from playwright.sync_api import Page, sync_playwright # import třídy Page kvůli nápovědám, import synchronní API Playwrightu pro fixture browser

# A) UNIVERZÁLNÍ FIXTURES BEZ SPOJENÍ S URL
# 1) FIXTURE PRO SPUŠTĚNÍ PROHLÍŽEČE - CHROMIUM
# vestavěná fixture 'browser' z pluginu pytest-playwright předefinovaná vlastními parametry:
# a) parametr headless=False zajistí viditelné okno prohlížeče;
# b) parametr slow_mo zpomaluje provádění jednotlivých kroků testu (v milisekundách), aby bylo možné sledovat, co test v prohlížeči provádí;
# fixture spouští Playwright a otevírá prohlížeč Chromium s těmito nastaveními;
@pytest.fixture()
def browser():
   with sync_playwright() as p:  # spuštění Playwrightu a vytvoření aliasu pro jeho instanci
    browser = p.chromium.launch(headless=False, slow_mo=1000) # otevření prohlížeče Chromium s viditelným oknem, zpomalení akcí o 1s
    yield browser    # předání objektu 'browser' dalším fixture nebo testům, po dokončení testu se vykoná kód za yieldem
    browser.close()  # uzavření prohlížeče po skončení testu


# 2) FIXTURE PRO VYTVOŘENÍ STRÁNKY (page)
# plugin pytest-playwright obsahuje vestavěnou fixture 'page', ale pokud si definuji sama už fixture 'browser', musím definovat už i vlastní fixture 'page';
# fixture vytvoří nové okno / stránku (tab) v již otevřeném prohlížeči a předá ji testu;
# po skončení testu se stránka automaticky uzavře
@pytest.fixture()
def page(browser):          # fixture pro vytvoření okna / stránky, parametrem je fixture pro spuštění prohlížeče (browser)
 page = browser.new_page()  # vytvoření nové stránky (nového panelu / tab) v již otevřeném prohlížeči
 yield page                 # vrací toto okno (objekt 'page')
 page.close()               # uzavření okna po skončení testu

######################################################
# B) SPECIFICKÉ FIXTURES PRO KONKRÉTNÍ URL - DESKTOP
# 3) FIXTURES PRO ZPRACOVÁNÍ COOKIES - DESKTOP
# vyčlenění pre-testovacího kroku (odkliknutí cookies) do samostatné fixture;
# fixture zajistí, že stránka bude již otevřená a cookies budou přijaty ještě před spuštěním testu;
# fixture používá vestavěný objekt / fixture "page", otevře konkrétní URL a provede přípravné kroky (odkliknutí cookies);
# pomocí "yield page" fixture předá tuto upravenou stránku testovací funkci;
# před "yeild page" je definováno krátké čekání, aby po odkliknutí cookies daná stránka stihla načíst základní HTMPL
# vestavěné fixtures "page", "context" a "browser" tvoří řetězec závislostí – při použití "page" se automaticky spustí i "context" a "browser";
# vestavěná fixture "browser" automaticky spustí Playwright, i když nikde výslovně nevoláme "sync_playwright()";

# FIXTURE PRO PŘIJETÍ VŠECH COOKIES - KNIHY DOBROVSKÝ (DESKTOP)
# fixture využívá testovací funkce test_dobrovsky_title (soubor test_playwright_cookies)
@pytest.fixture()
def page_cookies_dobrovsky(page: Page):
    page.goto("https://www.knihydobrovsky.cz/")             # otevření webové stránky Knihy Dobrovský
    button_allow_loc = "#ch2-dialog >> .ch2-allow-all-btn"  # CSS selektor pro tlačítko "Povolit vše"

    button_allow = page.locator(button_allow_loc)           # vytvoření lokátoru pro tlačítko "Povolit vše"
    button_allow.click()                                    # kliknutí na tlačítko "Povolit vše"
    page.wait_for_load_state("domcontentloaded")            # krátké čekání, aby po odkliknutí cookies stránka stihla znovu načíst základní HTML 
    yield page                                              # předání otevření stránky s již přijatými cookies testovací funkci


# FIXTURE PRO PŘIJETÍ VŠECH COOKIES - ENGETO (DESKTOP)
# fixture využívají testovací funkce ze souboru test_engeto.py
@pytest.fixture()
def page_cookies_engeto(page: Page):
    page.goto("https://engeto.cz/")
    cookies = page.locator("#cookiescript_injected")                  # vytvoření lokátoru pro cookie lištu
    if cookies.is_visible():                                          
        page.get_by_role("button", name="Chápu a přijímám!").click()  # kliknutí na element s rolí "tlačítko" a daným názvem

    page.wait_for_load_state("domcontentloaded")                      # krátké čekání, aby po odkliknutí cookies stránka stihla znovu načíst základní HTML 
    yield page

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# FIXTURES PRO TESTOVÁNÍ RŮZNÝCH TYPŮ MOBILNÍCH ZAŘÍZENÍ

# 1) PARAMETRIZOVANÁ FIXTURE PRO TYP MOBILNÍHO ZAŘÍZENÍ
# tuto fixture volá fixture 'mobile_page' 
@pytest.fixture(params=["iPhone 12", "Pixel 5"])    # test bude spuštěn 2x, vždy pro jiný typ zařízení uvedený v parametru
def mobile_device(request):                         
    return request.param                            # vrací aktuální hodnotu parametru (název zařízení)


# 2) FIXTURE PRO SPUŠTĚNÍ TESTU (BROWSER, CONTEXT, PAGE, ZPRACOVÁNÍ COOKIES - VŠE DOHROMADY)
# volá parametrizovanou fixture pro typ mobilního zařízení (mobile_device)
# všechny 3 fixtures ('browser', 'context', 'page') jsou zde nadefinované pod jednou hromadnou fixture s názvem 'mobile_page'
@pytest.fixture()
def mobile_page(mobile_device):        
    with sync_playwright() as p:                                          # spuštění Playwrightu (kontextový manažer)
        browser = p.chromium.launch(headless=False)                       # otevření viditelného okna Chromia
        device = p.devices[mobile_device]                                 # načtení vestavěné konfigurace daného mobilního zařízení
        context = browser.new_context(**device)                           # vytvoření mobilního kontextu (emulace zařízení)
        page = context.new_page()                                         # nová mobilní stránka (mobilní viewport, user-agent atd.)
        page.goto("https://engeto.cz/")                                   # otevření cílové stránky
        
        # zpracování cookie lišty
        cookies = page.locator("#cookiescript_injected")                  
        if cookies.is_visible():
            page.get_by_role("button", name="Chápu a přijímám!").click()

        page.wait_for_load_state("domcontentloaded")                      # jistota načtení základní struktury stránky
        yield page                                                        # předání stránky testu
        browser.close()                                                   # zavření celého prohlížeče po testu

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# FIXTURES PRO TESTOVÁNÍ RŮZNÝCH TYPŮ PROHLÍŽEČŮ

# 1) PARAMETRIZOVANÁ FIXTURE DEFINUJÍCÍ TYP PROHLÍŽEČE
# tuto fixture volá fixture 'browser_page' 
@pytest.fixture(params=["chromium", "webkit", "firefox"])   # test se spustí 3x, pro každý prohlížeč zvlášť
def browser_type(request):
    return request.param                                    # vrací aktuální název prohlížeče z parametru


# 2) FIXTURE PRO SPUŠTĚNÍ TESTU V RŮZNÝCH PROHLÍŽEČÍCH (BROWSER, CONTEXT, PAGE, ZPRACOVÁNÍ COOKIES - VŠE DOHROMADY)
# volá parametrizovanou fixture browser_type, která určuje, který prohlížeč se má použít;
# všechny 3 fixtures ('browser', 'context', 'page') jsou zde nadefinované pod jednou hromadnou fixture s názvem 'browser_page'
@pytest.fixture()
def browser_page(browser_type):
    with sync_playwright() as p:                                          # spuštění Playwrightu (kontextový manažer)
        browser_launcher = getattr(p, browser_type)                       # získání správného engine (chromium/webkit/firefox) s proměnnou p
        browser = browser_launcher.launch(headless=False)                 # spuštění zvoleného prohlížeče s viditelným oknem
        context = browser.new_context()                                   # vytvoření kontextu (samostatná instance okna)
        page = context.new_page()                                         # nová stránka
        page.goto("https://engeto.cz/")                                   # otevření cílové stránky
        
        # zpracování cookie lišty
        cookies = page.locator("#cookiescript_injected")
        if cookies.is_visible():
            page.get_by_role("button", name="Chápu a přijímám!").click()

        page.wait_for_load_state("domcontentloaded")                      # jistota načtení základní struktury stránky
        yield page                                                        # předání stránky testu
        browser.close()                                                   # zavření celého prohlížeče po testu



