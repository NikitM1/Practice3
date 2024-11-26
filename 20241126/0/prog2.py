import locale
w='вопрос'
print(w.encode('KOI8-R').decode('cp1251'))
print('бМЧЛЮМХЕ'.encode('CP1251').decode('KOI8-R'))
print('ЩЧРЮМХЕ'.encode('CP1251').decode('KOI8-R'))

