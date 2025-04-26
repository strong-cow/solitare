import random

class Karty:
    def __init__(self, karta=None):
        self.karta = karta

    @staticmethod # Statyczna metoda do tworzenia talii kart(czyli nie potrzebuje instancji klasy)
    def stwurz_karty():
        kolory = ['♣', '♦', '♥', '♠']
        wartosci = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        talia = []

        for kolor in kolory:
            for wartosc in wartosci:
                talia.append(f"{wartosc} {kolor}")

        random.shuffle(talia)  # Tasowanie talii
        return talia


def generuj_mape():
    talia = Karty.stwurz_karty()
    plansza = []
    for i in range(7):  # Tworzenie 7 wierszy
        wiersz = []
        for j in range(i + 1):
            wiersz.append(None)
        plansza.append(wiersz)  # Dodanie wiersza do planszy

    for i in range(7):  # Dodanie kart do planszy
        for j in range(i + 1):
            if talia:
                plansza[i][j] = talia.pop(0)  # Pobranie karty z talii
    ktory=0  # Zmienna do śledzenia, która karta jest odkryta
    for wiersz in plansza:# Wyświetlenie planszy
        ktory+=1
        print("? " * (len(wiersz)-1), end="")  # Wyrównanie do lewej
        print(wiersz[ktory-1])
    
    # Puste stosy na dole
    print("                               ♥")
    print("                               ♦")
    print("                               ♠")
    print("0                              ♣")


# Przykład użycia
if __name__ == "__main__":
    print("Mapa gry:")
    generuj_mape()