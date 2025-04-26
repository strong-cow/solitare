import random

class Karta:
    """Representuje pojedynczą kartę do gry."""
    def __init__(self, wartosc, znak):
        self.wartosc = wartosc  # Np. 'K', '7', 'A'
        self.znak = znak      # Np. '♠', '♥', '♦', '♣'

        # Określenie koloru (czerwony/czarny) na podstawie znaku
        if self.znak in ['♥', '♦']:
            self.kolor_rgb = "czerwony"
        elif self.znak in ['♠', '♣']:
            self.kolor_rgb = "czarny"
        else:
            self.kolor_rgb = "nieznany" # Na wszelki wypadek

    # Metoda __str__ kontroluje, jak obiekt karty będzie wyglądał po wydrukowaniu
    # Zwracamy format "Wartość Znak", aby pasował do poprzedniej wersji
    def __str__(self):
        return f"{self.wartosc} {self.znak}"

    # Metoda __repr__ jest używana m.in. przy wyświetlaniu listy kart
    # Możemy ją zdefiniować podobnie do __str__ dla czytelności
    def __repr__(self):
        return f"Karta({self.wartosc!r}, {self.znak!r})"

# Klasa Karty może teraz służyć tylko jako "fabryka" talii
# Można by ją nawet usunąć i zrobić stwurz_karty() zwykłą funkcją
class Karty:
    @staticmethod
    def stwurz_karty():
        """Tworzy i zwraca potasowaną talię obiektów Karta."""
        znaki = ['♣', '♦', '♥', '♠'] # Używamy teraz nazwy 'znaki'
        wartosci = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        talia = []

        for znak in znaki:
            for wartosc in wartosci:
                # Tworzymy obiekt klasy Karta zamiast stringa
                nowa_karta = Karta(wartosc, znak)
                talia.append(nowa_karta)

        random.shuffle(talia)  # Tasowanie talii obiektów Karta
        return talia

# --- Funkcje gry (generuj_mape, dobierz_dodatkowa_karte) ---
# Ważne: Te funkcje teraz będą operować na liście obiektów Karta, a nie stringów.
# Jednak dzięki metodzie __str__ w klasie Karta, ich działanie (zwłaszcza print)
# powinno pozostać bardzo podobne lub identyczne.

def generuj_mape(talia):
    plansza = []
    for i in range(7):
        wiersz = []
        for j in range(i + 1):
            wiersz.append(None)
        plansza.append(wiersz)

    for i in range(7):
        for j in range(i + 1):
            if talia:
                # Pobieramy obiekt Karta z talii
                plansza[i][j] = talia.pop(0)

    ktory = 0
    print("--- Plansza ---") # Dodajmy nagłówek dla czytelności
    for wiersz in plansza:
        ktory += 1
        # Drukujemy "?" dla ukrytych kart (None lub obiektów Karta)
        # Zakładamy, że tylko ostatnia karta w wierszu jest widoczna
        # (Uwaga: logika ukrywania/odkrywania kart może wymagać rozbudowy)
        linia_do_druku = []
        for idx, karta_lub_none in enumerate(wiersz):
            if idx < len(wiersz) - 1:
                 # Na razie drukujemy "?" dla wszystkich poza ostatnią
                 # W pełnej grze tu byłaby logika sprawdzania czy karta jest odkryta
                 linia_do_druku.append("?")
            else:
                # Ostatnia karta w wierszu - drukujemy jej reprezentację stringową
                # Jeśli wiersz jest pusty (co nie powinno się zdarzyć w tej strukturze),
                # lub karta to None, obsłuż to (choć tu raczej będzie obiekt Karta)
                 if karta_lub_none:
                     linia_do_druku.append(str(karta_lub_none)) # Używamy str() jawnie lub niejawnie przez print
                 else:
                     linia_do_druku.append("?") # Lub obsłuż inaczej

        # Wyrównanie i drukowanie
        print(" ".join(linia_do_druku))


    # Puste stosy na dole (bez zmian)
    print("\n--- Stosy Bazowe i Dobieranie ---") # Nagłówek
    print("                           ♥ [ ]") # Przykładowe oznaczenie pustego stosu
    print("                           ♦ [ ]")
    # Wyświetlenie karty ze stosu odkrytego (jeśli istnieje)
    odkryta_karta_str = str(dodatkowe_karty[0]) if dodatkowe_karty else "[ ]"
    print(f"Odkryta: {odkryta_karta_str:<5}              ♠ [ ]") # Używamy str() i formatowania
    print(f"Talia: {'[?]' if talia else '[ ]':<5}            ♣ [ ]") # Pokaż czy są karty w talii

# Zmieniona nazwa funkcji dla jasności
def dobierz_dodatkowa_karte():
    global talia, dodatkowe_karty # Jawne użycie globalnych zmiennych (lub przekazanie jako argumenty)
    if talia:
        dodatkowe_karty.insert(0, talia.pop(0)) # Dodaj na początek stosu odkrytego
    else:
        # Opcjonalnie: Przetasuj karty z 'dodatkowe_karty' (bez ostatniej?) z powrotem do 'talia'
        print("Talia jest pusta.")

# --- Główna część skryptu ---
talia = []
dodatkowe_karty = [] # Stos odkryty (karty dobierane)

talia = Karty.stwurz_karty()  # Tworzymy talię obiektów Karta

# Pobranie pierwszej karty do stosu odkrytego
if talia:
    dodatkowe_karty.append(talia.pop(0))
else:
    print("Błąd: Pusta talia!")
    exit()

# Pierwsze wyświetlenie planszy
generuj_mape(talia) # Przekazujemy resztę talii

# --- Pętla Gry ---
wygrana = False
while not wygrana:
    # Przykład dostępu do koloru karty (np. pierwszej odkrytej)
    if dodatkowe_karty:
        pierwsza_odkryta = dodatkowe_karty[0]
        print(f"(Debug: Kolor karty {pierwsza_odkryta} to {pierwsza_odkryta.kolor_rgb})")

    opcja = input("Wybierz opcję ").strip().lower()

    if opcja == "000":
        print("Przerwanie gry")
        wygrana = True
        break
    elif opcja == "0":
        dobierz_dodatkowa_karte()
        # Wyświetl stan gry ponownie
        print("-" * 30)
        generuj_mape(talia)
        print(f"Stos odkryty: {dodatkowe_karty}") # Wyświetli listę obiektów Karta
        print("-" * 30)
    else:
        print("Nieznana opcja.")

