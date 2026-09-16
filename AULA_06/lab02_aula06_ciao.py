"""Laboratório 02: nove cenários, cada um com semente 42 e repetições 0–9."""
from lab01_aula06_ciao import CENARIOS, executar_cenarios
from lab01_aula06_ciao import executar_aco

if __name__ == '__main__':
    executar_cenarios('lab02', executar_aco, CENARIOS)
