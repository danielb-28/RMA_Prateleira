import os
import numpy as np

path_pontos = os.path.dirname(os.path.abspath(__file__)) + "/Localizacao_dos_Checkpoints.csv"
arquivo_pontos = pd.read_csv(path_pontos, delimiter=',')
print(arquivo_pontos)
