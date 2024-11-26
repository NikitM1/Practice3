import binascii
with open('binf', 'rb') as f: 
    data=f.read()
dd=binascii.hexlify(data, ' ',4).decode().split()
for addr, i in enumerate(range(0, len(res), 4)): 
    print( f"{addr:08x}",":",  *dd[i:i+4])
