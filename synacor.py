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
    elif opcode == OpCodes.JMP:
        display(cmd)
        PC = a
    elif opcode == OpCodes.JT:
        display(cmd)
        if a:
            PC = b
        else:
            PC += 1
    elif opcode == OpCodes.JF:
        display(cmd)
        if not a:
            PC = b
        else:
            PC += 1
    elif opcode == OpCodes.OUT:
        print(chr(a), end="")
        PC += 2
    elif opcode == OpCodes.NOOP:
        PC += 1
    else:
        print(f"Didn't implement logic for command {cmd} with opcode {opcode}")
        exit(0)


if __name__ == "__main__":
    code = read_code("challenge.bin")
    memory.load_code(code)

    while PC < len(memory):
        execute()
