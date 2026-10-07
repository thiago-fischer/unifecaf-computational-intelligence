"""Ventilador fuzzy: referência da aula, bordas e evidências reproduzíveis."""
import argparse
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


from pathlib import Path
import math
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent / "results"


def validar_entrada(valor, nome, minimo, maximo):
    try:
        numero = float(valor)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{nome}: informe um número entre {minimo} e {maximo}.") from exc
    if not math.isfinite(numero) or not minimo <= numero <= maximo:
        raise ValueError(f"{nome}: informe um número finito entre {minimo} e {maximo}.")
    return numero


def simular(sistema, entradas, saida):
    sim = ctrl.ControlSystemSimulation(sistema, clip_to_bounds=False)
    variaveis = {v.label: v for v in sistema.antecedents}
    for nome, valor in entradas.items():
        var = variaveis[nome]
        sim.input[nome] = validar_entrada(valor, nome, var.universe[0], var.universe[-1])
    sim.compute()
    resultado = float(sim.output[saida.label])
    validar_entrada(resultado, saida.label, saida.universe[0], saida.universe[-1])
    return resultado, sim


def salvar_figura(fig, nome):
    RESULTS.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(RESULTS / nome, dpi=150)


def grafico_conjuntos(var, titulo, unidade, nome):
    fig, ax = plt.subplots(figsize=(8, 4))
    for termo, conjunto in var.terms.items():
        ax.plot(var.universe, conjunto.mf, label=termo)
    ax.set(title=titulo, xlabel=unidade, ylabel="Pertinência", ylim=(-0.03, 1.08))
    ax.legend()
    ax.grid(alpha=0.25)
    salvar_figura(fig, nome)


def finalizar(sem_janela):
    if not sem_janela:
        plt.show()
    plt.close("all")


def construir_modelo():
    temperatura = ctrl.Antecedent(np.arange(0, 41, 1), "temperatura")
    velocidade = ctrl.Consequent(np.arange(0, 101, 1), "velocidade", defuzzify_method="centroid")
    temperatura["frio"] = fuzz.trapmf(temperatura.universe, [0, 0, 15, 25])
    temperatura["morno"] = fuzz.trimf(temperatura.universe, [15, 25, 35])
    temperatura["quente"] = fuzz.trapmf(temperatura.universe, [25, 35, 40, 40])
    velocidade["baixa"] = fuzz.trimf(velocidade.universe, [0, 0, 50])
    velocidade["media"] = fuzz.trimf(velocidade.universe, [0, 50, 100])
    velocidade["alta"] = fuzz.trimf(velocidade.universe, [50, 100, 100])
    regras = [ctrl.Rule(temperatura[t], velocidade[v], label=t)
              for t, v in [("frio", "baixa"), ("morno", "media"), ("quente", "alta")]]
    return temperatura, velocidade, ctrl.ControlSystem(regras)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sem-janela", action="store_true")
    args = parser.parse_args()
    if args.sem_janela:
        import matplotlib.pyplot as plt
        plt.switch_backend("Agg")
    temperatura, velocidade, sistema = construir_modelo()
    for temp in [10, 20, 25, 30, 38, 0, 40]:
        valor, _ = simular(sistema, {"temperatura": temp}, velocidade)
        print(f"{temp}°C -> ventilador a {valor:.0f}% (preciso: {valor:.6f}%)")
    grafico_conjuntos(temperatura, "Temperatura — referência", "Temperatura (°C)", "lab01_temperatura.png")
    grafico_conjuntos(velocidade, "Velocidade — referência", "Comando do ventilador (%)", "lab01_velocidade.png")
    finalizar(args.sem_janela)


if __name__ == "__main__":
    main()
