print('A','+' if (a:=int(input()))%2==0 and a%25==0 else '-','B','+' if a%2 and a%25==0 else '-','C','+' if a%8==0 else '-')