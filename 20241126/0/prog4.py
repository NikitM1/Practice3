import random
import struct
with open('f', 'wb') as f: 
    for i in range(10):
        f.write(struct.pack('f3si', random.random(), bytes(random.randrange(256), random.randrange(256), random.randrange(256)), random.randrange(12345678)))
