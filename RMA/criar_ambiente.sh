python3 criadora_prateleira.py
cp pontos.csv localizacao_produtos_gerados.csv
python3 seleciona_produtos.py 5
cp pontos.csv localizacao_produtos_selecionados.csv
sed -i '1 i 0, 3, 3, 3, 0' pontos.csv 
cp pontos.csv ../planejamento/scripts/
cp mapa.pgm ../planejamento/scripts/
