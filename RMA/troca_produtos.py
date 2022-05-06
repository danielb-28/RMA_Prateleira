# Troca produtos
import os
import qrcode as qr
import sys
import numpy as np

argv = sys.argv
trocado1 = int(argv[1])
trocado2 = int(argv[2])

enderecoQR = os.path.join('meshes','materials','qr.png')

endereco1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'qrcode' + str(trocado1))
imagem1 = qr.make(str(trocado2))
imagem1.save(os.path.join(endereco1, enderecoQR))

endereco2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'qrcode' + str(trocado2))
imagem2 = qr.make(str(trocado1))
imagem2.save(os.path.join(endereco2, enderecoQR))


listaGerada = np.loadtxt(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'localizacao_produtos_gerados.csv'), delimiter = ',')

for i in range(len(listaGerada)):
    if listaGerada[i][0] == trocado1:
        aux1 = i
    if listaGerada[i][0] == trocado2:
        aux2 = i
listaGerada[aux1][0] = trocado2
listaGerada[aux2][0] = trocado1

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'localizacao_produtos_indices_trocados.csv'), 'w') as arquivoEscrita:
    for i in range(len(listaGerada)):
        arquivoEscrita.write(str(listaGerada[i][0]) + ',' + str(listaGerada[i][1]) + ',' + str(listaGerada[i][2]) + ',' + str(listaGerada[i][3]) + '\n')