"""PSO contínuo do zero: objetivo linear e temperaturas individuais constantes."""
import numpy as np

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
    print("## Lab 01 — PSO contínuo\n")
    print("C = [42, 35, 58, 30, 50, 65]; 200 iterações; inércia 0.7; c1=c2=1.5. "
          "Dez sementes (0–9) para cada população. Posições negativas são zeradas e "
          "normalizadas; vetor nulo recebe pesos uniformes. Históricos de pbest e gbest "
          "são mantidos em memória e retornados por PSO.executar().\n")
    print("Hipótese térmica: T_i=C_i, pois não foi fornecida relação entre carga e temperatura. "
          "Fitness = W@C + 10*sum(max(T_i-75,0)**2). A penalidade é externa e fica zero "
          "com os coeficientes fornecidos; para [80,77] °C, ela vale 290.\n")
    assert penalidade([80., 77.]) == 290.
    curvas = {}
    print("| Partículas | Melhor W (AZ1 a AZ6) | Soma | Fitness | Iteração média até 30 °C |")
    print("| --- | --- | --- | --- | --- |")
    for n in (10, 30, 50):
        resultados = [PSO(n, seed).executar() for seed in range(10)]
        curvas[n] = np.array([r[1] for r in resultados])
        w, h, _, _ = min(resultados, key=lambda r: r[1][-1])
        atingiu = [np.flatnonzero(r[1] <= 30+1e-6) for r in resultados]
        iteracoes = [int(a[0]) for a in atingiu if len(a)]
        media = f"{np.mean(iteracoes):.1f}" if iteracoes else "não atingiu"
        print(f"| {n} | {w.tolist()} | {w.sum():.10f} | {h[-1]:.4f} | {media} ({len(iteracoes)}/10) |")
    print("\nEvolução do melhor fitness: média de dez execuções, em iterações selecionadas.\n")
    print("| Iteração | 10 partículas | 30 partículas | 50 partículas |")
    print("| --- | --- | --- | --- |")
    for i in (0, 1, 2, 5, 10, 20, 50, 100, 200):
        print(f"| {i} | " + " | ".join(f"{curvas[n][:,i].mean():.6f}" for n in curvas) + " |")
    print("\nO mínimo analítico é 30 °C, obtido ao concentrar a carga na AZ4. "
          "Não há capacidade máxima por AZ ou distribuição mínima no enunciado; "
          "por isso esse resultado é coerente com o objetivo linear. A penalidade não "
          "modela aquecimento dinâmico sob a hipótese adotada. "
          "As avaliações de candidatos são N×201: 2.010, 6.030 e 10.050, respectivamente.\n")


if __name__ == '__main__':
    main()
