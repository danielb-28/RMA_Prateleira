import os
import numpy as np
import sys
argv = sys.argv

apagar = int(argv[1])

listaGerados = np.loadtxt(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pontos.csv'), delimiter = ',')

novaLista = []
for i in range(len(listaGerados)):
    if listaGerados[i][0] != apagar:
        novaLista.append(listaGerados[i])

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pontos.csv'), 'w') as arquivoEscrita:
    for i in range(len(novaLista)):
        arquivoEscrita.write(str(novaLista[i][0]) + ',' + str(novaLista[i][1]) + ',' + str(novaLista[i][2]) + ',' + str(novaLista[i][3]) + ',' + str(novaLista[i][4]) + '\n')