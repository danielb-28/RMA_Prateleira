# Removedora de arquivos
import shutil
import os


if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'localizacao_checkpoints.csv')): os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'localizacao_checkpoints.csv'))
if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'localizacao_produtos.csv')): os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'localizacao_produtos.csv'))
if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mapa.pgm')): os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mapa.pgm'))
if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trajetoria.csv')): os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trajetoria.csv'))

pastaCopia = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'qrcode1')
for qb in range(10000):
  pastaCola = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'qrcode' + str(qb+2))
  if os.path.isdir(pastaCola):
    shutil.rmtree(pastaCola)    
print('\nAssim como João Carlos Tonon Campi, seus arquivos se foram...  (; ⌣_⌣)')