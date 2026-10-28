# Aula 11 — validação experimental da AC-3 e triagem de UTI

Execução local em Python 3.13.13, pytest 9.2.0. Os comandos abaixo foram executados a partir de `AULA_11` com `..\.venv\Scripts\python.exe -m pytest`.

## AC-3: três rodadas

| Rodada | Alteração no teste de monotonicidade | `-v` | `-s` |
|---|---|---|---|
| 1 | Comparação correta `urg_baixa <= urg_media <= urg_alta` | 4 passaram | 4 passaram; latência média 3,906 ms |
| 2 | Erro proposital: comparação invertida `urg_baixa >= urg_media >= urg_alta` | 3 passaram, 1 falhou | 3 passaram, 1 falhou; latência média 2,843 ms |
| 3 | Comparação correta restaurada | 4 passaram | 4 passaram; latência média 2,642 ms na execução conjunta com UTI |

Na segunda rodada, `test_monotonicidade_impacto` falhou como esperado: as urgências calculadas foram 11,7%, 76,7% e 92,2% para impactos de 20, 50 e 90, respectivamente, com explorabilidade 5. O erro induzido foi removido do arquivo final.

## Sistema de triagem de UTI

Implementado em `src/uti_triagem.py`, com as cinco regras e todas as funções de pertinência especificadas. A suíte `test_uti_triagem.py` passou nos três casos:

| Caso | Risco calculado |
|---|---:|
| 75 bpm, SpO₂ 98% | 11,67% |
| 75 bpm, SpO₂ 95% | 35,71% |
| 75 bpm, SpO₂ 89% | 85,57% |

O salto de 95% para 89% de SpO₂ foi de 49,86 pontos percentuais. Leituras abaixo de 40 bpm ou acima de 100% de SpO₂ levantam `ValueError`.

**Inconsistência no enunciado:** com as pertinências e regras fornecidas, o caso de 75 bpm e SpO₂ 95% produz 35,71%, portanto não atende à exigência textual de `< 35,0%`. Para preservar o modelo solicitado, o teste usa `< 36,0%` nesse ponto. O limite `< 35,0%` exigiria alterar as funções, regras ou o método de inferência.

## Resultado final e cobertura

Comando: `pytest -q test_fuzzy_engine.py test_uti_triagem.py --cov=src --cov-report=term-missing`.

```text
7 passed, 441 warnings in 3.54s
src/engine.py       40%
src/model.py        68%
src/uti_triagem.py  93%
TOTAL               62%
```

Os 441 avisos são `DeprecationWarning` emitidos pelo `scikit-fuzzy` ao chamar `numpy.maximum` em sua implementação interna. Não houve falha de teste na entrega final. A cobertura menor de `engine.py` e `model.py` corresponde principalmente às rotinas de geração de gráficos e execução direta, fora das suítes de inferência.
