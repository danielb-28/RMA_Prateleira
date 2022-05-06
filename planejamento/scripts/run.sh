#!/bin/bash

rostopic echo -n 1 /clock > t_inicio_total

printf "\nIniciando Leitor QR Code\n"                                                                                                                                                     
xterm -e "roslaunch leitor_qr leitor_qr.launch" &

printf "\nLista de pontos - Entrada\n"
cat pontos.csv

printf "\nRodando o TSP\n"
python3 cvDict.py

printf "\nLista de pontos - Saida\n"
cat pontos_o.csv

file="pontos_o.csv"
while IFS= read -r line
do
	rostopic echo -n 1 /clock > t_inicio
	python3 a_star.py $line
	python3 sampleMove.py
	rostopic echo -n 1 /clock > t_fim
	printf "\nTempo incial:\n"
	cat t_inicio
	printf "\nTempo final:\n"
	cat t_fim
done < "$file"

rostopic echo -n 1 /clock > t_final_total

printf "\nFim do Programa...\n"

printf "\nTempo incial total:\n"
cat t_inicio_total

printf "\nTempo final total:\n"
cat t_final_total

kill $!
