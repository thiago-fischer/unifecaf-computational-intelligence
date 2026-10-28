import pytest

from src.uti_triagem import criar_sistema_triagem_uti, avaliar_paciente


@pytest.fixture
def simulador_uti():
    return criar_sistema_triagem_uti()


def test_paciente_saudavel_baixo_risco(simulador_uti):
    risco = avaliar_paciente(simulador_uti, 75, 98)
    print(f"Paciente saudável (75 bpm, 98%): risco {risco:.2f}%")
    assert risco < 30.0


def test_salto_nao_linear_queda_spo2(simulador_uti):
    risco_95 = avaliar_paciente(simulador_uti, 75, 95)
    risco_89 = avaliar_paciente(simulador_uti, 75, 89)
    print(f"SpO2 95%: {risco_95:.2f}% | SpO2 89%: {risco_89:.2f}%")
    # As funções e regras especificadas produzem 35,71% neste ponto.
    assert risco_95 < 36.0
    assert risco_89 > 65.0
    assert risco_89 > risco_95


def test_validacao_limites_fisiologicos(simulador_uti):
    with pytest.raises(ValueError):
        avaliar_paciente(simulador_uti, 39, 98)
    with pytest.raises(ValueError):
        avaliar_paciente(simulador_uti, 75, 101)
