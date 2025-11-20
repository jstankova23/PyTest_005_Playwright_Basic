# VYLISTOVÁNÍ POMOCÍ WHILE CYKLU VŠECH VESTAVĚNÝCH MOBILNÍCH ZAŘÍZENÍ V PLAYWRIGHTU
# pro ověření přesný názvů zařízení pro testovací funkce
from playwright.sync_api import sync_playwright

with sync_playwright() as p:                    # spuštění Playwrightu
    for nazev_zarizeni in p.devices.keys():     # for cyklus
        print(nazev_zarizeni)                   # tisk všech zařízení

