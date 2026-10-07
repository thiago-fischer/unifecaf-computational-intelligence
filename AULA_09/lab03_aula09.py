"""Prioridade de intervenção em servidor a partir de CPU e latência."""
import argparse
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Expectativas anteriores à execução, segundo a matriz de regras.
CENARIOS = [(10, 30, "baixa"), (50, 250, "media"), (90, 450, "alta"),
            (10, 450, "alta"), (0, 0, "baixa"), (100, 500, "alta"),
            (30, 150, "transicao baixa/media"), (70, 350, "transicao media/alta")]


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
    cpu = ctrl.Antecedent(np.arange(0, 101, 1), "cpu")
    latencia = ctrl.Antecedent(np.arange(0, 501, 1), "latencia")
    prioridade = ctrl.Consequent(np.arange(0, 101, 1), "prioridade", defuzzify_method="centroid")
    for var in (cpu, prioridade):
        var["baixa"] = fuzz.trapmf(var.universe, [0, 0, 20, 40])
        var["media"] = fuzz.trimf(var.universe, [20, 50, 80])
        var["alta"] = fuzz.trapmf(var.universe, [60, 80, 100, 100])
    latencia["baixa"] = fuzz.trapmf(latencia.universe, [0, 0, 100, 200])
    latencia["media"] = fuzz.trimf(latencia.universe, [100, 250, 400])
    latencia["alta"] = fuzz.trapmf(latencia.universe, [300, 400, 500, 500])
    termos = ["baixa", "media", "alta"]
    matriz = [["baixa", "media", "alta"], ["media", "media", "alta"], ["alta", "alta", "alta"]]
    regras = [ctrl.Rule(cpu[c] & latencia[l], prioridade[matriz[i][j]], label=f"r{i * 3 + j + 1}")
              for i, c in enumerate(termos) for j, l in enumerate(termos)]
    regras.append(ctrl.Rule(cpu["alta"] | latencia["alta"], prioridade["alta"], label="r10"))
    return cpu, latencia, prioridade, ctrl.ControlSystem(regras)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sem-janela", action="store_true")
    parser.add_argument("--cpu", type=float)
    parser.add_argument("--latencia", type=float)
    args = parser.parse_args()
    if args.sem_janela:
        import matplotlib.pyplot as plt
        plt.switch_backend("Agg")
    cpu, latencia, prioridade, sistema = construir_modelo()
    # Valida entrada personalizada antes de produzir artefatos.
    usuario = None
    if args.cpu is not None or args.latencia is not None:
        if args.cpu is None or args.latencia is None:
            parser.error("Informe --cpu e --latencia juntos.")
        try:
            valor, _ = simular(sistema, {"cpu": args.cpu, "latencia": args.latencia}, prioridade)
        except ValueError as exc:
            parser.error(str(exc))
        usuario = {"cpu": args.cpu, "latencia": args.latencia, "prioridade": valor}
        print(f"Entrada personalizada: {valor:.6f} pontos")
    for carga, tempo, expectativa in CENARIOS:
        valor, _ = simular(sistema, {"cpu": carga, "latencia": tempo}, prioridade)
        print(f"CPU {carga}% / latência {tempo} ms -> {valor:.6f} pontos; esperada: {expectativa}")
    for var, titulo, unidade in [(cpu, "Uso de CPU", "Uso de CPU (%)"),
                                 (latencia, "Latência", "Latência (ms)"),
                                 (prioridade, "Prioridade de intervenção", "Prioridade (pontos)")]:
        grafico_conjuntos(var, titulo, unidade, f"lab03_{var.label}.png")
    finalizar(args.sem_janela)


if __name__ == "__main__":
    main()
