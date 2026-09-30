"""Verificações de restrições, casos de borda e referências independentes."""
import unittest
import numpy as np
from lab01_aula08 import normalizar, penalidade, fitness, PSO
from lab02_aula08 import avaliar, carregar, diversidade, executar as ag, otimo_exato
from lab03_aula08 import construir, custo, validar_arvore, atualizar, executar as aco


class TestPSO(unittest.TestCase):
    def test_normalizacao(self):
        np.testing.assert_allclose(normalizar([-1., 0., -2.]), [1/3]*3)
        np.testing.assert_allclose(normalizar([1., -1., 3.]), [.25, 0, .75])

    def test_objetivo_e_penalidade(self):
        self.assertEqual(fitness([0, 0, 0, 1, 0, 0]), 30.)
        self.assertEqual(penalidade([75., 74.]), 0.)
        self.assertEqual(penalidade([80., 77.]), 290.)
        self.assertEqual(fitness([1., 0.], np.array([80., 30.])), 330.)

    def test_execucao_e_memorias(self):
        w, h, hp, hg = PSO(10, 0, iteracoes=30).executar()
        self.assertTrue(np.all(np.diff(h) <= 0))
        np.testing.assert_allclose(hp.sum(axis=-1), 1)
        np.testing.assert_allclose(hg.sum(axis=-1), 1)
        self.assertTrue(np.all(np.diff(hp @ np.array([42,35,58,30,50,65]), axis=0) <= 1e-8))
        np.testing.assert_array_equal(w, PSO(10, 0, iteracoes=30).executar()[0])


class TestAG(unittest.TestCase):
    def test_capacidades_e_penalidades(self):
        # Casos independentes: limite exato, excesso só de RAM e só de CPU.
        matriz = np.array([[100,16,8], [1,1,0], [1,0,1]], dtype=float)
        pop = np.array([[0,0,0], [1,0,0], [1,1,0], [1,0,1]])
        fa, viavel, _ = avaliar(pop, matriz, 'A')
        fb, _, _ = avaliar(pop, matriz, 'B')
        np.testing.assert_array_equal(fa, [0,100,0,0])
        np.testing.assert_array_equal(fb, [0,100,81,61])
        np.testing.assert_array_equal(viavel, [True,True,False,False])

    def test_diversidade(self):
        self.assertEqual(diversidade(np.zeros((10,15))), 0)
        self.assertEqual(diversidade(np.array([[0,0], [1,1]])), 1)

    def test_referencia_e_solucoes(self):
        _, matriz = carregar()
        sol, valor = otimo_exato(matriz)
        # Enumeração independente, com inteiros de meia unidade para RAM/CPU.
        melhor = 0
        for mascara in range(1 << 15):
            v = r = c = 0
            for i in range(15):
                if mascara & (1 << i):
                    v += int(matriz[i,0])
                    r += round(2*matriz[i,1])
                    c += round(2*matriz[i,2])
            if r <= 32 and c <= 16:
                melhor = max(melhor, v)
        self.assertEqual(valor, melhor)
        for estrategia in ('A', 'B'):
            x, h = ag(matriz, estrategia, 3, tamanho=20, geracoes=10)
            total = x @ matriz
            self.assertLessEqual(total[0], valor)
            self.assertLessEqual(total[1], 16)
            self.assertLessEqual(total[2], 8)
            self.assertTrue(np.all(np.diff([p['melhor_valor_viavel'] for p in h]) >= 0))


class TestACO(unittest.TestCase):
    def setUp(self):
        self.d = np.array([[0.,2,9,9], [2,0,3,9], [9,3,0,4], [9,9,4,0]])
        self.arvore = [(0,1), (1,2), (2,3)]

    def test_custo_caminhos(self):
        pares = np.array([[0,3,2], [1,3,1]])
        self.assertEqual(custo(self.arvore, self.d, pares), 25.)

    def test_arvores_invalidas(self):
        with self.assertRaises(AssertionError):
            validar_arvore([(0,1), (1,2), (0,2)], self.d)
        with self.assertRaises(AssertionError):
            validar_arvore([(0,1), (1,2)], self.d)
        with self.assertRaises(ValueError):
            construir(np.zeros((4,4)), np.ones((4,4)), np.random.default_rng(0))

    def test_feromonio_seletivo(self):
        tau = np.ones((4,4))
        atualizar(tau, self.arvore, 50.)
        self.assertAlmostEqual(tau[0,1], 2.8)
        self.assertEqual(tau[0,2], 1.)
        np.testing.assert_array_equal(tau, tau.T)

    def test_construcao_e_execucao(self):
        rng = np.random.default_rng(0)
        for aleatoria in (True, False):
            for _ in range(20):
                a = construir(self.d, np.ones((4,4)), rng, aleatoria)
                validar_arvore(a, self.d)
        pares = np.array([[0,3,2], [1,3,1]])
        arvore, valor, h = aco(self.d, pares, 0, formigas=5, iteracoes=10)
        validar_arvore(arvore, self.d)
        self.assertEqual(valor, custo(arvore, self.d, pares))
        self.assertTrue(np.all(np.diff(h) <= 0))


if __name__ == '__main__':
    unittest.main(verbosity=2)
