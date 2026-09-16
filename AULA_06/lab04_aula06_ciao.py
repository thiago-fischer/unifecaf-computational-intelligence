"""Laboratório 04: implementação independente da busca, com vizinhos pré-calculados."""
import random
import numpy as np
from lab01_aula06_ciao import BASE, CENARIOS, executar_cenarios, salvar_execucao

CUSTOS = np.array([
    [0, 2, 4, np.inf, np.inf, np.inf],
    [2, 0, 1, 5, np.inf, np.inf],
    [4, 1, 0, 2, 3, np.inf],
    [np.inf, 5, 2, 0, 1, 4],
    [np.inf, np.inf, 3, 1, 0, 2],
    [np.inf, np.inf, np.inf, 4, 2, 0],
], dtype=float)
ORIGEM, DESTINO = 0, 5


def executar_aco(semente=42, **alteracoes):
    p = BASE | alteracoes
    sorteio = random.Random(semente)
    vizinhos = {i: [j for j in range(len(CUSTOS)) if i != j and np.isfinite(CUSTOS[i, j])]
                for i in range(len(CUSTOS))}
    trilhas = np.where(np.isfinite(CUSTOS), 1.0, 0.0)
    melhor_rota, melhor_custo = None, float('inf')
    historico, diversidade, falhas = [], set(), 0
    for _ in range(p['NUM_ITERACOES']):
        solucoes = []
        for _ in range(p['NUM_FORMIGAS']):
            caminho = [ORIGEM]
            visitados = {ORIGEM}
            while caminho[-1] != DESTINO:
                atual = caminho[-1]
                opcoes = [v for v in vizinhos[atual] if v not in visitados]
                if not opcoes:
                    break
                pesos = [trilhas[atual, v] ** p['ALPHA'] * (1 / CUSTOS[atual, v]) ** p['BETA']
                         for v in opcoes]
                proximo = sorteio.choices(opcoes, weights=pesos if sum(pesos) > 0 else None)[0]
                caminho.append(proximo)
                visitados.add(proximo)
            if caminho[-1] != DESTINO:
                falhas += 1
                continue
            custo = float(sum(CUSTOS[a, b] for a, b in zip(caminho, caminho[1:])))
            solucoes.append((caminho, custo))
            diversidade.add(tuple(caminho))
            if custo < melhor_custo:
                melhor_rota, melhor_custo = caminho.copy(), custo
        trilhas *= 1 - p['TAXA_EVAPORACAO']
        for caminho, custo in solucoes:
            for a, b in zip(caminho, caminho[1:]):
                trilhas[a, b] += p['Q'] / custo
        historico.append(melhor_custo)
    return dict(parametros=p, semente=semente, melhor_rota=melhor_rota,
                melhor_custo=melhor_custo, historico=historico, feromonio=trilhas.tolist(),
                rotas_distintas=len(diversidade), rotas_incompletas=falhas)


if __name__ == '__main__':
    salvar_execucao('lab04', executar_aco())
    executar_cenarios('lab04_experimentos', executar_aco, CENARIOS + [
        ('poucas_iteracoes', {'NUM_ITERACOES': 10}),
        ('muitas_iteracoes', {'NUM_ITERACOES': 100}),
    ])
