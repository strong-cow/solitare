import random

# --- Klasy ---

class Karta:
    def __init__(self, wartosc, znak):
        self.wartosc = wartosc  # Np. K, 7, A
        self.znak = znak        # ♠ ♥ ♦ ♣
        self.odkryta = False    # Domyślnie karty na planszy są zakryte

        # Określenie koloru (czerwony/czarny) na podstawie znaku
        if self.znak in ['♥', '♦']:
            self.kolor_rgb = "czerwony"
        elif self.znak in ['♠', '♣']:
            self.kolor_rgb = "czarny"
        else:
            self.kolor_rgb = "nieznany"

    def __str__(self):
        # Reprezentacja tekstowa dla użytkownika
        return f"{self.wartosc}{self.znak}" if self.odkryta else "[?]"

    def __repr__(self):
        
        # Reprezentacja techniczna dla debugowania
        return f"Karta(wartosc={self.wartosc!r}, znak={self.znak!r}, odkryta={self.odkryta})"


class mapa_pasjansa:
    @staticmethod

    def generuj_mape(talia):
        """Rozkłada karty na planszy w strukturze pasjansa."""
        global mapa, plansza
        mapa = [[] for _ in range(7)]  # Lista list reprezentująca kolumny na planszy

        print(f"Funkcja generuj_mape: Rozkładanie {len(plansza)} kart z listy 'plansza' na mapie.")

        for i in range(7):  # Iterujemy przez 7 kolumn
            for j in range(i + 1):  # Dla każdej kolumny 'i', dodajemy 'i + 1' kart
                if not plansza:
                    print(f"OSTRZEŻENIE: Brak kart w 'plansza' do rozłożenia w kolumnie {i+1}, karcie {j+1}.")
                    break
                karta = plansza.pop(0)
                karta.odkryta = (j == i)  # Odkryj ostatnią kartę w kolumnie
                mapa[i].append(karta)

            if not plansza and i < 6:
                print(f"OSTRZEŻENIE: Lista 'plansza' pusta po kolumnie {i+1}. Nie można dokończyć rozkładania mapy.")
                break

    @staticmethod
    def wypisz_mape():
        """Wyświetla aktualny stan mapy planszy."""
        print("\n--- Mapa Planszy ---")
        max_wysokosc = max((len(kolumna) for kolumna in mapa), default=0)
    
        for j in range(max_wysokosc):  # Iterujemy przez "wiersze" głębokości
            linia_wydruku = ""
            for i in range(7):  # Iterujemy przez kolumny
                linia_wydruku += f"{str(mapa[i][j]):<5}" if j < len(mapa[i]) else "     "
                linia_wydruku += " "
            print(linia_wydruku)
        print("-" * 30)

        # Wyświetlanie stosów bazowych i dobierania
        print("\n--- Stosy Bazowe i Dobieranie ---")
        print("                           ♥ [ ]")
        print("                           ♦ [ ]")
        odkryta_karta_str = str(dodatkowe_karty[0]) if dodatkowe_karty else "[ ]"
        symbol_talii = "[?]" if talia else "[ ]"
        print(f"Odkryta: {odkryta_karta_str:<5}             ♠ [ ]")
        print(f"Talia: {symbol_talii:<5}               ♣ [ ]")
        print("-" * 30)

# --- Funkcje gry ---

def stworz_karty():
    """Tworzy i zwraca potasowaną talię obiektów Karta."""
    znaki = ['♣', '♦', '♥', '♠']
    wartosci = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    talia = [Karta(wartosc, znak) for znak in znaki for wartosc in wartosci]
    random.shuffle(talia)
    return talia

def posegreguj_karty(talia):
    """Przygotowuje karty do rozłożenia na planszy."""
    liczba_kart_potrzebna = 28
    print(f"Funkcja posegreguj_karty: Próba przeniesienia {liczba_kart_potrzebna} kart z talii do planszy.")

    global plansza

    liczba_kart_do_przeniesienia = min(len(talia), liczba_kart_potrzebna)
    if len(talia) < liczba_kart_potrzebna:
        print(f"OSTRZEŻENIE: W talii jest tylko {len(talia)} kart. Przenoszę wszystkie dostępne.")

    for _ in range(liczba_kart_do_przeniesienia):
        plansza.append(talia.pop(0))

    print(f"Funkcja posegreguj_karty: Zakończono. Lista 'plansza' zawiera teraz {len(plansza)} kart.")

def dobierz_dodatkowa_karte():
    """Dobiera kartę z talii do stosu odkrytego."""
    global talia, dodatkowe_karty
    if talia:
        dobrana_karta = talia.pop(0)
        dobrana_karta.odkryta = True
        dodatkowe_karty.insert(0, dobrana_karta)
        print(f"Dobrano kartę: {dobrana_karta}")
    elif dodatkowe_karty:
        talia.extend(dodatkowe_karty)
        dodatkowe_karty.clear()
    else:
        print("Talia i stos odkryty są puste.")


def poruszanie_kartami(linia_start, kolumna_docelowa, liczba_kart):
    """Przenosi karty między kolumnami."""
    try:
        print(f"Próba ruchu: z kolumny {linia_start + 1} do kolumny {kolumna_docelowa + 1}, {liczba_kart} kart.")

        # Definicja kolejności wartości kart
        wartosci_kart = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        # Sprawdź, czy w kolumnie startowej jest wystarczająca liczba kart
        if len(mapa[linia_start]) < liczba_kart:
            raise IndexError("Brak wystarczającej liczby kart w kolumnie startowej.")

        # Sprawdź, czy wszystkie karty do przeniesienia są odkryte
        for karta in mapa[linia_start][-liczba_kart:]:
            if not karta.odkryta:
                raise ValueError("Nie można przenieść zakrytych kart. Odkryj je przed przeniesieniem.")

        # Sprawdź, czy karty do przeniesienia są w odpowiedniej kolejności
        for i in range(-liczba_kart, -1):
            wartosc_aktualna = mapa[linia_start][i].wartosc
            wartosc_nastepna = mapa[linia_start][i + 1].wartosc
            if wartosci_kart.index(wartosc_aktualna) - 1 != wartosci_kart.index(wartosc_nastepna):
                raise ValueError("Karty do przeniesienia nie są w odpowiedniej kolejności.")

        # Sprawdź, czy karta w kolumnie docelowej ma odpowiednią wartość
        if mapa[kolumna_docelowa]:
            wartosc_docelowa = mapa[kolumna_docelowa][-1].wartosc
            wartosc_przenoszona = mapa[linia_start][-liczba_kart].wartosc
            if wartosci_kart.index(wartosc_przenoszona) + 1 != wartosci_kart.index(wartosc_docelowa):
                raise ValueError("Karta w kolumnie docelowej nie pasuje do przenoszonej karty.")

        tymczasowe = []

        # Pobierz karty z kolumny startowej
        for _ in range(liczba_kart):
            tymczasowe.append(mapa[linia_start].pop())

        # Odkryj ostatnią kartę w kolumnie startowej, jeśli istnieje
        if mapa[linia_start]:
            mapa[linia_start][-1].odkryta = True

        # Odwróć kolejność kart, aby zachować poprawną kolejność w kolumnie docelowej
        tymczasowe.reverse()

        # Dodaj karty do kolumny docelowej
        mapa[kolumna_docelowa].extend(tymczasowe)
        print(f"Karty przeniesione: {tymczasowe}")

    except ValueError as e:
        print(f"Błąd: {e}")
    except IndexError:
        print("Błąd: Podano nieistniejącą kolumnę lub brak wystarczającej liczby kart.")
    except Exception as blad:
        print(f"Wystąpił błąd podczas ruchu: {blad}")


# --- Główna część skryptu ---

# Inicjalizacja zmiennych globalnych
talia = []
dodatkowe_karty = []  # Stos odkryty
plansza = []  # Tymczasowa lista kart do rozłożenia na mapie
mapa = []  # Kolumny na planszy
stosy_bazowe = [[], [], [], []]  # Cztery stosy bazowe
wygrana = False

# 1. Tworzenie i tasowanie talii 52 kart
talia = stworz_karty()
print(f"Stworzono potasowaną talię: {len(talia)} kart.")

# 2. Przeniesienie 28 kart z talii do listy 'plansza'
posegreguj_karty(talia)

# 3. Dodanie pierwszej karty do stosu odkrytego
if talia:
    pierwsza_dobrana = talia.pop(0)
    pierwsza_dobrana.odkryta = True
    dodatkowe_karty.append(pierwsza_dobrana)
    print(f"Pierwsza karta dobrana do stosu odkrytego: {pierwsza_dobrana}")
else:
    print("Błąd krytyczny: Talia jest pusta po rozłożeniu na planszę!")
    exit()

# 4. Rozłożenie kart z 'plansza' na 'mapę' w strukturze pasjansa i wyświetlenie stanu początkowego
mapa_pasjansa.generuj_mape(talia)

# --- Debugowanie ---

#--------------------
# Wyświetlenie mapy po wprowadzeniu zmian
mapa_pasjansa.wypisz_mape()

# --- Pętla Gry ---
while not wygrana:
    if dodatkowe_karty:
        pierwsza_odkryta = dodatkowe_karty[0]
        print(f"(Debug: Pierwsza karta odkryta: {str(pierwsza_odkryta)})")
        print(f"(Debug: Talia pozostało: {len(talia)} kart)")

    opcja = input("\nWybierz opcję (np. '0' do dobierz, 'Z której(1-7) ile(od 1 w górę) do której' do ruchu, '000' aby wyjść): ").strip().lower()
    opcja = opcja.split()

    if len(opcja) == 1 and opcja[0] == "000":
        print("Przerwanie gry.")
        wygrana = True
    elif len(opcja) == 1 and opcja[0] == "0":
        dobierz_dodatkowa_karte()
        mapa_pasjansa.wypisz_mape()
    elif len(opcja) == 3:
        try:
            linia_start = int(opcja[0]) - 1
            liczba_kart = int(opcja[1])
            kolumna_docelowa = int(opcja[2]) - 1
            poruszanie_kartami(linia_start, kolumna_docelowa, liczba_kart)
            mapa_pasjansa.wypisz_mape()
        except ValueError:
            print("Błąd: Proszę podać poprawne liczby.")
        except IndexError:
            print("Błąd: Proszę podać poprawne kolumny.")
    else:
        print("Niepoprawna opcja. Spróbuj ponownie.")
        

print("Koniec gry.")