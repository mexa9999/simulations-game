import time
import functools
from bitarray import bitarray
import random

a = bitarray("101010")
b = bitarray("101010")
c = bitarray("11111111")

def bit_mutate(data):
    index = random.randrange(len(data))
    data[index] = not data[index]
    return data

def segment_mutate(data):
    g =random.randrange(1, len(data)-1)

    data[g-1:g+2] = bitarray(bin(random.getrandbits(3))[2:].zfill(3))
    
    return data

def segment_invert(data):
    g =random.randrange(1, len(data)-2)
    h = data[g-1:g+2]
    h.invert()
    data[g-1:g+2] = h
    return data

al = set()
start = time.perf_counter()
for x in range(100000):
    al.add(int.from_bytes(random.choice([bit_mutate,segment_mutate,segment_invert])(c).tobytes(), byteorder='big', signed=False)/10)
end = time.perf_counter()
print(end-start)
print(sorted(al))