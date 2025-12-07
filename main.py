import sys
class hex(int):
    def __new__(cls, value, places=2):
        obj = int.__new__(cls, value % (16**places))
        obj.places = places
        return obj

    def __str__(self):
        return f"0x{int(self):0{self.places}X}"
    
    def __repr__(self):
        return str(self)
    
    def __invert__(self):
        return hex(~int(self) % (16**self.places), self.places)

    
mem = [hex(0, 2) for i in range(255)]
reg = {
    "R0":hex(0, 2),
    "R1":hex(0, 2),
    "R2":hex(0, 2),
    "R3":hex(0, 2),
    "D_A":hex(0, 2),
    "D_B":hex(0, 2),
    "OP_SEL":hex(0, 1),
    "RES":hex(0, 2)
}

def h_commands():
    while True:
        command = input()
        if (command == ""): continue
        parts = command.replace(",", "").split()

        command = parts.pop(0).upper()
        handle(command,parts)

        
def handle(command,parts):
    match command:
            case 'OUT':
                if parts[0].startswith('[') and parts[0].endswith(']'):
                    addr = int(parts[0][1:-1], 16)
                    print(mem[addr])
                elif parts[0].strip().upper() in reg:
                    n_reg = parts[0].strip().upper()
                    print(reg[n_reg])
                else:
                    errors("<OUT addr> nie znaleziono addr")
            case 'EXIT':
                sys.exit()
            case 'MOV':
                if parts[0].startswith('[') and parts[0].endswith(']'):
                    addr = int(parts[0][1:-1], 16)
                    if parts[1].startswith('[') and parts[1].endswith(']'):
                        addr2 = int(parts[1][1:-1], 16)
                        mem[addr] = mem[addr2]
                    elif parts[1].strip().upper() in reg:
                        addr2 = parts[1].strip().upper()
                        mem[addr] = reg[addr2]
                    elif parts[1].isdigit():
                        mem[addr] = hex(int(parts[1]))
                    elif parts[1].startswith("0x"):
                        mem[addr] = hex(int(parts[1], 16))
                    else:
                        errors("<MOV addr1, addr2> nie znaleziono addr2")
                elif parts[0].strip().upper() in reg:
                    addr = parts[0].strip().upper()
                    if parts[1].startswith('[') and parts[1].endswith(']'):
                        addr2 = int(parts[1][1:-1], 16)
                        reg[addr] = mem[addr2]
                    elif parts[1].strip().upper() in reg:
                        addr2 = parts[1].strip().upper()
                        reg[addr] = reg[addr2]
                    elif parts[1].isdigit():
                        reg[addr] = hex(int(parts[1]))
                    elif parts[1].startswith("0x"):
                        reg[addr] = hex(int(parts[1], 16))
                    else:
                        errors("<MOV addr1, addr2> nie znaleziono addr2")
                else:
                    errors("<MOV addr1, addr2> nie znaleziono addr1")
            case 'ALU':
                alu()                
def errors(wiadomosc):
    print(f"[ERROR]:{wiadomosc}")

def alu():
    match reg["OP_SEL"]:
        case 1: # A + B
            reg["RES"] = hex(reg["D_A"]+reg["D_B"])
        case 2: # A - B
            reg["RES"] = hex(reg["D_A"]-reg["D_B"])
        case 3: # A AND B
            reg["RES"] = hex(reg["D_A"] & reg["D_B"])
        case 4: # A OR B
            reg["RES"] = hex(reg["D_A"] | reg["D_B"])
        case 5: # A XOR B
            reg["RES"] = hex(reg["D_A"] ^ reg["D_B"])
        case 6: # NOT A
            reg["RES"] = hex(~reg["D_A"])
        case 7: # SHL A
            reg["RES"] = hex(reg["D_A"] << 1)
        case 8: # SHR A
            reg["RES"] = hex(reg["D_A"] >> 1)
        case 9: # ROL A
            reg["RES"] = hex((reg["D_A"] << 1) | (reg["D_A"] >> 7))
        case 10: # ROR A    
            reg["RES"] = hex((reg["D_A"] >> 1) | (reg["D_A"] << 7))
        
            
if __name__ == "__main__":
    args = sys.argv[1:]

    plik = None
    i = 0
    while i < len(args):
        if args[i] in ("-f", "--file") and i + 1 < len(args):
            plik = args[i+1]
            i += 1
        i +=1

    if plik:
        with open(plik) as f:
            linie=f.readlines()

            labels = {}
            for idx, linia in enumerate(linie):
                linia = linia.strip()
                if linia.endswith(":"):
                    labels[linia[:-1:].upper()] = idx

            i = 0
            while i < len(linie):
                linia = linie[i]
                if linia and not linia.startswith(";") and not linia.endswith(":"):
                    parts = linia.replace(",", "").split()
                    command = parts.pop(0).upper()
                    if command == "JMP":  # bezwarunkowy skok
                        i = labels[parts[0].upper()]
                        continue
                    elif command == "JZ":  # skok jeśli zero (np. RES==0)
                        if reg[parts[0]] == 0:
                            i = labels[parts[1].upper()]
                            continue
                    elif command == "JNZ":  # skok jeśli zero (np. RES==0)
                        if reg[parts[0]] != 0:
                            i = labels[parts[1].upper()]
                            continue
                    handle(command, parts)
                i += 1


    else:
        h_commands()