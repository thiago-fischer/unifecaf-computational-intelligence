"""Laboratório 03: preenchimento dos quatro desafios do enunciado."""
import random
import numpy as np
from lab01_aula06_ciao import BASE, salvar_execucao

CUSTOS = np.array([
    [0, 2, 4, np.inf, np.inf, np.inf],
    [2, 0, 1, 5, np.inf, np.inf],
    [4, 1, 0, 2, 3, np.inf],
    [np.inf, 5, 2, 0, 1, 4],
    [np.inf, np.inf, 3, 1, 0, 2],
    [np.inf, np.inf, np.inf, 4, 2, 0],
], dtype=float)
ORIGEM, DESTINO = 0, 5
NUM_FORMIGAS, NUM_ITERACOES = 20, 50
ALPHA, BETA, TAXA_EVAPORACAO, Q = 1.0, 2.0, 0.5, 100
feromonio = np.ones_like(CUSTOS)
feromonio[~np.isfinite(CUSTOS)] = 0


def obter_vizinhos(no):
    return [j for j in range(len(CUSTOS)) if j != no and np.isfinite(CUSTOS[no, j])]


def calcular_atratividade(no_atual, proximo):
    fer = feromonio[no_atual][proximo]
    custo = CUSTOS[no_atual][proximo]
    atratividade = fer ** ALPHA * (1 / custo) ** BETA
    return atratividade


def evaporar_feromonio():
    global feromonio
    feromonio *= (1 - TAXA_EVAPORACAO)
    feromonio[CUSTOS == np.inf] = 0


def depositar_feromonio(rota, custo):
    deposito = Q / custo
    for i in range(len(rota) - 1):
        origem, destino = rota[i], rota[i + 1]
        feromonio[origem][destino] += deposito


def construir_rota():
    rota = [ORIGEM]
    atual = ORIGEM
    while atual != DESTINO:
        vizinhos = obter_vizinhos(atual)
        candidatos = [no for no in vizinhos if no not in rota]
        if not candidatos:
            return None
        atratividades = [calcular_atratividade(atual, no) for no in candidatos]
        soma = sum(atratividades)
        probabilidades = [valor / soma for valor in atratividades] if soma > 0 else None
        proximo = random.choices(candidatos, weights=probabilidades, k=1)[0]
        rota.append(proximo)
        atual = proximo
    return rota


def calcular_custo(rota):
    return float(sum(CUSTOS[a, b] for a, b in zip(rota, rota[1:])))


def executar_aco(semente=42):
    global feromonio
    random.seed(semente)
    feromonio = np.ones_like(CUSTOS)
    feromonio[~np.isfinite(CUSTOS)] = 0
    melhor_rota, melhor_custo = None, float('inf')
    historico, diversidade, falhas = [], set(), 0
    for _ in range(NUM_ITERACOES):
        rotas = []
        for _ in range(NUM_FORMIGAS):
            rota = construir_rota()
            if rota is None:
                falhas += 1
                continue
            custo = calcular_custo(rota)
            rotas.append((rota, custo))
            diversidade.add(tuple(rota))
            if custo < melhor_custo:
                melhor_rota, melhor_custo = rota.copy(), custo
        evaporar_feromonio()
        for rota, custo in rotas:
            depositar_feromonio(rota, custo)
        historico.append(melhor_custo)
    return dict(parametros=BASE.copy(), semente=semente, melhor_rota=melhor_rota,
                melhor_custo=melhor_custo, historico=historico, feromonio=feromonio.tolist(),
                rotas_distintas=len(diversidade), rotas_incompletas=falhas)


if __name__ == '__main__':
    salvar_execucao('lab03', executar_aco())
