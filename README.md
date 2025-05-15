# Pasjans Konsolowy (Solitaire)

## Opis Projektu

Projekt jest implementacją klasycznej gry karcianej Pasjans (Klondike Solitaire) w języku Python. Gra działa w trybie konsolowym i jej celem jest przeniesienie wszystkich 52 kart na cztery stosy bazowe, uporządkowane według koloru (znaku) i wartości (od Asa do Króla).
Projekt został przygotowany z myślą o konkursie programistycznym.

## Instalacja

Do uruchomienia gry wymagany jest Python w wersji 3.6 lub nowszej.
Projekt nie korzysta z żadnych zewnętrznych bibliotek poza standardową biblioteką `random` (do tasowania kart), która jest częścią każdej instalacji Pythona.

Nie ma potrzeby instalowania dodatkowych pakietów.

## Sposób Uruchomienia

1.  Upewnij się, że masz zainstalowany Python.
2.  Pobierz pliki projektu (np. `main.py` lub cały folder projektu).
3.  Otwórz terminal lub wiersz poleceń.
4.  Przejdź do katalogu, w którym znajdują się pliki gry.
5.  Uruchom grę komendą:
    ```bash
    python main.py
    ```
    (Jeśli plik główny ma inną nazwę, np. `pasjans.py`, użyj tej nazwy).

## Instrukcje Rozgrywki (Sterowanie)

Po uruchomieniu gry, na ekranie pojawi się plansza oraz lista dostępnych komend. Wpisuj komendy w konsoli i zatwierdzaj klawiszem Enter.

**Dostępne komendy:**

* `dobierz` - Dobiera jedną kartę ze stosu rezerwowego na stos kart odkrytych. Jeśli stos rezerwowy jest pusty, karty ze stosu odkrytego są odwracane i tworzą nowy stos rezerwowy.
* `dk K` - Przenosi wierzchnią kartę ze stosu ODKRYTYCH na KOLUMNĘ roboczą numer `K`. `K` to liczba od 1 do 7.
    * *Przykład:* `dk 3` (przenieś odkrytą kartę na 3. kolumnę)
* `db` - Przenosi wierzchnią kartę ze stosu ODKRYTYCH na odpowiedni STOS BAZOWY (jeśli ruch jest dozwolony).
* `kb K` - Przenosi wierzchnią (odkrytą) kartę z KOLUMNY roboczej numer `K` na odpowiedni STOS BAZOWY.
    * *Przykład:* `kb 5` (przenieś kartę z 5. kolumny na stos bazowy)
* `k K1 ILE K2` - Przenosi `ILE` odkrytych kart z wierzchu KOLUMNY roboczej `K1` na KOLUMNĘ roboczą `K2`.
    * `K1` - numer kolumny źródłowej (1-7).
    * `ILE` - liczba kart do przeniesienia (musi być co najmniej 1).
    * `K2` - numer kolumny docelowej (1-7).
    * *Przykład:* `k 1 2 4` (przenieś 2 karty z kolumny 1 na kolumnę 4)
* `pomoc` - Wyświetla ponownie listę dostępnych komend i instrukcje.
* `restart` - Rozpoczyna grę od nowa, tasując i rozdając karty.
* `zakoncz` - Kończy bieżącą rozgrywkę.
* `debug` - Włącza lub wyłącza tryb debugowania, który wyświetla szczegółowy stan wewnętrznych list kart (przydatne dla dewelopera).

**Zasady przenoszenia kart:**
* **Na kolumny robocze:** Karty muszą być układane malejąco (np. Dama na Króla) i naprzemiennie kolorami (czerwona na czarną lub czarna na czerwoną). Na pustą kolumnę można położyć tylko Króla.
* **Na stosy bazowe:** Karty muszą być tego samego znaku, układane rosnąco od Asa do Króla (np. 2♥ na A♥).

## Opis Klas i Funkcji

Kod jest zorganizowany w klasy i funkcje:

* **Klasa `Karta`**: Reprezentuje pojedynczą kartę do gry, przechowuje jej wartość, znak, kolor (czerwony/czarny) oraz stan (odkryta/zakryta).
* **Klasa `MenedzerRuchow`**: Zawiera logikę dla wszystkich możliwych ruchów kartami w grze (np. przenoszenie między kolumnami, ze stosu odkrytego na kolumny, na stosy bazowe).
* **Klasa `WyswietlaczMapy`**: Odpowiada za generowanie początkowego układu kart na kolumnach roboczych oraz za wyświetlanie całego stanu gry w konsoli.
* **Funkcje globalne**:
    * `stworz_nowa_talie()`: Tworzy i tasuje pełną talię 52 kart.
    * `przygotuj_karty_do_rozlozenia()`: Przygotowuje podzbiór kart z talii do ułożenia na kolumnach roboczych.
    * `dobierz_karte_ze_stosu()`: Implementuje mechanikę dobierania kart ze stosu rezerwowego.
    * `wyswietl_instrukcje_gry()`: Pokazuje graczowi dostępne komendy.
    * `inicjalizuj_gre()`: Ustawia (lub resetuje) grę do stanu początkowego.

## Wymagania Systemowe

* Python 3.6+

## Plik `requirements.txt`

Projekt wykorzystuje wyłącznie standardowe biblioteki Pythona. Główna używana biblioteka (wbudowana) to `random` (do tasowania kart). Nie ma potrzeby instalowania zewnętrznych zależności.

## Licencja

Ten projekt jest udostępniany na licencji GNU GPLv3.

## Autorzy

Maciej Kubiczek