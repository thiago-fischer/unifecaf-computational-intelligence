# LABORATÓRIO 1

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
### Porque o exercício se trata de uma análise combinatória, onde cada objeto que possa ser levado gera duas possibilidades (levar ou não levar), sendo assim, gera-se o resultado da quantidade de possibilidades elevado a quantidade de objetos
# 2. O que aconteceria se eu colocasse 15 itens?
### A quantidade de possibilidades iria aumentar drásticamente e o script ficaria mais demorado para executar a iteração em todas elas. Por ainda ser uma quantidade razoavelmente "baixa" ainda seria possível descobrir a solução ideal através de um algoritmo de força-bruta, mas conforme a quantidade aumenta o ideal seria buscarmos por uma solução heurística.
# 3.Voces conseguem imaginar um problema da vida real que seja parecido com este?
### Sim, um exemplo seria classificar o melhor restaurante com base em alguns critérios (distância, local para estacionar, qualidade da comida, preço). Nesse caso também se trata de uma análise combinatória e a solução seria semelhante.

# LABORATÓRIO 2

# OUTPUT

### =================================================================
### RESULTADOS DA FORCA-BRUTA NO TSP
### =================================================================

>>> 4 cidades
    Rotas avaliadas : 6
    Melhor custo    : 80
    Melhor rota     : (0, 1, 3, 2, 0)
    Tempo (segundos): 0.000051

>>> 5 cidades
    Rotas avaliadas : 24
    Melhor custo    : 41
    Melhor rota     : (0, 1, 2, 3, 4, 0)
    Tempo (segundos): 0.000045

>>> 6 cidades
    Rotas avaliadas : 120
    Melhor custo    : 91
    Melhor rota     : (0, 1, 3, 4, 5, 2, 0)
    Tempo (segundos): 0.000232

>>> 10 cidades
    Rotas avaliadas : 362880
    Melhor custo    : 83
    Melhor rota     : (0, 1, 2, 3, 4, 6, 7, 8, 5, 9, 0)
    Tempo (segundos): 0.284104

>>> 11 cidades
    Rotas avaliadas : 3628800
    Melhor custo    : 78
    Melhor rota     : (0, 4, 10, 9, 3, 5, 6, 2, 1, 7, 8, 0)
    Tempo (segundos): 3.044275

### =================================================================
### OBSERVE: o numero de rotas cresce como (n-1)!  (fatorial)
### 4 cidades -> 6 rotas | 5 -> 24 | 6 -> 120 | 10 -> 362880 | 15 -> 87 bilhoes
### =================================================================

# REFLEXÃO FINAL
# Tabela que as duplas/trio devem preencher
| Número de cidades | Rotas avaliadas | Tempo (s) | Melhor custo |
|---:|---:|---:|---:|
| 4 | 6 | 0.001530 | 80 |
| 5 | 24 | 0.000053 | 41 |
| 6 | 120 | 0.000318 | 91 |
| 10 | 362880 | 0.317649 | 62 |
| 11 | 3628800 | 3.038361 | 77 |

# Perguntas de reflexao (obrigatorias)
# 16.	O numero de rotas cresce de forma linear, quadratica ou muito mais rapido? Explique com as quantidades que voce coletou.
### Cresce muito mais rápido, criei uma função para gerar valores aleatórios de acordo com a quantidade informada no parametro. Quando aumentei para 10 cidades obtive mais de 360 mil rotas, para 11 cidades obtive mais de 3 milhões de rotas.
# 17.	Com base no padrao observado, estime (mesmo que de forma grosseira) quanto tempo levaria para 10 cidades no mesmo computador.
> 10 cidades
    Rotas avaliadas : 362880
    Melhor custo    : 62
    Melhor rota     : (0, 2, 5, 6, 4, 7, 3, 8, 1, 9, 0)
    Tempo (segundos): 0.317649
# 18.	Por que dizemos que o TSP e um problema “dificil”? A resposta nao e “porque e complicado de entender”, e sim por causa do crescimento do tempo.
### TSP é considerado um problema difícil porque conforme a entrada aumenta, as opções geradas cresce de forma quase descontrolada, no caso de rotas possíveis as opções crescem de forma fatorial a entrada. Para um algoritmo de força-bruta, se a entrada for alta, o script pode percorrer por bilhões de possíbilidades e "congelar" por nunca conseguir terminar o processo.

# LABORATÓRIO 3

# OUTPUT

> Rodando 20 instancias...
### Instancia  1 | Otimo:  199 | Gulosa:  199 | Gap:   0.0%
### Instancia  2 | Otimo:  170 | Gulosa:  170 | Gap:   0.0%
### Instancia  3 | Otimo:  155 | Gulosa:  155 | Gap:   0.0%
### Instancia  4 | Otimo:  147 | Gulosa:  147 | Gap:   0.0%
### Instancia  5 | Otimo:  261 | Gulosa:  261 | Gap:   0.0%
### Instancia  6 | Otimo:  214 | Gulosa:  214 | Gap:   0.0%
### Instancia  7 | Otimo:  191 | Gulosa:  187 | Gap:   2.1%
### Instancia  8 | Otimo:  183 | Gulosa:  183 | Gap:   0.0%
### Instancia  9 | Otimo:  215 | Gulosa:  206 | Gap:   4.2%
### Instancia 10 | Otimo:  174 | Gulosa:  174 | Gap:   0.0%
### Instancia 11 | Otimo:  262 | Gulosa:  262 | Gap:   0.0%
### Instancia 12 | Otimo:  206 | Gulosa:  206 | Gap:   0.0%
### Instancia 13 | Otimo:  231 | Gulosa:  231 | Gap:   0.0%
### Instancia 14 | Otimo:  309 | Gulosa:  309 | Gap:   0.0%
### Instancia 15 | Otimo:  294 | Gulosa:  294 | Gap:   0.0%
### Instancia 16 | Otimo:  247 | Gulosa:  247 | Gap:   0.0%
### Instancia 17 | Otimo:  136 | Gulosa:  134 | Gap:   1.5%
### Instancia 18 | Otimo:  212 | Gulosa:  212 | Gap:   0.0%
### Instancia 19 | Otimo:  243 | Gulosa:  243 | Gap:   0.0%
### Instancia 20 | Otimo:  193 | Gulosa:  193 | Gap:   0.0%

> ===== RESUMO =====
Gap medio     : 0.39%
Gap minimo    : 0.00%
Gap maximo    : 4.19%
Desvio padrao : 1.03%

# O que entregar / discutir:
# 19.	Codigo completo (com a funcao calcular_gap implementada e o loop funcionando).
### Feito no arquivo .ipynb
# 20.	Valor do gap medio obtido.
### Gap medio     : 0.39%
# 21.	Resposta: “A heuristica gulosa e boa o suficiente para este problema? Em quais situacoes voce usaria ela e em quais preferiria gastar mais tempo para achar o otimo?”
### Sim, a heuristica chegou no mesmo resultado do valor otimo varias vezes nos teste feitos. Usaria a heuristica quando a situaão tivesse varias opções de escolha, pois ela iria calcular o melhor valor em um tempo menor. Utilizaria força-bruta quando as opções de escolha fosse menores, pois ela traria a melhor opção dentro das disponiveis.