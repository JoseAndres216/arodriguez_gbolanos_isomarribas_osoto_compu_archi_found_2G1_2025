class PipelineSegmentado:
    def __init__(self):
        self.pc = 0
        self.registers = [0] * 32
        self.memory = {}
        self.instructions = []
        self.labels = {}
        self.running = True

        # Registros de pipeline
        self.if_id = {}
        self.id_ex = {}
        self.ex_mem = {}
        self.mem_wb = {}

    def load_program(self, program_text):
        self.instructions = []
        self.labels = {}
        self.pc = 0
        self.running = True

        lines = program_text.strip().split('\n')
        index = 0
        for line in lines:
            clean = line.strip()
            if not clean or clean.startswith('#'):
                continue
            if ':' in clean:
                label = clean.replace(":", "").strip()
                self.labels[label] = index
            else:
                self.instructions.append(clean)
                index += 1

    def tick(self):
        self.write_back()
        self.memory_access()
        self.execute()
        self.decode()
        self.fetch()

    def fetch(self):
        if self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            self.if_id = {'instr': instr, 'pc': self.pc}
            self.pc += 1
        else:
            self.if_id = {}

    def decode(self):
        if not self.if_id:
            self.id_ex = {}
            return

        parts = self.if_id['instr'].replace(',', '').split()
        op = parts[0].upper()
        info = {'op': op, 'pc': self.if_id['pc']}

        try:
            if op in ['ADD', 'SUB', 'AND', 'OR', 'XOR', 'SLL']:
                info['rd'] = int(parts[1][1:])
                info['rs1'] = int(parts[2][1:])
                info['rs2'] = int(parts[3][1:])
            elif op == 'ADDI':
                info['rd'] = int(parts[1][1:])
                info['rs1'] = int(parts[2][1:])
                info['imm'] = int(parts[3])
            elif op in ['LW', 'SW']:
                reg = int(parts[1][1:])
                offset, base = parts[2].replace(')', '').split('(')
                info['reg'] = reg
                info['base'] = int(base[1:])
                info['offset'] = int(offset)
            elif op == 'BEQ':
                info['rs1'] = int(parts[1][1:])
                info['rs2'] = int(parts[2][1:])
                info['label'] = parts[3]
            else:
                print(f"[ID] Instrucción no soportada: {op}")
        except:
            print(f"[ID] Error decodificando: {self.if_id['instr']}")

        self.id_ex = info

    def execute(self):
        if not self.id_ex:
            self.ex_mem = {}
            return

        op = self.id_ex['op']
        out = {'op': op, 'pc': self.id_ex['pc']}

        try:
            if op == 'ADDI':
                out['rd'] = self.id_ex['rd']
                out['value'] = self.registers[self.id_ex['rs1']] + self.id_ex['imm']

            elif op == 'ADD':
                out['rd'] = self.id_ex['rd']
                out['value'] = self.registers[self.id_ex['rs1']] + self.registers[self.id_ex['rs2']]

            elif op == 'SUB':
                out['rd'] = self.id_ex['rd']
                out['value'] = self.registers[self.id_ex['rs1']] - self.registers[self.id_ex['rs2']]

            elif op == 'AND':
                out['rd'] = self.id_ex['rd']
                out['value'] = self.registers[self.id_ex['rs1']] & self.registers[self.id_ex['rs2']]

            elif op == 'OR':
                out['rd'] = self.id_ex['rd']
                out['value'] = self.registers[self.id_ex['rs1']] | self.registers[self.id_ex['rs2']]

            elif op == 'XOR':
                out['rd'] = self.id_ex['rd']
                out['value'] = self.registers[self.id_ex['rs1']] ^ self.registers[self.id_ex['rs2']]

            elif op == 'SLL':
                shift = self.registers[self.id_ex['rs2']] & 0x1F
                out['rd'] = self.id_ex['rd']
                out['value'] = self.registers[self.id_ex['rs1']] << shift

            elif op == 'LW':
                base = self.registers[self.id_ex['base']]
                addr = base + self.id_ex['offset']
                out['addr'] = addr
                out['reg'] = self.id_ex['reg']

            elif op == 'SW':
                base = self.registers[self.id_ex['base']]
                addr = base + self.id_ex['offset']
                out['addr'] = addr
                out['value'] = self.registers[self.id_ex['reg']]

            elif op == 'BEQ':
                if self.registers[self.id_ex['rs1']] == self.registers[self.id_ex['rs2']]:
                    if self.id_ex['label'] in self.labels:
                        self.flush_pipeline()
                        self.pc = self.labels[self.id_ex['label']]
            
            elif op == 'NOP':
                pass
                        
        except:
            print(f"[EX] Error ejecutando: {op}")

        self.ex_mem = out

    def memory_access(self):
        if not self.ex_mem:
            self.mem_wb = {}
            return

        op = self.ex_mem['op']
        out = {'op': op}

        try:
            if op == 'LW':
                val = self.memory.get(self.ex_mem['addr'], 0)
                out['value'] = val
                out['rd'] = self.ex_mem['reg']

            elif op == 'SW':
                self.memory[self.ex_mem['addr']] = self.ex_mem['value']

            elif op in ['ADD', 'SUB', 'ADDI', 'AND', 'OR', 'XOR', 'SLL']:
                out['value'] = self.ex_mem['value']
                out['rd'] = self.ex_mem['rd']
        except:
            print(f"[MEM] Error accediendo memoria en: {op}")

        self.mem_wb = out

    def write_back(self):
        if not self.mem_wb:
            return

        op = self.mem_wb['op']
        try:
            if op in ['ADD', 'SUB', 'ADDI', 'AND', 'OR', 'XOR', 'SLL', 'LW']:
                rd = self.mem_wb['rd']
                if rd != 0:
                    self.registers[rd] = self.mem_wb['value']
        except:
            print(f"[WB] Error en write back: {op}")

    def flush_pipeline(self):
        self.if_id = {}
        self.id_ex = {}
        self.ex_mem = {}
        self.mem_wb = {}
