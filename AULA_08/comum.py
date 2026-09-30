"""Utilitários de saída; os algoritmos estão nos respectivos laboratórios."""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent
SEMENTES = range(10)


def preparar():
    for nome in ('dados', 'figuras', 'saidas'):
        (BASE / nome).mkdir(exist_ok=True)
    plt.rcParams.update({'figure.dpi': 130, 'font.size': 10, 'axes.grid': True,
                         'grid.alpha': 0.25, 'axes.spines.top': False,
                         'axes.spines.right': False})


def salvar_json(nome, dados):
    (BASE / 'saidas' / nome).write_text(
        json.dumps(dados, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def salvar_csv(nome, linhas):
    with (BASE / 'saidas' / nome).open('w', newline='', encoding='utf-8') as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        writer.writeheader()
        writer.writerows(linhas)


def salvar_figura(nome):
    plt.savefig(BASE / 'figuras' / nome, bbox_inches='tight')
    plt.close()
