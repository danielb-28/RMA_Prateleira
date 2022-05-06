# RMA_Prateleira
Disciplina Robôs Móveis Autônomos 2021/02

Grupo:

 - Daniel Amaral Brigante - 769867
 - Otavio de Paiva Pinheiro Neto - 769664
 - 

## Criação do ambiente
O ambiente é criado pelo script https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/criadora_prateleira.py a medida que editas o arquivos .world, .launch e os models deste pacote, a estrutura pode ser modificada entre as linhas 382 - 399, desde o número de fileiras e blocos e a posição de início até o quantidade de prateleiras que podem ser ocupadas por produtos/caixas. A forma como as fileiras se dispõe (iniciando orientadas para dentro ou fora do bloco) no cenário pode ser modificada alterando a varável p1. A quantidade de caixas é feita com porcentagem do espaço disponível e atualmente roda com aleatoridade entre 30 e 100%, podendo ser modificada na linha 452.

#### arquivos criados pelo criadora_prateleira.py
 - mapa.pgm -> Mapa utilizado pelo A* para o planejamento do rota (path planing).
 - QrCodes -> Dentro da pasta models são criados os arquivos para que se insira diferentes QRCodes no ambiente para posteior leitura pelo UAV.
 - localizacao_checkpoints.csv -> Lista de localizações e orientações no mapa por onde o UAV entende quando se inicia e termina uma fileira para poder percorrê-las.
 - localizacao_produtos_gerados.csv -> Lista das localizações e códigos dos produtos no mapa.
 - localização_produtos.csv -> Lista das localizações dos produtos no mapa.
 - pontos.csv -> Lista de localizações e orientações que o UAV deve atingir para ser capaz de ler os QrCodes.

## Resultados
A partir dos produtos encontrados pelo UAV é possível realizar uma comparação com os produtos gerados utilizando-se do script https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/compara_localizacao_produtos.py , ele entregará quais produtos estão corretos (com base em tolerância predeterminada entre as linhas 5 e 7), quais não estão corretos, quais não foram encontrados no ambiente e, ainda, os que foram encontrados, mas não estavam presentes na lista inicial.

Existem os scripts https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/remove_produtos.py e https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/troca_produtos.py que geram listas que podem ser comparadas pelo anterior ou utilizadas para investigar o funcionamento do UAV. Esses dois últimos funcionam chamando-os no terminal com o índice do produto que deseja remover (não sendo removido na simulação) e os ínidices dos produtos que deseja trocar de posição (sendo trocados inclusive na simulação). Nesse mesmo âmbito, foi criado o https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/seleciona_produtos.py , que faz o oposto do remove_produtos.py, esse script seleciona os produtos com base nos índices adicionados no vetor manter (linha 4).

#### arquivos criados por remove_produtos.py , seleciona_produtos.py e troca_produtos.py
 - pontos_percorrer_indices.csv -> Lista das localizações e códigos dos produtos a conferir no mapa.
 - pontos_percorrer.csv -> Lista das localizações dos produtos a conferir no mapa.
 - localizacao_produtos_indices_trocados.csv

## Remoção de arquivos
Para remover os arquivos csv, o mapa e os models de QR Codes adicionais, basta executar https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/removedora_arquivos.py e esses arquivos serão apagados.

## TSP - Caixeiro Viajante
Daniel é bobão

## Planejamento de Trajetória com A*
Foram feitas alterações para que o script no link abaixo fosse compatível com a estrutura do projeto, tornando-se o https://github.com/danielb-28/RMA_Prateleira/blob/main/RMA/a_star.py .

Link: 
https://github.com/danielb-28/RMA

###### Obs.: Existe uma proporção com a qual o mapa utilizado pelo A* para o cálculo da rota que modifica a escala de trabalho. Para modificá-la é necessário modificar o valor da variável porporcao no CriadoraPrateleira.py (linha 359) e no a_star.py (linha 43), ambos devem conter o mesmo valor e quando maior esse valor a resolução do mapa, mais aumenta o processamento do path planing.

## Guia de instalação
Este guia presume que o usuário possua uma distribuição linux Ubuntu 20.04 com os pacotes básicos do ROS já instalados no sistema, além do Gazebo, Catkin, Python etc. Bem como a workspace já compilada.
Instruções de como instalar todos esses ambientes encontram-se em: https://github.com/vivaldini/RMA .

Ainda assim são necessárias a instalação das dependências Python a seguir:
```bash
pip3 install numpy matplotlib qrcode
```

A montagem dos pacotes deve ser feita como se segue:
```bash
cd ~/workspace/src
git clone https://github.com/danielb-28/RMA_Prateleira.git
cd RMA_Prateleira
mv planejamento ..
mv leitor_qr ..
mv RMA ..
mv README.md ..
cd ..
rm -rf RMA_Prateleira/
```

É necessária a instalação da biblioteca de leitura do QrCode:
```bash
cd ~/workspace/src/leitor_qr/libquirc
sudo bash install.sh
```

Para finalizar basta compilar a workspace:
```bash
cd ~/workspace
catkin clean && catkin_make
```

## Rodando a Simulação
Para utilização da simulação proposta, inicialmente é necessária a execução do script gerar_ambiente.sh . Ele irá executar e movimentar os arquivos necessários para a realização da simulação criando novo ambiente.
```bash
cd ~/workspace/src/RMA
bash criar_ambiente.sh
cd /home/otavio/workspace/src/planejamento/scripts
bash ./run.sh
```

Para realizar a simulação no ambiente no mesmo ambiente da simulação anterior, execute em outro terminal:
```bash
bash ~/workspace/src/RMA/src/start/start.sh
cd /home/otavio/workspace/src/planejamento/scripts
bash ./run.sh
```

Para iniciar o leitor de QrCodes:
```bash
cd /home/otavio/workspace/src/planejamento/scripts
bash ./run.sh
```
