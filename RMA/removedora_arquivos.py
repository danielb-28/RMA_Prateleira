# Removedora de arquivos
import shutil
import os

# Apaga as pastas dos QrCodes com exceção da primeira
pastaCopia = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'qrcode1')
for qb in range(10000):
  pastaCola = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'qrcode' + str(qb+2))
  if os.path.isdir(pastaCola):
    shutil.rmtree(pastaCola)

# Apaga todos os arquivos .csv e .pgm da pasta
for arquivo in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)))):
  if '.csv' in arquivo or '.pgm' in arquivo:
    if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), arquivo)): os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), arquivo))
    

print('\nAssim como João Carlos Tonon Campi, seus arquivos se foram...  (; ⌣_⌣)')