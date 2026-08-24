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


# LABORATÓRIO 4

## Relatório — Atividade 4: Modelagem de um Problema Real

## Otimização de um cardápio com restrições de custo e calorias

### 1. Descrição do problema

O problema escolhido consiste em montar um cardápio para cinco dias utilizando uma base de 25 ingredientes. Cada prato deve ser composto por exatamente três ingredientes: uma proteína, um carboidrato e um vegetal.

Cada ingrediente possui um preço, uma quantidade de calorias e um tipo. No experimento, esses valores são gerados de forma aleatória dentro de faixas definidas para cada categoria. O objetivo é encontrar pratos que atendam às restrições nutricionais e financeiras e, entre as combinações válidas, selecionar as cinco de menor custo para formar o cardápio.

A meta energética definida é de 700 kcal por prato, com tolerância de 50 kcal para mais ou para menos. Portanto, cada prato válido deve possuir entre 650 e 750 kcal. Além disso, o preço total de cada prato não pode ultrapassar R$ 40,00.

Embora o comentário inicial do notebook mencione a menor quantidade de calorias, no código implementado as calorias funcionam como uma restrição. A função objetivo efetivamente utilizada é a minimização do custo dos pratos.

### 2. Modelagem formal

Uma solução candidata para um prato pode ser representada por um vetor binário de 25 posições:

`x = (x1, x2, ..., x25)`

Cada posição representa um ingrediente. Quando `xi = 1`, o ingrediente está presente no prato; quando `xi = 0`, ele não está.

Como o prato deve conter exatamente três ingredientes, uma solução candidata válida precisa satisfazer:

`Σ xi = 3`

Além disso, deve existir exatamente um ingrediente de cada categoria: proteína, carboidrato e vegetal.

Para formar o cardápio completo, a solução final é uma lista contendo cinco pratos válidos. O código permite que um mesmo ingrediente apareça em mais de um prato, desde que cada combinação de três ingredientes seja diferente.

### 3. Espaço de busca

Com 25 ingredientes representados de forma binária, existem:

`2^25 = 33.554.432`

subconjuntos possíveis.

O algoritmo exaustivo implementado percorre todas essas configurações e descarta imediatamente aquelas que não possuem exatamente três ingredientes.

Considerando somente subconjuntos com três ingredientes, existem:

`C(25, 3) = 2.300`

combinações.

Como os 25 ingredientes são distribuídos ciclicamente entre as três categorias, são geradas 9 proteínas, 8 carboidratos e 8 vegetais. Assim, antes de aplicar as restrições de calorias e preço, existem:

`9 × 8 × 8 = 576`

combinações que possuem exatamente uma proteína, um carboidrato e um vegetal.

Esse resultado mostra que a representação escolhida para a busca exaustiva percorre um espaço muito maior do que o conjunto de combinações que realmente interessam ao problema.

### 4. Função objetivo

A função objetivo é minimizar o custo total do cardápio.

Para um prato `p`, o custo é dado pela soma dos preços dos ingredientes selecionados:

`C(p) = Σ preço_i × xi`

Depois de encontrar todas as combinações válidas, o algoritmo exaustivo ordena os pratos pelo preço e seleciona os cinco mais baratos.

Assim, para o cardápio com cinco pratos, busca-se minimizar:

`C_total = C(p1) + C(p2) + C(p3) + C(p4) + C(p5)`

### 5. Restrições

Cada prato deve possuir exatamente três ingredientes, sendo uma proteína, um carboidrato e um vegetal.

A quantidade total de calorias deve permanecer dentro da faixa definida:

`650 ≤ calorias do prato ≤ 750`

O custo máximo permitido para cada prato é:

`preço do prato ≤ R$ 40,00`

Também é necessário que existam pelo menos cinco combinações válidas para que seja possível formar o cardápio completo. Caso isso não aconteça, as funções retornam `None`.

### 6. Estratégias de otimização utilizadas

Foram comparadas duas estratégias.

A primeira é a busca exaustiva. Ela percorre todas as 33.554.432 configurações binárias possíveis, filtra aquelas com três ingredientes e depois aplica as restrições de tipo, calorias e preço. Como todas as possibilidades são consideradas, a estratégia consegue identificar os pratos de menor custo dentro do espaço pesquisado.

A segunda é uma heurística. Antes de gerar as combinações, ela cria grupos de ingredientes candidatos de acordo com uma distribuição aproximada das 700 kcal: 50% para carboidratos, 40% para proteínas e 10% para vegetais. Em seguida, testa somente as combinações formadas pelos ingredientes que passaram por esse filtro.

Essa redução torna a busca muito mais rápida, porém pode eliminar ingredientes que participariam de uma boa solução quando analisados em conjunto. Por isso, a solução heurística não possui garantia de ser ótima.

### 7. Classificação do problema

Em sua forma geral, o problema pode ser considerado difícil, pois envolve uma quantidade combinatória de escolhas e múltiplas restrições simultâneas. À medida que o número de ingredientes, dias e critérios nutricionais aumenta, a quantidade de soluções possíveis pode crescer rapidamente.

Nesta versão simplificada, entretanto, cada prato possui exatamente três ingredientes. Isso reduz o conjunto relevante a 2.300 combinações de três elementos, das quais 576 já respeitam a divisão de tipos. Portanto, a instância atual é tratável computacionalmente.

O comportamento exponencial observado na implementação exaustiva ocorre principalmente porque o algoritmo percorre todos os `2^25` subconjuntos antes de filtrar os que possuem três elementos. Uma versão que gerasse diretamente as combinações de uma proteína, um carboidrato e um vegetal reduziria bastante esse custo.

Assim, a versão generalizada do planejamento de cardápios se aproxima de problemas combinatórios difíceis, enquanto a instância específica utilizada no laboratório ainda pode ser resolvida exatamente em tempo viável.

### 8. Conclusão

O experimento permitiu observar na prática a diferença entre uma solução exata e uma solução heurística. A busca exaustiva apresentou maior custo computacional, mas encontrou um cardápio mais barato. A heurística reduziu drasticamente o número de combinações analisadas e o tempo de execução, porém encontrou uma solução de custo maior.

O principal aprendizado é que algoritmos de otimização frequentemente envolvem um compromisso entre qualidade da solução e tempo de processamento. A busca exata pode ser adequada para espaços pequenos, enquanto heurísticas se tornam úteis quando o crescimento do espaço de busca torna a exploração completa inviável.
