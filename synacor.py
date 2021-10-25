import json

from architecture import Memory, Registers, Stack, OpCodes

memory = Memory()
registers = Registers()
stack = Stack()
PC = 0
# Make it until the teleporter part
terminal_input = """take tablet\ndoorway\nnorth\nnorth\nbridge\ncontinue\ndown\neast\ntake empty lantern\nwest\nwest\npassage\nladder\nwest\nsouth\nnorth\ntake can\nwest\nladder\nuse can\nuse lantern\ndarkness\ncontinue\nwest\nwest\nwest\nwest\nnorth\ntake red coin\nnorth\neast\ntake concave coin\ndown\ntake corroded coin\nup\nwest\nwest\ntake blue coin\nup\ntake shiny coin\ndown\neast\nuse blue coin\nuse red coin\nuse shiny coin\nuse concave coin\nuse corroded coin\nnorth\ntake teleporter\nuse teleporter\n"""
terminal_input = list(terminal_input)
enabled = False


def read_code(filename):
    with open(filename, "rb") as f:
        code = f.read()
    return code


def display(cmd, enabled=False):
    if enabled:
        with open("memory.dump", "a") as f:
            f.write(f"PC: {PC:5}, Command: {cmd}\n")
            f.write(str(registers))
            f.write("\n\n")
        """
        print(f"PC: {PC:5}, Command: {cmd}")
        print(registers)
        """


def reg_or_value(x):
    if x >= 32768 and x <= 32775:
        x = registers[x]
    return x


def bit_not(n, numbits=15):
    return (1 << numbits) - 1 - n


def execute():
    global PC
    global terminal_input
    global enabled

    opcode = OpCodes(memory[PC])
    cmd = opcode.name
    a = memory[PC + 1]
    b = memory[PC + 2]
    c = memory[PC + 3]

    if opcode == OpCodes.HALT:
        display(cmd, enabled)
        print("Halt. Exiting...")
        exit(0)
    if opcode == OpCodes.SET:
        display(f"{cmd} {a} {b}", enabled)
        b = reg_or_value(b)
        registers[a] = b
        PC += 3
    elif opcode == OpCodes.PUSH:
        display(f"{cmd} {a}", enabled)
        a = reg_or_value(a)
        stack.push(a)
        PC += 2
    elif opcode == OpCodes.POP:
        display(f"{cmd} {a}", enabled)
        # a = reg_or_value(a)
        registers[a] = stack.pop()
        PC += 2
    elif opcode == OpCodes.EQ:
        display(f"{cmd} {a} {b} {c}", enabled)
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = 1 if b == c else 0
        PC += 4
    elif opcode == OpCodes.GT:
        display(f"{cmd} {a} {b} {c}", enabled)
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = 1 if b > c else 0
        PC += 4
    elif opcode == OpCodes.JMP:
        display(f"{cmd} {a}", enabled)
        a = reg_or_value(a)
        PC = a
    elif opcode == OpCodes.JT:
        display(f"{cmd} {a} {b}", enabled)
        a = reg_or_value(a)
        if a != 0:
            PC = b
        else:
            PC += 3
    elif opcode == OpCodes.JF:
        display(f"{cmd} {a} {b}", enabled)
        a = reg_or_value(a)
        if a == 0:
            PC = b
        else:
            PC += 3
    elif opcode == OpCodes.ADD:
        display(f"{cmd} {a} {b} {c}", enabled)
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = (b + c) % 32768
        PC += 4
    elif opcode == OpCodes.MULT:
        display(f"{cmd} {a} {b} {c}", enabled)
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = (b * c) % 32768
        PC += 4
    elif opcode == OpCodes.MOD:
        display(f"{cmd} {a} {b} {c}", enabled)
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = (b % c) % 32768
        PC += 4
    elif opcode == OpCodes.AND:
        display(f"{cmd} {a} {b} {c}", enabled)
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = b & c
        PC += 4
    elif opcode == OpCodes.OR:
        display(f"{cmd} {a} {b} {c}", enabled)
        b = reg_or_value(b)
        c = reg_or_value(c)
        registers[a] = b | c
        PC += 4
    elif opcode == OpCodes.NOT:
        display(f"{cmd} {a} {b}", enabled)
        b = reg_or_value(b)
        registers[a] = bit_not(b)
        PC += 3
    elif opcode == OpCodes.RMEM:
        display(f"{cmd} {a} {b}", enabled)
        b = reg_or_value(b)
        registers[a] = memory[b]
        PC += 3
    elif opcode == OpCodes.WMEM:
        display(f"{cmd} {a} {b}", enabled)
        a = reg_or_value(a)
        b = reg_or_value(b)
        memory[a] = b
        PC += 3
    elif opcode == OpCodes.CALL:
        display(f"{cmd} {a}", enabled)
        stack.push(PC + 2)
        PC = reg_or_value(a)
    elif opcode == OpCodes.RET:
        display(f"{cmd}", enabled)
        if stack.is_empty():
            print("Empty Stack. Exiting...")
            exit(0)
        PC = stack.pop()
    elif opcode == OpCodes.OUT:
        #enabled = False
        display(f"{cmd} {a}", enabled)
        a = reg_or_value(a)
        print(chr(a), end="")
        PC += 2
    elif opcode == OpCodes.IN:
        display(f"{cmd} {a}", enabled)
        if not terminal_input:
            t_input = input()
            if t_input == "d":
                display(f"{cmd} {a}")
            elif t_input.startswith("set"):
                registers[7] = int(t_input[4:])
                return
            elif t_input == "dump":
                enabled = False if enabled else True
                return
            terminal_input = list(t_input + "\n")
        registers[a] = ord(terminal_input.pop(0))
        PC += 2

    elif opcode == OpCodes.NOOP:
        PC += 1
    else:
        print(f"Didn't implement logic for command {cmd} with opcode {opcode.value}")
        exit(0)


if __name__ == "__main__":
    code = read_code("challenge.bin")
    memory.load_code(code)

    # Bypass Confirmation process for 7th code, R8 = 25734
    memory[5485] = 6
    memory[5489] = 6
    memory[5490] = 5491
    
    while PC < len(memory):
        execute()
