# Resultados — Aula 07

## LAB 01

### Output da execução

```text
[LAB 01 - SUCESSO] Melhor Caminho: [0, 1, 3, 4, 2, 0] | Custo: 70
```

### 1. Como o uso da busca local 2-opt afeta o equilíbrio entre Exploration e Exploitation na busca de caminhos?

A construção probabilística dos caminhos pelas formigas promove a exploração de diferentes rotas. A busca local 2-opt intensifica o refinamento de cada rota, invertendo trechos e aceitando melhorias de custo. Assim, aumenta a intensificação (Exploitation) das soluções encontradas, podendo acelerar a obtenção de caminhos melhores, mas também reduzir a diversidade quando várias rotas convergem para a mesma solução local.

### 2. O que aconteceria com a convergência do algoritmo se a taxa de evaporação (rho) fosse definida em 0.0 (sem evaporação)?

Com rho = 0.0, o feromônio não evapora e os depósitos anteriores permanecem acumulados. As primeiras rotas reforçadas podem dominar as escolhas, reduzindo a exploração de alternativas e aumentando o risco de convergência prematura para caminhos subótimos. Isso não torna a falha inevitável, mas elimina o mecanismo de esquecimento do algoritmo.

## LAB 02

### Output da execução

```text
[LAB 02] Execute e teste o seu algoritmo preenchido!
```

### 1. Explique qual é o papel do operador de Mutação em um Algoritmo Genético e o que ocorre se a taxa de mutação for configurada em 100%.

A mutação introduz variações nos genes e ajuda a manter a diversidade da população, permitindo explorar combinações que o crossover pode não produzir. Neste código, uma taxa de 100% inverte todos os bits de cada filho. Isso transforma cada cromossomo em seu complemento, podendo desfazer boas combinações e prejudicar a convergência; não equivale a gerar indivíduos aleatórios independentes.

### 2. Por que a penalização do fitness (atribuir 0 para indivíduos que estouram a capacidade) é fundamental para a convergência das restrições?

A penalização impede que indivíduos acima da capacidade sejam favorecidos apenas por terem um valor total elevado. Ao receberem fitness 0, eles perdem vantagem na seleção diante de soluções viáveis com valor positivo. Isso orienta a busca para o respeito à restrição, embora não impeça a geração de novos indivíduos inviáveis nem garanta encontrar o ótimo.

## LAB 03

### Output da execução

```text
[LAB 03] Melhor posição encontrada pelo Enxame (gbest): [ 0.00949701 -0.04096786]
```

### 1. O que acontece com o comportamento das partículas se zerarmos a componente cognitiva (c_1 = 0)?

Com c1 = 0, desaparece a atração pela melhor posição individual. As partículas passam a atualizar sua velocidade apenas pela inércia e pela influência do melhor global. Isso pode reduzir a diversidade da busca e aumentar a concentração em uma mesma região, com risco de convergência prematura.

### 2. Qual a função do parâmetro de Inércia (w) na busca por mínimos globais?

O parâmetro w controla a parcela da velocidade anterior preservada na atualização. Valores maiores tendem a favorecer deslocamentos mais amplos e a exploração; valores menores amortecem o movimento e favorecem o refinamento local. Seu equilíbrio com as componentes cognitiva e social ajuda a busca, mas não garante alcançar o mínimo global.

## LAB 04

### Output da execução

```text
[LAB 04] Matriz de Feromônio Atualizada:
 [[0.75       0.91666667 0.91666667 0.75      ]
 [0.75       0.75       0.75       1.08333333]
 [0.75       0.91666667 0.75       0.75      ]
 [0.75       0.75       0.75       0.75      ]]
```

### 1. Por que a evaporação do feromônio é necessária no algoritmo ACO?

A evaporação reduz gradualmente a influência das decisões antigas e evita a acumulação indefinida de feromônio. Isso permite que rotas alternativas ganhem relevância e ajuda a manter a exploração e a adaptação da busca.

### 2. O que ocorreria em grafos complexos sem ela? Qual a relação matemática entre a latência de um enlace e sua atratividade inicial (eta) para as formigas?

Sem evaporação, rotas reforçadas inicialmente podem dominar as escolhas em grafos complexos, mesmo sendo subótimas, causando estagnação e dificultando a adaptação. Para um enlace de latência positiva L, a atratividade inicial é inversamente proporcional à latência: eta = 1 / L. Portanto, quanto menor a latência, maior a atratividade para as formigas.

## LAB 05

### 1. Qual a diferença fundamental de conceito entre um Algoritmo Genético Puro e um Algoritmo Memético?

Um Algoritmo Genético puro evolui soluções por seleção, crossover e mutação. Um Algoritmo Memético combina essa busca evolutiva com uma busca local que refina os indivíduos, acrescentando intensificação à exploração da população.

### 2. Em termos de custo computacional, qual o impacto de executar a busca local sobre todos os indivíduos de uma população a cada geração?

Aplicar busca local a todos os indivíduos em cada geração aumenta o custo computacional, pois exige avaliações adicionais da função objetivo para cada indivíduo. Com N indivíduos e L tentativas locais, são N × L avaliações de vizinhos por geração, além da avaliação inicial de cada busca local. O refinamento pode melhorar as soluções e reduzir o número de gerações necessárias, mas não garante menor tempo total de execução.
