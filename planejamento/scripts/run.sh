#!/bin/bash

printf "\nLista de pontos - Entrada\n"
cat pontos.csv

printf "\nRodando o TSP\n"
python3 cvDict.py

printf "\nLista de pontos - Saida\n"
cat pontos_o.csv

file="pontos_o.csv"
while IFS= read -r line
do
	python3 a_star.py $line
	python3 sampleMove.py
done < "$file"
