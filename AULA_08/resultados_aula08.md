# Resultados da Aula 08 — Fechamento da AC-2

## Execução e hipóteses

Os três algoritmos foram implementados do zero. Cada arquivo contém suas entradas e imprime as tabelas e saídas abaixo, sem criar arquivos auxiliares. As comparações são apresentadas em tabelas, conforme a opção gráficos/tabelas do roteiro.

Os dados dos microsserviços, a matriz de latências e os pares críticos são **sintéticos**, pois não constam do enunciado. Foram mantidos os dados da execução anterior e incorporados diretamente aos códigos. As hipóteses térmicas e de atualização do feromônio são explicitadas em cada laboratório; os resultados dependem dessas escolhas.

Executar da raiz do repositório, com Python e NumPy instalados:

```powershell
python AULA_08/lab01_aula08.py
python AULA_08/lab02_aula08.py
python AULA_08/lab03_aula08.py
```

Nesta máquina, o interpretador usado foi `.venv/Scripts/python.exe`, do ambiente na raiz do repositório. Não é necessário ambiente virtual dentro de `AULA_08`.

Ambiente de validação: Python 3.13.13, NumPy 2.5.1.

## Lab 01 — PSO contínuo

C = [42, 35, 58, 30, 50, 65]; 200 iterações; inércia 0.7; c1=c2=1.5. Dez sementes (0–9) para cada população. Posições negativas são zeradas e normalizadas; vetor nulo recebe pesos uniformes. Históricos de pbest e gbest são mantidos em memória e retornados por PSO.executar().

Hipótese térmica: T_i=C_i, pois não foi fornecida relação entre carga e temperatura. Fitness = W@C + 10*sum(max(T_i-75,0)**2). A penalidade é externa e fica zero com os coeficientes fornecidos; para [80,77] °C, ela vale 290.

| Partículas | Melhor W (AZ1 a AZ6) | Soma | Fitness | Iteração média até 30 °C |
| --- | --- | --- | --- | --- |
| 10 | [0.0, 0.0, 0.0, 1.0, 0.0, 0.0] | 1.0000000000 | 30.0000 | 11.4 (10/10) |
| 30 | [0.0, 0.0, 0.0, 1.0, 0.0, 0.0] | 1.0000000000 | 30.0000 | 6.5 (10/10) |
| 50 | [0.0, 0.0, 0.0, 1.0, 0.0, 0.0] | 1.0000000000 | 30.0000 | 6.7 (10/10) |

Evolução do melhor fitness: média de dez execuções, em iterações selecionadas.

| Iteração | 10 partículas | 30 partículas | 50 partículas |
| --- | --- | --- | --- |
| 0 | 41.026395 | 40.212830 | 39.585159 |
| 1 | 39.244472 | 37.005537 | 36.511980 |
| 2 | 36.211745 | 33.982873 | 33.642756 |
| 5 | 32.502549 | 30.918857 | 31.053127 |
| 10 | 30.627575 | 30.000000 | 30.000000 |
| 20 | 30.000000 | 30.000000 | 30.000000 |
| 50 | 30.000000 | 30.000000 | 30.000000 |
| 100 | 30.000000 | 30.000000 | 30.000000 |
| 200 | 30.000000 | 30.000000 | 30.000000 |

O mínimo analítico é 30 °C, obtido ao concentrar a carga na AZ4. Não há capacidade máxima por AZ ou distribuição mínima no enunciado; por isso esse resultado é coerente com o objetivo linear. A penalidade não modela aquecimento dinâmico sob a hipótese adotada. As avaliações de candidatos são N×201: 2.010, 6.030 e 10.050, respectivamente.

## Lab 02 — AG binário

Tabela sintética fixa dos 15 microsserviços (não fornecida pelo professor).

| ID | Serviço | Valor | RAM (GB) | CPU (cores) |
| --- | --- | --- | --- | --- |
| 1 | autenticacao | 35 | 2 | 1 |
| 2 | gateway | 45 | 2 | 1.5 |
| 3 | cache | 28 | 4 | 0.5 |
| 4 | telemetria | 18 | 1 | 0.5 |
| 5 | antifraude | 55 | 3 | 2 |
| 6 | recomendacao | 48 | 4 | 2 |
| 7 | busca | 42 | 3 | 1.5 |
| 8 | notificacao | 20 | 1 | 0.5 |
| 9 | pagamentos | 60 | 3 | 2 |
| 10 | catalogo | 32 | 2 | 1 |
| 11 | compressao | 22 | 1 | 1.5 |
| 12 | analise_eventos | 38 | 4 | 1 |
| 13 | sessoes | 25 | 2 | 0.5 |
| 14 | auditoria | 16 | 1 | 0.5 |
| 15 | roteamento | 30 | 2 | 1 |

Limites: 16 GB e 8 cores. População 100, 200 gerações, torneio de 3 sem reposição, crossover de ponto único com probabilidade 0.8, mutação por bit de 1/15 e um elite. Melhor solução viável arquivada separadamente. Dez sementes (0–9); A e B iniciam com a mesma população para cada semente.

A: fitness=V se viável, zero se violar RAM ou CPU. B: fitness=V-20*max(RAM-16,0)-40*max(CPU-8,0). Coeficientes de penalidade escolhidos previamente; não há reparação para isolar a comparação entre as duas penalidades exigidas.

Média e desvio-padrão do fitness dentro da população em cada geração (desvio com divisor N), depois promediados entre as dez sementes. Diversidade = Hamming média normalizada entre pares distintos; não é inferida do desvio-padrão do fitness.

| Geração | Média A | DP A | Diversidade A | Média B | DP B | Diversidade B |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 66.1270 | 92.2778 | 0.4996 | 149.3220 | 69.7991 | 0.4996 |
| 1 | 103.4340 | 96.2222 | 0.4876 | 183.7260 | 45.7558 | 0.4888 |
| 2 | 122.9350 | 94.7140 | 0.4726 | 193.5890 | 43.5999 | 0.4760 |
| 5 | 133.9660 | 96.7105 | 0.4493 | 201.4530 | 44.9430 | 0.4257 |
| 10 | 140.8910 | 99.4595 | 0.4090 | 209.4310 | 41.6510 | 0.3702 |
| 20 | 139.5450 | 107.1984 | 0.3476 | 213.1200 | 42.0464 | 0.3368 |
| 40 | 152.3570 | 103.1146 | 0.3203 | 219.6560 | 39.7296 | 0.2812 |
| 60 | 150.5090 | 105.9459 | 0.3013 | 220.2990 | 39.9131 | 0.2597 |
| 80 | 151.3960 | 103.1251 | 0.3233 | 217.8720 | 41.3122 | 0.2728 |
| 100 | 155.0170 | 104.0784 | 0.3078 | 222.0710 | 36.7226 | 0.2802 |
| 120 | 155.2610 | 104.2903 | 0.2973 | 219.3620 | 41.2300 | 0.2781 |
| 140 | 150.0590 | 105.7897 | 0.3011 | 219.9490 | 40.8009 | 0.2659 |
| 160 | 149.1160 | 107.8465 | 0.2915 | 220.8770 | 41.0761 | 0.2543 |
| 180 | 154.6340 | 106.5644 | 0.2801 | 223.9920 | 38.7842 | 0.2409 |
| 200 | 145.9500 | 105.6242 | 0.3175 | 218.8130 | 39.4969 | 0.2838 |

| Estratégia | Valor final médio ± DP entre sementes | Diversidade média (gerações 0–200) |
| --- | --- | --- |
| A | 265.00 ± 0.00 | 0.3204 |
| B | 265.00 ± 0.00 | 0.2866 |

Melhor solução A, semente 0: `110100011100101` (IDs 1–15). Valor 265, RAM 15/16 GB, CPU 8/8 cores.

Serviços: autenticacao, gateway, telemetria, notificacao, pagamentos, catalogo, sessoes, roteamento.

Melhor solução B, semente 0: `110100011100101` (IDs 1–15). Valor 265, RAM 15/16 GB, CPU 8/8 cores.

Serviços: autenticacao, gateway, telemetria, notificacao, pagamentos, catalogo, sessoes, roteamento.

A estratégia A preservou maior diversidade média nesta instância.
As estratégias empataram no melhor valor viável.
As escalas de fitness diferem por causa da penalidade; a qualidade final é comparada pelo valor de negócio viável. A conclusão é descritiva, condicionada aos dados sintéticos e coeficientes adotados.

## Lab 03 — ACO

Matriz D sintética em ms, switches 0–9. Não foi fornecida no enunciado. Origem: default_rng(808), matriz 10×10 de inteiros entre 2 e 30; triângulo superior estrito somado à transposta.
```text
[[ 0 14 15 12 11 21  9 11 10  9]
 [14  0 18  8  7 13 10  6  3 27]
 [15 18  0 10 24  6 14 12 22  7]
 [12  8 10  0 15 27 20 18 10 15]
 [11  7 24 15  0  6 28  6  4 28]
 [21 13  6 27  6  0  7  5 25  7]
 [ 9 10 14 20 28  7  0  5 20 29]
 [11  6 12 18  6  5  5  0 28 17]
 [10  3 22 10  4 25 20 28  0  2]
 [ 9 27  7 15 28  7 29 17  2  0]]
```

Pares críticos e pesos sintéticos (origem, destino, peso):
```text
[[0 5 3]
 [1 8 2]
 [2 9 3]
 [3 7 2]
 [4 6 1]
 [0 9 2]]
```

Custo = soma dos caminhos únicos na árvore entre os pares críticos, ponderados pelos pesos. Unidade: ms ponderados; não é a soma das nove arestas.

30 formigas, 200 iterações, alpha=1, beta=2, tau inicial=1, rho=0.2, Q=100. Union-Find impede ciclos; cada árvore tem nove arestas e dez switches conectados. Arestas elegíveis são sorteadas com peso tau/D². Pela leitura literal do enunciado, evaporação e depósito são aplicados apenas às arestas da melhor árvore da iteração: tau=0.8*tau+100/custo. Demais arestas ficam inalteradas.

Cada referência aleatória usa semente 1000+s e sorteia arestas elegíveis sem preferência por latência. Isso não equivale à distribuição uniforme de todas as árvores possíveis. Ganho = 100*(referência-ACO)/referência.

| Semente | Custo ACO | Custo aleatório | Ganho (%) |
| --- | --- | --- | --- |
| 0 | 132.0 | 352.0 | 62.50 |
| 1 | 132.0 | 257.0 | 48.64 |
| 2 | 132.0 | 671.0 | 80.33 |
| 3 | 132.0 | 605.0 | 78.18 |
| 4 | 132.0 | 419.0 | 68.50 |
| 5 | 132.0 | 714.0 | 81.51 |
| 6 | 134.0 | 414.0 | 67.63 |
| 7 | 132.0 | 624.0 | 78.85 |
| 8 | 132.0 | 468.0 | 71.79 |
| 9 | 132.0 | 418.0 | 68.42 |

Matriz de adjacência da melhor árvore, semente 0, custo 132:

```text
[[0 0 0 0 0 0 0 0 0 1]
 [0 0 0 1 0 0 0 1 1 0]
 [0 0 0 0 0 0 0 0 0 1]
 [0 1 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 1 0 0]
 [0 0 0 0 0 0 0 0 0 1]
 [0 0 0 0 0 0 0 1 0 0]
 [0 1 0 0 1 0 1 0 0 0]
 [0 1 0 0 0 0 0 0 0 1]
 [1 0 1 0 0 1 0 0 1 0]]
```

Arestas da árvore ACO (u, v):

```text
[(8, 9), (1, 8), (4, 7), (1, 7), (5, 9), (0, 9), (2, 9), (1, 3), (6, 7)]
```

Arestas da referência aleatória da mesma semente:

```text
[(2, 9), (3, 7), (2, 6), (0, 9), (3, 5), (1, 2), (1, 8), (4, 9), (3, 8)]
```

A matriz é simétrica, diagonal zero e tem 18 entradas iguais a 1 (nove arestas). A conectividade e a ausência de ciclos foram verificadas. O ganho vale para essa instância e referência; não certifica ótimo global. O ACO usa 6.000 árvores por execução, enquanto a referência usa uma; não é uma comparação sob igual orçamento.

## Análise final

No PSO, todas as populações atingiram 30 °C nas dez sementes; 30 partículas precisaram de menos iterações em média (6,5), frente a 11,4 para 10 e 6,7 para 50. Não houve ganho na qualidade final ao aumentar a população. A concentração na AZ4 decorre da ausência de restrições de capacidade/distribuição; o modelo térmico constante deixa a penalidade inativa no cenário fornecido.

No AG, A e B encontraram a mesma combinação de valor 265, usando 15 GB e 8 cores. A estratégia A preservou mais diversidade média (0,3204 contra 0,2866), embora B tenha maior média de fitness na sua própria escala. O fitness zero dos inviáveis em A amplia a dispersão dos valores de aptidão; isso não deve ser confundido com diversidade genética.

No ACO, nove sementes chegaram a custo 132 e uma a 134. A semente 0 reduziu o custo de 352 para 132 (62,5%). A validade da árvore é garantida pela seleção de arestas entre componentes distintos e verificada ao final de cada construção. Os ganhos variam com a referência aleatória e não demonstram ótimo global.

Validação: execução integral dos três arquivos (30 execuções PSO, 20 AG e 10 ACO), com verificações internas de normalização, viabilidade, conectividade e ausência de ciclos. Não foram necessários arquivos externos de dados ou módulos auxiliares da atividade.
