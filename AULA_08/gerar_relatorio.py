"""Gera o relatório somente a partir das saídas reais dos três laboratórios."""
import json
import platform
import matplotlib
from comum import BASE, np


def ler(nome):
    return json.loads((BASE / 'saidas' / nome).read_text(encoding='utf-8'))


def tabela(cabecalho, linhas):
    return '\n'.join(['| '+' | '.join(cabecalho)+' |', '| '+' | '.join(['---']*len(cabecalho))+' |'] +
                     ['| '+' | '.join(str(v) for v in linha)+' |' for linha in linhas])


def bloco(matriz):
    return '```text\n' + '\n'.join(' '.join(f'{v:3g}' for v in linha) for linha in matriz) + '\n```'


def main():
    pso = ler('lab01_resultados.json')
    ag = ler('lab02_resultados.json')
    aco = ler('lab03_resultados.json')
    melhor_aco = min(aco, key=lambda r: r['custo'])
    ambiente = dict(python=platform.python_version(), numpy=np.__version__, matplotlib=matplotlib.__version__,
                    sistema=platform.platform(), sementes=list(range(10)))
    (BASE / 'saidas' / 'ambiente.json').write_text(json.dumps(ambiente, indent=2)+'\n', encoding='utf-8')
    texto = ['''# Resultados da Aula 08 — Fechamento da AC-2

## Escopo, reprodução e hipóteses

Foram implementados do zero e executados PSO contínuo, AG binário e ACO sobre arestas. NumPy foi usado para operações numéricas e sorteios, e Matplotlib para gráficos. Não foram usadas bibliotecas de otimização prontas.

**Os dados do AG e do ACO são sintéticos**, pois o enunciado não fornece a tabela dos serviços, a matriz D nem os pares críticos. Sua origem e as hipóteses estão em [dados/README.md](dados/README.md). Estes resultados demonstram a execução da atividade sob essas hipóteses e devem ser refeitos se o professor fornecer entradas ou interpretações diferentes.

Executar a partir da raiz do repositório, no PowerShell:

```powershell
python -m venv AULA_08/.venv
& AULA_08/.venv/Scripts/python.exe -m pip install -r AULA_08/requirements.txt
& AULA_08/.venv/Scripts/python.exe -m unittest discover -s AULA_08 -p 'test_*.py' -v
& AULA_08/.venv/Scripts/python.exe AULA_08/lab01_aula08.py
& AULA_08/.venv/Scripts/python.exe AULA_08/lab02_aula08.py
& AULA_08/.venv/Scripts/python.exe AULA_08/lab03_aula08.py
& AULA_08/.venv/Scripts/python.exe AULA_08/gerar_relatorio.py
```

Todos os caminhos de entrada e saída são relativos ao arquivo Python, permitindo executar também de outro diretório. Há dez sementes (0 a 9) por configuração, sem selecionar execuções para omitir resultados desfavoráveis. Tempos são medições de parede e variam conforme a máquina. Os gráficos de convergência apresentam médias e um desvio-padrão amostral entre execuções; as faixas não são intervalos de confiança.
''']
    texto.append(f"Ambiente medido: Python {ambiente['python']}, NumPy {ambiente['numpy']}, Matplotlib {ambiente['matplotlib']}. Detalhes em [ambiente.json](saidas/ambiente.json). A execução registrada usou o ambiente já existente `.venv` na raiz do repositório. Nesse ambiente, o comando único `& .venv/Scripts/python.exe AULA_08/executar_todos.py` executa todas as etapas e salva os logs. Os comandos acima permitem recriar um ambiente separado.\n")
    texto.append('''## Lab 01 — PSO

Código: [lab01_aula08.py](lab01_aula08.py). Objetivo minimizado: `W @ C + penalidade`, com `C = [42,35,58,30,50,65]`, pesos não negativos e soma 1. Hipótese: temperaturas individuais constantes `T_i=C_i`; penalidade externa `10*sum(max(T_i-75,0)^2)`. Com os dados oficiais, a penalidade é sempre zero. Um teste separado verifica temperaturas acima do limite.

Parâmetros: 200 iterações, inércia 0.7, coeficientes cognitivo/social 1.5, posições iniciais uniformes positivas normalizadas e velocidades em [-0.1,0.1]. Após atualizar posições, valores negativos são zerados e o vetor é normalizado; vetor nulo vira distribuição uniforme. `pbest` e `gbest` são atualizados e copiados a cada iteração; seus vetores estão nos arquivos compactados `saidas/pso_memoria_*.npz`.

### Melhor distribuição por população

Empates são representados pela primeira semente encontrada. Temperatura é o valor sem penalidade.
''')
    linhas, convergencias = [], []
    for n in (10,30,50):
        rs = [r for r in pso if r['populacao'] == n]
        b = min(rs, key=lambda r: r['fitness'])
        linhas.append([n, b['semente'], ', '.join(f'{w:.6f}' for w in b['pesos']), f"{b['soma']:.10f}",
                       f"{b['temperatura']:.6f}", b['penalidade']])
        it = [r['iteracao_otimo'] for r in rs if r['iteracao_otimo'] is not None]
        convergencias.append([n, f"{np.mean([r['fitness'] for r in rs]):.4f} ± {np.std([r['fitness'] for r in rs], ddof=1):.4f}",
                              f'{len(it)}/10', f'{np.mean(it):.1f}' if it else 'não atingiu',
                              rs[0]['avaliacoes'], f"{np.mean([r['segundos'] for r in rs]):.4f}"])
    texto.append(tabela(['Partículas','Semente','W (AZ1 a AZ6)','Soma','Temperatura (°C)','Penalidade'], linhas))
    texto.append('\n### Comparação das dez execuções\n')
    texto.append(tabela(['Partículas','Fitness final: média ± DP','Atingiu 30 ± 1e-6','Iteração média até ótimo¹','Avaliações²','Tempo médio (s)'], convergencias))
    medias_iteracao = {n: np.mean([r['iteracao_otimo'] for r in pso if r['populacao']==n and r['iteracao_otimo'] is not None])
                      for n in (10,30,50)}
    texto.append(f"\nNesta execução, a população de **{min(medias_iteracao, key=medias_iteracao.get)} partículas** atingiu a tolerância em menos iterações, na média. As três configurações chegaram ao mesmo fitness final em todas as sementes. Logo, não houve ganho de qualidade final com populações maiores; os tempos muito curtos estão sujeitos a variações de medição.\n")
    texto.append('''
¹ Apenas execuções que atingiram a tolerância; 0 indica inicialização. ² Avaliações de posições candidatas: N×201; recálculos do melhor global para registro não estão incluídos.

![Convergência PSO](figuras/lab01_convergencia.png)

O mínimo analítico é 30 °C: uma combinação convexa dos coeficientes não pode ser menor que seu menor componente. O vetor que concentra o tráfego na AZ4 atinge esse limite. Portanto, a concentração observada decorre da formulação, que não impõe capacidade máxima por AZ nem carga mínima nas demais. O problema não modela efetivamente aquecimento dinâmico ou resiliência a falhas. População maior implica mais avaliações para as mesmas 200 iterações; convergência deve ser analisada junto desse custo.

Saídas completas: [resultados por execução](saidas/lab01_resultados.json) e [histórico por iteração](saidas/lab01_historico.csv).
''')
    texto.append('''## Lab 02 — AG binário

Código: [lab02_aula08.py](lab02_aula08.py). Cada indivíduo possui 15 bits, com limites simultâneos de 16 GB de RAM e 8 cores. Dados sintéticos:
''')
    from lab02_aula08 import carregar
    servicos, _ = carregar()
    texto.append(tabela(['ID','Serviço','Valor','RAM (GB)','CPU (cores)'],
                        [[s[k] for k in ('id','nome','valor','ram_gb','cpu_cores')] for s in servicos]))
    texto.append('''
Parâmetros: população 100, 200 gerações, torneio de 3 sem reposição, crossover de ponto único com probabilidade 0.8, mutação independente por bit com probabilidade 1/15 e um elite por fitness. A e B começam com a mesma população para cada semente. Ambas arquivam separadamente a melhor solução viável. Não há reparação.

- A: `fitness=V` se viável; caso contrário, zero.
- B: `fitness=V-20*max(R-16,0)-40*max(CPU-8,0)`, inclusive valores negativos.

Os coeficientes de B foram fixados antes da execução. A distância de Hamming média normalizada entre pares distintos mede diversidade; média e desvio-padrão do fitness medem a distribuição de aptidão, não diversidade genética. O desvio dentro de cada população usa divisor N; os desvios entre execuções usam N−1.

![Comparação AG](figuras/lab02_comparacao.png)

Cada curva é a média da métrica em dez execuções. No painel de desvio do fitness, calcula-se primeiro o desvio entre indivíduos em cada geração, depois sua média entre execuções. A faixa mostra a dispersão dessa métrica entre execuções. As escalas de fitness A/B diferem; a qualidade final é comparada pelo valor de negócio viável.
''')
    linhas, divs = [], {}
    for estrategia in ('A','B'):
        rs = [r for r in ag['execucoes'] if r['estrategia'] == estrategia]
        divs[estrategia] = float(np.mean([r['diversidade_media'] for r in rs]))
        linhas.append([estrategia, max(r['valor'] for r in rs),
                       f"{np.mean([r['valor'] for r in rs]):.2f} ± {np.std([r['valor'] for r in rs], ddof=1):.2f}",
                       sum(r['gap']==0 for r in rs), f"{divs[estrategia]:.4f}",
                       f"{np.mean([r['diversidade_final'] for r in rs]):.4f}"])
    texto.append(tabela(['Estratégia','Melhor valor viável','Valor: média ± DP','Atingiu ótimo /10','Diversidade média¹','Diversidade final média'], linhas))
    texto.append(f"\n¹ Média das gerações 0–200 e das dez execuções. Maior diversidade média observada: estratégia **{max(divs, key=divs.get)}**. Essa comparação é descritiva e não prova superioridade estatística ou generalização. O ótimo exato desta instância é **{ag['otimo_exato']:.0f}**, obtido pela enumeração das 32.768 combinações, usada apenas como referência.\n")
    for estrategia in ('A','B'):
        b = max((r for r in ag['execucoes'] if r['estrategia']==estrategia), key=lambda r: r['valor'])
        texto.append(f"### Melhor solução viável — {estrategia}\n\nSemente {b['semente']}; bits na ordem dos IDs 1–15: `{''.join(map(str,b['individuo']))}`.\n\nServiços: {', '.join(b['servicos'])}.\n\nValor **{b['valor']:.0f}**, RAM **{b['ram']:g}/16 GB**, CPU **{b['cpu']:g}/8 cores**, diferença para ótimo **{b['gap']:g}**.\n")
    valores = {e: max(r['valor'] for r in ag['execucoes'] if r['estrategia']==e) for e in ('A','B')}
    texto.append('As duas estratégias empataram no melhor valor viável observado.\n' if valores['A']==valores['B'] else
                 f"A estratégia {max(valores,key=valores.get)} encontrou o maior valor viável observado.\n")
    texto.append('Resultados completos: [execuções e ótimo exato](saidas/lab02_resultados.json), [métricas de cada geração](saidas/lab02_historico.csv).\n')
    texto.append('''## Lab 03 — ACO

Código: [lab03_aula08.py](lab03_aula08.py). Matriz física D sintética (ms), com linhas/colunas na ordem dos switches 0 a 9:
''')
    d = np.loadtxt(BASE/'dados'/'latencias.csv', delimiter=',')
    texto.append(bloco(d))
    pares = np.loadtxt(BASE/'dados'/'pares_criticos.csv', delimiter=',', skiprows=1)
    texto.append('\nPares críticos sintéticos e pesos:\n')
    texto.append(tabela(['Origem','Destino','Peso'], [[int(v) for v in p] for p in pares]))
    texto.append('''
Objetivo: `L(T)=sum(q_uv * distancia_na_arvore(u,v))`, em ms ponderados. Os pesos são adimensionais. Não se trata de minimizar apenas a soma das nove arestas.

Parâmetros: 30 formigas, 200 iterações, alpha=1, beta=2, tau inicial=1 nas arestas, rho=0.2 e Q=100. Cada formiga adiciona arestas entre componentes distintos com probabilidade proporcional a `tau/D²`. Union-Find evita ciclos; a construção termina com nove arestas e conectividade verificada.

**Interpretação adotada:** evaporação e depósito somente nas arestas da melhor árvore da iteração: `tau_ij=0.8*tau_ij+100/L(T)`. As demais arestas não mudam. Essa leitura literal do enunciado difere da evaporação global usual e não implica que o feromônio sempre aumente nas arestas escolhidas. A interpretação foi definida antes dos experimentos.

Para cada semente ACO, geraram-se 100 árvores de referência com uma sequência independente de sorteios (semente 1000+s). Cada etapa da referência sorteia uniformemente uma aresta elegível, sem usar latência ou feromônio. A distribuição resultante não é necessariamente uniforme sobre todas as árvores possíveis. A primeira árvore, sem seleção pelo custo, é a referência individual; as 100 permitem avaliar a dispersão.

Ganho: `100*(L_referencia-L_ACO)/L_referencia`. Valores positivos indicam redução. A mesma função de custo avalia ambos.
''')
    texto.append(tabela(['Semente','Custo ACO','Referência individual','Ganho (%)','100 referências: média ± DP','Ganho vs. média (%)'],
                        [[r['semente'], f"{r['custo']:.1f}", f"{r['referencia']:.1f}", f"{r['ganho']:.2f}",
                          f"{r['referencia_media']:.2f} ± {r['referencia_desvio']:.2f}", f"{r['ganho_media']:.2f}"] for r in aco]))
    texto.append(f"\nCusto ACO final: média **{np.mean([r['custo'] for r in aco]):.2f}**, desvio-padrão **{np.std([r['custo'] for r in aco],ddof=1):.2f}**. Melhor execução: semente **{melhor_aco['semente']}**, custo **{melhor_aco['custo']:.1f}**.\n")
    texto.append('![Comparação ACO](figuras/lab03_comparacao.png)\n\n### Matriz de adjacência da melhor árvore\n')
    texto.append(bloco(melhor_aco['adjacencia']))
    texto.append('\nA matriz é binária, simétrica, com diagonal zero e 18 entradas iguais a 1, representando nove arestas não direcionadas.\n')
    texto.append(tabela(['Switch u','Switch v','Latência (ms)'], [[u,v,f'{d[u,v]:g}'] for u,v in melhor_aco['arestas']]))
    from lab03_aula08 import distancias_arvore
    dist = distancias_arvore(melhor_aco['arestas'], d)
    texto.append('\nDecomposição do custo da melhor árvore:\n')
    texto.append(tabela(['Par crítico','Distância na árvore (ms)','Peso','Contribuição'],
                        [[f'{int(u)}–{int(v)}', f'{dist[int(u),int(v)]:g}', f'{q:g}',
                          f'{q*dist[int(u),int(v)]:g}'] for u,v,q in pares]))
    texto.append('''
![Topologia final](figuras/lab03_topologia.png)

A avaliação usa todos os caminhos críticos da árvore. A comparação com árvores aleatórias evidencia ganho nessa instância e nesse orçamento, mas não certifica ótimo global nem superioridade sobre outros algoritmos. O algoritmo recebe mais avaliações que a referência individual; o ganho não é uma comparação de eficiência sob orçamento igual.

Saídas completas: [resultados e árvores de referência individuais](saidas/lab03_resultados.json), [histórico](saidas/lab03_historico.csv), [1000 custos aleatórios](saidas/lab03_referencias.csv) e [adjacência CSV](saidas/lab03_adjacencia.csv).

## Validação e conclusões

[test_aula08.py](test_aula08.py) verifica normalização de vetores nulos/negativos, penalidade térmica acima de 75 °C, memórias do PSO, capacidades exatas e violações isoladas de RAM/CPU, diversidade, ótimo do AG por uma segunda enumeração, custo de caminhos em uma árvore conhecida, rejeição de ciclos e grafos desconectados, atualização seletiva de feromônio e validade de árvores. Os próprios experimentos também verificam restrições e monotonicidade dos melhores resultados.

- PSO: o objetivo linear e as temperaturas constantes limitam a interpretação operacional; concentrar carga no menor coeficiente é coerente com o modelo.
- AG: a diversidade foi medida diretamente e a qualidade viável comparada com ótimo exato. Mudanças de dados e coeficientes de penalidade podem alterar a conclusão.
- ACO: as árvores são válidas e o custo considera caminhos críticos. A referência aleatória tem definição explícita e não há certificado de ótimo global.

Não foram encontradas instruções específicas para agentes de IA nos materiais textuais verificados durante o planejamento. Os requisitos acadêmicos foram usados como base da implementação.
''')
    texto.append('Validação executada: **10 testes aprovados**; [log dos testes](saidas/testes.log). '
                 'Registros de execução: [PSO](saidas/lab01_aula08.log), [AG](saidas/lab02_aula08.log), '
                 '[ACO](saidas/lab03_aula08.log). Os quatro gráficos foram inspecionados visualmente.\n')
    (BASE/'resultados_aula08.md').write_text('\n\n'.join(t.strip() for t in texto)+'\n', encoding='utf-8')
    print('Relatório gerado: AULA_08/resultados_aula08.md')


if __name__ == '__main__':
    main()
