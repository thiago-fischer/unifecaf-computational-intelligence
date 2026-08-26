# Resultados - Aula 03

## LAB-01 - Compreensão e Execução

### Saída da execução

```text
==================================================
ALGORITMO GENÉTICO PASSO A PASSO
==================================================

População inicial: [[0, 1, 0, 0, 1], [0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 1, 0, 1], [0, 1, 0, 0, 0], [0, 1, 0, 0, 0]]

==================== GERAÇÃO 0 ====================

Avaliação dos indivíduos:
  [0, 1, 0, 0, 1] → x= 9 → f(x)= 81
  [0, 1, 1, 0, 0] → x=12 → f(x)=144
  [0, 1, 0, 0, 0] → x= 8 → f(x)= 64
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [0, 1, 0, 0, 0] → x= 8 → f(x)= 64
  [0, 1, 0, 0, 0] → x= 8 → f(x)= 64

 Melhor: x = 29 → f(x) = 841

==================== GERAÇÃO 1 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 0, 0, 0, 1] → x=17 → f(x)=289
  [1, 1, 0, 1, 0] → x=26 → f(x)=676
  [0, 1, 0, 0, 0] → x= 8 → f(x)= 64
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 1, 1, 0, 1] → x=29 → f(x)=841

 Melhor: x = 29 → f(x) = 841

==================== GERAÇÃO 2 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 0, 0, 0, 1] → x=17 → f(x)=289
  [1, 1, 0, 0, 0] → x=24 → f(x)=576

 Melhor: x = 29 → f(x) = 841

==================== GERAÇÃO 3 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [0, 0, 1, 0, 1] → x= 5 → f(x)= 25
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 0, 0, 1] → x=25 → f(x)=625
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [1, 1, 1, 0, 1] → x=29 → f(x)=841

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 4 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [1, 1, 0, 0, 1] → x=25 → f(x)=625
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [1, 1, 1, 0, 1] → x=29 → f(x)=841

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 5 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [0, 1, 0, 0, 1] → x= 9 → f(x)= 81
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 0, 0, 1] → x=25 → f(x)=625
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [1, 1, 0, 0, 1] → x=25 → f(x)=625

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 6 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 1, 0, 0, 1] → x=25 → f(x)=625
  [1, 0, 0, 0, 1] → x=17 → f(x)=289
  [1, 1, 0, 0, 1] → x=25 → f(x)=625
  [1, 1, 0, 0, 0] → x=24 → f(x)=576

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 7 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 0, 1, 0, 1] → x=21 → f(x)=441
  [1, 1, 0, 0, 1] → x=25 → f(x)=625
  [1, 0, 0, 1, 1] → x=19 → f(x)=361
  [1, 1, 0, 1, 0] → x=26 → f(x)=676
  [1, 1, 0, 0, 1] → x=25 → f(x)=625

 Melhor: x = 31 → f(x) = 961

==================================================
RESULTADO FINAL
==================================================

Melhor indivíduo: [1, 1, 1, 1, 1]
x = 31
f(x) = 961

Ótimo global: x = 31, f(x) = 961
Erro: 0
```

### Considerações

A base matemática foi muito interessante. O algoritmo pega os índices dos vetores e os coloca na base 2, lendo da direita para a esquerda, e eleva a base à posição do número. Para nós, é claro que o melhor indivíduo (Fitness) seria o 31, mas o computador não sabe disso previamente. Então, ele apenas segue cada parâmetro das funções estabelecidas e, através da evolução, chega no melhor resultado.

---

## LAB-02 - Execução código pronto

### Saída da execução

```text
==================================================
ONEMAX - AG com 30 indivíduos, 50 gerações
==================================================
Geração   0: Melhor = 14/20, Média = 10.37
Geração  10: Melhor = 20/20, Média = 19.07
Geração  20: Melhor = 20/20, Média = 19.53
Geração  30: Melhor = 20/20, Média = 19.37
Geração  40: Melhor = 20/20, Média = 19.43

 MELHOR FITNESS: 20/20
   Ótimo = 20 (todos os bits são 1)

==================================================
DESAFIO: Mude os parâmetros e veja o que acontece!
==================================================
1. Aumente a TAXA_MUT para 0.1. O que acontece?
2. Diminua POPULACAO para 10. O que acontece?
3. Aumente GERACOES para 100. O que acontece?
4. Mude ELITE para 0. O que acontece?
```

### Considerações

O algoritmo conseguiu alcançar o melhor fitness possível, `20/20`, já na geração 10. Também foi possível perceber que a média da população aumentou ao longo das gerações e ficou próxima do valor máximo. Isso mostra que a população foi convergindo para indivíduos com cada vez mais bits iguais a 1.

---

## LAB-03 - Execução código semi-pronto

### Saída da execução

```text
==================================================
OTIMIZANDO f(x) = x * sin(3x)
==================================================
Geração   0: Melhor f(x) = 6.3846 (x = 6.9412)
Geração  10: Melhor f(x) = 8.8039 (x = 8.8627)
Geração  20: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  30: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  40: Melhor f(x) = 8.9019 (x = 8.9020)

 MELHOR SOLUÇÃO: x = 8.9020, f(x) = 8.9019
```

### Considerações

Nesta atividade foi necessário completar as funções de conversão dos bits para um valor real, cálculo do fitness e mutação. Durante a execução, o algoritmo encontrou soluções cada vez melhores até chegar em `x = 8.9020`, com `f(x) = 8.9019`. A partir da geração 20, o melhor resultado permaneceu o mesmo, indicando a convergência do algoritmo para essa solução.
