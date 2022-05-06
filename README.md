# RMA_Prateleira
Disciplina Robôs Móveis Autônomos 2021/02

Grupo:

 - Daniel Amaral Brigante - 769867
 - Otavio de Paiva Pinheiro Neto - 769664

## Planejamento de Trajetória com A*
Foram feitas alterações para que o script no link abaixo fosse compatível com a estrutura do projeto, tornando-se o https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/a_star.py .

Link: 
https://github.com/danielb-28/RMA

##### Obs.: Existe uma proporção com a qual o mapa utilizado pelo A* para o cálculo da rota que modifica a escala de trabalho. Para modificá-la é necessário modificar o valor da variável porporcao no CriadoraPrateleira.py (linha 359) e no a_star.py (linha 43), ambos devem contar o mesmo valor e quando maior esse valor maior a resolução do mapa, mas aumenta o processamento do path planing.

## Criação do ambiente
O ambiente é criado pelo script https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/CriadoraPrateleira.py , a estrutura pode ser modificada entre as linhas 382 - 399, desde o número de fileiras e blocos e a posição de início até o quantidade de prateleiras que podem ser ocupadas por produtos/caixas. A forma como as fileiras se dispõe (iniciando orientadas para dentro ou fora do bloco) no cenário pode ser modificada alterando a varável p1. A quantidade de caixas é feita com porcentagem do espaço disponível e atualmente roda com aleatoridade entre 30 e 100%, podendo ser modificada na linha 452.

Este mesmo script cria o mapa.pgm que será utilizado pelo A* como explicado anteriormente. Gera diversos arquivos csv que auxilia na obtenção dos resultados como a localização dos produtos, adiciona checkpoints no mapa por onde o drone pode saber quando se inicia e termina uma fileira para poder percorrê-las e também cria uma lista com posição e orientação que ele deve atingir para conseguir realizar a leitura dos QR Codes também criados no CriadoraPreteleiras.py.


