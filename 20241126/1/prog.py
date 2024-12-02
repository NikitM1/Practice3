import sys
s=sys.stdin.buffer.read(); n=s[0]; l=len(s)-1; st=s[1:-1]
a=[st[i*int(l/n): (i+1)*int(l/n)] for i in range(n-1)]+[st[(n-1)*int(l/n):]] if n < l else st
sys.stdout.buffer.write(bytes([s[0]]))
try:
    for t in sorted(a): sys.stdout.buffer.write(t)
except:
    sys.stdout.buffer.write(bytes(list(sorted(a))))