import sys
sys.stdout.write(sys.stdin.read().encode('latin1',errors='replace').decode('cp1251'))
