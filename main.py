import random

# --- Klasy ---

class Karta:
    def __init__(self, wartosc, znak):
        self.wartosc = wartosc  # Np K 7 A
        self.znak = znak        # ♠ ♥ ♦ ♣
        self.odkryta = False # Domyślnie karty na planszy są zakryte

        # Określenie koloru (czerwony/czarny) na podstawie znaku
        if self.znak in ['♥', '♦']:
            self.kolor_rgb = "czerwony"
        elif self.znak in ['♠', '♣']:
            self.kolor_rgb = "czarny"
        else:
            self.kolor_rgb = "nieznany"

    def __str__(self):
        # Reprezentacja tekstowa dla użytkownika
        if self.odkryta:
             return f"{self.wartosc}{self.znak}"
        else:
             return "[?]" # Symbol dla zakrytej karty

    def __repr__(self):
        # Reprezentacja techniczna dla debugowania
        return f"Karta(wartosc={self.wartosc!r}, znak={self.znak!r}, odkryta={self.odkryta})"


class Fabryka_Kart:
    @staticmethod
    def stworz_karty():
        """Tworzy i zwraca potasowaną talię obiektów Karta."""
        znaki = ['♣', '♦', '♥', '♠']
        wartosci = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        talia = []
        for znak in znaki:
            for wartosc in wartosci:
                talia.append(Karta(wartosc, znak))
        random.shuffle(talia)
        return talia

# ---Funkcje gry---

def posegreguj_karty(talia):
    # Przygotowuje karty do rozłożenia na planszy.
    liczba_kart_potrzebna = 28
    print(f"Funkcja posegreguj_karty: Próba przeniesienia {liczba_kart_potrzebna} kart z talii do planszy.")

    global plansza

    if len(talia) < liczba_kart_potrzebna:
        print(f"OSTRZEŻENIE: W talii jest tylko {len(talia)} kart, a potrzebne jest {liczba_kart_potrzebna}. Przenoszę wszystkie dostępne.")
        liczba_kart_do_przeniesienia = len(talia)
    else:
        liczba_kart_do_przeniesienia = liczba_kart_potrzebna

    for _ in range(liczba_kart_do_przeniesienia):
        if talia:
             plansza.append(talia.pop(0))
        else:
             print("OSTRZEŻENIE: Talia wyczerpana przed przeniesieniem wszystkich kart na planszę.")
             break

    print(f"Funkcja posegreguj_karty: Zakończono. Lista 'plansza' zawiera teraz {len(plansza)} kart.")


def generuj_mape(talia):
    global mapa, plansza
    mapa = [[] for _ in range(7)] # Lista list reprezentująca kolumny na planszy

    print(f"Funkcja generuj_mape: Rozkładanie {len(plansza)} kart z listy 'plansza' na mapie.")

    # Rozkładanie kart na planszy w strukturze pasjansa (1, 2, 3, ... 7 kart w kolumnach)
    for i in range(7): # Iterujemy przez 7 kolumn (i od 0 do 6)
        for j in range(i + 1): # Dla każdej kolumny 'i', dodajemy 'i + 1' kart
            if not plansza: # Sprawdzenie, czy lista 'plansza' nie jest pusta
                print(f"OSTRZEŻENIE: Brak kart w 'plansza' do rozłożenia w kolumnie {i+1}, karcie {j+1}.")
                break # Przerwij dodawanie kart do tej kolumny
            karta = plansza.pop(0) # Pobierz pierwszą kartę z listy 'plansza'
            # Ustawiamy odkrycie tylko dla ostatniej karty w każdej kolumnie
            if j == i:
                karta.odkryta = True
            mapa[i].append(karta) # Dodaj kartę do bieżącej kolumny 'i'

        if not plansza and i < 6:
             print(f"OSTRZEŻENIE: Lista 'plansza' pusta po kolumnie {i+1}. Nie można dokończyć rozkładania mapy.")
             break

    # === Drukowanie mapy w formie kolumnowej ===
    print("\n--- Mapa Planszy ---")
    # Znajdź maksymalną wysokość kolumny do celów formatowania wydruku
    max_wysokosc = max((len(kolumna) for kolumna in mapa), default=0)

    for j in range(max_wysokosc): # Iterujemy przez "wiersze" głębokości
        linia_wydruku = ""
        for i in range(7): # Iterujemy przez kolumny
            if j < len(mapa[i]):
                # Używamy str() na obiekcie Karta PRZED zastosowaniem formatowania f-stringa
                linia_wydruku += f"{str(mapa[i][j]):<5}"
            else:
                linia_wydruku += "     " # Pusta przestrzeń
            linia_wydruku += " " # Odstęp między kolumnami
        print(linia_wydruku)
    print("-" * 30)

    # === Drukowanie stosów bazowych i dobierania ===
    print("\n--- Stosy Bazowe i Dobieranie ---")
    print("                           ♥ [ ]")
    print("                           ♦ [ ]")

    # Wyświetlanie pierwszej karty ze stosu dodatkowych kart (odkrytej)
    odkryta_karta_str = str(dodatkowe_karty[0]) if dodatkowe_karty else "[ ]"
    # Wyświetlanie symbolu talii (zakrytej)
    symbol_talii = "[?]" if talia else "[ ]"

    print(f"Odkryta: {odkryta_karta_str:<5}              ♠ [ ]")
    print(f"Talia: {symbol_talii:<5}              ♣ [ ]")
    print("-" * 30)


def dobierz_dodatkowa_karte():
    global talia, dodatkowe_karty
    if talia:
        # Dodajemy dobraną kartę na początek listy dodatkowe_karty (stos odkryty)
        dobrana_karta = talia.pop(0)
        dobrana_karta.odkryta = True # Nowa dobrana karta jest odkryta
        dodatkowe_karty.insert(0, dobrana_karta)
        print(f"Dobrano kartę: {dobrana_karta}")
    elif dodatkowe_karty:
        print("Talia pusta. Stos odkryty nie może być przewinięty w tej wersji.")
        # Tutaj można by zaimplementować przewijanie stosu odkrytego
    else:
        print("Talia i stos odkryty są puste.")

def poruszanie_kartami(linia_start, kolumna_docelowa, liczba_kart):
    # Funkcja wymaga dalszej implementacji logiki ruchów
    try:
        print(f"Próba ruchu: z kolumny {linia_start} do kolumny {kolumna_docelowa}, {liczba_kart} kart.")
        # Tu będzie logika sprawdzania poprawności ruchu i przenoszenia kart
        pass
    except ValueError:
        print("Błąd: Niepoprawne dane wejściowe dla ruchu.")
    except IndexError:
        print("Błąd: Podano nieistniejącą kolumnę lub kartę.")
    except Exception as e:
        print(f"Wystąpił błąd podczas ruchu: {e}")


# --- Główna część skryptu ---

# Inicjalizacja zmiennych globalnych
talia = []
dodatkowe_karty = [] # Stos odkryty
plansza = [] # Tymczasowa lista kart do rozłożenia na mapie
mapa = [] # Kolumny na planszy
stosy_bazowe = [[], [], [], []] # Cztery stosy bazowe
wygrana = False

# 1. Tworzenie i tasowanie talii 52 kart
talia = Fabryka_Kart.stworz_karty()
print(f"Stworzono potasowaną talię: {len(talia)} kart.")

# 2. Przeniesienie 28 kart z talii do listy 'plansza'
posegreguj_karty(talia)

# 3. Dodanie pierwszej karty do stosu odkrytego
if talia:
    pierwsza_dobrana = talia.pop(0)
    pierwsza_dobrana.odkryta = True # Pierwsza karta dobierana jest odkryta
    dodatkowe_karty.append(pierwsza_dobrana)
    print(f"Pierwsza karta dobrana do stosu odkrytego: {pierwsza_dobrana}")
else:
    print("Błąd krytyczny: Talia jest pusta po rozłożeniu na planszę!")
    exit()

# 4. Rozłożenie kart z 'plansza' na 'mapę' w strukturze pasjansa i wyświetlenie stanu początkowego
generuj_mape(talia)


# --- Start Gry ---

# --- Pętla Gry ---

while not wygrana:
    if dodatkowe_karty:
        pierwsza_odkryta = dodatkowe_karty[0]
        print(f"(Debug: Pierwsza karta odkryta: {str(pierwsza_odkryta)})")
        print(f"(Debug: Talia pozostało: {len(talia)} kart)")


    opcja = input("\nWybierz opcję (np. '0' do dobierz, 'X Y Z' do ruchu (niezaimplementowane), '000' aby wyjść): ").strip().lower()

    if opcja == "000":
        print("Przerwanie gry.")
        wygrana = True
    elif opcja == "0":
        dobierz_dodatkowa_karte()
        generuj_mape(talia) # Odśwież widok planszy po dobraniu
    else:
        # Logika ruchu - wciąż niezaimplementowana w pełni
        print("Nieznana opcja lub format ruchu niezaimplementowany.")


print("Koniec gry.")