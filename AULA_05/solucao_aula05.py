"""Solução reproduzível das quatro missões da Aula 05: PSO.

Os resultados usam sementes fixas para permitir a conferência no notebook e
no relatório. Na parte logística, o fitness é o custo positivo e o algoritmo
minimiza esse valor; isso mantém a função objetivo coerente com o enunciado.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


def missao_1(seed: int = 5) -> dict:
    """PSO de uma partícula para f(x) = x²."""
    rng = np.random.default_rng(seed)
    limite = 10.0
    iteracoes = 20
    w, c1, c2 = 0.8, 1.5, 1.5

    posicao = float(rng.uniform(-limite, limite))
    velocidade = float(rng.uniform(-1, 1))
    fitness = posicao**2
    pbest_pos, pbest_fit = posicao, fitness
    gbest_pos, gbest_fit = posicao, fitness
    historico_pos = [posicao]
    historico_fit = [fitness]
    historico_pbest = [pbest_fit]

    for _ in range(iteracoes):
        r1, r2 = rng.random(), rng.random()
        velocidade_nova = (
            w * velocidade
            + c1 * r1 * (pbest_pos - posicao)
            + c2 * r2 * (gbest_pos - posicao)
        )
        posicao_nova = float(np.clip(posicao + velocidade_nova, -limite, limite))
        fitness_novo = posicao_nova**2

        posicao, velocidade, fitness = posicao_nova, velocidade_nova, fitness_novo
        if fitness < pbest_fit:
            pbest_fit, pbest_pos = fitness, posicao
        if fitness < gbest_fit:
            gbest_fit, gbest_pos = fitness, posicao

        historico_pos.append(posicao)
        historico_fit.append(fitness)
        historico_pbest.append(pbest_fit)

    return {
        "seed": seed,
        "posicao_inicial": historico_pos[0],
        "fitness_inicial": historico_fit[0],
        "posicao_final": posicao,
        "fitness_final": fitness,
        "pbest_pos": pbest_pos,
        "pbest_fit": pbest_fit,
        "gbest_pos": gbest_pos,
        "gbest_fit": gbest_fit,
        "melhor_iteracao": int(np.argmin(historico_pbest)),
        "encontrou_minimo": bool(pbest_fit <= 1e-4),
        "historico_pos": historico_pos,
        "historico_fit": historico_fit,
        "historico_pbest": historico_pbest,
    }


def rosenbrock(posicao: np.ndarray) -> float:
    x, y = posicao
    return float((1 - x) ** 2 + 100 * (y - x**2) ** 2)


@dataclass
class Particula:
    posicao: np.ndarray
    velocidade: np.ndarray
    fitness: float
    pbest_pos: np.ndarray
    pbest_fit: float


def criar_particula_rosenbrock(rng: np.random.Generator) -> Particula:
    posicao = rng.uniform([-2, -1], [2, 3])
    velocidade = rng.uniform(-0.5, 0.5, 2)
    fit = rosenbrock(posicao)
    return Particula(posicao, velocidade, fit, posicao.copy(), fit)


def missao_2(seed: int = 12) -> dict:
    """PSO com 20 partículas para a função de Rosenbrock."""
    rng = np.random.default_rng(seed)
    num_particulas, iteracoes = 20, 50
    w, c1, c2 = 0.7, 1.8, 1.8
    enxame = [criar_particula_rosenbrock(rng) for _ in range(num_particulas)]
    melhor = min(enxame, key=lambda p: p.fitness)
    gbest_pos, gbest_fit = melhor.posicao.copy(), melhor.fitness
    historico_melhor = [gbest_fit]
    historico_media = [float(np.mean([p.fitness for p in enxame]))]

    for _ in range(iteracoes):
        for p in enxame:
            r1, r2 = rng.random(2), rng.random(2)
            p.velocidade = (
                w * p.velocidade
                + c1 * r1 * (p.pbest_pos - p.posicao)
                + c2 * r2 * (gbest_pos - p.posicao)
            )
            p.posicao = np.clip(p.posicao + p.velocidade, [-2, -1], [2, 3])
            p.fitness = rosenbrock(p.posicao)
            if p.fitness < p.pbest_fit:
                p.pbest_fit, p.pbest_pos = p.fitness, p.posicao.copy()
            if p.fitness < gbest_fit:
                gbest_fit, gbest_pos = p.fitness, p.posicao.copy()
        historico_melhor.append(gbest_fit)
        historico_media.append(float(np.mean([p.fitness for p in enxame])))

    return {
        "seed": seed,
        "gbest_pos": gbest_pos,
        "gbest_fit": gbest_fit,
        "encontrou_minimo": bool(gbest_fit <= 1e-2),
        "melhor_iteracao": int(np.argmin(historico_melhor)),
        "historico_melhor": historico_melhor,
        "historico_media": historico_media,
    }


def gerar_dados_logistica(seed: int = 42, limite: float = 10.0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    clientes = rng.random((50, 2)) * limite
    demandas = rng.integers(1, 100, 50)
    return clientes, demandas


def custo_logistico(
    posicoes_centros: np.ndarray,
    clientes: np.ndarray,
    demandas: np.ndarray,
    num_centros: int = 5,
) -> float:
    centros = posicoes_centros.reshape(num_centros, 2)
    distancias = np.linalg.norm(clientes[:, None, :] - centros[None, :, :], axis=2)
    menor_distancia = np.min(distancias, axis=1)
    return float(np.sum(menor_distancia * demandas))


def criar_particula_logistica(
    rng: np.random.Generator,
    clientes: np.ndarray,
    demandas: np.ndarray,
    limite: float = 10.0,
    num_centros: int = 5,
) -> Particula:
    dim = 2 * num_centros
    posicao = rng.uniform(0, limite, dim)
    velocidade = rng.uniform(-0.5, 0.5, dim)
    fit = custo_logistico(posicao, clientes, demandas, num_centros)
    return Particula(posicao, velocidade, fit, posicao.copy(), fit)


def executar_logistica(
    rng: np.random.Generator,
    clientes: np.ndarray,
    demandas: np.ndarray,
    num_particulas: int = 30,
    iteracoes: int = 100,
    w: float = 0.7,
    c1: float = 1.8,
    c2: float = 1.8,
    limite: float = 10.0,
    num_centros: int = 5,
) -> dict:
    enxame = [
        criar_particula_logistica(rng, clientes, demandas, limite, num_centros)
        for _ in range(num_particulas)
    ]
    melhor = min(enxame, key=lambda p: p.fitness)
    gbest_pos, gbest_fit = melhor.posicao.copy(), melhor.fitness
    custo_inicial = gbest_fit
    historico = [gbest_fit]

    for _ in range(iteracoes):
        for p in enxame:
            r1, r2 = rng.random(2 * num_centros), rng.random(2 * num_centros)
            p.velocidade = (
                w * p.velocidade
                + c1 * r1 * (p.pbest_pos - p.posicao)
                + c2 * r2 * (gbest_pos - p.posicao)
            )
            p.posicao = np.clip(p.posicao + p.velocidade, 0, limite)
            p.fitness = custo_logistico(p.posicao, clientes, demandas, num_centros)
            if p.fitness < p.pbest_fit:
                p.pbest_fit, p.pbest_pos = p.fitness, p.posicao.copy()
            if p.fitness < gbest_fit:
                gbest_fit, gbest_pos = p.fitness, p.posicao.copy()
        historico.append(gbest_fit)

    return {
        "gbest_pos": gbest_pos,
        "gbest_fit": gbest_fit,
        "custo_inicial": custo_inicial,
        "historico": historico,
        "centros": gbest_pos.reshape(num_centros, 2),
    }


def missao_3(seed: int = 42) -> dict:
    clientes, demandas = gerar_dados_logistica(seed)
    resultado = executar_logistica(np.random.default_rng(seed + 1), clientes, demandas)
    resultado.update({"seed": seed, "clientes": clientes, "demandas": demandas})
    return resultado


def missao_4(seed: int = 42) -> dict:
    """Compara seis configurações, com cinco execuções cada."""
    base = {
        "num_particulas": 30,
        "iteracoes": 50,
        "w": 0.7,
        "c1": 1.8,
        "c2": 1.8,
        "limite": 10.0,
        "num_centros": 5,
    }
    experimentos = [
        ("Padrão", {}),
        ("Inércia Alta", {"w": 0.9}),
        ("Inércia Baixa", {"w": 0.5}),
        ("Cognitivo Alto", {"c1": 2.5}),
        ("Social Alto", {"c2": 2.5}),
        ("Mais Partículas", {"num_particulas": 60}),
    ]
    clientes, demandas = gerar_dados_logistica(seed)
    resultados = {}
    for indice, (nome, alteracoes) in enumerate(experimentos):
        params = {**base, **alteracoes}
        custos, historicos = [], []
        for execucao in range(5):
            rng = np.random.default_rng(seed + 1000 * indice + execucao)
            r = executar_logistica(rng, clientes, demandas, **params)
            custos.append(r["gbest_fit"])
            historicos.append(r["historico"])
        resultados[nome] = {
            "params": params,
            "custo_medio": float(np.mean(custos)),
            "custo_std": float(np.std(custos)),
            "melhor_custo": float(np.min(custos)),
            "pior_custo": float(np.max(custos)),
            "historico_medio": np.mean(historicos, axis=0),
            "custos": custos,
        }
    melhor = min(resultados, key=lambda nome: resultados[nome]["custo_medio"])
    pior = max(resultados, key=lambda nome: resultados[nome]["custo_medio"])
    return {
        "seed": seed,
        "resultados": resultados,
        "melhor_configuracao": melhor,
        "pior_configuracao": pior,
    }


def imprimir_resumo() -> None:
    m1 = missao_1()
    m2 = missao_2()
    m3 = missao_3()
    m4 = missao_4()

    print("MISSÃO 1")
    print(f"  inicial: x={m1['posicao_inicial']:.6f}, f={m1['fitness_inicial']:.6f}")
    print(f"  final:   x={m1['posicao_final']:.6f}, f={m1['fitness_final']:.6f}")
    print(f"  melhor:  x={m1['pbest_pos']:.6f}, f={m1['pbest_fit']:.6f}, iteração={m1['melhor_iteracao']}")
    print(f"  mínimo conforme critério f<=1e-4: {m1['encontrou_minimo']}")

    print("\nMISSÃO 2")
    print(f"  melhor posição: ({m2['gbest_pos'][0]:.6f}, {m2['gbest_pos'][1]:.6f})")
    print(f"  melhor fitness: {m2['gbest_fit']:.6f}, iteração={m2['melhor_iteracao']}")
    print(f"  mínimo conforme critério f<=1e-2: {m2['encontrou_minimo']}")

    print("\nMISSÃO 3")
    print(f"  custo inicial: {m3['custo_inicial']:.2f}")
    print(f"  custo final:   {m3['gbest_fit']:.2f}")
    print(f"  melhoria:      {100 * (1 - m3['gbest_fit'] / m3['custo_inicial']):.2f}%")
    for i, centro in enumerate(m3["centros"], start=1):
        print(f"  centro {i}: ({centro[0]:.4f}, {centro[1]:.4f})")

    print("\nMISSÃO 4")
    for nome, r in m4["resultados"].items():
        print(
            f"  {nome}: médio={r['custo_medio']:.2f}, "
            f"melhor={r['melhor_custo']:.2f}, pior={r['pior_custo']:.2f}, "
            f"desvio={r['custo_std']:.2f}"
        )
    print(f"  melhor configuração: {m4['melhor_configuracao']}")
    print(f"  pior configuração:   {m4['pior_configuracao']}")


if __name__ == "__main__":
    imprimir_resumo()
