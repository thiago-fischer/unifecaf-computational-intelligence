"""Motor Mamdani para urgência de incidentes e desafio dos extremos."""

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


PASTA = Path(__file__).resolve().parent
MATRIZ = (
    ("baixa", "baixa", "media"),
    ("media", "alta", "alta"),
    ("critica", "critica", "critica"),
)


def construir_modelo(*, trapezio_critico=False, metodo="centroid"):
    """Cria as nove regras da matriz, com uma alteração experimental opcional."""
    impacto = ctrl.Antecedent(np.arange(0, 101, 1), "impacto")
    explorabilidade = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "explorabilidade")
    urgencia = ctrl.Consequent(np.arange(0, 100.01, 0.1), "urgencia", defuzzify_method=metodo)

    impacto["baixo"] = fuzz.trapmf(impacto.universe, [0, 0, 20, 40])
    impacto["medio"] = fuzz.trimf(impacto.universe, [20, 50, 80])
    impacto["alto"] = fuzz.trapmf(impacto.universe, [60, 80, 100, 100])
    explorabilidade["baixa"] = fuzz.trapmf(explorabilidade.universe, [0, 0, 2, 4])
    explorabilidade["moderada"] = fuzz.trimf(explorabilidade.universe, [2, 5, 8])
    explorabilidade["alta"] = fuzz.trapmf(explorabilidade.universe, [6, 8, 10, 10])

    # Triângulos de referência: centroides 4,333... e 87,5 nos extremos.
    urgencia["baixa"] = fuzz.trimf(urgencia.universe, [0, 0, 13])
    urgencia["media"] = fuzz.trimf(urgencia.universe, [0, 33, 66])
    urgencia["alta"] = fuzz.trimf(urgencia.universe, [40, 70, 90])
    if trapezio_critico:
        urgencia["critica"] = fuzz.trapmf(urgencia.universe, [62.5, 90, 100, 100])
    else:
        urgencia["critica"] = fuzz.trimf(urgencia.universe, [62.5, 100, 100])

    linhas = ("baixo", "medio", "alto")
    colunas = ("baixa", "moderada", "alta")
    regras = [
        ctrl.Rule(impacto[linha] & explorabilidade[coluna], urgencia[MATRIZ[i][j]], label=f"R{i * 3 + j + 1}")
        for i, linha in enumerate(linhas)
        for j, coluna in enumerate(colunas)
    ]
    return impacto, explorabilidade, urgencia, ctrl.ControlSystem(regras)


def calcular(sistema, impacto, explorabilidade):
    for nome, valor, limite in (("Impacto", impacto, 100), ("Explorabilidade", explorabilidade, 10)):
        if not math.isfinite(valor) or not 0 <= valor <= limite:
            raise ValueError(f"{nome} deve ser finito e estar entre 0 e {limite}.")
    simulacao = ctrl.ControlSystemSimulation(sistema, clip_to_bounds=False)
    simulacao.input["impacto"] = impacto
    simulacao.input["explorabilidade"] = explorabilidade
    simulacao.compute()
    return float(simulacao.output["urgencia"])


def grafico_saida(modelos):
    fig, eixos = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
    for eixo, (impacto, explorabilidade) in zip(eixos, ((0, 0), (100, 10))):
        _, _, urgencia, _ = modelos["centroide"]
        for nome, termo in urgencia.terms.items():
            eixo.plot(urgencia.universe, termo.mf, label=nome)
        if impacto == 100:
            curva_trapezio = modelos["trapézio"][2]["critica"].mf
            eixo.plot(urgencia.universe, curva_trapezio, color="darkred", linestyle=":",
                      label="crítica trapezoidal")
        for nome, modelo in modelos.items():
            resultado = calcular(modelo[3], impacto, explorabilidade)
            eixo.axvline(resultado, linestyle="--", label=f"{nome}: {resultado:.2f}%")
        eixo.set(title=f"Impacto {impacto}% · Explorabilidade {explorabilidade}",
                 xlabel="Urgência (%)", xlim=(0, 100), ylim=(0, 1.08))
        eixo.grid(alpha=0.2)
        eixo.legend(fontsize=8)
    eixos[0].set_ylabel("Pertinência")
    fig.tight_layout()
    fig.savefig(PASTA / "saida_extremos.png", dpi=160)
    plt.close(fig)


def superficie(sistema):
    impactos = np.linspace(0, 100, 51)
    explorabilidades = np.linspace(0, 10, 41)
    xx, yy = np.meshgrid(impactos, explorabilidades)
    zz = np.empty_like(xx)
    for indice in np.ndindex(xx.shape):
        zz[indice] = calcular(sistema, float(xx[indice]), float(yy[indice]))
    if not np.isfinite(zz).all():
        raise RuntimeError("A superfície contém pontos sem saída válida.")
    fig = plt.figure(figsize=(10, 7))
    eixo = fig.add_subplot(111, projection="3d")
    malha = eixo.plot_surface(xx, yy, zz, cmap="viridis", linewidth=0, antialiased=True)
    eixo.set(xlabel="Impacto (%)", ylabel="Explorabilidade (0–10)", zlabel="Urgência (%)",
             title="Superfície de decisão · Mamdani com centroide", zlim=(0, 100))
    fig.colorbar(malha, ax=eixo, shrink=0.65, label="Urgência (%)")
    fig.tight_layout()
    fig.savefig(PASTA / "superficie_decisao.png", dpi=160)
    plt.close(fig)
    return zz


def main():
    modelos = {
        "centroide": construir_modelo(),
        "trapézio": construir_modelo(trapezio_critico=True),
        "MOM": construir_modelo(metodo="mom"),
    }
    for impacto, explorabilidade in ((0, 0), (100, 10), (50, 5), (70, 7)):
        valores = {nome: calcular(modelo[3], impacto, explorabilidade) for nome, modelo in modelos.items()}
        print(f"Impacto {impacto:3}% / Explorabilidade {explorabilidade:2}: "
              + " | ".join(f"{nome} = {valor:.6f}%" for nome, valor in valores.items()))
    grafico_saida(modelos)
    zz = superficie(modelos["centroide"][3])
    print(f"Superfície: {zz.size} pontos; mínimo = {zz.min():.6f}%; máximo = {zz.max():.6f}%")
    print(f"Imagens salvas em {PASTA}")


if __name__ == "__main__":
    main()
