"""AG binário do zero; dados sintéticos explicitados em dados/README.md."""
import csv
from time import perf_counter
from comum import np, plt, preparar, salvar_csv, salvar_json, salvar_figura, BASE, SEMENTES


def carregar():
    with (BASE / 'dados' / 'microsservicos.csv').open(encoding='utf-8') as f:
        dados = list(csv.DictReader(f))
    matriz = np.array([[float(s[k]) for k in ('valor', 'ram_gb', 'cpu_cores')] for s in dados])
    return dados, matriz


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


def otimo_exato(matriz):
    pop = ((np.arange(2**len(matriz))[:, None] >> np.arange(len(matriz))) & 1)
    fit, _, _ = avaliar(pop, matriz, 'A')
    return pop[np.argmax(fit)], float(fit.max())


def main():
    preparar()
    dados, matriz = carregar()
    exato, valor = otimo_exato(matriz)
    resumo, linhas, historicos = [], [], {}
    for estrategia in ('A', 'B'):
        historicos[estrategia] = []
        for seed in SEMENTES:
            inicio = perf_counter()
            solucao, h = executar(matriz, estrategia, seed)
            tempo = perf_counter()-inicio
            v, r, c = solucao @ matriz
            historicos[estrategia].append(h)
            resumo.append(dict(estrategia=estrategia, semente=seed, individuo=solucao.tolist(),
                               servicos=[s['nome'] for i, s in enumerate(dados) if solucao[i]],
                               valor=float(v), ram=float(r), cpu=float(c), gap=valor-float(v),
                               diversidade_media=float(np.mean([x['diversidade'] for x in h])),
                               diversidade_final=h[-1]['diversidade'], segundos=tempo))
            linhas.extend(dict(estrategia=estrategia, semente=seed, **x) for x in h)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), layout='constrained')
    for ax, metrica, titulo in zip(axes.flat, ('media', 'desvio', 'diversidade', 'fracao_viavel'),
                                  ('Média do fitness da população', 'Desvio-padrão do fitness da população',
                                   'Diversidade: Hamming normalizada', 'Fração de indivíduos viáveis')):
        for estrategia, hs in historicos.items():
            valores = np.array([[x[metrica] for x in h] for h in hs])
            m, s = valores.mean(axis=0), valores.std(axis=0, ddof=1)
            ax.plot(m, label=f'Estratégia {estrategia}')
            ax.fill_between(range(201), m-s, m+s, alpha=.15)
        ax.set_title(titulo)
        ax.set_xlabel('Geração')
        ax.legend()
    fig.suptitle('AG: curvas médias de 10 execuções; faixas = desvio entre execuções')
    salvar_figura('lab02_comparacao.png')
    salvar_csv('lab02_historico.csv', linhas)
    salvar_json('lab02_resultados.json',
                {'execucoes': resumo, 'otimo_exato': valor, 'individuo_exato': exato.tolist()})
    print('AG: 20 execuções. Ótimo exato:', valor)
    for estrategia in ('A', 'B'):
        print(estrategia, 'melhor valor:', max(r['valor'] for r in resumo if r['estrategia'] == estrategia))


if __name__ == '__main__':
    main()
