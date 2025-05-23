import random
import time
from stale import WARTOSCI_KART, ZNAKI_KART
from classy import Karta

talia = []
odkryte_z_talii = []
kolumny_gry = [[], [], [], [], [], [], []]
stosy_bazowe = [[], [], [], []]
gra_wygrana = False
ile_czasu = 0
ruchy = 0
dobrane_karty = 0


def stworz_nowa_talie():
    """Tworzy i tasuje nową talię 52 kart."""
    talia_kart = [
        Karta(w, z) for z in ZNAKI_KART for w in WARTOSCI_KART
    ]
    random.shuffle(talia_kart)
    return talia_kart


def dobierz_karte_z_talii():
    """Dobiera kartę z talii lub odwraca stos odkrytych kart."""
    # 'dobrane_karty' jest przypisywane, więc global jest potrzebny
    global dobrane_karty
    if talia:
        karta = talia.pop(0)
        karta.odkryta = True
        odkryte_z_talii.insert(0, karta)
        dobrane_karty += 1
        print(f"Dobrano: {karta}")
    elif odkryte_z_talii:
        print("Talia pusta. Odwracam stos odkryty.")
        # Odwracamy stos odkrytych kart i przenosimy do talii, zakrywając je
        talia.extend(reversed(odkryte_z_talii))
        for k_in_deck in talia:
            k_in_deck.odkryta = False
        odkryte_z_talii.clear()
        if talia:  # Po odwróceniu talii, od razu dobierz pierwszą kartę
            dobierz_karte_z_talii()
    else:
        print("Brak kart do dobrania.")


def pokaz_pomoc():
    print("\n--- JAK GRAC? ---")
    print("Komendy (podaj numer kolumny 1-7):")
    print("  dobierz                 - Dobierz kartę z talii.")
    print("  dk <numer>              - Przenieś odkrytą kartę na kol.")
    print("  db                      - Przenieś odkrytą kartę na bazę.")
    print("  kb <numer>              - Przenieś kartę z kol. <numer> na bazę.")
    print("  k <skad> <ile> <dokad>  - Przenieś <ile> kart z kol. <skad>")
    print("                            do <dokad>.")
    print("\nInne komendy:")
    print("  pomoc                   - Pokaż instrukcję.")
    print("  restart                 - Nowa gra.")
    print("  koniec                  - Zakończ grę.")
    print("  debug                   - Włącz/Wyłącz debug.")
    print("-------------------")


def rozpocznij_gre():
    """Inicjalizuje lub resetuje stan gry."""
    # Te zmienne są przypisywane, więc 'global' jest potrzebny
    global gra_wygrana, ile_czasu, ruchy, dobrane_karty

    print("\n--- Zaczynamy nową grę! ---")
    # Używamy clear() i extend() zamiast ponownego przypisywania,
    # aby zachować referencje do list w main.py
    talia.clear()
    talia.extend(stworz_nowa_talie())
    odkryte_z_talii.clear()
    # Modyfikujemy listy w miejscu, aby main.py miał aktualne referencje
    for i in range(7):
        kolumny_gry[i].clear()
    for i in range(4):
        stosy_bazowe[i].clear()

    gra_wygrana = False
    ruchy = 0
    dobrane_karty = 0
    ile_czasu = time.time()
