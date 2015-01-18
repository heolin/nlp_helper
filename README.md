# nlp_helper

Program używa analizatora morfologicznego - Morfologik,
więcej o projekcie tutaj: http://morfologik.blogspot.com/

1. Instalacja:
Aby użyć programu należy zainstalować interpreter języka Python w wersji 2.7.8.
Instalator można pobrać klikając link poniżej.
https://www.python.org/downloads/release/python-278/

2. Format pliku wejściowego:
Obecnie obsługiwane są tylko pliki w formacie txt. W przyszłości zostaną dodane kolejne.
Program zakłada, że w każdej lini pliku wejściowego jest dokładnie jedno zdanie (zdania nie są dzielone w sposób automatyczny).

Zobacz plik plik_wejsciowy.txt

3. Sposób użycia:

Program został podzielony na dwa moduły:
process.py - który przetwarza zdania wejściowe i uzupełnia metadanę.
stats.py - który dokonuje statystyki w oparciu o metadanę i tworzy raport z analizy.

Aby użyć modułu process należy wpisać komendę:
python process.py -i plik_wejsciowy.txt -o plik_metadane.txt

Następnie można użyć modułu stats wpisując komendę:
python stats.py -i plik_metadane.txt -o plik_statystyki.txt -l lista_frekwencyjna_form_podstawowych.txt -w lista_frekwencyjna_wyrazow.txt -s lista_frekwencyjna_zdan.txt -ss lista_frekwencyjna_zdan_prostych.txt -cs lista_frekwencyjna_zdan_zlozonych.txt

4. Format plików wynikowych:
Format liku metadanych:
Analizowane zdanie
Wyraz1	Forma_podstawowa1	możliwa_część_mowy,liczba;możliwa_cześć_mowy2,liczba2...
Wyraz2	Forma_podstawowa2	możliwa_część_mowy,liczba
Wyraz3	Forma_podstawowa3	możliwa_część_mowy,liczba

-> Jeżeli program nie jest dokładnie określić możliwej części mowy wypisuje wszystkie możliwe.
Formy oddzielone są ";", w kolejności od najpopularniejszej, do najmniej popularnej
