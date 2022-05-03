import numpy as np
import os

path = os.path.dirname(os.path.abspath(__file__)) + "/out_a_estrela.csv"
print(path)

dados = np.genfromtxt(path, delimiter=',')
print(dados)
