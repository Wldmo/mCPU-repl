
# mCPU-REPL

**Mini CPU z własnym ALU i prostym REPL-em/assemblerem w Pythonie**  

`mCPU-REPL` to lekki, edukacyjny emulator 8-bitowego procesora z własnym ALU, rejestrami i pamięcią RAM. Możesz wykonywać operacje arytmetyczne, logiczne, przesunięcia bitowe, a także pisać mini-programy w stylu assemblera. Obsługuje zarówno tryb plikowy, jak i interaktywny REPL.  

## Funkcje

- **8-bitowe rejestry i RAM** (255 bajtów)  
- **Własne ALU** z operacjami:  
  - ADD, SUB  
  - AND, OR, XOR, NOT  
  - SHL, SHR, ROL, ROR  
- **Instrukcje REPL / assembler:**  
  - `MOV <reg|[addr]>, <reg|[addr]|value>` – ładowanie danych  
  - `ALU` – wykonanie operacji wybranej w `OP_SEL`  
  - `OUT <reg|[addr]>` – wypisanie wartości  
  - `JMP <label>` – skok bezwarunkowy  
  - `JZ <reg> <label>` – skok jeśli zero  
  - `JNZ <reg> <label>` – skok jeśli nie zero  
  - `EXIT` – zakończenie programu  

- **Etykiety** i skoki pozwalają tworzyć pętle i warunki w programach  

## Tabela OP_SEL

| OP_SEL | Operacja | Opis                                      |
|--------|----------|--------------------------------------------|
| 1      | ADD      | D_A + D_B                                  |
| 2      | SUB      | D_A - D_B                                  |
| 3      | AND      | D_A & D_B                                  |
| 4      | OR       | D_A \| D_B                                 |
| 5      | XOR      | D_A ^ D_B                                  |
| 6      | NOT      | ~D_A                                       |
| 7      | SHL      | Przesunięcie bitowe w lewo D_A            |
| 8      | SHR      | Przesunięcie bitowe w prawo D_A           |
| 9      | ROL      | Rotacja w lewo D_A                         |
| 10     | ROR      | Rotacja w prawo D_A                        |
| 11     | INC      | Zwiększa D_A o 1                           |
| 12     | DEC      | Zmniejsza D_A o 1                          |


## Rozmiar danych

* Wszystkie rejestry poza `OP_SEL` są 8-bitowe (`0x00`–`0xFF`)
* `OP_SEL` ma 4 bity (`0x0`–`0xF`) i wybiera operację ALU
* RAM ma 255 bajtów, adresy `[0x00]` do `[0xFE]`
* Dostępne rejestry: `R0, R1, R2, R3, D_A, D_B, OP_SEL, RES`

  * `D_A` i `D_B` to wejścia do ALU
  * `RES` dostaje wynik

### Dynamiczne rejestry użytkownika (DEF)

Możesz tworzyć własne rejestry komendą:

```
DEF INT|STR|HEX <NAZWA> <WIELKOSC>
```

* `WIELKOSC` podajesz w hex
* 1 jednostka wielkości = 4 bity
* Przykłady:

  * `DEF INT MYREG 0x2` → 8-bitowy rejestr
  * `DEF HEX TMP 0x4` → 16-bitowa przestrzeń
  * `DEF STR BUF 0x10` → bufor 64-bitowy (8 bajtów)
  - Albo
  * `DEF INT MYREG 2` → 8-bitowy rejestr
  * `DEF HEX TMP 4` → 16-bitowa przestrzeń
  * `DEF STR BUF 16` → bufor 64-bitowy (8 bajtów)

Rejestry stworzone przez `DEF` zachowują się jak normalne pola pamięci z określonym rozmiarem i możesz ich używać w MOV, OUT itd.


## Przykłady użycia

### Tryb plikowy
Stwórz plik `program.masm`:

```

start:
MOV D_A, 15
MOV D_B, 70
MOV OP_SEL, 1
ALU
OUT RES
JMP start

````

Uruchom w terminalu:  

```bash
python3 main.py -f program.masm
````

### Tryb interaktywny (REPL)

```bash
python3 main.py
```

Wpisuj komendy na żywo:

```
MOV D_A, 15
MOV D_B, 70
MOV OP_SEL, 1
ALU
OUT RES
```

## Typy danych

* Wartości są reprezentowane w **hex** (np. `0x0F`)
* Własna klasa `hex` obsługuje maskowanie i negację bitową

## Licencja

MIT License – możesz używać, modyfikować i dzielić się kodem, zachowując informację o autorze.
