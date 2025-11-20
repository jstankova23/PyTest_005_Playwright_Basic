# Playwright – ukázkový soubor pro výuku základů debuggování v Pytestu

from playwright.sync_api import Page                    # import třídy Page z knihovny Playwright kvůli nápovědám metod objektu page

# 1) Režim debuggování pomocí proměnné prostředí PWDEBUG
# pytest má režim debuggování přímo zabudovaný v sobě. Stačí pytest spustit d nastavenou proměnnou prostředí (PWDEBUG=1) 
# spustit v Git Bash: PWDEBUG=1 pytest test_playwright_debug.py::test_click
def test_pwdebug_click(page: Page):
 page.goto("http://www.uitestingplayground.com/click")

 button = page.locator("#badButton")
 button.click()

 button_success = page.locator(".btn-success")
 assert button_success.is_visible() == True


# 2) Funkce page.screenshot()
# nástroj pro ladění testů – umožní uložit aktuální stav stránky v okamžiku testu
# výsledný .png soubor je vygenerován a uložen v aktuálním pracovním adresáři (tzn. odkud je pytest spuštěn)
def test_click_screenshot(page: Page):
 page.goto("http://www.uitestingplayground.com/click")
 page.screenshot(path="screenshot.png")  # vytvoří a uloží screenshot celé stránky do souboru screenshot.png

 button = page.locator("#badButton")
 button.click()

 button_success = page.locator(".btn-success")
 assert button_success.is_visible() == True


# 3) Recording / Nahrávání testu
# možnost konfigurace různých typů záznamu: screenshots (snímky obrazovky), snapshots (stav stránky) a sources (zdrojové soubory)
# výsledný soubor trace.zip je vygenerován a uložen v aktuálním pracovním adresáři (tzn. odkud je pytest spuštěn)
# pro zpětnou analýzu záznamu (souboru trace.zip) je nutné spuštění Playwright Trace Viewer přes příkaz: playwright show-trace trace.zip

def test_trace(page: Page):
# spuštění nahrávání před začátkem testu
# parametry určují, že se mají ukládat snímky obrazovky, stavy stránky a zdrojové soubory
# playwright show-trace trace.zip
 page.context.tracing.start(screenshots=True, snapshots=True, sources=True)

 # jednotlivé kroky testu – vyplnění pole, interakce s tlačítkem apod.
 page.goto("http://www.uitestingplayground.com/textinput")

 text_input = page.locator("#newButtonName")
 text_input.fill("Hello World")

 button = page.locator("#updatingButton")
 button.hover()

 # ukončení nahrávání po skončení testu
 page.context.tracing.stop(path="trace.zip")

# spuštění Playwright Trace Viewer: playwright show-trace trace.zip


# 4) Funkce page_pause()
# test interaktivního debugování;
# slouží k pozastavení běhu testu přesně v místě, kde je tato funkce uvedena;
# po zastavení běhu testu se otevře Playwright Inspector;
# test v tuto chvíli čeká na manuální zásah – dokud tester ručně neprovede požadovanou akci
# a) kliknutí na dlouhé modré tlačítko 'Button That Should Change it´s Name Based on Input Value'
# b) nespustí test dále v Inspectoru (Continue / Step Over);
# pokud tester neklikne na modré tlačítko 'Button That Should Change it´s Name Based on Input Value', test selže na AssertionError;

# testovací funkce v příkladu využívá fixture page pro vytvoření nové stránky / okna;
# fixture page sama volá další fixture browser pro spuštění prohlížeče;
# u fixture browser byl přenastaven parametr na headless=False, aby byly akce v prohlížeči viditelné;
# obě fixtures jsou definovány v souboru conftest.py

def test_page_pause(page: Page):              # používá stránku (page) vytvořenou vlastní fixture 'page' z conftest.py
 page.goto("http://www.uitestingplayground.com/textinput")

 text_input = page.locator("#newButtonName")
 text_input.fill("Hello World")

 page.pause() # stránka se zastaví, otevře se Playwright Inspector a čeká se na manuální akci testera

 button = page.locator("#updatingButton")
 button.hover()

 assert button.inner_text() == "Hello World"



