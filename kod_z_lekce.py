import json
from pprint import pprint
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def main():
    datum = datetime.now().strftime("%Y%m%d") #datum ve formatu YYYYMMDD
    restaurace = "Taste_of_India"
    url = "https://www.taste-of-india.cz/"
    jmeno_souboru = f"{datum}_{restaurace}_menu.json"
    menu_slovnik = denni_menu(url)
    uloz_menu_do_json(menu_slovnik, jmeno_souboru)


def denni_menu(url) -> dict:
    """
    Funkce, ktera zajistuje cely proces web scrapingu.
    """
    soup = zpracuj_odpoved_serveru(url)
    vsechny_tagy_li = najdi_sekci_menu(soup)
    # print(vsechny_tagy_li[1].prettify())
    tento_tyden = [ filtruj_jidlo(li) for li in vsechny_tagy_li[1:6] ]
    # pprint(tento_tyden)
    tento_tyden_slovnik = {den.pop('den'): den for den in tento_tyden}
    # pprint(tento_tyden_slovnik)
    return tento_tyden_slovnik


def zpracuj_odpoved_serveru(url: str):
    """
    Odesli pozadavek na url adresu a vracene
    HTML parsuj pomoci 'BeatutifulSoup'.
    """
    odpoved = requests.get(url)
    return BeautifulSoup(odpoved.text, 'html.parser')

def najdi_sekci_menu(soup):
    """Najdi cast html s dennim menu a
    rozdel ji na jednotlive dny."""
    # ul = unordered list, li = list
    sekce_menu = soup.find("ul", {"class": "daily-menu"})
    return sekce_menu.find_all("li")


def filtruj_jidlo(li_tag):
    """
    Z kazdeho radku ('\n') vyber jidlo a jeho cenu
    a zabal je do slovniku.
    """
    radky = li_tag.get_text("\n").splitlines()
    radky = [r.replace("\xa0", " ") for r in radky]
    return {
        "den": radky[0],
        "polevka": jidlo_a_cena(radky[1]),
        "menu_1": jidlo_a_cena(radky[2]),
        "menu_2": jidlo_a_cena(radky[3]),
        "menu_3": jidlo_a_cena(radky[4]),
        "menu_4": jidlo_a_cena(radky[5]),
    }


def jidlo_a_cena(radek: str) -> dict:
    *jidlo, cena = radek.split(" ")
    # print(jidlo, cena, sep="\n")
    return {" ".join(jidlo): int(cena[:-2])}


def uloz_menu_do_json(menu_slovnik, nazev_souboru):
    with open(nazev_souboru, mode="w", encoding='utf-8') as json_soubor:
        json.dump(menu_slovnik, json_soubor)
    print(f"Ulozeno do {nazev_souboru}")


if __name__ == "__main__":
    main()