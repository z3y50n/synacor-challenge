from architecture import Memory, Registers, Stack, OpCodes

memory = Memory()
registers = Registers()
stack = Stack()
PC = 0


def read_code(filename):
    with open(filename, "rb") as f:
        code = f.read()
    return code


def display(cmd):
    print(f"PC: {PC:5}, Command: {cmd}")
    print(registers)


def reg_or_value(x):
    if x >= 32768 and x <= 32775:
        x = registers[x]
    return x


def bit_not(n, numbits=15):
    return (1 << numbits) - 1 - n


def execute():
    global PC
    opcode = OpCodes(memory[PC])
    cmd = opcode.name
    a = memory[PC + 1]
    b = memory[PC + 2]
    c = memory[PC + 3]

    if opcode == OpCodes.HALT:
        display(cmd)
        print("Halt. Exiting...")
        exit(0)
    if opcode == OpCodes.SET:
        display(f"{cmd} {a} {b}")
        b = reg_or_value(b)
        registers[a] = b
        PC += 3
    elif opcode == OpCodes.PUSH:
        display(f"{cmd} {a}")
        a = reg_or_value(a)
        stack.push(a)
        PC += 2
    elif opcode == OpCodes.POP:
        display(f"{cmd} {a}")
        # a = reg_or_value(a)
        val = stack.pop()
        registers[a] = val
        PC += 2
    elif opcode == OpCodes.EQ:
        display(f"{cmd} {a} {b} {c}")
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = 1 if b == c else 0
        PC += 4
    elif opcode == OpCodes.GT:
        display(f"{cmd} {a} {b} {c}")
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = 1 if b > c else 0
        PC += 4
    elif opcode == OpCodes.JMP:
        display(f"{cmd} {a}")
        PC = a
    elif opcode == OpCodes.JT:
        display(f"{cmd} {a} {b}")
        a = reg_or_value(a)
        if a:
            PC = b
        else:
            PC += 3
    elif opcode == OpCodes.JF:
        display(f"{cmd} {a} {b}")
        a = reg_or_value(a)
        if not a:
            PC = b
        else:
            PC += 3
    elif opcode == OpCodes.ADD:
        display(f"{cmd} {a} {b} {c}")
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = (b + c) % 32768
        PC += 4
    elif opcode == OpCodes.MULT:
        display(f"{cmd} {a} {b} {c}")
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = (b * c) % 32768
        PC += 4
    elif opcode == OpCodes.MOD:
        display(f"{cmd} {a} {b} {c}")
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = b % c
        PC += 4
    elif opcode == OpCodes.AND:
        display(f"{cmd} {a} {b} {c}")
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = b & c
        PC += 4
    elif opcode == OpCodes.OR:
        display(f"{cmd} {a} {b} {c}")
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = b | c
        PC += 4
    elif opcode == OpCodes.NOT:
        display(f"{cmd} {a} {b}")
        b = reg_or_value(b)
        registers[a] = bit_not(b)
        PC += 3
    elif opcode == OpCodes.RMEM:
        display(f"{cmd} {a} {b}")
        b = reg_or_value(b)
        registers[a] = memory[b]
        PC += 3
    elif opcode == OpCodes.WMEM:
        display(f"{cmd} {a} {b}")
        a = reg_or_value(a)
        b = reg_or_value(b)
        memory[a] = b
        PC += 3
    elif opcode == OpCodes.CALL:
        display(f"{cmd} {a}")
        stack.push(PC + 2)
        PC = reg_or_value(a)
    elif opcode == OpCodes.RET:
        display(f"{cmd}")
        if stack.is_empty():
            print("Empty Stack. Exiting...")
            exit(0)
        PC = stack.pop()
    elif opcode == OpCodes.OUT:
        display(f"{cmd} {a}")
        a = reg_or_value(a)
        print(chr(a), end="")
        PC += 2
    elif opcode == OpCodes.IN:
        display(f"{cmd} {a}")
        txt = input()
        # if not txt:
        # txt = "\n"
        # registers[a] = 10
        # else:
        registers[a] = sum(ord(c) for c in txt) % 32768
        PC += 2
    elif opcode == OpCodes.NOOP:
        PC += 1
    else:
        print(f"Didn't implement logic for command {cmd} with opcode {opcode.value}")
        exit(0)


if __name__ == "__main__":
    code = read_code("challenge.bin")
    memory.load_code(code)

    while PC < len(memory):
        execute()
