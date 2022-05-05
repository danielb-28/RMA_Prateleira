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
	rosservice call /uav1/control_manager/goto_altitude "goal: 0.6" 
	rosrun scan_prateleira scan_prateleira_node
	printf "\nTempo incial:\n"
        cat t_inicio
    	printf "\nTempo final:\n"
	cat t_final
done < "$file"
