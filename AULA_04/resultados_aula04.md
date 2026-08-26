# Resultados - Aula 04

## Exercício 1 - Análise do Elitismo na Estabilidade Algorítmica

O exercício compara o comportamento do algoritmo genético com e sem elitismo.

### Resultados obtidos

| Configuração | Menor custo final | Vezes em que o melhor custo piorou |
|---|---:|---:|
| Com elitismo | 269,49 | 0 |
| Sem elitismo | 262,12 | 2 |

Na execução com elitismo, o melhor custo encontrado não piorou em nenhuma geração. Já na execução sem elitismo, o melhor custo piorou em 2 momentos.

Mesmo que nesta execução o menor custo final sem elitismo tenha sido menor (`262,12`) do que com elitismo (`269,49`), o teste mostra que o elitismo torna a evolução mais estável, pois preserva a melhor solução encontrada entre as gerações.

**Conclusão:** o elitismo ajuda a evitar a perda de boas soluções durante a evolução. Porém, por se tratar de um algoritmo estocástico, utilizar elitismo não significa obrigatoriamente obter o menor custo em todas as execuções.

---

## Exercício 2 - Inserção de Penalidades por Descumprimento de SLA

A rota testada foi:

```text
0 -> 1 -> 2 -> 3 -> 4 -> 5
```

### Latência dos enlaces

| Enlace | Latência | Situação |
|---|---:|---|
| 0 -> 1 | 18,42 ms | OK |
| 1 -> 2 | 13,38 ms | OK |
| 2 -> 3 | 20,79 ms | OK |
| 3 -> 4 | 62,04 ms | Viola SLA |
| 4 -> 5 | 45,38 ms | OK |

O limite do SLA é de `50 ms`. Apenas o enlace `3 -> 4`, com `62,04 ms`, ultrapassou esse limite.

Para cada violação foi adicionada uma penalização fixa de `1000 ms`.

O resultado exibido pelo programa foi:

```text
Custo Total (Com Penalizações de SLA): 1160.00 ms
```

**Conclusão:** a penalização aumenta significativamente o custo de uma rota que possui enlaces acima do limite permitido, fazendo com que essas soluções sejam menos atrativas durante a otimização.

---

## Exercício 3 - Balanceamento de Carga em Servidores

O algoritmo distribuiu 20 tarefas entre 4 servidores com o objetivo de minimizar o **makespan**, que representa a maior carga acumulada entre os servidores.

### Indivíduo encontrado

```text
[3, 2, 0, 2, 0, 2, 1, 3, 3, 2, 1, 1, 0, 3, 0, 1, 1, 2, 0, 2]
```

Cada posição representa uma tarefa e o valor armazenado representa o servidor escolhido para executá-la.

### Distribuição das tarefas

| Servidor | Índices das tarefas | Tempos das tarefas | Carga total |
|---|---|---|---:|
| 0 | 2, 4, 12, 14, 18 | 40, 15, 50, 25, 5 | 135 s |
| 1 | 6, 10, 11, 15, 16 | 19, 14, 28, 33, 42 | 136 s |
| 2 | 1, 3, 5, 9, 17, 19 | 35, 8, 22, 31, 10, 29 | 135 s |
| 3 | 0, 7, 8, 13 | 12, 45, 60, 18 | 135 s |

### Resultado final

```text
Makespan encontrado: 136 s
Limite inferior teórico: 136 s
O makespan encontrado atingiu o menor valor teoricamente possível.
```

As cargas finais ficaram muito próximas:

```text
Servidor 0: 135 s
Servidor 1: 136 s
Servidor 2: 135 s
Servidor 3: 135 s
```

**Conclusão:** o algoritmo conseguiu distribuir as tarefas de forma equilibrada. O maior tempo acumulado foi de `136 s`, exatamente igual ao limite inferior teórico calculado no notebook. Portanto, nesta execução, a solução encontrada atingiu o menor makespan teoricamente possível.
