class PipelineProcessor:
    def __init__(self):
        self.pc = 0
        self.registers = [0] * 32  # Registros x0 a x31
        self.memory = {}          # Memoria simulada
        self.instructions = []    # Instrucciones en texto
        self.labels = {}            #diccionario para etiquetas
        self.running = False

    def load_program(self, program_text):
        self.instructions = []
        self.labels = {}
        self.pc = 0
        self.running = True

        lines = program_text.strip().split('\n')

        # Paso 1: mapa de etiquetas
        index = 0
        for line in lines:
            clean = line.strip()
            if not clean or clean.startswith("#"):
                continue
            if ":" in clean:
                label = clean.replace(":", "").strip()
                self.labels[label] = index
            else:
                self.instructions.append(clean)
                index += 1

    def step(self):
        """Ejecuta una instrucción"""
        if self.pc >= len(self.instructions):
            print("Fin del programa.")
            self.running = False
            return

        line = self.instructions[self.pc].strip()
        if not line or line.startswith('#'):
            self.pc += 1
            return

        print(f"PC={self.pc:02d} → {line}")
        self.execute_instruction(line)
        self.pc += 1

    def execute_instruction(self, line):
        """Interpreta y ejecuta una sola instrucción"""
        parts = line.replace(',', '').split()
        if not parts:
            return

        op = parts[0].upper()

        try:
            if op == "ADDI":
                rd = int(parts[1][1:])
                rs1 = int(parts[2][1:])
                imm = int(parts[3])
                self.registers[rd] = self.registers[rs1] + imm

            elif op == "ADD":
                rd = int(parts[1][1:])
                rs1 = int(parts[2][1:])
                rs2 = int(parts[3][1:])
                self.registers[rd] = self.registers[rs1] + self.registers[rs2]

            elif op == "SUB":
                rd = int(parts[1][1:])
                rs1 = int(parts[2][1:])
                rs2 = int(parts[3][1:])
                self.registers[rd] = self.registers[rs1] - self.registers[rs2]

            elif op == "LW":
                rd = int(parts[1][1:])
                offset, base = parts[2].replace(')', '').split('(')
                addr = self.registers[int(base[1:])] + int(offset)
                self.registers[rd] = self.memory.get(addr, 0)

            elif op == "SW":
                rs2 = int(parts[1][1:])
                offset, base = parts[2].replace(')', '').split('(')
                addr = self.registers[int(base[1:])] + int(offset)
                self.memory[addr] = self.registers[rs2]

            elif op == "BEQ":
                rs1 = int(parts[1][1:])
                rs2 = int(parts[2][1:])
                label = parts[3]
                if self.registers[rs1] == self.registers[rs2]:
                    if label in self.labels:
                        self.pc = self.labels[label] - 1  # -1 porque el step suma +1 después
                    else:
                        print(f"Etiqueta no encontrada: {label}")

            else:
                print(f"Instrucción no soportada: {op}")

        except Exception as e:
            print(f"Error ejecutando '{line}': {e}")
