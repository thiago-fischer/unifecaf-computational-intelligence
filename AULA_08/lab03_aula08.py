"""ACO do zero: dados sintéticos e custo de caminhos entre pares críticos."""
import numpy as np

# Matriz sintética em ms: seed 808, inteiros [2,30], triângulo superior + transposta.
D = np.array([
    [0, 14, 15, 12, 11, 21, 9, 11, 10, 9],
    [14, 0, 18, 8, 7, 13, 10, 6, 3, 27],
    [15, 18, 0, 10, 24, 6, 14, 12, 22, 7],
    [12, 8, 10, 0, 15, 27, 20, 18, 10, 15],
    [11, 7, 24, 15, 0, 6, 28, 6, 4, 28],
    [21, 13, 6, 27, 6, 0, 7, 5, 25, 7],
    [9, 10, 14, 20, 28, 7, 0, 5, 20, 29],
    [11, 6, 12, 18, 6, 5, 5, 0, 28, 17],
    [10, 3, 22, 10, 4, 25, 20, 28, 0, 2],
    [9, 27, 7, 15, 28, 7, 29, 17, 2, 0],
], dtype=float)

# Pares e pesos sintéticos (origem, destino, peso adimensional).
PARES = np.array([[0, 5, 3], [1, 8, 2], [2, 9, 3], [3, 7, 2], [4, 6, 1], [0, 9, 2]], dtype=float)


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


def main():
    d, pares = D, PARES
    assert d.shape == (10, 10) and np.allclose(d, d.T)
    assert np.all(np.diag(d) == 0) and np.all(d[np.triu_indices(10, 1)] > 0)
    print("## Lab 03 — ACO\n")
    print("Matriz D sintética em ms, switches 0–9. Não foi fornecida no enunciado. "
          "Origem: default_rng(808), matriz 10×10 de inteiros entre 2 e 30; "
          "triângulo superior estrito somado à transposta.\n```text")
    print(d.astype(int))
    print("```\n\nPares críticos e pesos sintéticos (origem, destino, peso):\n```text")
    print(pares.astype(int))
    print("```\n\nCusto = soma dos caminhos únicos na árvore entre os pares críticos, "
          "ponderados pelos pesos. Unidade: ms ponderados; não é a soma das nove arestas.\n")
    print("30 formigas, 200 iterações, alpha=1, beta=2, tau inicial=1, rho=0.2, Q=100. "
          "Union-Find impede ciclos; cada árvore tem nove arestas e dez switches conectados. "
          "Arestas elegíveis são sorteadas com peso tau/D². Pela leitura literal do enunciado, "
          "evaporação e depósito são aplicados apenas às arestas da melhor árvore da iteração: "
          "tau=0.8*tau+100/custo. Demais arestas ficam inalteradas.\n")
    print("Cada referência aleatória usa semente 1000+s e sorteia arestas elegíveis sem preferência "
          "por latência. Isso não equivale à distribuição uniforme de todas as árvores possíveis. "
          "Ganho = 100*(referência-ACO)/referência.\n")
    print("| Semente | Custo ACO | Custo aleatório | Ganho (%) |")
    print("| --- | --- | --- | --- |")
    resultados = []
    for seed in range(10):
        arvore, valor, _ = executar(d, pares, seed)
        referencia = construir(d, np.ones_like(d), np.random.default_rng(1000+seed), aleatoria=True)
        aleatorio = custo(referencia, d, pares)
        ganho = 100*(aleatorio-valor)/aleatorio
        resultados.append((valor, seed, arvore, referencia))
        print(f"| {seed} | {valor:.1f} | {aleatorio:.1f} | {ganho:.2f} |")
    valor, seed, arvore, referencia = min(resultados, key=lambda r: r[0])
    adj = np.zeros((10, 10), dtype=int)
    for u, v in arvore:
        adj[u, v] = adj[v, u] = 1
    assert adj.sum() == 18 and np.array_equal(adj, adj.T)
    print(f"\nMatriz de adjacência da melhor árvore, semente {seed}, custo {valor:g}:\n\n```text")
    print(adj)
    print("```\n\nArestas da árvore ACO (u, v):\n\n```text")
    print([(int(u),int(v)) for u,v in arvore])
    print("```\n\nArestas da referência aleatória da mesma semente:\n\n```text")
    print([(int(u),int(v)) for u,v in referencia])
    print("```\n\nA matriz é simétrica, diagonal zero e tem 18 entradas iguais a 1 "
          "(nove arestas). A conectividade e a ausência de ciclos foram verificadas. "
          "O ganho vale para essa instância e referência; não certifica ótimo global. "
          "O ACO usa 6.000 árvores por execução, enquanto a referência usa uma; "
          "não é uma comparação sob igual orçamento.\n")


if __name__ == '__main__':
    main()
