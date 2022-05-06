# RMA_Prateleira
Disciplina Robôs Móveis Autônomos 2021/02

Grupo:

 - Daniel Amaral Brigante - 769867
 - Otavio de Paiva Pinheiro Neto - 769664
 - Wilson Daniel Bruno

## Planejamento de Trajetória com A*
Foram feitas alterações para que o script no link abaixo fosse compatível com a estrutura do projeto, tornando-se o https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/a_star.py .

Link: 
https://github.com/danielb-28/RMA

##### Obs.: Existe uma proporção com a qual o mapa utilizado pelo A* para o cálculo da rota que modifica a escala de trabalho. Para modificá-la é necessário modificar o valor da variável porporcao no CriadoraPrateleira.py (linha 359) e no a_star.py (linha 43), ambos devem contar o mesmo valor e quando maior esse valor maior a resolução do mapa, mas aumenta o processamento do path planing.

## Criação do ambiente
O ambiente é criado pelo script https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/CriadoraPrateleira.py a medida que editas o arquivos .world, .launch e os models deste pacote, a estrutura pode ser modificada entre as linhas 382 - 399, desde o número de fileiras e blocos e a posição de início até o quantidade de prateleiras que podem ser ocupadas por produtos/caixas. A forma como as fileiras se dispõe (iniciando orientadas para dentro ou fora do bloco) no cenário pode ser modificada alterando a varável p1. A quantidade de caixas é feita com porcentagem do espaço disponível e atualmente roda com aleatoridade entre 30 e 100%, podendo ser modificada na linha 452.

Este mesmo script cria o mapa.pgm que será utilizado pelo A* como explicado anteriormente. Gera diversos arquivos csv que auxilia na obtenção dos resultados como a localização dos produtos, adiciona checkpoints no mapa por onde o drone pode saber quando se inicia e termina uma fileira para poder percorrê-las e também cria uma lista com posição e orientação que ele deve atingir para conseguir realizar a leitura dos QR Codes também criados no CriadoraPreteleiras.py.

## Resultados
A partir dos produtos encontrados pelo drone é possível realizar uma comparação com os produtos gerados utilizando-se do script https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/compara_localizacao_produtos.py , ele entregará quais produtos estão corretos (com base em tolerância predeterminada entre as linhas 5 e 7), quais não estão corretos, quais não foram encontrados no ambiente e, ainda, os que foram encontrados, mas não estavam presentes na lista inicial.

Existem os scripts https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/remove_produtos.py e https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/troca_produtos.py que geram listas que podem ser comparadas pelo anterior ou utilizadas para investigar o funcionamento do drone. Esses dois últimos funcionam chamando-os no terminal com o índice do produto que deseja remover (não sendo removido na simulação) e os ínidices dos produtos que deseja trocar de posição (sendo trocados inclusive na simulação).

## Remoção de arquivos
Para remover os arquivos csv, o mapa e os models dos QR Codes adicionais, basta executar https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/removedora_arquivos.py e esses arquivos serão apagados.
