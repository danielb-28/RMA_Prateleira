# Troca produtos
import os
import qrcode as qr
import sys

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

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'localizacao_produtos_indice.csv'), 'r') as arquivoLeitura:
    linhas = arquivoLeitura.readlines() #cada linha é um elemento da lista linhas

for i in range(len(linhas)):
    if linhas[i][0] == str(trocado1):
        linhas[i] = linhas[i][0].replace(str(trocado1), str(trocado2)) + linhas[i][1:]
    else:
        linhas[i] = linhas[i][0].replace(str(trocado2), str(trocado1)) + linhas[i][1:]

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'localizacao_produtos_indices_trocados.csv'), 'w') as arquivoEscrita:
    arquivoEscrita.writelines(linhas) 