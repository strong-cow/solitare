import unittest
from classy import Karta
from funkcje import stworz_nowa_talie
from stale import WARTOSCI_KART, ZNAKI_KART


class TestKarta(unittest.TestCase):

    def test_kolor_czerwony(self):
        karta = Karta('A', '♥')
        self.assertEqual(karta.kolor, "czerwony")

    def test_kolor_czarny(self):
        karta = Karta('K', '♣')
        self.assertEqual(karta.kolor, "czarny")

    def test_str_odkryta(self):
        karta = Karta('5', '♦')
        karta.odkryta = True
        tekst = str(karta)
        self.assertIn('5♦', tekst)

    def test_str_zakryta(self):
        karta = Karta('5', '♦')
        karta.odkryta = False
        self.assertEqual(str(karta), "[?]")


class TestTalia(unittest.TestCase):

    def test_stworz_nowa_talie(self):
        talia = stworz_nowa_talie()
        self.assertEqual(len(talia), 52)
        znaki = set(k.znak for k in talia)
        wartosci = set(k.wartosc for k in talia)
        self.assertEqual(znaki, set(ZNAKI_KART))
        self.assertEqual(wartosci, set(WARTOSCI_KART))
        # Sprawdź, czy są unikalne karty
        unique_cards = set((k.wartosc, k.znak) for k in talia)
        self.assertEqual(len(unique_cards), 52)


if __name__ == '__main__':
    unittest.main()
