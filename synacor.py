from architecture import Memory, Registers, Stack

memory = Memory()
registers = Registers()
stack = Stack()
PC = 0
commands = {
    0: "halt",
    1: "set",
    2: "push",
    3: "pop",
    4: "eq",
    5: "gt",
    6: "jmp",
    7: "jt",
    8: "jf",
    9: "add",
    10: "mult",
    11: "mod",
    12: "and",
    13: "or",
    14: "not",
    15: "rmem",
    16: "wmem",
    17: "call",
    18: "ret",
    19: "out",
    20: "in",
    21: "noop",
}


def read_code(filename):
    with open(filename, "rb") as f:
        code = f.read()
    return code


def display(cmd):
    print(f"Cmd: {cmd}")
    print(f"PC: {PC:5}")
    print(registers)


def execute():
    global PC
    opcode = memory[PC]
    a = memory[PC + 1]
    b = memory[PC + 2]
    c = memory[PC + 3]
    cmd = commands[opcode]

    if opcode == 0:
        display(cmd)
        print("Halt")
        exit(0)
    elif opcode == 6:
        display(cmd)
        PC = a
    elif opcode == 7:
        display(cmd)
        if a:
            PC = b
        else:
            PC += 1
    elif opcode == 8:
        display(cmd)
        if not a:
            PC = b
        else:
            PC += 1
    elif opcode == 19:
        print(chr(a), end="")
        PC += 2
    elif opcode == 21:
        PC += 1
    else:
        print(f"Didn't implement logic for opcode {opcode}")
        exit(0)


if __name__ == "__main__":
    code = read_code("challenge.bin")
    memory.load_code(code)
    PC = 487

    while PC < len(memory):
        execute()
