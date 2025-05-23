# Pasjans Konsolowy (Solitaire)

## Opis Projektu

Projekt jest implementacją klasycznej gry karcianej Pasjans (Klondike Solitaire) w języku Python. Gra działa w trybie konsolowym i jej celem jest przeniesienie wszystkich 52 kart na cztery stosy bazowe, uporządkowane według koloru (znaku) i wartości (od Asa do Króla).

## Instalacja

Do uruchomienia gry wymagany jest Python w wersji 3.6 lub nowszej oraz biblioteka colorama.

Instalacja wymaganych pakietów:
```bash
pip install -r requirements.txt
```

## Uruchomienie

1. Upewnij się, że masz zainstalowany Python
2. Pobierz pliki projektu
3. Przejdź do katalogu z grą
4. Uruchom:
```bash
python main.py
```

## Sterowanie

Dostępne komendy:

* `dobierz` - dobiera kartę z talii
* `dk N` - przenosi odkrytą kartę na kolumnę N (1-7)
* `db` - przenosi odkrytą kartę na stos bazowy
* `kb N` - przenosi wierzchnią kartę z kolumny N na bazę
* `k N M K` - przenosi M kart z kolumny N na K
* `pomoc` - pokazuje komendy
* `restart` - rozpoczyna nową grę
* `koniec` - kończy grę

## Zasady

* Na kolumny: karty malejąco i naprzemiennie kolory
* Na bazy: karty tego samego koloru rosnąco od asa

## Wymagania

* Python 3.6+
* colorama

## Autor

Maciej Kubiczek