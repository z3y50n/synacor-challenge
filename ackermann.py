from collections import deque, defaultdict
import sys

sys.setrecursionlimit(50000)


# Recursion
def A(m, n):
    if m == 0:
        return n+1
    if n == 0:
        return A(m-1, R8 % 32768)
    n2 = A(m, n-1)
    return A(m-1, n2)

# Using Stack, Faster
def Ack(m, n):
    stack = deque([])
    stack.extend([m, n])

    while len(stack) > 1:
        n, m = stack.pop(), stack.pop()
        if m == 0:
            stack.append(n+1)
        elif m == 1:
            stack.append(n+2)
        elif m == 2:
            stack.append(2*n+3)
        elif m == 3:
            stack.append(2 ** (n+3) - 3)
        elif n == 0:
            stack.extend([m-1, R8])
        else:
            stack.extend([m-1, m, n-1])
    return stack[0]

memory = defaultdict(dict)
def A_m(m, n):
    if memory[(m, n)]:
        return memory[(m, n)]
    if m == 0:
        val = n+1
        memory[(m, n)] = val
        return val
    if n == 0:
        val = A_m(m-1, R8)
        memory[(m, n)] = val
        return val

    n2 = A_m(m, n-1)
    val = A_m(m-1, n2)
    memory[(m, n)] = val
    return val

def AA(m, n):
    if m == 0:
        return n+1
    elif m == 1:
        return n+2
    elif m == 2:
        return 2*n+3
    elif n == 0 and m > 2:
        return AA(m-1, R8)
    else:
        return AA(m-1, AA(m, n-1))



R8 = 25734
#R8 = 1
#print(A_m(4, 1))
#print(AA(4, 1))
#print(Ack(4, 1))
#print(Ack(4, 1) % 32768)
