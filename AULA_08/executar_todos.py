"""Executa testes, laboratórios e relatório, salvando os logs de cada etapa."""
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent


def main():
    (BASE / 'saidas').mkdir(exist_ok=True)
    etapas = [('testes', ['-m', 'unittest', 'discover', '-s', str(BASE), '-p', 'test_*.py', '-v'])]
    etapas += [(nome, [str(BASE/f'{nome}.py')]) for nome in
               ('lab01_aula08', 'lab02_aula08', 'lab03_aula08', 'gerar_relatorio')]
    for nome, args in etapas:
        print(f'Executando {nome}...', flush=True)
        resultado = subprocess.run([sys.executable, '-X', 'utf8', *args],
                                   capture_output=True, text=True, encoding='utf-8')
        saida = resultado.stdout + resultado.stderr
        (BASE/'saidas'/f'{nome}.log').write_text(saida, encoding='utf-8')
        print(saida, flush=True)
        if resultado.returncode:
            raise SystemExit(resultado.returncode)


if __name__ == '__main__':
    main()
