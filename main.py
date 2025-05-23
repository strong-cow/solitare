import time
from colorama import init

# Importujemy klasy z classy.py
from classy import ZarzadcaRuchow, PlanszaWyswietlacz
# Importujemy funkcje i zmienne globalne z funkcje.py
from funkcje import (
    talia, odkryte_z_talii, kolumny_gry, stosy_bazowe,
    gra_wygrana, ile_czasu, ruchy, dobrane_karty,
    dobierz_karte_z_talii, pokaz_pomoc, rozpocznij_gre
)

init(autoreset=True)


# --- Główna Pętla Gry ---
if __name__ == "__main__":
    rozpocznij_gre()
    # Zarządca ruchów musi być zainicjalizowany z referencjami
    # do aktualnych list
    tryb_debug = False
    zarzadca = ZarzadcaRuchow(
        kolumny_gry, odkryte_z_talii, stosy_bazowe, talia, tryb_debug
    )
    PlanszaWyswietlacz.przygotuj_uklad_poczatkowy(talia, kolumny_gry)
    PlanszaWyswietlacz.wypisz_stan(kolumny_gry, odkryte_z_talii,
                                   stosy_bazowe, talia)

    pokaz_pomoc()
    wykonano_ruch_w_turze = False

    while not gra_wygrana:
        if wykonano_ruch_w_turze:
            ruchy += 1
            wykonano_ruch_w_turze = False

        if tryb_debug:
            print("--- DEBUG ---")
            print(f"Talia ({len(talia)}): {[str(k) for k in talia]}")
            print(f"Odkryte ({len(odkryte_z_talii)}): "
                  f"{[str(k) for k in odkryte_z_talii]}")

        komenda_input = input("Twój ruch: ").strip().lower()
        czesci = komenda_input.split()
        akcja = czesci[0] if czesci else ""

        udany_ruch = False

        if akcja == "koniec":
            print("Kończę grę.")
            break
        elif akcja == "pomoc":
            pokaz_pomoc()
            continue
        elif akcja == "restart":
            rozpocznij_gre()
            zarzadca = ZarzadcaRuchow(
                kolumny_gry, odkryte_z_talii, stosy_bazowe, talia, tryb_debug
            )
            PlanszaWyswietlacz.przygotuj_uklad_poczatkowy(talia, kolumny_gry)
            PlanszaWyswietlacz.wypisz_stan(kolumny_gry, odkryte_z_talii,
                                           stosy_bazowe, talia)
            pokaz_pomoc()
            wykonano_ruch_w_turze = False
            continue
        elif akcja == "debug":
            tryb_debug = not tryb_debug
            print(f"Tryb debugowania: "
                  f"{'WŁĄCZONY' if tryb_debug else 'WYŁĄCZONY'}.")
            continue

        elif akcja == "dobierz":
            dobierz_karte_z_talii()
            udany_ruch = True

        elif akcja == "dk" and len(czesci) == 2:
            try:
                kol_cel_idx = int(czesci[1]) - 1
                if 0 <= kol_cel_idx < 7:
                    if zarzadca.przenies_odkryta_na_kolumne(kol_cel_idx):
                        udany_ruch = True
                else:
                    print("Numer kolumny musi być między 1 a 7.")
            except ValueError:
                print("Podaj poprawny numer kolumny (1-7) po 'dk'.")

        elif akcja == "db" and len(czesci) == 1:
            if zarzadca.przenies_na_baze("odkryte"):
                udany_ruch = True

        elif akcja == "kb" and len(czesci) == 2:
            try:
                kol_zrodlo_idx = int(czesci[1]) - 1
                if 0 <= kol_zrodlo_idx < 7:
                    if zarzadca.przenies_na_baze("kolumna", kol_zrodlo_idx):
                        udany_ruch = True
                else:
                    print("Numer kolumny musi być między 1 a 7.")
            except ValueError:
                print("Podaj poprawny numer kolumny (1-7) po 'kb'.")

        elif akcja == "k" and len(czesci) == 4:
            try:
                kol_start_idx = int(czesci[1]) - 1
                liczba_kart_do_przeniesienia = int(czesci[2])
                kol_cel_idx = int(czesci[3]) - 1
                if 0 <= kol_start_idx < 7 and 0 <= kol_cel_idx < 7:
                    if zarzadca.przenies_kolumna_na_kolumne(
                        kol_start_idx,
                        kol_cel_idx,
                        liczba_kart_do_przeniesienia
                    ):
                        udany_ruch = True
                else:
                    print("Numery kolumn muszą być między 1 a 7.")
            except ValueError:
                print("Sprawdź format: k <skad> <ile> <dokad> (liczby!).")

        else:
            if komenda_input:
                print(f"Nie rozumiem komendy '{komenda_input}'. "
                      "Wpisz 'pomoc'.")

        if udany_ruch:
            wykonano_ruch_w_turze = True

        if akcja not in ["pomoc", "restart", "debug", "koniec"]:
            PlanszaWyswietlacz.wypisz_stan(kolumny_gry, odkryte_z_talii,
                                           stosy_bazowe, talia)

        # Sprawdzenie warunku wygranej musi używać aktualnego stanu
        if sum(len(s) for s in stosy_bazowe) == 52:
            czas_koniec = time.time()
            czas_gry_sek = int(czas_koniec - ile_czasu)
            minuty = czas_gry_sek // 60
            sekundy = czas_gry_sek % 60

            final_ruchy = ruchy
            if wykonano_ruch_w_turze:
                final_ruchy += 1

            print("\n*****************************")
            print("*** GRATULACJE! WYGRAŁEŚ! ***")
            print("*****************************\n")
            print("Dziękuję za grę!")

            staty_text = "Chcesz zobaczyć statystyki? (tak/nie): "
            staty_tak_nie = input(staty_text).strip().lower()
            if staty_tak_nie == "tak":
                print("Statystyki:")
                print(f"Czas gry: {minuty} minut {sekundy} sekund")
                print(f"Liczba ruchów: {final_ruchy}")
                if final_ruchy > 0 and czas_gry_sek > 0:
                    sr_czas_ruch = czas_gry_sek / final_ruchy
                    sr_ruchy_min = final_ruchy / (czas_gry_sek / 60)
                    print(f"Średni czas na ruch: {sr_czas_ruch:.2f} s")
                    print("Śr. ruchów na minutę: "
                          f"{sr_ruchy_min:.2f}")
                elif final_ruchy > 0:
                    print("Średni czas na ruch: b.d. (czas gry 0s)")
                    print("Śr. ruchów na minutę: b.d. (czas gry 0s)")
                else:
                    print("Średni czas na ruch: b.d. (brak ruchów)")
                    print("Śr. ruchów na minutę: b.d. (brak ruchów)")
                print(f"Ilość dobranych kart: {dobrane_karty}")
            gra_wygrana = True
