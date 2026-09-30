# Roteiro de execução — Aula 08

Objetivo: concluir a AC-2 com três laboratórios de otimização e documentar resultados reproduzíveis. Este arquivo é um plano de trabalho; não contém resultados de experimentos executados.

Fonte principal: `roteiro_aula08.txt`, nesta pasta. O planejamento de AC-3/AC-4 trata de entregas futuras, e o gabarito AAI serve como material de revisão.

## 1. Conferência das orientações

Não foram encontradas instruções específicas para agentes de IA no enunciado da aula 08, no texto extraído dos dois PDFs da pasta ou nos arquivos de orientação pesquisados no repositório. Também não foi encontrado `AGENTS.md` na hierarquia de diretórios até a raiz. As instruções acadêmicas do enunciado foram mantidas como requisitos da atividade.

## 2. Preparar os arquivos e resolver as lacunas

Entregas obrigatórias dentro de `AULA_08/`:

- `lab01_aula08.py` ou `.ipynb`.
- `lab02_aula08.py` ou `.ipynb`.
- `lab03_aula08.py` ou `.ipynb`.
- `resultados_aula08.md`, com análises técnicas, tabelas/gráficos e saídas reais dos programas.

Sugestão de organização: criar também `dados/` para entradas e `figuras/` para gráficos. Implementar os algoritmos do zero; usar NumPy para operações numéricas e Matplotlib para gráficos é uma escolha prática, sem substituir os algoritmos por otimizadores prontos.

Antes dos experimentos finais, esclarecer:

| Laboratório | Lacuna do enunciado | Ação |
|---|---|---|
| PSO | Não há equação ligando carga à temperatura de cada AZ | Confirmar o modelo térmico. Se adotar interpretação própria, identificá-la como hipótese |
| AG | Não foram fornecidos valores de negócio, RAM e CPU dos 15 serviços | Solicitar a tabela; para desenvolver, usar dados sintéticos fixos e explicitamente identificados |
| ACO | Não foram fornecidos a matriz D, os pares críticos nem seus pesos | Solicitar os dados; manter qualquer instância sintética claramente separada dos dados oficiais |
| ACO | A redação não deixa claro se a restrição às melhores topologias vale para a evaporação ou para o depósito | Confirmar a regra ou registrar explicitamente a interpretação implementada |

É possível desenvolver as estruturas dos algoritmos enquanto esses dados são esclarecidos. Não apresentar dados assumidos como se tivessem sido fornecidos pelo professor.

## 3. Lab 01 — PSO contínuo

### Modelagem

Representar cada partícula por seis pesos não negativos, cuja soma seja 1. Usar os coeficientes oficiais:

```text
C = [42, 35, 58, 30, 50, 65]
```

A interpretação direta da temperatura média ponderada é `T_media(W) = sum(w_i * C_i)`, a ser minimizada.

**Limitação do modelo:** nessa interpretação, o mínimo teórico é 30 °C, com `W = [0, 0, 0, 1, 0, 0]`. Sem restrições adicionais de capacidade ou distribuição mínima, o objetivo favorece concentrar todo o tráfego na quarta AZ. Isso decorre da formulação, não necessariamente de uma falha do PSO.

O enunciado não define `T_i(W)` para avaliar a temperatura individual das AZs. Se `T_i = C_i`, nenhuma supera 75 °C e a penalidade fica inativa. Não inventar silenciosamente uma relação carga/temperatura para corrigir isso.

### Implementação e execução

1. Criar funções para normalizar pesos, calcular temperatura, calcular penalidade e avaliar fitness.
2. Normalizar após cada atualização: zerar componentes negativas e dividir pela soma; se a soma for zero, usar pesos uniformes `1/6`.
3. Implementar velocidade e posição: `v = omega*v + c1*r1*(pbest-x) + c2*r2*(gbest-x)` e `x = normalizar(x+v)`.
4. Atualizar e armazenar `pbest` e `gbest`, copiando os vetores para evitar alterações acidentais das melhores soluções.
5. Após definir o modelo térmico, usar uma penalidade externa, por exemplo `lambda * sum(max(0, T_i(W)-75)**2)`, somada ao objetivo. Documentar `lambda` e as unidades/modelo.
6. Executar obrigatoriamente com **10, 30 e 50 partículas**, mantendo os demais parâmetros iguais.
7. Exportar curvas de melhor fitness por iteração e uma tabela com os seis pesos, sua soma, temperatura e penalidade de cada configuração.

Sugestão inicial, ajustável: 200 iterações, `omega=0.7`, `c1=c2=1.5`. Esses valores não são exigidos pelo enunciado. Com igual número de iterações, populações maiores usam mais avaliações; registrar esse custo ao comparar.

### Verificações e análise

- Pesos finitos e não negativos; soma igual a 1 dentro de tolerância numérica, por exemplo `1e-8`.
- Melhor fitness global não aumenta ao longo das iterações, pois o problema é de minimização.
- Verificar a penalidade com um caso controlado acima de 75 °C, separado do experimento oficial.
- Se usar o objetivo linear direto, comparar com o mínimo analítico de 30 °C e explicar a concentração na quarta AZ.
- Responder: qual população convergiu mais rápido? Houve ganho final? Qual foi o custo computacional?

## 4. Lab 02 — AG binário

### Modelagem

Cada indivíduo possui 15 bits. Calcular `V = sum(x_i*valor_i)`, `R = sum(x_i*ram_i)` e `P = sum(x_i*cpu_i)`. Uma solução é viável quando `R <= 16` e `P <= 8`.

Implementar as duas avaliações obrigatórias:

- **A — penalidade rígida:** fitness igual a `V` para soluções viáveis e zero para as demais.
- **B — penalidade proporcional:** uma escolha documentável é `fitness = V - lambda_ram*max(0,R-16) - lambda_cpu*max(0,P-8)`. Definir os coeficientes antes da comparação e explicar sua escala.

Manter um registro separado da melhor solução **viável**. Um bom fitness penalizado não garante que os limites sejam respeitados. Apesar de o título citar reparação, os requisitos detalhados pedem a comparação entre duas penalidades; tratar reparação como extensão opcional, sem alterar a comparação principal.

### Implementação e execução

1. Cadastrar e exibir a tabela dos 15 serviços com identificador, valor, RAM e CPU.
2. Implementar inicialização binária, seleção por torneio, crossover de ponto único e mutação por inversão de bits.
3. Usar os mesmos parâmetros, dados e populações iniciais para comparar A e B.
4. A cada geração, registrar média e desvio-padrão do fitness **entre os indivíduos**, melhor valor viável, proporção de soluções viáveis e diversidade genética.
5. Medir diversidade diretamente, por exemplo pela distância de Hamming média entre pares de indivíduos dividida por 15. Desvio-padrão do fitness, sozinho, não mede diversidade genética.
6. Gerar gráficos de média e desvio-padrão do fitness e de diversidade ao longo das gerações.
7. Exibir, para cada estratégia, os serviços da melhor solução viável, seu valor total, RAM e CPU.

Sugestão inicial, ajustável: população de 100, 200 gerações, torneio de 3, crossover de 0.8 e mutação por bit de `1/15`. Se usar elitismo, aplicar igualmente nas duas estratégias e registrá-lo.

### Verificações e análise

- Indivíduos sempre possuem 15 posições com valores 0 ou 1.
- Testar avaliações em casos viáveis, no limite e acima de cada limite.
- Validar os totais da solução final independentemente do fitness.
- Comparar qualidade final pelo **valor de negócio das soluções viáveis**, já que as estratégias usam escalas de penalização diferentes.
- Responder com os gráficos: qual estratégia preservou melhor a diversidade? Qual encontrou maior valor viável? A diferença foi consistente entre execuções?
- Verificação opcional: enumerar as `2^15 = 32768` combinações para obter o ótimo exato dessa instância e medir a diferença do AG. Essa referência não substitui o AG exigido.

## 5. Lab 03 — ACO para árvore de rede

### Modelagem

Preparar a matriz `D` de dimensão 10×10. Para uma rede não direcionada, validar simetria, diagonal zero e latências positivas nas arestas existentes. Representar arestas ausentes separadamente, sem confundi-las com enlaces de latência zero.

Definir o custo antes de implementar. A expressão “latência total acumulada entre os pares mais críticos” sugere somar a latência dos caminhos na árvore para os pares críticos:

```text
L(T) = soma, sobre os pares críticos (u,v), de q_uv * distancia_na_arvore(T,u,v)
```

Os pares e os pesos `q_uv` precisam ser fornecidos ou assumidos explicitamente. Minimizar apenas a soma das latências das nove arestas é outro objetivo, o de árvore geradora mínima; só adotar essa simplificação se confirmada ou claramente declarada.

### Implementação e execução

1. Inicializar feromônios positivos nas arestas permitidas.
2. Para cada formiga, construir uma árvore adicionando arestas que conectem componentes distintos. Usar Union-Find ou uma busca no grafo para impedir ciclos.
3. Sortear entre as arestas elegíveis com probabilidade proporcional a `tau_ij**alpha * (1/D_ij)**beta`. Tratar soma nula de probabilidades e ausência de candidatos.
4. Encerrar a construção com exatamente nove arestas e todos os dez nós conectados.
5. Calcular o custo usando a função escolhida, incluindo os caminhos entre pares quando essa for a modelagem.
6. Atualizar feromônios com **rho = 0.2** e selecionar explicitamente quais são as melhores topologias da iteração, por exemplo a melhor formiga.
7. Registrar a interpretação da atualização: uma opção usual é evaporar todas as arestas e depositar apenas nas melhores árvores. A redação do enunciado pode também ser lida como evaporação restrita às melhores topologias; não tratar a primeira opção como requisito inequívoco.
8. Construir uma árvore aleatória válida sobre a mesma matriz, usando arestas elegíveis sorteadas sem preferência por latência, e calcular o mesmo custo.
9. Imprimir a matriz de adjacência binária final 10×10 e a lista de arestas. A matriz de latências pode ser apresentada adicionalmente.
10. Calcular `ganho_percentual = 100 * (L_aleatoria - L_ACO) / L_aleatoria`, com custo de referência positivo. Manter um resultado negativo se o ACO tiver desempenho pior.

Sugestão inicial, ajustável: 30 formigas, 200 iterações, `alpha=1`, `beta=2`. Documentar a intensidade do depósito, por exemplo `Q/L(T)`, e atualizar simetricamente os feromônios de arestas não direcionadas.

### Verificações e análise

- Árvore final com dez nós, nove arestas, conectada e sem ciclos.
- Adjacência simétrica, diagonal zero e exatamente 18 entradas iguais a 1.
- Nenhuma aresta inexistente utilizada; custo recalculado pela mesma função para ACO e referência aleatória.
- Relatar custos, ganho percentual e a influência da aleatoriedade da referência.
- Recomendação adicional: comparar com várias árvores aleatórias e informar média e dispersão, evitando depender de uma única referência desfavorável.

## 6. Protocolo de experimentos

Para os três laboratórios, registrar dados, parâmetros, sementes, critério de parada e versões das bibliotecas. Como recomendação, executar cada configuração com dez sementes fixas, por exemplo de 0 a 9. Essa repetição é uma sugestão de qualidade experimental, não uma exigência explícita da aula 08.

Separar as estatísticas: no AG, o requisito de média/desvio-padrão ao longo das gerações se refere à população; a dispersão entre execuções é uma análise adicional. Não misturar as duas sem identificar o que cada curva representa.

Executar os programas integralmente. Se usar notebooks, reiniciar o kernel e executar todas as células na ordem. Só preencher tabelas de resultados depois da execução real.

## 7. Montar `resultados_aula08.md`

Usar esta sequência:

1. **Objetivo e ambiente:** ferramentas e instruções para reproduzir.
2. **Dados e hipóteses:** origem das entradas e resolução das lacunas.
3. **Lab 01:** formulação, parâmetros, curvas, tabela dos pesos e discussão da penalidade/ótimo.
4. **Lab 02:** tabela dos serviços, avaliações A/B, curvas de média/desvio-padrão, diversidade e melhores soluções viáveis.
5. **Lab 03:** matriz D, função de custo, regra de feromônio, adjacência final, custos e ganho percentual.
6. **Conclusões:** o que os resultados sustentam, limitações e possíveis melhorias.

Incluir links relativos para as figuras e saídas suficientes para comprovar cada requisito. Evitar conclusões antecipadas, como afirmar que população maior ou penalidade proporcional sempre será melhor.

## 8. Revisar e entregar

- [ ] Os três algoritmos foram implementados do zero e executados integralmente.
- [ ] PSO: populações 10/30/50, curvas de fitness, pesos, soma validada e penalidade externa.
- [ ] AG: estratégias A/B, operadores exigidos, média/desvio-padrão, diversidade e solução final viável.
- [ ] ACO: árvore válida, rho=0.2, melhores topologias, adjacência 10×10 e ganho sobre referência aleatória.
- [ ] Dados ausentes e hipóteses estão identificados.
- [ ] Relatório contém resultados reais, figuras legíveis e comandos de reprodução.
- [ ] Revisão de `git status` e do conteúdo a incluir; commit dos artefatos da atividade e push para o repositório.

O commit/push integra a entrega final pedida no enunciado e deve ocorrer após implementar e revisar os laboratórios. A criação deste roteiro não conclui a atividade.
