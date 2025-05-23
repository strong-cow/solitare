from colorama import Fore, Style
from stale import WARTOSCI_KART, ZNAKI_KART  # Import stałych


class Karta:
    def __init__(self, wartosc, znak):
        self.wartosc = wartosc
        self.znak = znak
        self.odkryta = False
        self.kolor = "czerwony" if self.znak in ['♥', '♦'] else "czarny"

    def __str__(self):
        if not self.odkryta:
            return "[?]"
        kolor = Fore.RED if self.kolor == "czerwony" else Fore.BLACK
        return f"{kolor}{self.wartosc}{self.znak}{Style.RESET_ALL}"

    def __repr__(self):
        # Pomocne do debugowania, żeby widzieć stan karty
        return (f"Karta('{self.wartosc}', '{self.znak}', "
                f"odkryta={self.odkryta})")


class ZarzadcaRuchow:
    # Obsługuje logikę ruchów kart.
    def __init__(self, kolumny, odkryte, bazy, talia_ref, tryb_debug=False):
        self.kolumny = kolumny
        self.odkryte = odkryte
        self.bazy = bazy
        self.talia = talia_ref
        self.tryb_debug = tryb_debug

    def przenies_kolumna_na_kolumne(self, zrodlo_idx, cel_idx, ile_kart):
        try:
            kol_start = self.kolumny[zrodlo_idx]
            kol_cel = self.kolumny[cel_idx]

            if not (0 < ile_kart <= len(kol_start)):
                print(f"Nieprawidłowa liczba kart: {ile_kart}.")
                return False

            stos_do_przeniesienia = kol_start[-ile_kart:]

            if not all(k.odkryta for k in stos_do_przeniesienia):
                print("Nie mogę przenieść zakrytych kart.")
                return False

            if ile_kart > 1:
                for i in range(ile_kart - 1):
                    k1 = stos_do_przeniesienia[i]
                    k2 = stos_do_przeniesienia[i + 1]
                    idx1 = WARTOSCI_KART.index(k1.wartosc)
                    idx2 = WARTOSCI_KART.index(k2.wartosc)

                    if k1.kolor == k2.kolor or idx1 != idx2 + 1:
                        print("Stos nie jest poprawny (kolor/kolejność).")
                        return False

            karta_na_wierzchu_stosu = stos_do_przeniesienia[0]

            if not kol_cel:  # Pusta kolumna docelowa
                if karta_na_wierzchu_stosu.wartosc != 'K':
                    print("Na pustą kolumnę można położyć tylko Króla.")
                    return False
            else:  # Kolumna docelowa nie jest pusta
                ostatnia_karta_w_celu = kol_cel[-1]
                idx_cel = WARTOSCI_KART.index(ostatnia_karta_w_celu.wartosc)
                idx_przenoszone = WARTOSCI_KART.index(
                    karta_na_wierzchu_stosu.wartosc
                )

                if (ostatnia_karta_w_celu.kolor ==
                        karta_na_wierzchu_stosu.kolor or
                        idx_przenoszone + 1 != idx_cel):
                    print(f"Karta {karta_na_wierzchu_stosu} "
                          f"nie pasuje na {ostatnia_karta_w_celu}.")
                    return False

            # Wykonanie ruchu
            self.kolumny[zrodlo_idx] = kol_start[:-ile_kart]
            self.kolumny[cel_idx].extend(stos_do_przeniesienia)

            if (self.kolumny[zrodlo_idx] and
                    not self.kolumny[zrodlo_idx][-1].odkryta):
                self.kolumny[zrodlo_idx][-1].odkryta = True
                print(f"Odkryto kartę w kolumnie {zrodlo_idx + 1}.")

            print(f"Przeniesiono {ile_kart} kart z kol. {zrodlo_idx + 1} "
                  f"do kol. {cel_idx + 1}.")
            return True

        except IndexError:
            print("Nieprawidłowe numery kolumn. Użyj liczb od 1 do 7.")
            return False
        except ValueError:
            print("Wystąpił problem z wartością karty.")
            return False
        except Exception as ex:
            print(f"Błąd przy ruchu kolumna->kolumna: {ex}")
            return False

    def przenies_odkryta_na_kolumne(self, cel_idx):
        """Próba przeniesienia karty z 'Odkryte' na kolumnę 'cel_idx'."""
        if not self.odkryte:
            print("Stos odkryty jest pusty.")
            return False

        karta_z_odkrytych = self.odkryte[0]

        try:
            kol_cel = self.kolumny[cel_idx]

            if not kol_cel:  # Pusta kolumna docelowa
                if karta_z_odkrytych.wartosc == 'K':
                    self.kolumny[cel_idx].append(self.odkryte.pop(0))
                    print(f"Przeniesiono {karta_z_odkrytych} na pustą "
                          f"kolumnę {cel_idx + 1}.")
                    return True
                else:
                    print(f"Tylko Król ({karta_z_odkrytych}) "
                          "może iść na pustą kolumnę.")
                    return False
            else:  # Kolumna docelowa nie jest pusta
                ostatnia_w_celu = kol_cel[-1]
                idx_odkryta = WARTOSCI_KART.index(karta_z_odkrytych.wartosc)
                idx_cel = WARTOSCI_KART.index(ostatnia_w_celu.wartosc)

                if (karta_z_odkrytych.kolor == ostatnia_w_celu.kolor or
                        idx_odkryta + 1 != idx_cel):
                    print(f"Karta {karta_z_odkrytych} "
                          f"nie pasuje na {ostatnia_w_celu}.")
                    return False

            # Ruch poprawny
            self.kolumny[cel_idx].append(self.odkryte.pop(0))
            print(f"Przeniesiono {karta_z_odkrytych} "
                  f"na kolumnę {cel_idx + 1}.")
            return True

        except IndexError:
            print("Nieprawidłowy numer kolumny (1-7).")
            return False
        except ValueError:
            print("Wystąpił problem z wartością karty.")
            return False

    def przenies_na_baze(self, zrodlo_typ, zrodlo_idx=None):
        # Próba przeniesienia karty na stos bazowy.
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
                    print(f"Karta w kol. {zrodlo_idx + 1} jest zakryta.")
                    return False
            else:
                print(f"Kolumna {zrodlo_idx + 1} jest pusta/nieprawidłowa.")
                return False
        else:
            print("Nieznane źródło karty do przeniesienia na bazę.")
            return False

        if not udane_pobranie_karty:
            return False

        try:
            idx_bazowy = ZNAKI_KART.index(karta_do_przeniesienia.znak)
            baza_cel = self.bazy[idx_bazowy]

            if not baza_cel:  # Pusta baza
                if karta_do_przeniesienia.wartosc == 'A':
                    pass
                else:
                    print(f"Na pustą bazę {ZNAKI_KART[idx_bazowy]} "
                          "można dać tylko Asa.")
                    return False
            else:  # Baza nie jest pusta
                ostatnia_w_bazie = baza_cel[-1]
                idx_przenoszone = WARTOSCI_KART.index(
                    karta_do_przeniesienia.wartosc
                )
                idx_ostatnia_w_bazie = WARTOSCI_KART.index(
                    ostatnia_w_bazie.wartosc
                )

                if (karta_do_przeniesienia.znak != ostatnia_w_bazie.znak or
                        idx_przenoszone != idx_ostatnia_w_bazie + 1):
                    print(f"Karta {karta_do_przeniesienia} nie pasuje "
                          f"na {ostatnia_w_bazie} w bazie.")
                    return False

            # Wykonanie ruchu
            if zrodlo_typ == "odkryte":
                self.bazy[idx_bazowy].append(self.odkryte.pop(0))
                print(f"Przeniesiono {karta_do_przeniesienia} do bazy "
                      f"{ZNAKI_KART[idx_bazowy]}.")
                return True
            elif zrodlo_typ == "kolumna":
                self.bazy[idx_bazowy].append(self.kolumny[zrodlo_idx].pop())
                print(f"Przeniesiono {karta_do_przeniesienia} z kol. "
                      f"{zrodlo_idx + 1} do bazy {ZNAKI_KART[idx_bazowy]}.")
                if (self.kolumny[zrodlo_idx] and
                        not self.kolumny[zrodlo_idx][-1].odkryta):
                    self.kolumny[zrodlo_idx][-1].odkryta = True
                    print(f"Odkryto kartę w kolumnie {zrodlo_idx + 1}.")
                return True

        except ValueError:
            print(f"Problem ze znakiem karty {karta_do_przeniesienia.znak}.")
            return False
        except IndexError:
            print("Wystąpił problem z indeksowaniem baz.")
            return False
        except Exception as ex:
            print(f"Nieoczekiwany błąd przy ruchu do bazy: {ex}")
            return False
        return False


class PlanszaWyswietlacz:
    """Wyświetla stan gry w konsoli."""

    @staticmethod
    def przygotuj_uklad_poczatkowy(talia_zrodlowa, kolumny_ref):
        print("Rozkładanie kart na planszy...")

        for i in range(7):
            for j in range(i + 1):
                if not talia_zrodlowa:
                    print(f"OSTRZEŻENIE: Zabrakło kart przy rozkładaniu "
                          f"kolumny {i + 1}!")
                    break
                karta = talia_zrodlowa.pop(0)
                karta.odkryta = (j == i)
                kolumny_ref[i].append(karta)
            if not talia_zrodlowa and i < 6:
                print("OSTRZEŻENIE: Talia pusta. Układ niekompletny.")
                break

    @staticmethod
    def wypisz_stan(kolumny, odkryte, bazy, talia_ref):
        print("\n" + "=" * 10 + " PASJANS " + "=" * 10)

        print("\n--- Bazy / Talia ---")
        linia1_bazy = ""
        linia2_bazy = ""
        for i in range(4):
            symbol = ZNAKI_KART[i]
            karta_na_bazie = str(bazy[i][-1]) if bazy[i] else "[ ]"
            display_str = f"Baza {symbol}: {karta_na_bazie:<4}"
            if i < 2:
                linia1_bazy += display_str + "    "
            else:
                linia2_bazy += display_str + "    "
        print(linia1_bazy.rstrip())
        print(linia2_bazy.rstrip())

        karta_odkryta_str = str(odkryte[0]) if odkryte else "[ ]"
        symbol_talii = "[?]" if talia_ref else "[X]"
        print(f"Odkryta: {karta_odkryta_str:<5}        "
              f"Talia: {symbol_talii:<5} ({len(talia_ref)})")
        print("-" * 30)

        print("\n--- Kolumny ---")
        max_wysokosc = max((len(kol) for kol in kolumny), default=0)

        numerki_kolumn = []
        for i in range(7):
            numerki_kolumn.append(f" {i + 1}. ")
        print("".join(numerki_kolumn))
        print("-----" * 7 + "-")

        for j in range(max_wysokosc):
            linia_kart = ""
            for i in range(7):
                if j < len(kolumny[i]):
                    linia_kart += f"{str(kolumny[i][j]):<4}"
                else:
                    linia_kart += "    "
                linia_kart += " "
            print(linia_kart.rstrip())

        print("=" * 30)
