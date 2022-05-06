import os
import numpy as np

def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l

listaGerados = np.loadtxt(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pontos.csv'), delimiter = ',')

maior = 0
menor = 1000

for i in range(len(listaGerados)):
    if maior < listaGerados[i][0]:
        maior = listaGerados[i][0]
    if menor > listaGerados[i][0]:
        menor = listaGerados[i][0]
    
quantidadeSelecionados = 5

manter = np.random.randint(menor,maior, quantidadeSelecionados)
manter = remove_repetidos(manter)

while len(manter) != quantidadeSelecionados:
    print('babaca')
    iguais = True
    manter = np.random.randint(menor,maior, quantidadeSelecionados)
    manter = remove_repetidos(manter)

novaLista = []
for i in range(len(listaGerados)):
    if listaGerados[i][0] in manter:
        novaLista.append(listaGerados[i])

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pontos.csv'), 'w') as arquivoEscrita:
    for i in range(len(novaLista)):
        arquivoEscrita.write(str(novaLista[i][0]) + ',' + str(novaLista[i][1]) + ',' + str(novaLista[i][2]) + ',' + str(novaLista[i][3]) + ',' + str(novaLista[i][4]) + '\n')