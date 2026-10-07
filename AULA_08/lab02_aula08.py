"""AG binário do zero; serviços sintéticos, pois a tabela não consta do enunciado."""
import numpy as np

# (nome, valor de negócio, RAM em GB, CPU em cores): dados sintéticos fixos.
SERVICOS = [
    ('autenticacao', 35, 2, 1),
    ('gateway', 45, 2, 1.5),
    ('cache', 28, 4, 0.5),
    ('telemetria', 18, 1, 0.5),
    ('antifraude', 55, 3, 2),
    ('recomendacao', 48, 4, 2),
    ('busca', 42, 3, 1.5),
    ('notificacao', 20, 1, 0.5),
    ('pagamentos', 60, 3, 2),
    ('catalogo', 32, 2, 1),
    ('compressao', 22, 1, 1.5),
    ('analise_eventos', 38, 4, 1),
    ('sessoes', 25, 2, 0.5),
    ('auditoria', 16, 1, 0.5),
    ('roteamento', 30, 2, 1),
]


def carregar():
    nomes = [s[0] for s in SERVICOS]
    matriz = np.array([s[1:] for s in SERVICOS], dtype=float)
    return nomes, matriz


def avaliar(pop, matriz, estrategia):
    totais = pop @ matriz
    v, r, c = totais.T
    viavel = (r <= 16) & (c <= 8)
    if estrategia == 'A':
        fit = np.where(viavel, v, 0)
    elif estrategia == 'B':
        fit = v - 20*np.maximum(r-16, 0) - 40*np.maximum(c-8, 0)
    else:
        raise ValueError('Estratégia deve ser A ou B')
    return fit, viavel, totais


def diversidade(pop):
    """Hamming média normalizada entre todos os pares distintos, sem matriz N×N."""
    n, d = pop.shape
    uns = pop.sum(axis=0)
    return float((2*uns*(n-uns)).sum() / (n*(n-1)*d)) if n > 1 else 0.


def torneio(pop, fit, rng, k=3):
    candidatos = rng.choice(len(pop), k, replace=False)
    return pop[candidatos[np.argmax(fit[candidatos])]].copy()


def executar(matriz, estrategia, semente, tamanho=100, geracoes=200):
    rng = np.random.default_rng(semente)
    pop = rng.integers(0, 2, (tamanho, len(matriz)))
    melhor = np.zeros(len(matriz), dtype=int)
    valor_melhor = 0.
    historico = []
    for g in range(geracoes+1):
        fit, viavel, totais = avaliar(pop, matriz, estrategia)
        candidatos = np.flatnonzero(viavel)
        if len(candidatos):
            idx = candidatos[np.argmax(totais[candidatos, 0])]
            if totais[idx, 0] > valor_melhor:
                melhor, valor_melhor = pop[idx].copy(), float(totais[idx, 0])
        historico.append(dict(geracao=g, media=float(fit.mean()), desvio=float(fit.std(ddof=0)),
                              diversidade=diversidade(pop), fracao_viavel=float(viavel.mean()),
                              melhor_valor_viavel=valor_melhor))
        if g == geracoes:
            break
        # Um elite pelo fitness; a melhor solução viável é arquivada separadamente.
        nova = [pop[np.argmax(fit)].copy()]
        while len(nova) < tamanho:
            a, b = torneio(pop, fit, rng), torneio(pop, fit, rng)
            if rng.random() < .8:
                corte = rng.integers(1, len(matriz))
                a, b = np.r_[a[:corte], b[corte:]], np.r_[b[:corte], a[corte:]]
            for filho in (a, b):
                filho ^= (rng.random(len(matriz)) < 1/len(matriz)).astype(int)
                nova.append(filho)
        pop = np.array(nova[:tamanho])
        assert np.isin(pop, [0, 1]).all()
    total = melhor @ matriz
    assert total[1] <= 16 and total[2] <= 8
    return melhor, historico


def main():
    nomes, matriz = carregar()
    print("## Lab 02 — AG binário\n")
    print("Tabela sintética fixa dos 15 microsserviços (não fornecida pelo professor).\n")
    print("| ID | Serviço | Valor | RAM (GB) | CPU (cores) |")
    print("| --- | --- | --- | --- | --- |")
    for i, (nome, v, r, c) in enumerate(SERVICOS, 1):
        print(f"| {i} | {nome} | {v} | {r} | {c} |")
    print("\nLimites: 16 GB e 8 cores. População 100, 200 gerações, torneio de 3 sem reposição, "
          "crossover de ponto único com probabilidade 0.8, mutação por bit de 1/15 e um elite. "
          "Melhor solução viável arquivada separadamente. Dez sementes (0–9); A e B iniciam "
          "com a mesma população para cada semente.\n")
    print("A: fitness=V se viável, zero se violar RAM ou CPU. "
          "B: fitness=V-20*max(RAM-16,0)-40*max(CPU-8,0). "
          "Coeficientes de penalidade escolhidos previamente; não há reparação para isolar "
          "a comparação entre as duas penalidades exigidas.\n")
    resultados = {}
    for estrategia in ('A', 'B'):
        resultados[estrategia] = [executar(matriz, estrategia, seed) for seed in range(10)]
    print("Média e desvio-padrão do fitness dentro da população em cada geração "
          "(desvio com divisor N), depois promediados entre as dez sementes. "
          "Diversidade = Hamming média normalizada entre pares distintos; "
          "não é inferida do desvio-padrão do fitness.\n")
    print("| Geração | Média A | DP A | Diversidade A | Média B | DP B | Diversidade B |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for g in (0, 1, 2, 5, 10, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200):
        valores = [np.mean([h[g][k] for _, h in resultados[e]])
                   for e in ('A', 'B') for k in ('media', 'desvio', 'diversidade')]
        print(f"| {g} | " + " | ".join(f"{v:.4f}" for v in valores) + " |")
    divs, melhores = {}, {}
    print("\n| Estratégia | Valor final médio ± DP entre sementes | Diversidade média (gerações 0–200) |")
    print("| --- | --- | --- |")
    for e, rs in resultados.items():
        valores = [float((x @ matriz)[0]) for x, _ in rs]
        divs[e] = float(np.mean([h[g]['diversidade'] for _, h in rs for g in range(201)]))
        melhores[e] = max(valores)
        print(f"| {e} | {np.mean(valores):.2f} ± {np.std(valores, ddof=1):.2f} | {divs[e]:.4f} |")
    for e, rs in resultados.items():
        seed, (x, _) = max(enumerate(rs), key=lambda r: (r[1][0] @ matriz)[0])
        v, ram, cpu = x @ matriz
        print(f"\nMelhor solução {e}, semente {seed}: `{''.join(map(str,x))}` (IDs 1–15). "
              f"Valor {v:g}, RAM {ram:g}/16 GB, CPU {cpu:g}/8 cores.")
        print("\nServiços: " + ", ".join(nomes[i] for i in range(15) if x[i]) + ".")
    print(f"\nA estratégia {max(divs,key=divs.get)} preservou maior diversidade média nesta instância.")
    print("As estratégias empataram no melhor valor viável." if melhores['A']==melhores['B'] else
          f"A estratégia {max(melhores,key=melhores.get)} encontrou o maior valor viável.")
    print("As escalas de fitness diferem por causa da penalidade; a qualidade final é comparada "
          "pelo valor de negócio viável. A conclusão é descritiva, condicionada aos dados "
          "sintéticos e coeficientes adotados.\n")


if __name__ == '__main__':
    main()
