# Instrukcja oznaczania egzaminów

## Zawartość archiwów .zip
* `<egzamin_id>.pdf` - właściwy arkusz egzaminu w formacie PDF który należy wydrukować
* `<egzamin_id>.txt` - oczekiwane oznaczenia w poszczególnych pytaniach danego egzaminu

## Interpretacja oczekiwanych oznaczeń

Przykładowy wiersz pojedynczego pytania:

|             | Answer 1   | Answer 2   | Answer 3   | Answer 4   | Answer 5   | Answer 6   |
|-------------|------------|------------|------------|------------|------------|------------|
|.............|............|............|............|............|............|............|
| Question 8  | negation   | mark       | no mark    | no mark    |            |            |
|.............|............|............|............|............|............|............|

### Możliwe wartości oznaczeń:

* `mark` - oznaczenie danej odpowiedzi jako poprawnej
    - **SPOSÓB ZAZNACZENIA ZNAJDUJE SIĘ NA POCZĄTKU PLIKU EGZAMINU**
* `no mark` - brak jakiegokolwiek oznaczenia danej odpowiedzi
* `negation` - oznaczenie danej odpowiedzi jako błędnej(anulowanie odpowiedzi)
    - **SPOSÓB ZAZNACZENIA ZNAJDUJE SIĘ NA POCZĄTKU PLIKU EGZAMINU**
* `____` - (puste miejsce) - pytanie nie posiada danej odpowiedzi(ze względu na różną ilość
    odpowiedzi w pytaniach)

## Zasady poprawnej realizacji egzaminu

1. Ściśle przestrzegaj klucza odpowiedzi. Wpisz własny numer indeksu na pierwszej stronie egzaminu w wyznaczonym polu.
2. Jeżeli popełnisz błąd przy zaznaczaniu lub anulowaniu, zarówno w przypadku niewłaściwej metody zaznaczania lub zaznaczysz (anulujesz) niewłaściwe pytanie, zrób nowe ksero tej kartki.
3. Zachowaj kolejność kartek dla każdego egzaminu przy kserowaniu.
4. Drukuj kartki w czerni i bieli.
5. Po skończeniu wszystkich egzaminów:
    * Zeskanuj (za pomocą skanera) wszystkie kartki utrzymując kolejność wewnątrz każdego egzaminu.
    * Zanieś prace do gabinetu prowadzącego (EA 521) we wcześniej ustalonych godzinach.
6. Nie pisz po pracy poniżej UUID. Jeżeli przypadkiem zamazany został UUID lub w jakikolwiek sposób zanieczyszczony został obszar UUID i poniżej, zrób nowe ksero kartki której to dotyczy.

## Skanowanie prac za pomocą własnych zasobów

Jeżeli wykonane prace będą zeskanowane przy pomocy własnych zasobów:
1. Zeskanuj (za pomocą skanera) wszystkie kartki utrzymując kolejność wewnątrz każdego egzaminu.
2. Zapisz wszystkie prace w formacie `pdf`. Możesz pozostawić przy tym puste kartki. Nazwij plik `numer_indeksu.pdf`.
3. Dokonaj kompresji do formatu `zip`. Archiwum zip nazwij `numer_indeksu.zip`. Nie zabezpieczaj archiwum hasłem.
