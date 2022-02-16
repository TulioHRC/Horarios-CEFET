lista = []
impar = [1, 3, 5, 7, 9]
par = [0, 2, 4, 6, 8, 10]

for c in range(0, 5):
    for d in range(0, 3) if (c in par) else range(10, 13):
        lista.append(d)

print(lista)
