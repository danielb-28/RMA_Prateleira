#!/usr/bin/env python3
import math
import time
import numpy as np
import os

def dist_euclidiana(v1, v2):
	dim, soma = len(v1), 0
	for i in range(dim):
		soma += math.pow(v1[i] - v2[i], 2)
	return math.sqrt(soma)

tempo = time.time()

path_pontos = os.path.dirname(os.path.abspath(__file__)) + "/pontos.csv"
arquivo_pontos = np.genfromtxt(path_pontos, delimiter=',')

x = list(arquivo_pontos[:, 0])
y = list(arquivo_pontos[:, 1])
z = list(arquivo_pontos[:, 2])
h = list(arquivo_pontos[:, 3])

camFinalX = [x[0]]
camFinalY = [y[0]]
camFinalZ = [z[0]]
camFinalH = [h[0]]

#x = [0.75, 7, 3, 4, 6, 7]
#y = [0.5, 0.5, 1, 3, 2, 7]
#camFinalX = [0.75]
#camFinalY = [0.5]
distancias = []

while len(x) > 1:
    d = float("inf")
    coord, index = [], 0
    for i in range(1, len(x)):
        dist = dist_euclidiana([camFinalX[-1], camFinalY[-1]], [x[i], y[i]])
        if dist < d:
            index = i
            coord = [x[i], y[i], z[i], h[i]]
            d = dist
    del x[index]
    del y[index]
    del z[index]
    del h[index]

    distancias.append(d)
    camFinalX.append(coord[0])
    camFinalY.append(coord[1])
    camFinalZ.append(coord[2])
    camFinalH.append(coord[3])

print(camFinalX)
print(camFinalY)
print(distancias)
print("Tempo de execucao: " + str(time.time()-tempo))

arquivo_pontos_o = open(os.path.dirname(os.path.abspath(__file__)) + "/pontos_o.csv", 'w')

for i in range(len(camFinalX)-1):
    
    arquivo_pontos_o.write(str(camFinalX[i]) + " " + str(camFinalY[i]) + " " + str(camFinalZ[i]) + " " + str(camFinalH[i]))
    arquivo_pontos_o.write(" " + str(camFinalX[i+1]) + " " + str(camFinalY[i+1]) + " " + str(camFinalZ[i+1]) + " " + str(camFinalH[i+1]) + "\n")
    #arquivo_pontos_o.write(str(arquivo_pontos[i, 0]) + " " + str(arquivo_pontos[i, 1]) + " " + str(arquivo_pontos[i, 2]) + " " + str(arquivo_pontos[i, 3]))
    #arquivo_pontos_o.write(" " + str(arquivo_pontos[i+1, 0]) + " " + str(arquivo_pontos[i+1, 1]) + " " + str(arquivo_pontos[i+1, 2]) + " " + str(arquivo_pontos[i+1, 3]) + "\n")

arquivo_pontos_o.close()
