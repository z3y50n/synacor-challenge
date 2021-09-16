import struct


class Registers:
    def __init__(self):
        self.registers = [struct.pack("<H", 0)] * 8

    def __getitem__(self, k):
        if k < 0 or (k > 7 and k < 32768) or k > 32775:
            raise Exception("Wrong register address")
        return struct.unpack("<H", self.registers[k % 32768])[0]

    def __setitem__(self, k, v):
        if k < 32768 or k > 32775:
            raise Exception("Wrong register address")
        self.registers[k % 32768] = struct.pack("<H", v)

    def __repr__(self):
        text = "R0: {:>5}, R1: {:>5}, R2: {:>5}, R3: {:>5}\n".format(
            self[0], self[1], self[2], self[3]
        )
        text += "R4: {:>5}, R5: {:>5}, R6: {:>5}, R7: {:>5}\n".format(
            self[4], self[5], self[6], self[7]
        )
        return text


class Memory:
    def __init__(self):
        self.memory = struct.pack("<" + "H" * 2 ** 15, *[0 for _ in range(2 ** 15)])

    def __len__(self):
        return len(self.memory)

    def __getitem__(self, k):
        if isinstance(k, slice):
            size = k.stop - k.start
            return struct.unpack(
                "<" + "H" * size, self.memory[2 * k.start : 2 * k.stop]
            )
        return struct.unpack("<H", self.memory[2 * k : 2 * k + 2])[0]

    def load_code(self, code):
        if len(code) > len(self.memory):
            raise Exception("Code doesn't fit in memory")
        self.memory = code + self.memory[len(code) :]

    def get_memory(self):
        return self.memory


class Stack:
    def __init__(self):
        self.data = []

    def push(self, val):
        self.data.append(struct.pack("<H", val))

    def pop(self):
        if self.is_empty():
            raise Exception("Stack is empty")
        return struct.unpack("<H", self.data.pop())[0]

    def __len__(self):
        return len(self.data)

    def is_empty(self):
        return len(self.data) == 0
