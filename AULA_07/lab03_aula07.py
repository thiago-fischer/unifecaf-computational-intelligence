import numpy as np
# Função de Custo Esférica (Queremos encontrar o mínimo em x=0, y=0)
def fitness_function(position):
    return np.sum(position**2)

num_particles = 10
dimensions = 2
max_iter = 15

# Inicialização de Posições e Velocidades
X = np.random.uniform(-5, 5, (num_particles, dimensions))
V = np.random.uniform(-1, 1, (num_particles, dimensions))

pbest_X = np.copy(X)
pbest_fitness = np.array([fitness_function(p) for p in pbest_X])

gbest_index = np.argmin(pbest_fitness)
gbest_X = np.copy(pbest_X[gbest_index])

w = 0.5   # Inércia
c1 = 1.5  # Componente Cognitiva (Individual)
c2 = 1.5  # Componente Social (Coletiva)

for t in range(max_iter):
    for i in range(num_particles):
        r1, r2 = np.random.rand(), np.random.rand()
        
        # TODO: Implementar a equação de atualização da velocidade da partícula i
        # V[i] = (w * V[i]) + (c1 * r1 * (pbest_X[i] - X[i])) + (c2 * r2 * (gbest_X - X[i]))
        # Preencha a linha abaixo desbalancada:
        V[i] = (w * V[i]) + (c1 * r1 * (pbest_X[i] - X[i])) + (c2 * r2 * (gbest_X - X[i]))
        
        # Atualização da posição
        X[i] = X[i] + V[i]
        
        # Avaliação de Fitness
        current_fitness = fitness_function(X[i])
        if current_fitness < pbest_fitness[i]:
            pbest_fitness[i] = current_fitness
            pbest_X[i] = X[i]
            
            if current_fitness < fitness_function(gbest_X):
                gbest_X = X[i]
print(f"[LAB 03] Melhor posição encontrada pelo Enxame (gbest): {gbest_X}")
