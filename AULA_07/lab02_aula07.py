import numpy as np
# Problema da Mochila (Blindagem de Ativos)
weights = np.array([12, 2, 1, 4, 1])   # Custo/Consumo de Memória dos ativos
values = np.array([4, 2, 1, 10, 2])    # Cobertura de Risco/Valor do ativo
max_weight = 15

pop_size = 10
num_genes = len(weights)
generations = 10
mutation_rate = 0.1

# Inicialização da População (Matriz Binária 10x5)
population = np.random.randint(0, 2, size=(pop_size, num_genes))

def calculate_fitness(ind):
    total_weight = np.sum(ind * weights)
    total_value = np.sum(ind * values)
    # TODO 1: Implementar a restrição de peso. Se total_weight > max_weight, 
    # retorne fitness = 0 (penalização). Caso contrário, retorne total_value.
    return 0 if total_weight > max_weight else total_value

def tournament_selection(pop, fitnesses):
    # TODO 2: Selecionar 2 indivíduos aleatórios da população e retornar 
    # o indivíduo que possui o maior fitness (Seleção por Torneio).
    indices = np.random.choice(len(pop), size=2, replace=False)
    winner = indices[np.argmax(fitnesses[indices])]
    return pop[winner]

def crossover(parent1, parent2):
    point = np.random.randint(1, num_genes)
    child1 = np.concatenate([parent1[:point], parent2[point:]])
    child2 = np.concatenate([parent2[:point], parent1[point:]])
    return child1, child2

def mutate(ind):
    for i in range(num_genes):
        if np.random.rand() < mutation_rate:
            ind[i] = 1 - ind[i] # Inverte o bit (0 -> 1 ou 1 -> 0)
    return ind

# Loop Evolutivo
for g in range(generations):
    fitnesses = np.array([calculate_fitness(ind) for ind in population])
    new_population = []
    
    for _ in range(pop_size // 2):
        # Descomente e complete após preencher as funções acima:
        p1 = tournament_selection(population, fitnesses)
        p2 = tournament_selection(population, fitnesses)
        c1, c2 = crossover(p1, p2)
        new_population.extend([mutate(c1), mutate(c2)])
        
    population = np.array(new_population)

print("[LAB 02] Execute e teste o seu algoritmo preenchido!")
