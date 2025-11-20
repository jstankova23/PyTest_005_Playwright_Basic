# PyTest_005_Playwright_Basic  
Automatizované testy pomocí **Playwright + Pytest** (Python)

**Autor:** Jana Staňková  
**Verze projektu:** 1.1.1  
**Python:** 3.10+  
**Licence:** MIT  

---

## Popis projektu

Tento projekt obsahuje ucelenou sbírku testů vytvořených během studia Playwrightu s Pytestem.
Ukazuje práci s lokátory, cookies, mobilními zařízeními, různými prohlížeči, debugováním, trace,
zpomalováním testů, čekáním, parametrizací a dalšími užitečnými funkcemi Playwrightu.

Projekt obsahuje 9 testovacích souborů s celkem 30 testovacími funkcemi.
Díky parametrizaci některých testů se celkový počet spuštění zvyšuje na 34 běhů.

Z výukových důvodů je fixture browser nastavena s viditelným oknem prohlížeče (headless=False),
aby bylo možné pozorovat průběh testů a zároveň využívat Playwright Inspector.

Projekt obsahuje běžné fixtures, fixtures pro cookies,
parametrizované fixtures i mobilní konfigurace.

Celý projekt slouží k výuce automatizace testování webových stránek na desktopu,
v různých mobilních zařízeních, i ve více webových prohlížečích.
---

## Struktura projektu

PyTest_005_Playwright_Basic/
│
├─ tests/
│ ├─ test_pw_cookies.py
│ ├─ test_pw_debug.py
│ ├─ test_pw_delay.py
│ ├─ test_pw_engeto.py
│ ├─ test_pw_filtry.py
│ ├─ test_pw_login.py
│ ├─ test_pw_metody.py
│ ├─ test_pw_mobil.py
│ └─ test_pw_prohlizec.py
│
├─ conftest.py              # společné fixtures pro testy
├─ devices.py               # pomocný skript (výpis vestavěných mobilních zařízení Playwrightu)
├─ README.md
├─ requirements.txt
└─ .gitignore

---

## Výpis testovacích funkcí v jednotlivých souborech:

tests/test_pw_cookies.py
test_refuse_cookies                                # zpracování cookies přímo v testovací funkci
test_accept_all_cookies                            # zpracování cookies přímo v testovací funkci
test_cookies                                       # zpracování cookies v pomocné funkci
test_dobrovsky_title                               # zpracování cookies pomocí fixture

tests/test_pw_debug.py
test_pwdebug_click                                 # režim debuggování pomocí proměnné prostředí PWDEBUG
test_click_screenshot                              # funkce page.screenshot()
test_trace                                         # recording / Nahrávání testu
test_page_pause                                    # test interaktivního debugování, pytest vyžaduje manuální zásah testera

tests/test_pw_delay.py         
test_slow_load                                     # metoda page.wait_for_load_state()  
test_slow_selector                                 # metoda page.wait_for_selector()
test_cookies_slow                                  # metoda page.wait_for_timeout()
test_slow_mo                                       # parametr slow_mo

tests/test_pw_engeto.py
test_hlavni_nadpis_je_viditelny                    # test pro ověření viditelnosti zvoleného nadpisu
test_viditelnost_loga                              # test pro ověření viditelnosti loga v hlavním menu
test_viditelnost_linku_vyukovy_portal              # test pro ověření viditelnosti odkazu na Výukový portál z hlavního menu
test_odkaz_na_spravnou_url                         # test ověření, že odkaz na Výukový portál v hlavním menu vede na správnou URL - kontrola atributu v HTML struktuře
test_klik_na_odkaz                                 # test ověření, že odkaz na Výukový portál v hlavním menu vede na správnou URL - kontrola kliknutím
test_scroll_a_presmerovani_na_blog                 # test skrolování myší, kliknutí na link Blog v zápatí domovské stránky a kontrola URL po přesměrování
test_presmerovani_a_navrat[Blog-blog]              # parametrizovaný test: kliknutí na odkaz Blog v domovské stránce Engeta, kontrola URL po přesměrování a návrat zpět
test_presmerovani_a_navrat[Reference-absolventi]   # parametrizovaný test: kliknutí na odkaz Reference v domovské stránce Engeta, kontrola URL po přesměrování a návrat zpět

tests/test_pw_filtry.py
test_filter                                        # test filtrování akademií na stránce Engeta

tests/test_pw_login.py
test_login                                         # test přihlášení na stránce Demoqa a přesměrování na cílovou podstránku

tests/test_pw_metody.py
test_click                                         # metoda click()
test_text_input                                    # metoda fill()
test_login                                         # metoda fill()
test_press_enter                                   # metoda press()
test_hover                                         # metoda hover()   POZOR - NEBYLA V SEZNAMU
test_more_h4                                       # metoda all()
test_drag_and_drop                                 # metoda drag_to()   POZOR - NEBYLA V SEZNAMU

tests/test_pw_mobil.py                             # test přesměrování kliknutím na link "Výukový portál" po otevření hlavního menu přes ikonku hamburger menu ve vybraných typech mobilů
test_mobile_menu[iPhone 12]                        
test_mobile_menu[Pixel 5]                          

tests/test_pw_prohlizec.py                         # test ověřuje, že odkaz "Výukový portál" je viditelný na stránce Engeto při spuštění v různých webových prohlížečích
test_browser_kompatibilita[chromium]               
test_browser_kompatibilita[firefox]                
test_browser_kompatibilita[webkit]                  

---

## Poznámky

### **Test `test_page_pause()`**
- Test vyžaduje manuální zásah uživatele (otevře Playwright Inspector a čeká, až tester klikne manuálně na modré tlačítko 
  'Button That Should Change it´s Name Based on Input Value' a dokončí test přes Playwright Inspector.

### **Test `test_filter`**
- Může padat i při správném kódu.  
- Důvodem je nestabilní nebo nefunkční webová funkcionalita filtrů na webu Engeto.

---

## Spuštění testů

Spuštění všech testů v projektu:

```bash
pytest -v


Spuštění pouze jedné složky tests/:

```bash
pytest tests/ -v

---

## Instalace závislostí

pip install -r requirements.txt

---

## Technologie

Python 3.10+
Pytest
Playwright
Fixtures
Parametrizované testy
Testování mobilních zařízení
Testování kompatibility prohlížečů

---

## Fixtures (conftest.py)

Soubor `conftest.py` obsahuje:

### 1) Fixture `browser`
- univerzální browser pro všechny testy  
- běží v režimu `headless=False`, tzn. s viditelným oknem prohlížeče kvůli didaktickým účelům  
- slouží jako základ pro desktop testy

### 2) Fixture `page`
- univerzální stránka pro testy  
- **nenaviguje sama na URL** → test si stránku otevírá sám pomocí `page.goto(...)`

### 3) Cookies fixtures  
Např. `cookies_engeto`, `cookies_dobrovsky`:
- obsahují logiku specifickou pro konkrétní web
- otevírají URL + odklikávají cookies
- poté vrací připravený objekt `page`

### 4) Mobilní fixtures
- `mobile_device` — parametrizované testování (např. *iPhone 12*, *Pixel 5*)
- `mobile_page` — vytvoří mobilní kontext a stránku + vyřeší cookies

### 5) Fixtures pro různé typy prohlížečů
- `browser_type` — parametrizované testování (např. *chromium*, *webkit*, *firefox*)
- `browser_page` — vytvoří kontext a stránku + vyřeší cookies
---