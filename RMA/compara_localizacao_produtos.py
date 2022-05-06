import os
import numpy as np

# Tolerâncias quanto a diferenças de localização que ainda se consideram corretas
toleranciaX = 0.3
toleranciaY = 0.3
toleranciaZ = 0.3

listaGerada = np.loadtxt(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'localizacao_produtos_gerados.csv'), delimiter = ',')
listaEncontrada = np.loadtxt(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'localizacao_produtos_encontrados.csv'), delimiter = ',')
#listaEncontrada = listaEncontrada[listaEncontrada[:, 0].argsort()]  # Ordena vetor pelo índice

equivalencias = []      # Lista onde serão atribuídos os índices dos produtos que se encontram na mesma localização para ambas as listas
incongruencias = []     # Lista onde serão atribuídos os índices dos produtos que se encontram em localizações diferentes nas listas
existentes = []         # Lista onde serão atribuídos os índices dos produtos que existem para ambas as listas
inexistentes = []       # Lista onde serão atribuídos os índices dos produtos que se encontram na lista gerada, mas não foram encontrados
encontradosInesperados = []

for i in range(len(listaGerada)):
    achou = False
    for j in range(len(listaEncontrada)):
        if listaEncontrada[j][0] == listaGerada[i][0] and abs(listaEncontrada[j][1] - listaGerada[i][1]) < toleranciaX and abs(listaEncontrada[j][2] - listaGerada[i][2]) < toleranciaY and abs(listaEncontrada[j][3] - listaGerada[i][3]) < toleranciaZ:
            #print('O produto', int(listaGerada[i][0]), 'está no lugar certo')
            equivalencias.append(int(listaGerada[i][0]))
            existentes.append(int(listaGerada[i][0]))
            achou = True

    if not achou:
        for k in range(len(listaEncontrada)):
            if (listaGerada[i][0] == listaEncontrada[k][0]):
                existentes.append(int(listaGerada[i][0]))
                incongruencias.append(int(listaGerada[i][0]))
                achou = True
    
    if not achou:
        inexistentes.append(int(listaGerada[i][0]))
    
    
for i in range(len(listaEncontrada)):
    if not listaEncontrada[i][0] in listaGerada.T[:][0]:
        encontradosInesperados.append(int(listaEncontrada[i][0]))

print()
print(existentes, 'são os produtos encontrados, sendo que', equivalencias, 'estão no local esperado')
print(inexistentes, 'são os produtos não encontrados')
print(encontradosInesperados, 'são produtos que foram encontrados, mas não estavam na lista prévia')
print()

for incongruente in incongruencias:
    for i in range(len(listaEncontrada)): 
        if listaEncontrada[i][0] == incongruente:             
            indice = int(listaGerada[i][0])
    print('O produto', incongruente, 'encontra-se em ' + str(listaEncontrada[indice-1][1:]) + ', mas a lista de geração diz que deveria estar em ' + str(listaGerada[incongruente-1][1:]) + '.\n')