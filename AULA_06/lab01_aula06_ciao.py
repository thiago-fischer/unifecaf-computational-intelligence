"""Laboratório 01: ACO parametrizável, com depósito no sentido percorrido."""
import random

import numpy as np

import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

PASTA = Path(__file__).resolve().parent
BASE = dict(NUM_FORMIGAS=20, NUM_ITERACOES=50, ALPHA=1.0, BETA=2.0,
            TAXA_EVAPORACAO=0.5, Q=100)
CENARIOS = [
    ('referencia', {}), ('alpha_baixo', {'ALPHA': 0.1}), ('alpha_alto', {'ALPHA': 5.0}),
    ('beta_baixo', {'BETA': 0.5}), ('beta_alto', {'BETA': 5.0}),
    ('evaporacao_baixa', {'TAXA_EVAPORACAO': 0.1}),
    ('evaporacao_alta', {'TAXA_EVAPORACAO': 0.9}),
    ('poucas_formigas', {'NUM_FORMIGAS': 5}), ('muitas_formigas', {'NUM_FORMIGAS': 50}),
]


def salvar_execucao(nome, resultado):
    (PASTA / 'figuras').mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(range(1, len(resultado['historico']) + 1), resultado['historico'])
    ax.set(xlabel='Iteração', ylabel='Melhor custo acumulado', title=f'Convergência — {nome}')
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(PASTA / 'figuras' / f'{nome}_convergencia.png', dpi=140)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(resultado['feromonio'], cmap='hot', vmin=0)
    ax.set(xlabel='Nó de destino', ylabel='Nó de origem', title=f'Feromônio final — {nome}')
    fig.colorbar(im, ax=ax, label='Quantidade de feromônio')
    fig.tight_layout()
    fig.savefig(PASTA / 'figuras' / f'{nome}_feromonio.png', dpi=140)
    plt.close(fig)
    print(json.dumps(resultado, ensure_ascii=False, indent=2, allow_nan=False))


def executar_cenarios(nome, executar, cenarios):
    resultados = []
    for titulo, alteracoes in cenarios:
        referencia = executar(semente=42, **alteracoes)
        repeticoes = [executar(semente=s, **alteracoes) for s in range(10)]
        resultados.append(dict(cenario=titulo, execucao=referencia, repeticoes=repeticoes))
    (PASTA / 'figuras').mkdir(exist_ok=True)
    linhas = (len(resultados) + 2) // 3
    for tipo in ('convergencia', 'feromonio'):
        fig, axs = plt.subplots(linhas, 3, figsize=(15, 3.8 * linhas), layout='constrained')
        limite = max(np.max(r['execucao']['feromonio']) for r in resultados)
        for ax, r in zip(axs.flat, resultados):
            e = r['execucao']
            ax.set_title(r['cenario'].replace('_', ' '))
            if tipo == 'convergencia':
                ax.plot(range(1, len(e['historico']) + 1), e['historico'])
                ax.set(xlabel='Iteração', ylabel='Melhor custo')
                ax.set_ylim(7.5, max(8.5, max(max(v['execucao']['historico']) for v in resultados) + .5))
                ax.grid(alpha=.3)
            else:
                im = ax.imshow(e['feromonio'], cmap='hot', vmin=0, vmax=limite)
                ax.set(xlabel='Destino', ylabel='Origem')
        for ax in list(axs.flat)[len(resultados):]:
            ax.set_visible(False)
        if tipo == 'feromonio':
            fig.colorbar(im, ax=list(axs.flat), label='Feromônio (escala comum)', shrink=.8)
        fig.suptitle(f'{nome} — semente 42')
        fig.savefig(PASTA / 'figuras' / f'{nome}_{tipo}.png', dpi=120)
        plt.close(fig)
    for r in resultados:
        e = r['execucao']
        print(r['cenario'], e['parametros'], 'semente:', e['semente'],
              'rota:', e['melhor_rota'], 'custo:', e['melhor_custo'])
    return resultados

CUSTOS = np.array([
    [0, 2, 4, np.inf, np.inf, np.inf],
    [2, 0, 1, 5, np.inf, np.inf],
    [4, 1, 0, 2, 3, np.inf],
    [np.inf, 5, 2, 0, 1, 4],
    [np.inf, np.inf, 3, 1, 0, 2],
    [np.inf, np.inf, np.inf, 4, 2, 0],
], dtype=float)
ORIGEM, DESTINO = 0, 5


def obter_vizinhos(no):
    return [j for j in range(len(CUSTOS)) if j != no and np.isfinite(CUSTOS[no, j])]


def calcular_custo(rota):
    return float(sum(CUSTOS[a, b] for a, b in zip(rota, rota[1:])))


def escolher_proximo(no_atual, visitados, feromonio, rng, alpha, beta):
    candidatos = [no for no in obter_vizinhos(no_atual) if no not in visitados]
    if not candidatos:
        return None
    atratividades = [feromonio[no_atual, no] ** alpha * (1 / CUSTOS[no_atual, no]) ** beta
                    for no in candidatos]
    soma = sum(atratividades)
    probabilidades = [x / soma for x in atratividades] if soma > 0 else None
    return rng.choices(candidatos, weights=probabilidades, k=1)[0]


def construir_rota(feromonio, rng, alpha, beta):
    rota = [ORIGEM]
    while rota[-1] != DESTINO:
        proximo = escolher_proximo(rota[-1], rota, feromonio, rng, alpha, beta)
        if proximo is None:
            return None
        rota.append(proximo)
    return rota


def evaporar_feromonio(feromonio, taxa):
    feromonio *= 1 - taxa
    feromonio[~np.isfinite(CUSTOS)] = 0


def depositar_feromonio(feromonio, rota, custo, q):
    for origem, destino in zip(rota, rota[1:]):
        feromonio[origem, destino] += q / custo


def executar_aco(semente=42, **alteracoes):
    parametros = BASE | alteracoes
    rng = random.Random(semente)
    feromonio = np.ones_like(CUSTOS)
    feromonio[~np.isfinite(CUSTOS)] = 0
    melhor_rota, melhor_custo = None, float('inf')
    historico, diversidade, falhas = [], set(), 0
    for _ in range(parametros['NUM_ITERACOES']):
        rotas = []
        for _ in range(parametros['NUM_FORMIGAS']):
            rota = construir_rota(feromonio, rng, parametros['ALPHA'], parametros['BETA'])
            if rota is None:
                falhas += 1
                continue
            custo = calcular_custo(rota)
            diversidade.add(tuple(rota))
            rotas.append((rota, custo))
            if custo < melhor_custo:
                melhor_rota, melhor_custo = rota.copy(), custo
        evaporar_feromonio(feromonio, parametros['TAXA_EVAPORACAO'])
        for rota, custo in rotas:
            depositar_feromonio(feromonio, rota, custo, parametros['Q'])
        historico.append(melhor_custo)
    return dict(parametros=parametros, semente=semente, melhor_rota=melhor_rota,
                melhor_custo=melhor_custo, historico=historico, feromonio=feromonio.tolist(),
                rotas_distintas=len(diversidade), rotas_incompletas=falhas)


def main():
    inicial = np.ones_like(CUSTOS)
    inicial[~np.isfinite(CUSTOS)] = 0
    rng = random.Random(42)
    demonstracoes = [construir_rota(inicial, rng, 1.0, 2.0) for _ in range(5)]
    resultado = executar_aco()
    resultado['matriz_inicial'] = inicial.tolist()
    resultado['vizinhos'] = {'0': obter_vizinhos(0), '2': obter_vizinhos(2)}
    resultado['rotas_demonstrativas'] = [dict(rota=r, custo=calcular_custo(r) if r else None)
                                        for r in demonstracoes]
    salvar_execucao('lab01', resultado)


if __name__ == '__main__':
    main()
