# Origem dos dados e hipóteses

O enunciado `../roteiro_aula08.txt` fornece apenas os coeficientes do PSO, as capacidades do AG e o número de switches do ACO. As entradas abaixo são **sintéticas**, criadas para esta implementação; não foram fornecidas pelo professor.

- `microsservicos.csv`: 15 serviços fictícios com valores de negócio, RAM e CPU fixos, escolhidos manualmente. Limites oficiais: 16 GB e 8 cores.
- `latencias.csv`: grafo completo não direcionado de dez switches, numerados de 0 a 9, em milissegundos. Gerado com `np.random.default_rng(808).integers(2, 31, size=(10,10))`; conserva-se apenas o triângulo superior estrito, somado à transposta. Diagonal zero. O arquivo é a fonte fixa usada nos experimentos.
- `pares_criticos.csv`: seis pares e pesos adimensionais escolhidos manualmente. O objetivo soma o comprimento do caminho único na árvore, ponderado por esses pesos; não soma apenas as nove arestas.

PSO: `T_i = C_i` constantes; objetivo `W @ C + 10*sum(max(T_i-75,0)**2)`. A penalidade é implementada, mas fica inativa com os coeficientes oficiais. Um caso sintético acima de 75 °C é verificado separadamente pelos testes. Não se assume uma dinâmica térmica não especificada.

AG: penalidade proporcional de 20 pontos por GB excedido e 40 pontos por core excedido, escolhida previamente à execução. São escolhas de modelagem, não parâmetros fornecidos pelo professor. Um elite por fitness; melhor indivíduo viável arquivado separadamente. Não há reparação, para isolar o efeito das penalidades.

ACO: adota-se a leitura literal de evaporação **e** depósito somente nas arestas da melhor árvore de cada iteração: `tau = 0.8*tau + 100/custo`. As demais arestas ficam inalteradas. Isso difere da evaporação global usual; a escolha atende à redação “aplicada apenas às melhores topologias”. Inicialização em 1, alpha=1, beta=2. A referência aleatória sorteia uniformemente uma aresta entre as elegíveis em cada etapa; isso não implica amostragem uniforme entre todas as árvores possíveis.

As conclusões são condicionadas a essas hipóteses. Se forem fornecidos dados oficiais ou outra interpretação do modelo, substituir as entradas/regras e executar novamente.
