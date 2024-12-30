# Concurrent Gaussian Elimination
Projekt wykorzystuje teorię śladów do współbieżnego rozwiązania układu równań metodą Eliminacji Gaussa.

# Opis zawartości repozytorium

Projekt został napisany w języku Python. Opis wykorzystanych modułów znajduje się w pliku environment.yml.

1) input - folder zawierający przykładowe dane wejściowe
2) output - folder zawierający przykładowe dane wyjściowe:
    1) gauss_output.txt - zawiera rozwiązanie układu równań
    2) traces_theory_output.txt - zawiera wyznaczony alfabet w sensie teorii śladów, relację zależności, słowo oraz klasy Foaty
    3) diekert_graph.png - wyrenderowany graf Diekerta dla zadanego układu równań
3) checker.py - moduł wykorzystujący sprawdzarkę do oceny poprawności kodu (Patrz: sekcja Uruchomienie checkera)
4) main.py - główny moduł, wywołuje funkcje wyznaczające obiekty matematyczne związane z teorią śladów oraz wyznacza rozwiązanie układu równań
5) scheduler.py - moduł odpowiedzialny za współbieżne wyznaczenie macierzy trójkątnej górnej przy wykorzystaniu rdzeni CUDA i wyznaczenie rozwiązania układu równań
6) traces_theory.py - moduł odpowiedzialny za wyznaczenie obiektów matematycznych związanych z teorią śladów
7) tools.py - funkcje pomocnicze do wyznaczania obiektów matematycznych związanych z teorią śladów
8) utility.py - funkcje pomocnicze realizujące zapis / odczyt do plików

# Uruchommienie projektu

Do uruchomienia projektu wymagana jest zainstalowana Anadonda (przetestowane na wersji 23.9.0). Oraz karta graficzna firmy Nvidia
posiadająca rdzenie CUDA. Kompatybilne karty można znaleźć tutaj: https://developer.nvidia.com/cuda-gpus.

W celu zainstalowania wymaganych zależności należy w terminalu kolejno wpisać:

```bash
cd "Concurrent Gauss Elimination"
conda env create -f environment.yml
conda activate Concurrent-Gauss-Elimination
python main.py input/example_input.txt output
```

Domyślnie graf Diekerta nie jest rysowany dla macierzy o rozmiarach większych od 10 bo jest on nieczytelny,
zachowanie to można zmienić ustawiając flagę force_graph na true w
funkcji traces_run w pliku main.py.

Funkcje traces_run i scheduler_run w pliku main.py działają niezależnie od siebie, pierwsza jest odpowiedzialna za wyznaczenie
obiektów matematycznych związanych z teorią śladów, a druga za rozwiązanie układu równań (oczywiście wyznaczając wcześniej klasy Foaty).

# Uruchomienie checkera

W celu skorzystania ze sprawdzarki wymagana jest instalacja Javy (przetesowane na wersji 21.0.2). Checker automatycznie
kompiluje i uruchamia sprawdzarkę korzystając z poleceń 'javac' i 'java'.

W folderze sprawdzarka znajduje się plik checker.py, a w nim funkcja check przyjmująca liczbę naturalną jako argument.
Uruchamia ona załączoną do treści zadania sprawdzarkę dla danego rozmiaru macierzy.
