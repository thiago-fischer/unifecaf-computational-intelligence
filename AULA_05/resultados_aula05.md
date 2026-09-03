# Resultados — Aula 05: PSO

## Entregáveis

- Notebook: `aula05_pso.ipynb`
- Implementação reproduzível: `solucao_aula05.py`
- Este relatório: `resultados_aula05.md`

As execuções usam sementes fixas. Na Missão 3, o fitness foi implementado como custo positivo e minimizado. Isso corrige a inconsistência do código-base, que retornava `-custo` mas usava `min` para escolher o melhor resultado.

## Missão 1 — A partícula solitária

- Função: `f(x) = x²`
- Posição inicial: `x = 6,100058`
- Fitness inicial: `37,210713`
- Melhor posição após 20 iterações: `x = 3,239543`
- Melhor fitness: `10,494642`
- Encontrou o mínimo global `x = 0`? **Não**, usando o critério `f(x) <= 10⁻⁴`.
- Dificuldade: **Médio**.

Observação: com uma única partícula, `pBest` e `gBest` começam iguais à posição atual. Assim, os termos cognitivo e social são inicialmente nulos, e a partícula não recebe uma atração em direção ao mínimo.

## Missão 2 — O enxame

- Função: Rosenbrock.
- Mínimo global esperado: `(1, 1)`, com fitness `0`.
- Melhor posição: `(1,130272, 1,278378)`.
- Melhor fitness: `0,017045`, na iteração `45`.
- Encontrou exatamente o mínimo pelo critério `f <= 10⁻²`? **Não**.
- O resultado ficou próximo do mínimo global? **Sim**.
- Foi mais eficiente que a partícula solitária? **Sim**, pois o enxame colaborou e alcançou uma solução muito mais próxima do ótimo.
- Dificuldade: **Médio**.

## Missão 3 — Problema corporativo/logístico

- Clientes: `50`.
- Centros de distribuição: `5`.
- Custo inicial: `4611,84`.
- Custo final: `3233,68`.
- Melhoria: `29,88%`.
- Centros encontrados:

| Centro | Coordenada `(x, y)` |
|---|---:|
| 1 | `(1,3082, 4,4986)` |
| 2 | `(2,2546, 6,7216)` |
| 3 | `(7,5569, 7,7285)` |
| 4 | `(4,4345, 2,2698)` |
| 5 | `(7,6503, 2,6497)` |

- O custo melhorou? **Sim**.
- Quantos centros foram alocados? **5**.
- Dificuldade: **Difícil**.

## Missão 4 — Otimização de parâmetros

Cada configuração foi executada cinco vezes. Menor custo médio é melhor.

| Configuração | Custo médio | Melhor | Pior | Desvio-padrão |
|---|---:|---:|---:|---:|
| Padrão | 3367,20 | 3269,36 | 3464,72 | 82,08 |
| Inércia Alta (`w=0,9`) | 3645,00 | 3532,41 | 3809,79 | 92,87 |
| Inércia Baixa (`w=0,5`) | 3349,66 | 3233,46 | 3567,22 | 125,69 |
| Cognitivo Alto (`c1=2,5`) | 3482,60 | 3398,63 | 3538,34 | 46,61 |
| Social Alto (`c2=2,5`) | 3646,57 | 3411,28 | 3850,84 | 150,30 |
| Mais Partículas (`60`) | **3322,06** | 3257,98 | 3375,81 | 46,59 |

- Melhor configuração: `w=0,7`, `c1=1,8`, `c2=1,8`, `60` partículas.
- Pior configuração: `w=0,7`, `c1=1,8`, `c2=2,5`, `30` partículas.
- Inércia: `w=0,5` apresentou custo médio ligeiramente melhor que o padrão; `w=0,9` piorou a convergência.
- Componente cognitivo: aumentar `c1` piorou o custo médio nesta amostra.
- Componente social: aumentar `c2` foi a pior alteração, sugerindo maior risco de convergência prematura ou instabilidade.
- Número de partículas: aumentar de `30` para `60` produziu o melhor custo médio e menor dispersão entre as execuções.
- Recomendação: usar `w=0,7`, `c1=1,8`, `c2=1,8` e `60` partículas, pois foi a melhor configuração média observada.
- Dificuldade: **Difícil**.

## Relatório final — respostas conceituais

1. **O que é PSO?**

   PSO é um algoritmo de otimização inspirado no comportamento coletivo de grupos de animais. Cada partícula representa uma solução candidata e se movimenta pelo espaço de busca atualizando sua velocidade com base na inércia, na melhor posição pessoal e na melhor posição do grupo.

2. **Diferença entre `pBest` e `gBest`:**

   `pBest` é a melhor solução já encontrada por uma partícula específica. `gBest` é a melhor solução encontrada por qualquer partícula do enxame. O `pBest` preserva a experiência individual, enquanto o `gBest` permite a cooperação do grupo.

3. **Dificuldades gerais:**

   A Missão 1 exige atenção à fórmula e à limitação de uma única partícula. A Missão 2 acrescenta estruturas para várias partículas. A Missão 3 é a mais trabalhosa por envolver dez variáveis, clientes, demandas e distâncias. A Missão 4 exige várias execuções e interpretação estatística dos resultados.
