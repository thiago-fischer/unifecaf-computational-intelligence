"""Gorjeta: referência e cinco experimentos independentes."""
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


def pertinencias(var, valor):
    return {nome: float(fuzz.interp_membership(var.universe, termo.mf, valor))
            for nome, termo in var.terms.items()}


def grafico_curvas(x, curvas, titulo, xlabel, ylabel, nome):
    fig, ax = plt.subplots(figsize=(8, 4))
    for legenda, y in curvas.items():
        ax.plot(x, y, label=legenda)
    ax.set(title=titulo, xlabel=xlabel, ylabel=ylabel)
    ax.legend()
    ax.grid(alpha=0.25)
    salvar_figura(fig, nome)


def grafico_agregado(saida, sim, nome):
    from skfuzzy.control.controlsystem import CrispValueCalculator
    universo, agregado, termos = CrispValueCalculator(saida, sim).find_memberships()
    fig, ax = plt.subplots(figsize=(8, 4))
    for termo, mf in termos.items():
        ax.plot(universo, mf, label=f"{termo} ativada")
    ax.fill_between(universo, agregado, alpha=0.25, color="gray", label="Área agregada (máximo)")
    ax.axvline(sim.output[saida.label], color="black", linestyle="--", label="Centroide")
    ax.set(title="Gorjeta: referência (serviço 7, comida 3)", xlabel="Gorjeta (% da conta)",
           ylabel="Pertinência", ylim=(-0.03, 1.08))
    ax.legend()
    ax.grid(alpha=0.25)
    salvar_figura(fig, nome)


def construir_modelo(*, regra2_e=False, formato="triangular", metodo="centroid", excelente=False):
    servico = ctrl.Antecedent(np.linspace(0, 10, 101), "servico")
    comida = ctrl.Antecedent(np.linspace(0, 10, 101), "comida")
    gorjeta = ctrl.Consequent(np.linspace(0, 25, 51), "gorjeta", defuzzify_method=metodo)
    for var in (servico, comida):
        for nome, parametros in [("ruim", [0, 0, 5]), ("medio", [0, 5, 10]), ("bom", [5, 10, 10])]:
            var[nome] = fuzz.trimf(var.universe, parametros)
    if formato == "trapezoidal":
        for nome, parametros in [("ruim", [0, 0, 2, 5]), ("medio", [2, 4, 6, 8]), ("bom", [5, 8, 10, 10])]:
            servico[nome] = fuzz.trapmf(servico.universe, parametros)
    elif formato != "triangular":
        raise ValueError("Formato deve ser triangular ou trapezoidal.")
    gorjeta["baixa"] = fuzz.trimf(gorjeta.universe, [0, 0, 13])
    gorjeta["media"] = fuzz.trimf(gorjeta.universe, [0, 13, 25])
    gorjeta["alta"] = fuzz.trimf(gorjeta.universe, [13, 25, 25])
    antecedente2 = servico["medio"] & comida["medio"] if regra2_e else servico["medio"]
    regras = [ctrl.Rule(servico["ruim"] | comida["ruim"], gorjeta["baixa"], label="regra1"),
              ctrl.Rule(antecedente2, gorjeta["media"], label="regra2"),
              ctrl.Rule(servico["bom"] | comida["bom"], gorjeta["alta"], label="regra3")]
    if excelente:
        servico["excelente"] = fuzz.trapmf(servico.universe, [8, 9, 10, 10])
        regras.append(ctrl.Rule(servico["excelente"], gorjeta["alta"], label="regra4"))
    return servico, comida, gorjeta, ctrl.ControlSystem(regras)


def avaliar(modelo, nota_servico, nota_comida):
    servico, comida, gorjeta, sistema = modelo
    valor, sim = simular(sistema, {"servico": nota_servico, "comida": nota_comida}, gorjeta)
    ativacoes = {r.label: float(r.aggregate_firing[sim]) for r in sistema.rules}
    return {"servico": float(nota_servico), "comida": float(nota_comida), "gorjeta": valor,
            "pertinencias_servico": pertinencias(servico, nota_servico),
            "pertinencias_comida": pertinencias(comida, nota_comida), "ativacoes": ativacoes}, sim


def pedir_nota(texto, padrao):
    resposta = input(f"{texto} (0-10) [{padrao}]: ").strip()
    return validar_entrada(resposta.replace(",", ".") if resposta else padrao, texto, 0, 10)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sem-janela", action="store_true", help="Sem janela; notas padrão 7 e 3")
    parser.add_argument("--servico", type=float)
    parser.add_argument("--comida", type=float)
    args = parser.parse_args()
    if args.sem_janela:
        import matplotlib.pyplot as plt
        plt.switch_backend("Agg")
    try:
        ns = args.servico if args.servico is not None else (7 if args.sem_janela else pedir_nota("Nota do serviço", 7))
        nc = args.comida if args.comida is not None else (3 if args.sem_janela else pedir_nota("Nota da comida", 3))
        modelo = construir_modelo()
        usuario, _ = avaliar(modelo, ns, nc)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"Gorjeta sugerida ({ns}, {nc}): {usuario['gorjeta']:.1f}% ({usuario['gorjeta']:.6f}%)")
    referencia, sim = avaliar(modelo, 7, 3)
    regra2, _ = avaliar(construir_modelo(regra2_e=True), 7, 3)
    trapezio = construir_modelo(formato="trapezoidal")
    formato, _ = avaliar(trapezio, 7, 3)
    metodos = {m: avaliar(construir_modelo(metodo=m), 7, 3)[0] for m in ["centroid", "bisector", "mom"]}
    quarto = construir_modelo(excelente=True)
    excelentes = [{"referencia": avaliar(modelo, s, c)[0], "excelente": avaliar(quarto, s, c)[0]}
                  for s, c in [(8, 3), (9, 3), (10, 3), (9, 10)]]
    bordas = [avaliar(modelo, s, c)[0] for s, c in [(0, 0), (10, 10), (5, 5)]]
    for var, titulo, unidade, nome in [
        (modelo[0], "Serviço — referência", "Nota do serviço (pontos)", "servico"),
        (modelo[1], "Comida — referência", "Nota da comida (pontos)", "comida"),
        (modelo[2], "Gorjeta — referência", "Gorjeta (% da conta)", "gorjeta"),
        (trapezio[0], "Serviço — experimento trapezoidal", "Nota do serviço (pontos)", "servico_trapezoidal"),
        (quarto[0], "Serviço — quarto conjunto", "Nota do serviço (pontos)", "servico_excelente")]:
        grafico_conjuntos(var, titulo, unidade, f"lab02_{nome}.png")
    grafico_agregado(modelo[2], sim, "lab02_agregado.png")
    x = np.linspace(0, 10, 101)
    curvas = {"Triangular": [avaliar(modelo, s, 3)[0]["gorjeta"] for s in x],
              "Trapezoidal": [avaliar(trapezio, s, 3)[0]["gorjeta"] for s in x]}
    grafico_curvas(x, curvas, "Resposta com comida fixa em 3", "Nota do serviço (pontos)",
                   "Gorjeta (% da conta)", "lab02_formatos_resposta.png")
    suavidade = {k: {"maior_variacao_passo_0_1": float(np.max(np.abs(np.diff(v)))),
                     "maior_segunda_diferenca": float(np.max(np.abs(np.diff(v, n=2))))}
                 for k, v in curvas.items()}
    print(f"Referência: {referencia['gorjeta']:.6f}%; regra 2 E: {regra2['gorjeta']:.6f}%")
    for m, caso in metodos.items():
        print(f"{m}: {caso['gorjeta']:.6f}%")
    print(f"Serviço trapezoidal em (7,3): {formato['gorjeta']:.6f}%")
    for familia, medidas in suavidade.items():
        print(f"{familia}: variação máxima por 0,1 = {medidas['maior_variacao_passo_0_1']:.6f}; "
              f"segunda diferença máxima = {medidas['maior_segunda_diferenca']:.6f}")
    for caso in excelentes:
        ref, novo = caso['referencia'], caso['excelente']
        print(f"Serviço excelente ({ref['servico']}, {ref['comida']}): "
              f"{ref['gorjeta']:.6f}% -> {novo['gorjeta']:.6f}%")
    for caso in bordas:
        print(f"Borda/centro ({caso['servico']}, {caso['comida']}): {caso['gorjeta']:.6f}%")
    finalizar(args.sem_janela)


if __name__ == "__main__":
    main()
