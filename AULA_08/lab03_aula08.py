"""ACO do zero sobre arestas, com custo dos caminhos entre pares críticos."""
from time import perf_counter
from comum import np, plt, preparar, salvar_csv, salvar_json, salvar_figura, BASE, SEMENTES


def carregar():
    d = np.loadtxt(BASE / 'dados' / 'latencias.csv', delimiter=',')
    pares = np.loadtxt(BASE / 'dados' / 'pares_criticos.csv', delimiter=',', skiprows=1)
    assert d.shape == (10, 10) and np.allclose(d, d.T)
    assert np.all(np.diag(d) == 0) and np.all(d[np.triu_indices(10, 1)] > 0)
    return d, pares


class UnionFind:
    def __init__(self, n):
        self.pai = list(range(n))

    def raiz(self, u):
        while u != self.pai[u]:
            self.pai[u] = self.pai[self.pai[u]]
            u = self.pai[u]
        return u

    def unir(self, u, v):
        a, b = self.raiz(u), self.raiz(v)
        if a == b:
            return False
        self.pai[b] = a
        return True


def validar_arvore(arestas, d):
    n = len(d)
    assert len(arestas) == n-1
    uf = UnionFind(n)
    for u, v in arestas:
        assert 0 <= u < n and 0 <= v < n and u != v
        assert np.isfinite(d[u, v]) and d[u, v] > 0
        assert uf.unir(u, v), 'Ciclo ou aresta duplicada'
    assert len({uf.raiz(u) for u in range(n)}) == 1


def construir(d, tau, rng, aleatoria=False):
    n = len(d)
    uf = UnionFind(n)
    candidatas = [(u, v) for u in range(n) for v in range(u+1, n)
                  if np.isfinite(d[u, v]) and d[u, v] > 0]
    arvore = []
    while len(arvore) < n-1:
        elegiveis = [(u, v) for u, v in candidatas if uf.raiz(u) != uf.raiz(v)]
        if not elegiveis:
            raise ValueError('Grafo desconectado: não existe árvore geradora')
        pesos = np.ones(len(elegiveis)) if aleatoria else np.array(
            [tau[u, v] / d[u, v]**2 for u, v in elegiveis])
        total = pesos.sum()
        probs = pesos/total if total > 0 else np.full(len(pesos), 1/len(pesos))
        u, v = elegiveis[rng.choice(len(elegiveis), p=probs)]
        uf.unir(u, v)
        arvore.append((u, v))
    validar_arvore(arvore, d)
    return arvore


def distancias_arvore(arestas, d):
    n = len(d)
    vizinhos = [[] for _ in range(n)]
    for u, v in arestas:
        vizinhos[u].append((v, d[u, v]))
        vizinhos[v].append((u, d[u, v]))
    dist = np.full((n, n), np.inf)
    for origem in range(n):
        dist[origem, origem] = 0
        pilha = [(origem, -1)]
        while pilha:
            u, pai = pilha.pop()
            for v, peso in vizinhos[u]:
                if v != pai:
                    dist[origem, v] = dist[origem, u] + peso
                    pilha.append((v, u))
    return dist


def custo(arestas, d, pares):
    dist = distancias_arvore(arestas, d)
    return float(sum(peso * dist[int(u), int(v)] for u, v, peso in pares))


def atualizar(tau, melhor, valor, rho=.2, q=100.):
    # Interpretação literal: evaporação E depósito só na melhor árvore da iteração.
    for u, v in melhor:
        tau[u, v] = (1-rho)*tau[u, v] + q/valor
        tau[v, u] = tau[u, v]


def executar(d, pares, seed, formigas=30, iteracoes=200):
    rng = np.random.default_rng(seed)
    tau = np.ones_like(d)
    np.fill_diagonal(tau, 0)
    melhor, valor = None, float('inf')
    historico = []
    for _ in range(iteracoes):
        arvores = [construir(d, tau, rng) for _ in range(formigas)]
        custos = [custo(a, d, pares) for a in arvores]
        i = int(np.argmin(custos))
        if custos[i] < valor:
            melhor, valor = arvores[i].copy(), custos[i]
        atualizar(tau, arvores[i], custos[i])
        historico.append(valor)
    assert np.all(np.diff(historico) <= 0)
    return melhor, valor, historico


def desenhar_topologia(melhor, d):
    """Layout em níveis da árvore, para evitar cruzamentos e rótulos sobrepostos."""
    vizinhos = [[] for _ in range(len(d))]
    for u, v in melhor['arestas']:
        vizinhos[u].append(v)
        vizinhos[v].append(u)
    pos, folhas = {}, [0]

    def posicionar(u, pai, nivel):
        filhos = sorted(v for v in vizinhos[u] if v != pai)
        for v in filhos:
            posicionar(v, u, nivel+1)
        if filhos:
            x = float(np.mean([pos[v][0] for v in filhos]))
        else:
            x = folhas[0]
            folhas[0] += 1
        pos[u] = np.array([x, -nivel], dtype=float)

    posicionar(9, -1, 0)
    plt.figure(figsize=(9, 6))
    for u, v in melhor['arestas']:
        linha = np.array([pos[u], pos[v]])
        plt.plot(linha[:, 0], linha[:, 1], color='#56788a', lw=2)
        meio = (pos[u]+pos[v])/2
        plt.text(*meio, f'{d[u,v]:g} ms', fontsize=9, ha='center',
                 bbox=dict(facecolor='white', alpha=.95, edgecolor='none'))
    pontos = np.array([pos[i] for i in range(len(d))])
    plt.scatter(pontos[:, 0], pontos[:, 1], s=650, color='#183d56', zorder=3)
    for i in range(len(d)):
        plt.text(*pos[i], str(i), color='white', ha='center', va='center', zorder=4)
    plt.title(f"Melhor árvore ACO — custo {melhor['custo']:.1f} ms ponderados")
    plt.xlim(pontos[:, 0].min()-.5, pontos[:, 0].max()+.5)
    plt.ylim(pontos[:, 1].min()-.5, .5)
    plt.axis('off')
    salvar_figura('lab03_topologia.png')


def main():
    preparar()
    d, pares = carregar()
    resumo, linhas, curvas, baselines = [], [], [], []
    for seed in SEMENTES:
        inicio = perf_counter()
        arvore, valor, h = executar(d, pares, seed)
        tempo = perf_counter()-inicio
        rng = np.random.default_rng(1000+seed)
        referencias = [construir(d, np.ones_like(d), rng, aleatoria=True) for _ in range(100)]
        custos = [custo(a, d, pares) for a in referencias]
        baselines.extend(dict(semente=seed, referencia=i, custo=c) for i, c in enumerate(custos))
        adj = np.zeros_like(d, dtype=int)
        for u, v in arvore:
            adj[u, v] = adj[v, u] = 1
        assert adj.sum() == 18 and np.array_equal(adj, adj.T)
        resumo.append(dict(semente=seed, arestas=arvore, adjacencia=adj.tolist(), custo=valor,
                           referencia_arestas=referencias[0], referencia=custos[0],
                           referencia_media=float(np.mean(custos)),
                           referencia_desvio=float(np.std(custos, ddof=1)),
                           ganho=100*(custos[0]-valor)/custos[0],
                           ganho_media=100*(np.mean(custos)-valor)/np.mean(custos), segundos=tempo))
        curvas.append(h)
        linhas.extend(dict(semente=seed, iteracao=i+1, custo=c) for i, c in enumerate(h))
    curvas = np.array(curvas)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), layout='constrained')
    media, sd = curvas.mean(axis=0), curvas.std(axis=0, ddof=1)
    axes[0].plot(range(1, 201), media, label='ACO: média de 10 execuções')
    axes[0].fill_between(range(1, 201), media-sd, media+sd, alpha=.2, label='±1 desvio-padrão')
    axes[0].set(xlabel='Iteração', ylabel='Custo dos pares críticos (ms ponderados)', title='Convergência do ACO')
    axes[0].legend()
    axes[1].boxplot([[r['custo'] for r in resumo], [b['custo'] for b in baselines]],
                    tick_labels=['ACO (10)', 'Árvores aleatórias (1000)'])
    axes[1].set(ylabel='Custo dos pares críticos (ms ponderados)', title='Distribuição dos custos finais')
    salvar_figura('lab03_comparacao.png')
    melhor = min(resumo, key=lambda x: x['custo'])
    desenhar_topologia(melhor, d)
    salvar_json('lab03_resultados.json', resumo)
    salvar_csv('lab03_historico.csv', linhas)
    salvar_csv('lab03_referencias.csv', baselines)
    np.savetxt(BASE / 'saidas' / 'lab03_adjacencia.csv', melhor['adjacencia'], fmt='%d', delimiter=',')
    print('ACO: 10 execuções. Melhor custo:', melhor['custo'])
    print('Matriz de adjacência final (switches 0 a 9):')
    print(np.array(melhor['adjacencia']))


if __name__ == '__main__':
    main()
