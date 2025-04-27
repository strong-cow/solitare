import random

# --- Klasy ---

class Karta:
    """TYLKO KARTA"""
    def __init__(self, wartosc, znak):
        self.wartosc = wartosc  # Np K 7 A
        self.znak = znak      # ♠ ♥ ♦ ♣

        # Określenie koloru (czerwony/czarny) na podstawie znaku
        if self.znak in ['♥', '♦']:
            self.kolor_rgb = "czerwony"
        elif self.znak in ['♠', '♣']:
            self.kolor_rgb = "czarny"
        else:
            self.kolor_rgb = "nieznany" 

    def __str__(self):
        return f"{self.wartosc} {self.znak}" # Używamy __str__ do reprezentacji stringowej

    def __repr__(self):
        return f"Karta({self.wartosc!r}, {self.znak!r})" # Używamy __repr__ do debugowania

class Fabryka_Talii_Kart:
    @staticmethod
    def stwurz_karty():
        """Tworzy i zwraca potasowaną talię."""
        znaki = ['♣', '♦', '♥', '♠'] #
        wartosci = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        talia = []

        for znak in znaki:
            for wartosc in wartosci:
                # Tworzymy obiekt klasy Karta zamiast stringa
                nowa_karta = Karta(wartosc, znak)
                talia.append(nowa_karta)

        random.shuffle(talia)
        return talia


# ---Funkcje gry---
def posegreguj_karty(talia):
    for ile in range(1, 8):
        print("0")
        for i in range(7-ile):
            print("1")
            plansza.append(talia.pop(0))
    print(f"to jest posegrowana plansza{talia}")

    pass

def generuj_mape(talia):
    '''for i in range(7):
        wiersz = []
        for j in range(i + 1):
            wiersz.append(None)
        plansza.append(wiersz)

    for i in range(7):
        for j in range(i + 1):
            if talia:
                plansza[i][j] = talia.pop(0)

    ktory = 0
    print("--- Plansza ---")
    for wiersz in plansza: # ten sposób jest zły
        ktory += 1
        linia_do_druku = []
        for sprwadzanlnik, karta_lub_brak in enumerate(wiersz): # enumerate zamiast range(len(wiersz))
            if sprwadzanlnik < len(wiersz) - 1:
                 linia_do_druku.append("?")
            else:
                 if karta_lub_brak:
                     linia_do_druku.append(str(karta_lub_brak))
                 else:
                     linia_do_druku.append("?")

        print(" ".join(linia_do_druku))

    print("\n--- Stosy Bazowe i Dobieranie ---") 
    print("                           ♥ [ ]") 
    print("                           ♦ [ ]")
    odkryta_karta_str = str(dodatkowe_karty[0]) if dodatkowe_karty else "[ ]"
    print(f"Odkryta: {odkryta_karta_str:<5}              ♠ [ ]") 
    print(f"Talia: {'[?]' if talia else '[ ]':<5}            ♣ [ ]") '''
    pass

def dobierz_dodatkowa_karte():
    global talia, dodatkowe_karty 
    if talia:
        dodatkowe_karty.insert(0, talia.pop(0)) 
    else:
        
        print("Talia jest pusta.")

def poruszanie_kartami(linia, dokąd, ile):
    try:
        pass
    except ValueError:
        print("Błąd: Niepoprawne dane wejściowe.")

# --- Główna część skryptu ---

talia = []
dodatkowe_karty = [] 
plansza = []
wygrana = False

talia = Fabryka_Talii_Kart.stwurz_karty() 
posegreguj_karty(talia)

if talia:
    dodatkowe_karty.append(talia.pop(0))
else:
    print("Błąd: Pusta talia!")
    exit()

generuj_mape(talia)

# --- Pętla Gry ---

while not wygrana:
    if dodatkowe_karty:
        pierwsza_odkryta = dodatkowe_karty[0]
        #debug
        print(f"(Debug: Kolor karty {pierwsza_odkryta} to {pierwsza_odkryta.kolor_rgb})")
        print(f"Tak wygląda mapa po koleji: {talia}")

    opcja = input("Wybierz opcję ").strip().lower()

    if opcja == "000":
        print("Przerwanie gry")
        wygrana = True
        break
    elif opcja == "0":
        dobierz_dodatkowa_karte()
        print("-" * 30)
        generuj_mape(talia)
        print(f"Stos odkryty: {dodatkowe_karty}") 
        print("-" * 30)
    else:
        print("Nieznana opcja.")

