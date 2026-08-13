# OUTPUT

Total de solucoes avaliadas: 32
Tempo de execucao: 0.001014 segundos
Melhor valor encontrado: 9
Combinacao otima (0=nao leva, 1=leva): (1, 1, 0, 1, 1)

Itens escolhidos:
 - Livro (peso: 2 , valor: 3 )
 - Fone (peso: 1 , valor: 2 )
 - Carregador (peso: 1 , valor: 3 )
 - Chocolate (peso: 1 , valor: 1 )

# PERGUNTAS:
# 1. Por que o total de solucoes avaliadas e exatamente 32?
### Porque o exercício se trata de uma análise combinatória, onde cada objeto que possa ser levado gera duas possibilidades (levar ou não levar), sendo assim o resultado de (quantidade de possibilidades elevado a quantidade de objetos)
# 2. O que aconteceria se eu colocasse 15 itens?
### A quantidade de possibilidades iria aumentar drásticamente e o script ficaria mais demorado para executar a iteração em todas elas. Por ainda ser uma quantidade razoavelmente "baixa" ainda seria possível descobrir a solução ideal através de um algoritmo de força-bruta, mas conforme a quantidade aumenta o ideal seria buscarmos por uma solução heurística.
# 3.Voces conseguem imaginar um problema da vida real que seja parecido com este?
### Sim, um exemplo seria classificar o melhor restaurante com base em alguns critérios (distância, local para estacionar, qualidade da comida, preço). Nesse caso também se trata de uma análise combinatória e a solução seria semelhante.


# REFLEXÃO FINAL
# Tabela que as duplas/trio devem preencher
| Número de cidades | Rotas avaliadas | Tempo (s) | Melhor custo |
|---:|---:|---:|---:|
| 4 | 6 | 0.000040 | 80 |
| 5 | 24 | 0.000032 | 41 |
| 6 | 120 | 0.000140 | 91 |
| 10 | 362880 | 0.217983 | 29 |
| 11 | 3628800 | 2.217849 | 50 |

# Perguntas de reflexao (obrigatorias)
# 16.	O numero de rotas cresce de forma linear, quadratica ou muito mais rapido? Explique com as quantidades que voce coletou.
### Cresce muito mais rápido, criei uma função para gerar valores aleatórios de acordo com a quantidade informada no parametro. Quando aumentei para 10 cidades obtive mais de 360 mil rotas, para 11 cidades obtive mais de 3 milhões de rotas.
# 17.	Com base no padrao observado, estime (mesmo que de forma grosseira) quanto tempo levaria para 10 cidades no mesmo computador.
>>> 10 cidades
    Rotas avaliadas : 362880
    Melhor custo    : 29
    Melhor rota     : (0, 9, 8, 7, 2, 6, 5, 1, 4, 3, 0)
    Tempo (segundos): 0.217983
# 18.	Por que dizemos que o TSP e um problema “dificil”? A resposta nao e “porque e complicado de entender”, e sim por causa do crescimento do tempo.