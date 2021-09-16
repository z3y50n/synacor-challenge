from architecture import Memory, Registers, Stack

memory = Memory()
registers = Registers()
stack = Stack()
PC = 0


def read_code(filename):
    with open(filename, "rb") as f:
        code = f.read()
    return code


def display():
    print("PC: {:>5}".format(PC))
    print(registers)


if __name__ == "__main__":
    display()
    code = read_code("challenge.bin")
    memory.load_code(code)

    # Ugly way just to get the second code
    # Read enough characters to display the message
    txt = []
    for i in range(302):
        if memory[i] == 19:
            txt.append(chr(memory[i + 1]))
    print("".join(txt))
