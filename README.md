# PyTest_005_Playwright_Basic

Automatizované testy pomocí **Playwright + Pytest** (Python)

**Autor:** Jana Staňková  
**Verze projektu:** 1.1.1  
**Python:** 3.10+  
**Licence:** MIT  

---

## Popis projektu

Tento projekt obsahuje sbírku testů vytvořených během studia Playwrightu a Pytestu.  
Demonstruje:

- práci s lokátory
- práci s cookies
- mobilní zařízení (vestavěné profily Playwrightu)
- více webových prohlížečů (Chromium, Firefox, WebKit)
- debugování (PWDEBUG, page.pause, trace)
- zpomalování testů a čekání
- parametrizaci a fixtures

Projekt obsahuje:

- **9 testovacích souborů**
- **30 testovacích funkcí**
- díky parametrizaci → **34 skutečných běhů**

Fixture `browser` je záměrně v režimu **headless=False**, aby bylo během výuky možné sledovat průběh testů
a používat Playwright Inspector.

---

## Struktura projektu

```text
PyTest_005_Playwright_Basic/
│
├─ tests/
│   ├─ test_pw_cookies.py
│   ├─ test_pw_debug.py
│   ├─ test_pw_delay.py
│   ├─ test_pw_engeto.py
│   ├─ test_pw_filtry.py
│   ├─ test_pw_login.py
│   ├─ test_pw_metody.py
│   ├─ test_pw_mobil.py
│   └─ test_pw_prohlizec.py
│
├─ conftest.py          # společné fixtures pro testy
├─ devices.py           # výpis vestavěných mobilních zařízení Playwrightu
├─ requirements.txt
├─ README.md
└─ .gitignore


---

## Výpis testovacích funkcí

```text
tests/test_pw_cookies.py
  ├─ test_refuse_cookies               # zpracování cookies přímo v testu
  ├─ test_accept_all_cookies           # zpracování cookies přímo v testu
  ├─ test_cookies                      # pomocná funkce pro cookies
  └─ test_dobrovsky_title              # cookies pomocí speciální fixture

tests/test_pw_debug.py
  ├─ test_pwdebug_click                # režim PWDEBUG
  ├─ test_click_screenshot             # page.screenshot()
  ├─ test_trace                         # trace recording
  └─ test_page_pause                   # interaktivní zastavení testu

tests/test_pw_delay.py
  ├─ test_slow_load                    # page.wait_for_load_state()
  ├─ test_slow_selector                # page.wait_for_selector()
  ├─ test_cookies_slow                 # page.wait_for_timeout()
  └─ test_slow_mo                      # parametr slow_mo

tests/test_pw_engeto.py
  ├─ test_hlavni_nadpis_je_viditelny   # viditelnost nadpisu
  ├─ test_viditelnost_loga             # viditelnost loga
  ├─ test_viditelnost_linku_vyukovy_portal    # odkaz "Výukový portál"
  ├─ test_odkaz_na_spravnou_url        # kontrola href přes HTML
  ├─ test_klik_na_odkaz                # kliknutí → kontrola URL
  ├─ test_scroll_a_presmerovani_na_blog        # scroll → klik → URL
  ├─ test_presmerovani_a_navrat[Blog-blog]     # parametrizace 1
  └─ test_presmerovani_a_navrat[Reference-absolventi]   # parametrizace 2

tests/test_pw_filtry.py
  └─ test_filter                       # filtrování akademií (nestabilní web)

tests/test_pw_login.py
  └─ test_login                        # login + redirect na Demoqa

tests/test_pw_metody.py
  ├─ test_click                        # metoda click()
  ├─ test_text_input                   # metoda fill()
  ├─ test_login                        # fill()
  ├─ test_press_enter                  # press()
  ├─ test_hover                        # hover()
  ├─ test_more_h4                      # all()
  └─ test_drag_and_drop                # drag_to()

tests/test_pw_mobil.py
  ├─ test_mobile_menu[iPhone 12]       # test mobilního menu – iPhone 12
  └─ test_mobile_menu[Pixel 5]         # test mobilního menu – Pixel 5

tests/test_pw_prohlizec.py
  ├─ test_browser_kompatibilita[chromium]
  ├─ test_browser_kompatibilita[firefox]
  └─ test_browser_kompatibilita[webkit]

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