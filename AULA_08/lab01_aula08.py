"""PSO contínuo do zero: objetivo linear e temperaturas individuais constantes."""
from time import perf_counter
from comum import np, plt, preparar, salvar_csv, salvar_json, salvar_figura, BASE, SEMENTES

C = np.array([42., 35., 58., 30., 50., 65.])


def normalizar(x):
    x = np.maximum(np.asarray(x, dtype=float), 0)
    soma = x.sum(axis=-1, keepdims=True)
    return np.divide(x, soma, out=np.full_like(x, 1 / x.shape[-1]), where=soma > 0)


def penalidade(temperaturas, limite=75., coeficiente=10.):
    return coeficiente * np.square(np.maximum(np.asarray(temperaturas) - limite, 0)).sum(axis=-1)


def fitness(x, temperaturas=C):
    return np.asarray(x) @ temperaturas + penalidade(temperaturas)


class PSO:
    def __init__(self, tamanho, semente, iteracoes=200, omega=.7, c1=1.5, c2=1.5):
        self.tamanho, self.iteracoes = tamanho, iteracoes
        self.omega, self.c1, self.c2 = omega, c1, c2
        self.rng = np.random.default_rng(semente)

    def executar(self):
        x = normalizar(self.rng.random((self.tamanho, 6)))
        v = self.rng.uniform(-.1, .1, x.shape)
        pbest, custos = x.copy(), fitness(x)
        gbest = pbest[np.argmin(custos)].copy()
        historico, historico_p, historico_g = [], [], []
        for passo in range(self.iteracoes + 1):
            assert np.all(x >= 0) and np.allclose(x.sum(axis=1), 1, atol=1e-8)
            historico.append(float(fitness(gbest)))
            historico_p.append(pbest.copy())
            historico_g.append(gbest.copy())
            if passo == self.iteracoes:
                break
            r1, r2 = self.rng.random(x.shape), self.rng.random(x.shape)
            v = self.omega*v + self.c1*r1*(pbest-x) + self.c2*r2*(gbest-x)
            x = normalizar(x + v)
            novos = fitness(x)
            melhora = novos < custos
            pbest[melhora], custos[melhora] = x[melhora].copy(), novos[melhora]
            gbest = pbest[np.argmin(custos)].copy()
        assert np.all(np.diff(historico) <= 1e-9)
        return gbest, np.array(historico), np.array(historico_p), np.array(historico_g)


def main():
    preparar()
    resumo, linhas = [], []
    plt.figure(figsize=(9, 5))
    for tamanho in (10, 30, 50):
        curvas = []
        for seed in SEMENTES:
            inicio = perf_counter()
            w, h, hp, hg = PSO(tamanho, seed).executar()
            tempo = perf_counter() - inicio
            curvas.append(h)
            atingiu = np.flatnonzero(h <= 30 + 1e-6)
            resumo.append(dict(populacao=tamanho, semente=seed, pesos=w.tolist(),
                               soma=float(w.sum()), temperatura=float(w @ C),
                               penalidade=float(penalidade(C)), fitness=float(h[-1]),
                               iteracao_otimo=int(atingiu[0]) if len(atingiu) else None,
                               avaliacoes=tamanho*201, segundos=tempo))
            linhas.extend(dict(populacao=tamanho, semente=seed, iteracao=i, gbest=float(f))
                          for i, f in enumerate(h))
            np.savez_compressed(BASE / 'saidas' / f'pso_memoria_n{tamanho}_s{seed}.npz',
                                pbest=hp, gbest=hg)
        curvas = np.array(curvas)
        media, desvio = curvas.mean(axis=0), curvas.std(axis=0, ddof=1)
        plt.plot(media, label=f'{tamanho} partículas')
        plt.fill_between(range(201), media-desvio, media+desvio, alpha=.13)
    plt.axhline(30, color='black', ls='--', lw=1, label='Ótimo analítico = 30 °C')
    plt.xlabel('Iteração (0 = inicialização)')
    plt.ylabel('Melhor fitness global')
    plt.title('PSO: média e desvio-padrão entre 10 execuções')
    plt.legend()
    salvar_figura('lab01_convergencia.png')
    salvar_csv('lab01_historico.csv', linhas)
    salvar_json('lab01_resultados.json', resumo)
    print('PSO: 30 execuções concluídas. Melhor fitness:', min(r['fitness'] for r in resumo))


if __name__ == '__main__':
    main()
