import random

# --- Stałe Gry ---
WARTOSCI_KART = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
ZNAKI_KART = ['♣', '♦', '♥', '♠']

# --- Stan Gry ---
talia = []
odkryte_z_talii = []
kolumny_gry = [[] for _ in range(7)]
stosy_bazowe = [[] for _ in range(4)]
tryb_debug = False
gra_wygrana = False

# --- Klasy Kart i Logiki ---

class Karta:
    """Reprezentuje pojedynczą kartę."""
    def __init__(self, wartosc, znak):
        self.wartosc = wartosc
        self.znak = znak
        self.odkryta = False
        self.kolor = "czerwony" if self.znak in ['♥', '♦'] else "czarny"

    def __str__(self):
        return f"{self.wartosc}{self.znak}" if self.odkryta else "[?]"

    def __repr__(self):
        if tryb_debug:
             return f"Karta('{self.wartosc}', '{self.znak}', odkryta={self.odkryta})"
        return self.__str__() # Zwróć to samo co str w trybie niedebugowym

class ZarzadcaRuchow:
    """Obsługuje logikę ruchów kart."""
    def __init__(self, kolumny, odkryte, bazy, talia_ref):
        self.kolumny = kolumny
        self.odkryte = odkryte
        self.bazy = bazy
        self.talia = talia_ref

    def przenies_kolumna_na_kolumne(self, zrodlo_idx, cel_idx, ile_kart):
        """Próba przeniesienia 'ile_kart' z kolumny 'zrodlo_idx' do 'cel_idx'."""
        try:
            kol_start = self.kolumny[zrodlo_idx]
            kol_cel = self.kolumny[cel_idx]

            if ile_kart <= 0 or ile_kart > len(kol_start):
                print(f"Nieprawidłowa liczba kart do przeniesienia: {ile_kart}.")
                return False

            stos_do_przeniesienia = kol_start[-ile_kart:]

            if not all(k.odkryta for k in stos_do_przeniesienia):
                print("Nie mogę przenieść zakrytych kart.")
                return False

            if ile_kart > 1:
                for i in range(ile_kart - 1):
                    k1 = stos_do_przeniesienia[i]
                    k2 = stos_do_przeniesienia[i+1]
                    idx1 = WARTOSCI_KART.index(k1.wartosc)
                    idx2 = WARTOSCI_KART.index(k2.wartosc)

                    if k1.kolor == k2.kolor or idx1 != idx2 + 1:
                        print("Przenoszony stos kart nie jest poprawny (kolor/kolejność).")
                        return False

            karta_na_wierzchu_stosu = stos_do_przeniesienia[0]

            if not kol_cel:
                if karta_na_wierzchu_stosu.wartosc != 'K':
                    print("Na pustą kolumnę można położyć tylko Króla.")
                    return False
            else:
                ostatnia_karta_w_celu = kol_cel[-1]
                idx_cel = WARTOSCI_KART.index(ostatnia_karta_w_celu.wartosc)
                idx_przenoszone = WARTOSCI_KART.index(karta_na_wierzchu_stosu.wartosc)

                if ostatnia_karta_w_celu.kolor == karta_na_wierzchu_stosu.kolor or idx_przenoszone + 1 != idx_cel:
                    print(f"Karta {karta_na_wierzchu_stosu} nie pasuje na {ostatnia_karta_w_celu}.")
                    return False

            # Wykonanie ruchu
            self.kolumny[cel_idx].extend(stos_do_przeniesienia)
            self.kolumny[zrodlo_idx] = kol_start[:-ile_kart]

            if self.kolumny[zrodlo_idx] and not self.kolumny[zrodlo_idx][-1].odkryta:
                self.kolumny[zrodlo_idx][-1].odkryta = True
                print(f"Odkryto kartę w kolumnie {zrodlo_idx + 1}.")

            print(f"Przeniesiono {ile_kart} kart z kolumny {zrodlo_idx+1} do kolumny {cel_idx+1}.")
            return True

        except IndexError:
            print("Nieprawidłowe numery kolumn. Użyj liczb od 1 do 7.")
            return False
        except ValueError:
            print("Wystąpił problem z wartością karty.")
            return False
        except Exception as ex:
            print(f"Wystąpił nieoczekiwany błąd przy ruchu kolumna->kolumna: {ex}")
            return False


    def przenies_odkryta_na_kolumne(self, cel_idx):
        """Próba przeniesienia karty z 'Odkryte' na kolumnę 'cel_idx'."""
        if not self.odkryte:
            print("Stos odkryty jest pusty.")
            return False

        karta_z_odkrytych = self.odkryte[0]

        try:
            kol_cel = self.kolumny[cel_idx]

            if not kol_cel:
                if karta_z_odkrytych.wartosc == 'K':
                    self.kolumny[cel_idx].append(self.odkryte.pop(0))
                    print(f"Przeniesiono {karta_z_odkrytych} na pustą kolumnę {cel_idx + 1}.")
                    return True
                else:
                    print(f"Tylko Król ({karta_z_odkrytych}) może iść na pustą kolumnę.")
                    return False
            else:
                ostatnia_w_celu = kol_cel[-1]
                idx_odkryta = WARTOSCI_KART.index(karta_z_odkrytych.wartosc)
                idx_cel = WARTOSCI_KART.index(ostatnia_w_celu.wartosc)

                if karta_z_odkrytych.kolor == ostatnia_w_celu.kolor or idx_odkryta + 1 != idx_cel:
                    print(f"Karta {karta_z_odkrytych} nie pasuje na {ostatnia_w_celu}.")
                    return False

            # Ruch poprawny
            self.kolumny[cel_idx].append(self.odkryte.pop(0))
            print(f"Przeniesiono {karta_z_odkrytych} na kolumnę {cel_idx + 1}.")
            return True

        except IndexError:
            print("Nieprawidłowy numer kolumny docelowej. Użyj liczby od 1 do 7.")
            return False
        except ValueError:
            print("Wystąpił problem z wartością karty.")
            return False


    def przenies_na_baze(self, zrodlo_typ, zrodlo_idx=None):
        """Próba przeniesienia karty na stos bazowy z 'odkryte' lub kolumny."""
        karta_do_przeniesienia = None
        udane_pobranie_karty = False

        if zrodlo_typ == "odkryte":
            if self.odkryte:
                karta_do_przeniesienia = self.odkryte[0]
                udane_pobranie_karty = True
            else:
                print("Stos odkryty jest pusty.")
                return False
        elif zrodlo_typ == "kolumna":
            if 0 <= zrodlo_idx < 7 and self.kolumny[zrodlo_idx]:
                karta_do_przeniesienia = self.kolumny[zrodlo_idx][-1]
                if karta_do_przeniesienia.odkryta:
                    udane_pobranie_karty = True
                else:
                    print(f"Karta na wierzchu kolumny {zrodlo_idx+1} jest zakryta.")
                    return False
            else:
                print(f"Kolumna {zrodlo_idx+1} jest pusta lub nieprawidłowa.")
                return False
        else:
            print("Nieznane źródło karty do przeniesienia na bazę.")
            return False

        if not udane_pobranie_karty:
            return False

        try:
            idx_bazowy = ZNAKI_KART.index(karta_do_przeniesienia.znak)
            baza_cel = self.bazy[idx_bazowy]

            if not baza_cel:
                if karta_do_przeniesienia.wartosc == 'A':
                    pass
                else:
                    print(f"Na pustą bazę {ZNAKI_KART[idx_bazowy]} można dać tylko Asa.")
                    return False
            else:
                ostatnia_w_bazie = baza_cel[-1]
                idx_przenoszone = WARTOSCI_KART.index(karta_do_przeniesienia.wartosc)
                idx_ostatnia_w_bazie = WARTOSCI_KART.index(ostatnia_w_bazie.wartosc)

                if karta_do_przeniesienia.znak != ostatnia_w_bazie.znak or idx_przenoszone != idx_ostatnia_w_bazie + 1:
                    print(f"Karta {karta_do_przeniesienia} nie pasuje na {ostatnia_w_bazie} w bazie.")
                    return False

            # Wykonanie ruchu
            if zrodlo_typ == "odkryte":
                self.bazy[idx_bazowy].append(self.odkryte.pop(0))
                print(f"Przeniesiono {karta_do_przeniesienia} do bazy {ZNAKI_KART[idx_bazowy]}.")
                return True
            elif zrodlo_typ == "kolumna":
                self.bazy[idx_bazowy].append(self.kolumny[zrodlo_idx].pop())
                print(f"Przeniesiono {karta_do_przeniesienia} z kolumny {zrodlo_idx+1} do bazy {ZNAKI_KART[idx_bazowy]}.")
                if self.kolumny[zrodlo_idx] and not self.kolumny[zrodlo_idx][-1].odkryta:
                    self.kolumny[zrodlo_idx][-1].odkryta = True
                    print(f"Odkryto kartę w kolumnie {zrodlo_idx + 1}.")
                return True

        except ValueError:
            print(f"Wystąpił problem z znakiem karty {karta_do_przeniesienia.znak}.")
            return False
        except IndexError:
            print("Wystąpił problem z indeksowaniem baz.")
            return False
        except Exception as ex:
            print(f"Wystąpił nieoczekiwany błąd przy ruchu do bazy: {ex}")
            return False


# --- Wyświetlanie Planszy ---

class PlanszaWyswietlacz:
    """Wyświetla stan gry w konsoli."""
    @staticmethod
    def przygotuj_uklad_poczatkowy(talia_zrodlowa, kolumny_ref):
        print("Rozkładanie kart na planszy...")

        for i in range(7):
            for j in range(i + 1):
                if not talia_zrodlowa:
                    print(f"OSTRZEŻENIE: Zabrakło kart przy rozkładaniu kolumny {i+1}!")
                    break
                karta = talia_zrodlowa.pop(0)
                karta.odkryta = (j == i)
                kolumny_ref[i].append(karta)
            if not talia_zrodlowa and i < 6:
                 print(f"OSTRZEŻENIE: Talia pusta. Układ początkowy może być niekompletny.")
                 break

    @staticmethod
    def wypisz_stan(kolumny, odkryte, bazy, talia_ref):
        print("\n" + "="*10 + " PASJANS " + "="*10)

        print("\n--- Bazy / Talia ---")
        linia1 = ""
        linia2 = ""
        for i in range(4):
            symbol = ZNAKI_KART[i]
            karta_na_bazie = str(bazy[i][-1]) if bazy[i] else "[ ]"
            display_str = f"Baza {symbol}: {karta_na_bazie:<4}"
            if i < 2:
                linia1 += display_str + "    "
            else:
                linia2 += display_str + "    "
        print(linia1.rstrip())
        print(linia2.rstrip())

        karta_odkryta_str = str(odkryte[0]) if odkryte else "[ ]"
        symbol_talii = "[?]" if talia_ref else "[X]"
        print(f"Odkryta: {karta_odkryta_str:<5}         Talia: {symbol_talii:<5} ({len(talia_ref)})")
        print("-" * 30)

        print("\n--- Kolumny ---")
        max_wysokosc = max((len(kol) for kol in kolumny), default=0)

        print(" ".join([f" {i+1}. " for i in range(7)]))
        print("-----" * 7 + "-")

        for j in range(max_wysokosc):
            linia = ""
            for i in range(7):
                if j < len(kolumny[i]):
                    linia += f"{str(kolumny[i][j]):<4}"
                else:
                    linia += "    "
                linia += " "
            print(linia.rstrip())

        print("="*30)


# --- Inne Funkcje Gry ---

def stworz_nowa_talie():
    """Tworzy potasowaną talię 52 kart."""
    talia_kart = [Karta(w, z) for z in ZNAKI_KART for w in WARTOSCI_KART]
    random.shuffle(talia_kart)
    return talia_kart

def dobierz_karte_z_talii():
    """Dobiera kartę z talii na stos odkryty lub odwraca stos odkryty."""
    global talia, odkryte_z_talii
    if talia:
        karta = talia.pop(0)
        karta.odkryta = True
        odkryte_z_talii.insert(0, karta)
        print(f"Dobrano: {karta}")
    elif odkryte_z_talii:
        print("Talia pusta. Odwracam stos odkryty.")
        talia = list(reversed(odkryte_z_talii))
        for k in talia:
            k.odkryta = False
        odkryte_z_talii.clear()
        if talia:
            dobierz_karte_z_talii()
    else:
        print("Brak kart do dobrania.")


def pokaz_pomoc():
    """Wyświetla instrukcje dotyczące komend gry."""
    print("\n--- JAK GRAC? ---")
    print("Komendy (podaj numer kolumny 1-7):")
    print("  dobierz             - Dobierz karte z talii.")
    print("  dk <numer>          - Przenies wierzchnia karte z odkrytych na kolumne <numer>.")
    print("  db                  - Przenies wierzchnia karte z odkrytych na odpowiednia baze.")
    print("  kb <numer>          - Przenies wierzchnia karte z kolumny <numer> na baze.")
    print("  k <skad> <ile> <dokad> - Przenies <ile> kart z kolumny <skad> do <dokad>.")
    print("\nInne komendy:")
    print("  pomoc               - Pokaz ten tekst pomocy.")
    print("  restart             - Zacznij nowa gre.")
    print("  koniec              - Koniec gry.")
    print("  debug               - Pokaz/ukryj informacje debugowania.")
    print("-------------------\n")


def rozpocznij_gre():
    """Inicjuje wszystkie zmienne stanu gry i rozkłada karty."""
    global talia, odkryte_z_talii, kolumny_gry, stosy_bazowe, gra_wygrana

    print("\n--- Zaczynamy nową grę! ---")

    talia = stworz_nowa_talie()
    odkryte_z_talii.clear()
    kolumny_gry = [[] for _ in range(7)]
    stosy_bazowe = [[] for _ in range(4)]
    gra_wygrana = False

    PlanszaWyswietlacz.przygotuj_uklad_poczatkowy(talia, kolumny_gry)

    if talia:
        dobierz_karte_z_talii()


# --- Główna Pętla Gry ---
if __name__ == "__main__":
    rozpocznij_gre()

    zarzadca = ZarzadcaRuchow(kolumny_gry, odkryte_z_talii, stosy_bazowe, talia)

    PlanszaWyswietlacz.wypisz_stan(kolumny_gry, odkryte_z_talii, stosy_bazowe, talia)
    pokaz_pomoc()

    while not gra_wygrana:
        if tryb_debug:
            print("\n--- DEBUG ---")
            print(f"Talia ({len(talia)} kart): {talia[:5]}...")
            print(f"Odkryte ({len(odkryte_z_talii)} kart): {odkryte_z_talii}")
            print("-------------\n")

        komenda_input = input("Twój ruch: ").strip().lower()
        czesci = komenda_input.split()
        akcja = czesci[0] if czesci else ""

        # --- Obsługa komend ---
        if akcja == "koniec":
            print("Kończę grę.")
            break
        elif akcja == "pomoc":
            pokaz_pomoc()
            continue
        elif akcja == "restart":
            rozpocznij_gre()
            zarzadca = ZarzadcaRuchow(kolumny_gry, odkryte_z_talii, stosy_bazowe, talia)
            PlanszaWyswietlacz.wypisz_stan(kolumny_gry, odkryte_z_talii, stosy_bazowe, talia)
            continue
        elif akcja == "debug":
            tryb_debug = not tryb_debug
            print(f"Tryb debugowania: {'WŁĄCZONY' if tryb_debug else 'WYŁĄCZONY'}.")
            continue
        elif akcja == "dobierz":
            dobierz_karte_z_talii()

        # --- Obsługa ruchów ---
        elif akcja == "dk" and len(czesci) == 2:
            try:
                kol_cel = int(czesci[1]) - 1
                if 0 <= kol_cel < 7:
                    zarzadca.przenies_odkryta_na_kolumne(kol_cel)
                else:
                    print("Numer kolumny musi być między 1 a 7.")
            except ValueError:
                print("Podaj poprawny numer kolumny (1-7) po 'dk'.")

        elif akcja == "db" and len(czesci) == 1:
            zarzadca.przenies_na_baze("odkryte")

        elif akcja == "kb" and len(czesci) == 2:
            try:
                kol_zrodlo = int(czesci[1]) - 1
                if 0 <= kol_zrodlo < 7:
                    zarzadca.przenies_na_baze("kolumna", kol_zrodlo)
                else:
                    print("Numer kolumny musi być między 1 a 7.")
            except ValueError:
                print("Podaj poprawny numer kolumny (1-7) po 'kb'.")

        elif akcja == "k" and len(czesci) == 4:
            try:
                kol_start = int(czesci[1]) - 1
                ile_k = int(czesci[2])
                kol_cel = int(czesci[3]) - 1
                if 0 <= kol_start < 7 and 0 <= kol_cel < 7:
                    zarzadca.przenies_kolumna_na_kolumne(kol_start, kol_cel, ile_k)
                else:
                    print("Numery kolumn muszą być między 1 a 7.")
            except ValueError:
                print("Sprawdź format komendy 'k': k <skad> <ile> <dokad> (gdzie <skad>, <ile>, <dokad> to liczby!).")

        # --- Obsługa nieznanej komendy ---
        else:
            if komenda_input:
                print(f"Nie rozumiem komendy '{komenda_input}'. Wpisz 'pomoc', aby zobaczyć dostępne komendy.")

        # --- Wyświetlenie stanu i sprawdzenie wygranej ---
        if akcja not in ["pomoc", "restart", "debug", "koniec"]:
             PlanszaWyswietlacz.wypisz_stan(kolumny_gry, odkryte_z_talii, stosy_bazowe, talia)

        if sum(len(s) for s in stosy_bazowe) == 52:
            print("\n*****************************")
            print("*** GRATULACJE! WYGRAŁEŚ! ***")
            print("*****************************\n")
            gra_wygrana = True

