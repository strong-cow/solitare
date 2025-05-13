import random

# --- Globalne Stałe ---
WARTOSCI_KART_ORDER = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITS_ORDER = ['♣', '♦', '♥', '♠'] # Kolejność dla stosów bazowych

# --- Klasy ---

class Karta:
    def __init__(self, wartosc, znak):
        self.wartosc = wartosc
        self.znak = znak
        self.odkryta = False

        if self.znak in ['♥', '♦']:
            self.kolor_rgb = "czerwony"
        elif self.znak in ['♠', '♣']:
            self.kolor_rgb = "czarny"
        else:
            self.kolor_rgb = "nieznany"

    def __str__(self):
        return f"{self.wartosc}{self.znak}" if self.odkryta else "[?]"

    def __repr__(self):
        return f"Karta(w={self.wartosc!r}, z={self.znak!r}, o={self.odkryta})"


class Przenoszenie:
    def __init__(self, mapa_gry, dodatkowe_karty_gry, stosy_bazowe_gry, talia_gry, wartosci_order, suits_order):
        self.mapa = mapa_gry
        self.dodatkowe_karty = dodatkowe_karty_gry
        self.stosy_bazowe = stosy_bazowe_gry
        self.talia = talia_gry # Mimo że nie używana w tych metodach, może być potrzebna dla innych
        self.WARTOSCI_KART_ORDER = wartosci_order
        self.SUITS_ORDER = suits_order

    def przenies_tableau_na_tableau(self, kolumna_start_idx, kolumna_docelowa_idx, liczba_kart):
        try:
            # print(f"Próba ruchu: z kolumny {kolumna_start_idx + 1} do kolumny {kolumna_docelowa_idx + 1}, {liczba_kart} kart.") # Już jest w pętli gry

            if not (0 <= kolumna_start_idx < 7 and 0 <= kolumna_docelowa_idx < 7):
                raise IndexError("Nieprawidłowy numer kolumny.")
            if liczba_kart <= 0:
                raise ValueError("Liczba kart do przeniesienia musi być dodatnia.")

            kolumna_start = self.mapa[kolumna_start_idx]
            
            if len(kolumna_start) < liczba_kart:
                raise ValueError(f"Brak {liczba_kart} kart w kolumnie startowej {kolumna_start_idx + 1} (jest {len(kolumna_start)}).")

            karty_do_przeniesienia_stack = kolumna_start[-liczba_kart:]

            for karta in karty_do_przeniesienia_stack:
                if not karta.odkryta:
                    raise ValueError("Nie można przenieść zakrytych kart.")
            
            karta_do_polozenia = karty_do_przeniesienia_stack[0]

            kolumna_docelowa = self.mapa[kolumna_docelowa_idx]
            if not kolumna_docelowa:
                if karta_do_polozenia.wartosc != 'K':
                    raise ValueError("Na pustą kolumnę można położyć tylko Króla.")
            else:
                ostatnia_karta_docelowa = kolumna_docelowa[-1]
                if ostatnia_karta_docelowa.kolor_rgb == karta_do_polozenia.kolor_rgb:
                    raise ValueError("Kolory kart muszą być naprzemienne.")
                idx_docelowa = self.WARTOSCI_KART_ORDER.index(ostatnia_karta_docelowa.wartosc)
                idx_przenoszona = self.WARTOSCI_KART_ORDER.index(karta_do_polozenia.wartosc)
                if idx_przenoszona + 1 != idx_docelowa:
                    raise ValueError("Wartość przenoszonej karty nie pasuje (musi być o jeden niższa).")

            self.mapa[kolumna_docelowa_idx].extend(kolumna_start[-liczba_kart:])
            self.mapa[kolumna_start_idx] = kolumna_start[:-liczba_kart]

            if self.mapa[kolumna_start_idx] and not self.mapa[kolumna_start_idx][-1].odkryta:
                self.mapa[kolumna_start_idx][-1].odkryta = True
                print(f"Odkryto kartę {self.mapa[kolumna_start_idx][-1]} w kolumnie {kolumna_start_idx + 1}.")

            print(f"Przeniesiono {liczba_kart} kart z kolumny {kolumna_start_idx+1} do {kolumna_docelowa_idx+1}.")
            return True
        except (ValueError, IndexError) as e:
            print(f"Błąd ruchu T->T: {e}")
            return False
        except Exception as blad:
            print(f"Wystąpił nieoczekiwany błąd podczas ruchu T->T: {blad}")
            return False

    def przenies_odkryte_na_tableau(self, kolumna_docelowa_idx):
        if not self.dodatkowe_karty:
            print("Błąd: Stos kart dobranych jest pusty.")
            return False

        karta_do_przeniesienia = self.dodatkowe_karty[0]

        if not (0 <= kolumna_docelowa_idx < len(self.mapa)):
            print("Błąd: Nieprawidłowy numer kolumny docelowej.")
            return False

        docelowa_kolumna_list = self.mapa[kolumna_docelowa_idx]

        if not docelowa_kolumna_list:
            if karta_do_przeniesienia.wartosc == 'K':
                self.mapa[kolumna_docelowa_idx].append(self.dodatkowe_karty.pop(0))
                print(f"Przeniesiono {karta_do_przeniesienia} na pustą kolumnę {kolumna_docelowa_idx + 1}.")
                return True
            else:
                print(f"Błąd: Na pustą kolumnę można położyć tylko Króla. {karta_do_przeniesienia} nie pasuje.")
                return False

        ostatnia_karta_w_kolumnie = docelowa_kolumna_list[-1]

        if karta_do_przeniesienia.kolor_rgb == ostatnia_karta_w_kolumnie.kolor_rgb:
            print(f"Błąd: Kolory muszą być naprzemienne.")
            return False

        idx_przenoszona = self.WARTOSCI_KART_ORDER.index(karta_do_przeniesienia.wartosc)
        idx_docelowa = self.WARTOSCI_KART_ORDER.index(ostatnia_karta_w_kolumnie.wartosc)

        if idx_przenoszona + 1 == idx_docelowa:
            self.mapa[kolumna_docelowa_idx].append(self.dodatkowe_karty.pop(0))
            print(f"Przeniesiono {karta_do_przeniesienia} na {ostatnia_karta_w_kolumnie} w kolumnie {kolumna_docelowa_idx + 1}.")
            return True
        else:
            print(f"Błąd: Wartość nie pasuje. {karta_do_przeniesienia} ({self.WARTOSCI_KART_ORDER[idx_przenoszona]}) "
                  f"nie może być położona na {ostatnia_karta_w_kolumnie} ({self.WARTOSCI_KART_ORDER[idx_docelowa]}).")
            return False
        return False # Domyślnie

    def przenies_na_baze(self, zrodlo_typ, zrodlo_idx=None):
        karta_do_przeniesienia = None

        if zrodlo_typ == "dodatkowe":
            if not self.dodatkowe_karty:
                print("Błąd: Stos kart dobranych jest pusty.")
                return False
            karta_do_przeniesienia = self.dodatkowe_karty[0]
        elif zrodlo_typ == "mapa":
            if not (0 <= zrodlo_idx < len(self.mapa)) or not self.mapa[zrodlo_idx]:
                print("Błąd: Nieprawidłowa lub pusta kolumna źródłowa.")
                return False
            karta_do_przeniesienia = self.mapa[zrodlo_idx][-1]
            if not karta_do_przeniesienia.odkryta:
                print("Błąd: Karta na wierzchu kolumny jest zakryta.")
                return False
        else:
            print("Błąd: Nieznany typ źródła dla przeniesienia do bazy.")
            return False

        try:
            target_foundation_idx = self.SUITS_ORDER.index(karta_do_przeniesienia.znak)
        except ValueError:
            print(f"Błąd: Nieznany znak karty {karta_do_przeniesienia.znak}.")
            return False

        docelowy_stos_bazowy = self.stosy_bazowe[target_foundation_idx]

        if not docelowy_stos_bazowy:
            if karta_do_przeniesienia.wartosc == 'A':
                pass
            else:
                print(f"Błąd: Na pusty stos bazowy {self.SUITS_ORDER[target_foundation_idx]} można położyć tylko Asa.")
                return False
        else:
            ostatnia_karta_w_bazie = docelowy_stos_bazowy[-1]
            idx_przenoszona = self.WARTOSCI_KART_ORDER.index(karta_do_przeniesienia.wartosc)
            idx_ostatnia_w_bazie = self.WARTOSCI_KART_ORDER.index(ostatnia_karta_w_bazie.wartosc)

            if idx_przenoszona != idx_ostatnia_w_bazie + 1:
                print(f"Błąd: {karta_do_przeniesienia} nie pasuje na {ostatnia_karta_w_bazie} w stosie bazowym.")
                return False

        if zrodlo_typ == "dodatkowe":
            docelowy_stos_bazowy.append(self.dodatkowe_karty.pop(0))
        elif zrodlo_typ == "mapa":
            docelowy_stos_bazowy.append(self.mapa[zrodlo_idx].pop())
            if self.mapa[zrodlo_idx] and not self.mapa[zrodlo_idx][-1].odkryta:
                self.mapa[zrodlo_idx][-1].odkryta = True
                print(f"Odkryto kartę {self.mapa[zrodlo_idx][-1]} w kolumnie {zrodlo_idx + 1}.")

        print(f"Przeniesiono {karta_do_przeniesienia} do stosu bazowego {self.SUITS_ORDER[target_foundation_idx]}.")
        return True
        return False # Domyślnie

class mapa_pasjansa: # Ta klasa pozostaje bez zmian, operuje na globalnych
    @staticmethod
    def generuj_mape(talia_do_rozlozenia):
        global mapa, plansza
        mapa = [[] for _ in range(7)]
        # ... (reszta bez zmian) ...
        print(f"Funkcja generuj_mape: Rozkładanie {len(plansza)} kart z listy 'plansza' na mapie.")

        for i in range(7):
            for j in range(i + 1):
                if not plansza:
                    print(f"OSTRZEŻENIE: Brak kart w 'plansza' do rozłożenia w kolumnie {i+1}, karcie {j+1}.")
                    break
                karta = plansza.pop(0)
                karta.odkryta = (j == i)
                mapa[i].append(karta)
            if not plansza and i < 6: 
                if (i + 1) + 1 > 0 : 
                     print(f"OSTRZEŻENIE: Lista 'plansza' pusta po kolumnie {i+1}. Nie można dokończyć rozkładania mapy.")

    @staticmethod
    def wypisz_mape():
        global mapa, dodatkowe_karty, talia, stosy_bazowe, SUITS_ORDER
        # ... (reszta bez zmian) ...
        print("\n--- Mapa Planszy ---")
        max_wysokosc = max((len(kolumna) for kolumna in mapa), default=0)

        for j in range(max_wysokosc):
            linia_wydruku = ""
            for i in range(7):
                linia_wydruku += f"{str(mapa[i][j]):<4}" if j < len(mapa[i]) else "    " 
                linia_wydruku += " "
            print(linia_wydruku.rstrip())
        print("-" * (7 * 5)) 

        print("\n--- Stosy Bazowe i Dobieranie ---")
        foundation_lines = ["", ""]
        for i in range(4):
            suit_char = SUITS_ORDER[i]
            top_card_in_foundation = str(stosy_bazowe[i][-1]) if stosy_bazowe[i] else "[ ]"
            display_str = f"Baza {suit_char}: {top_card_in_foundation:<4}"
            if i < 2:
                foundation_lines[0] += display_str + "   "
            else:
                foundation_lines[1] += display_str + "   "

        print(foundation_lines[0].rstrip())
        print(foundation_lines[1].rstrip())

        odkryta_karta_str = str(dodatkowe_karty[0]) if dodatkowe_karty else "[ ]"
        symbol_talii = "[?]" if talia else "[X]" 
        print(f"Odkryta: {odkryta_karta_str:<5}          Talia: {symbol_talii:<5}")
        print("-" * (7 * 5))


# --- Funkcje gry (pozostające poza klasą MenedzerRuchow) ---

def stworz_karty():
    global WARTOSCI_KART_ORDER, SUITS_ORDER
    talia = [Karta(wartosc, znak) for znak in SUITS_ORDER for wartosc in WARTOSCI_KART_ORDER]
    random.shuffle(talia)
    return talia

def posegreguj_karty(talia_gry):
    global plansza
    liczba_kart_potrzebna = 28
    # ... (reszta bez zmian) ...
    print(f"Funkcja posegreguj_karty: Próba przeniesienia {liczba_kart_potrzebna} kart z talii do listy 'plansza'.")

    liczba_kart_do_przeniesienia = min(len(talia_gry), liczba_kart_potrzebna)
    if len(talia_gry) < liczba_kart_potrzebna:
        print(f"OSTRZEŻENIE: W talii jest tylko {len(talia_gry)} kart. Przenoszę wszystkie dostępne.")

    for _ in range(liczba_kart_do_przeniesienia):
        plansza.append(talia_gry.pop(0))

    print(f"Funkcja posegreguj_karty: Zakończono. Lista 'plansza' zawiera teraz {len(plansza)} kart.")


def dobierz_dodatkowa_karte():
    global talia, dodatkowe_karty
    # ... (reszta bez zmian) ...
    if talia:
        dobrana_karta = talia.pop(0)
        dobrana_karta.odkryta = True
        dodatkowe_karty.insert(0, dobrana_karta) 
        print(f"Dobrano kartę: {dobrana_karta}")
    elif dodatkowe_karty: 
        print("Talia pusta. Odwracam stos odkryty.")
        talia.extend(reversed(dodatkowe_karty)) 
        for karta in talia:
            karta.odkryta = False 
        dodatkowe_karty.clear()
        if talia:
             dobierz_dodatkowa_karte()
    else:
        print("Talia i stos odkryty są puste.")

# --- Główna część skryptu ---

talia = []
dodatkowe_karty = []
plansza = []
mapa = []
stosy_bazowe = [[] for _ in range(4)]
wygrana = False

talia = stworz_karty()
posegreguj_karty(talia)

if talia:
    pierwsza_dobrana = talia.pop(0)
    pierwsza_dobrana.odkryta = True
    dodatkowe_karty.insert(0, pierwsza_dobrana) # Używamy insert, aby była na [0]
else:
    print("Błąd krytyczny: Talia jest pusta po rozłożeniu na planszę!")
    exit()

mapa_pasjansa.generuj_mape(talia)

# UTWORZENIE INSTANCJI MENEDŻERA RUCHÓW
menedzer_ruchow = MenedzerRuchow(mapa, dodatkowe_karty, stosy_bazowe, talia, WARTOSCI_KART_ORDER, SUITS_ORDER)

mapa_pasjansa.wypisz_mape()

# --- Pętla Gry ---
while not wygrana:
    print(f"(Debug: Odkryte: {dodatkowe_karty[0] if dodatkowe_karty else 'brak'}, Talia: {len(talia)})")

    opcja_str = input("\nOpcje: [0]dobierz, [dk K]odkryta->kol K, [db]odkryta->baza, [kb K]kol K->baza, [Z K1 ILE K2]ruch, [000]koniec: ").strip().lower()
    opcje_wejsciowe = opcja_str.split()
    akcja = opcje_wejsciowe[0] if opcje_wejsciowe else ""

    if akcja == "000":
        print("Przerwanie gry.")
        wygrana = True
    elif akcja == "0":
        dobierz_dodatkowa_karte()
    elif akcja == "dk" and len(opcje_wejsciowe) == 2:
        try:
            kol_docelowa = int(opcje_wejsciowe[1]) - 1
            menedzer_ruchow.przenies_odkryte_na_tableau(kol_docelowa)
        except ValueError:
            print("Błąd: Nieprawidłowy numer kolumny dla 'dk'.")
    elif akcja == "db" and len(opcje_wejsciowe) == 1:
        menedzer_ruchow.przenies_na_baze("dodatkowe")
    elif akcja == "kb" and len(opcje_wejsciowe) == 2:
        try:
            kol_zrodlowa = int(opcje_wejsciowe[1]) - 1
            menedzer_ruchow.przenies_na_baze("mapa", kol_zrodlowa)
        except ValueError:
            print("Błąd: Nieprawidłowy numer kolumny dla 'kb'.")
    elif len(opcje_wejsciowe) == 3: # Ruch Z K1 ILE K2 - zakładamy, że pierwszy element to kolumna źródłowa
        try:
            # Poprawiona interpretacja dla Z K1 ILE K2 - opcje_wejsciowe[0] to Z
            kol_start = int(opcje_wejsciowe[0]) - 1 # Pierwszy argument to kolumna startowa
            liczba_k = int(opcje_wejsciowe[1])     # Drugi to liczba kart
            kol_doc = int(opcje_wejsciowe[2]) - 1   # Trzeci to kolumna docelowa
            menedzer_ruchow.przenies_tableau_na_tableau(kol_start, kol_doc, liczba_k)
        except ValueError:
            print("Błąd: Nieprawidłowe argumenty dla ruchu (np. Z K1 ILE K2). Podaj liczby.")
        except IndexError:
            print("Błąd: Nieprawidłowy numer kolumny dla ruchu.")
    else:
        print("Niepoprawna opcja. Spróbuj ponownie.")

    mapa_pasjansa.wypisz_mape()

    if sum(len(s) for s in stosy_bazowe) == 52:
        print("Gratulacje! Wygrałeś!")
        wygrana = True

print("Koniec gry.")