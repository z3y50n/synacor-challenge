from architecture import Memory, Registers, Stack

memory = Memory()
registers = Registers()
stack = Stack()

def read_code(filename):
    with open(filename, "rb") as f:
        code = f.read()
    return code

if __name__ == "__main__":
    code = read_code("challenge.bin")
    memory.load_code(code)

    # Ugly way just to get the second code
    # Read enough characters to display the message
    txt = []
    for i in range(302):
        if memory[i] == 19:
            txt.append(chr(memory[i+1]))
    print("".join(txt))
