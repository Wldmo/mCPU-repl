
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

## Przykłady użycia

### Tryb plikowy
Stwórz plik `program.asb`:

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
python3 main.py -f program.asb
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

## Struktura pamięci i rejestrów

* **Rejestry:** `R0, R1, R2, R3, D_A, D_B, OP_SEL, RES`
* **RAM:** 255 bajtów, adresowane od `[0x00]` do `[0xFE]`

## Licencja

MIT License – możesz używać, modyfikować i dzielić się kodem, zachowując informację o autorze.

```
