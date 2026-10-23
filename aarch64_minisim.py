# aarch64_minisim.py — tiny ARMv8/AArch64-ish simulator for learning

from typing import List, Dict, Tuple

U64 = (1 << 64) - 1


def u64(x):
  return x & U64


def sgn64(x):
  return (x >> 63) & 1


class CPU:

  def __init__(self, mem_size=64 * 1024):
    # X0..X30 (31 general), SP separate, PC is instruction index (not byte address here)
    self.X = [0] * 31
    self.SP = 0
    self.PC = 0
    self.N = 0
    self.Z = 0
    self.C = 0
    self.V = 0
    self.mem = bytearray(mem_size)
    self.program: List[Tuple[str, List[str]]] = []
    self.labels: Dict[str, int] = {}

  def set_flags_nzcv(self, result, carry=None, overflow=None):
    r = u64(result)
    self.N = sgn64(r)
    self.Z = 1 if r == 0 else 0
    if carry is not None:
      self.C = 1 if carry else 0
    if overflow is not None:
      self.V = 1 if overflow else 0
    return r

  def read_reg(self, name: str) -> int:
    name = name.strip().upper()
    if name == 'SP':
      return self.SP
    if name.startswith('X'):
      idx = int(name[1:])
      if idx == 31:
        # X31 is often SP or zero depending on context; we’ll treat as zero reg here.
        return 0
      return self.X[idx]
    raise ValueError(f"Bad reg {name}")

  def write_reg(self, name: str, val: int):
    name = name.strip().upper()
    val = u64(val)
    if name == 'SP':
      self.SP = val
      return
    if name.startswith('X'):
      idx = int(name[1:])
      if idx == 31:
        # Treat X31 as zero register (writes ignored) in this tiny sim
        return
      self.X[idx] = val
      return
    raise ValueError(f"Bad reg {name}")

  def load64(self, addr: int) -> int:
    addr &= len(self.mem) - 1
    return int.from_bytes(self.mem[addr:addr + 8], 'little', signed=False)

  def store64(self, addr: int, val: int):
    addr &= len(self.mem) - 1
    self.mem[addr:addr + 8] = u64(val).to_bytes(8, 'little')

  # --- Assembler (very small) ---
  def assemble(self, src: str):
    lines = []
    for raw in src.splitlines():
      line = raw.split(';', 1)[0].split('#', 1)[0].strip()  # strip comments
      if line:
        lines.append(line)

    # pass 1: collect labels
    pc = 0
    for line in lines:
      if line.endswith(':'):
        self.labels[line[:-1].strip()] = pc
      else:
        pc += 1

    # pass 2: build program
    prog = []
    for line in lines:
      if line.endswith(':'):
        continue
      parts = [p.strip() for p in line.replace(',', ' ').split()]
      op = parts[0].upper()
      args = parts[1:]
      prog.append((op, args))
    self.program = prog

  # --- Execution ---
  def eval_operand(self, tok: str) -> int:
    if tok.startswith('#'):
      return int(tok[1:], 0)
    if tok.upper() in self.labels:
      return self.labels[tok.upper()]
    return self.read_reg(tok)

  def step(self) -> bool:
    if not (0 <= self.PC < len(self.program)):
      return False
    op, args = self.program[self.PC]
    # default: advance
    next_pc = self.PC + 1

    def set_pc_label(lbl):
      nonlocal next_pc
      if lbl.upper() not in self.labels:
        raise ValueError(f"Unknown label {lbl}")
      next_pc = self.labels[lbl.upper()]

    # --- Tiny subset ---
    if op == 'MOV':
      # MOV Xd, Xn|#imm
      dst, src = args
      val = self.eval_operand(src)
      self.write_reg(dst, val)

    elif op == 'ADD':
      # ADD Xd, Xn, Xm|#imm
      dst, rn, rm = args
      a = self.read_reg(rn)
      b = self.eval_operand(rm)
      self.write_reg(dst, u64(a + b))

    elif op == 'SUBS' or op == 'CMP':
      # SUBS Xd, Xn, Xm|#imm   (we ignore writing result if op == CMP)
      # CMP Xn, Xm|#imm        -> SUBS XZR, Xn, Xm
      if op == 'CMP':
        rn, rm = args
        a = self.read_reg(rn)
        b = self.eval_operand(rm)
        res = (a - b) & ((1 << 65) - 1)
        carry = (a >= b)  # borrow not needed
        # Overflow for subtraction (a - b) in two's complement:
        sa = sgn64(a)
        sb = sgn64(b)
        sr = sgn64(res)
        overflow = (sa != sb) and (sr != sa)
        self.set_flags_nzcv(res, carry=carry, overflow=overflow)
      else:
        dst, rn, rm = args
        a = self.read_reg(rn)
        b = self.eval_operand(rm)
        res = (a - b) & ((1 << 65) - 1)
        carry = (a >= b)
        sa = sgn64(a)
        sb = sgn64(b)
        sr = sgn64(res)
        overflow = (sa != sb) and (sr != sa)
        r64 = self.set_flags_nzcv(res, carry=carry, overflow=overflow)
        self.write_reg(dst, r64)

    elif op == 'CBZ' or op == 'CBNZ':
      # CBZ Xt, label | CBNZ Xt, label
      rt, label = args
      val = self.read_reg(rt)
      take = (val == 0) if op == 'CBZ' else (val != 0)
      if take:
        set_pc_label(label)

    elif op == 'B':
      set_pc_label(args[0])

    elif op == 'LDR':
      # LDR Xd, [Xn, #imm]
      dst, addr_spec = args[0], args[1]
      # Expect addr like [Xn, #imm] or [Xn]
      spec = " ".join([addr_spec] + args[2:])
      inside = spec.strip().strip('[]').split(',')
      base = inside[0].strip()
      off = int(inside[1].strip()[1:], 0) if len(inside) > 1 else 0
      addr = self.read_reg(base) + off
      self.write_reg(dst, self.load64(addr))

    elif op == 'STR':
      # STR Xs, [Xn, #imm]
      src, addr_spec = args[0], args[1]
      spec = " ".join([addr_spec] + args[2:])
      inside = spec.strip().strip('[]').split(',')
      base = inside[0].strip()
      off = int(inside[1].strip()[1:], 0) if len(inside) > 1 else 0
      addr = self.read_reg(base) + off
      self.store64(addr, self.read_reg(src))

    elif op == 'ADR':
      # ADR Xd, label  (compute address/index of label into reg)
      dst, label = args
      if label.upper() not in self.labels:
        raise ValueError(f"Unknown label {label}")
      self.write_reg(dst, self.labels[label.upper()])

    elif op == 'NOP':
      pass

    else:
      raise ValueError(f"Unsupported op: {op} (args={args})")

    self.PC = next_pc
    return True

  def run(self, max_steps=100000):
    steps = 0
    while steps < max_steps and self.step():
      steps += 1
    return steps

  def dump(self, regs=True, flags=True, mem=None):
    if regs:
      xs = " ".join([f"X{i}={self.X[i]:#018x}" for i in range(8)])
      print(xs)
      xs = " ".join([f"X{i}={self.X[i]:#018x}" for i in range(8, 16)])
      print(xs)
      xs = " ".join([f"X{i}={self.X[i]:#018x}" for i in range(16, 24)])
      print(xs)
      xs = " ".join([f"X{i}={self.X[i]:#018x}" for i in range(24, 31)])
      print(xs)
      print(f"SP={self.SP:#018x} PC={self.PC}")
    if flags:
      print(f"N={self.N} Z={self.Z} C={self.C} V={self.V}")
    if mem:
      addr, count = mem
      data = self.mem[addr:addr + count]
      print(f"mem[{addr:#x}..{addr+count:#x}]:", data.hex())


# --- Demo program: sum 1..5 into X0 and store at memory[0x100] ---
demo = """
        MOV X0, #0        ; sum = 0
        MOV X1, #1        ; i = 1
        MOV X2, #5        ; n = 5
        MOV X3, #0x100    ; base memory address

LOOP:   ADD X0, X0, X1    ; sum += i
        ADD X1, X1, #1    ; i++
        CMP X2, X1        ; sets flags on (n - i)
        CBNZ X2, LOOP     ; (lazy trick) if X2 != 0? No—this is wrong logically.
                          ; We'll do it properly with a temp:

        ; Proper loop using a temp register:
"""

demo_fixed = """
        MOV X0, #0
        MOV X1, #1
        MOV X2, #5
        MOV X3, #0x100

LOOP:   ADD X0, X0, X1
        ADD X1, X1, #1
        SUBS X4, X2, X1   ; X4 = n - i, set NZCV
        CBNZ X4, LOOP

        STR X0, [X3, #0]  ; store result
        NOP
"""

if __name__ == "__main__":
  cpu = CPU()
  cpu.assemble(demo_fixed)
  steps = cpu.run()
  print(f"Ran {steps} steps")
  cpu.dump(mem=(0x100, 8))  # show where we stored the sum

