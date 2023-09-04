import labirinto as lb
import numpy as np
from geneticalgorithm import geneticalgorithm as ga #lib algoritmo genetico
from pyswarms.single.global_best import GlobalBestPSO #lib pso

larg = 4
alt = 4
inicio = (0, 0)
obj = (alt - 1, larg - 1)

sem_muros = lb.cria_labirinto(larg, alt)
lb.desenha_labirinto(lab = sem_muros, larg = larg, alt = alt)

#direções: (11, 00, 01, 10) -> (N, S, L, O)
#exemplo:
#+--+--+--+
#| i      |
#+--+--+  +
#|       o|
#+--+--+--+
#solução: 010100...
#+--+--+--+
#| i      |
#+--+--+  +
#| o      |
#+--+--+--+
#solução: 0101001010

sol_tam = (larg * alt - 1) * 2


def normalizar_gene(i):
  if i >= 0.5:
    return 1
  return 0

def normalizar_populacao(populacao):
  return list(map(normalizar_gene, populacao))

def imprimir_caminho(caminho):
  def obter_direcao(x,y):
    if x == y:
      if x == 0:
        return 'v'
      else:
        return '^'

    if x == 1:
        return '<'

    return '>'

  i = 0
  c = []
  while i < len(caminho)-1:
    c.append(obter_direcao(caminho[i], caminho[i+1]))
    i+= 2

  print(c)


def aptidao_pso(swarm):

  apt = []
  for particle in swarm:
    particula_normalizada = normalizar_populacao(list(particle))
    custo = aptidao_ga(particula_normalizada);
    apt.append(custo)
  return np.array(apt)

def aptidao_ga(solucao):

  def calc_vizinho(pos, direcao):
    if direcao == (1, 1):
      return(pos[0] - 1, pos[1])
    elif direcao == (0, 0):
      return(pos[0] + 1, pos[1])
    elif direcao == (0, 1):
      return(pos[0], pos[1] + 1)
    elif direcao == (1, 0):
      return(pos[0], pos[1] - 1)

  atual = inicio
  i = 0
  while i < (sol_tam - 1) and atual != obj:
    direcao = (solucao[i], solucao[i + 1])
    vizinho = calc_vizinho(atual, direcao)

    if atual + vizinho in sem_muros or vizinho + atual in sem_muros:
      atual = vizinho
    i += 2

  return(abs(atual[0] - obj[0]) + abs(atual[1] - obj[1]))


def algoritmo_genetico():
  parametros = {
   'max_num_iteration': 10000,
   'population_size':10,
   'mutation_probability':0.1,
   'elit_ratio': 0.01,
   'crossover_probability': 0.5,
   'parents_portion': 0.3,
   'crossover_type':'one_point',
   'max_iteration_without_improv': 10000
  }

  exp = ga(function = aptidao_ga,
        dimension = sol_tam,
        variable_type = 'int',
        variable_boundaries = np.array([[0, 1]] * sol_tam),
        algorithm_parameters = parametros)

  exp.run()

def pso():
  x_max = 1 * np.ones(sol_tam)
  x_min = 0 * x_max
  bounds = (x_min, x_max)
  options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
  optimizer = GlobalBestPSO(n_particles=10, dimensions=sol_tam, options=options, bounds=bounds)

  custo, pos = optimizer.optimize(aptidao_pso, 10000)

  imprimir_caminho(list(map(normalizar_gene, pos)))




#Atividade:
#1. variar parametros do problema
#2. resolver com Simulated Annealing
#3. resolver com PSO


algoritmo_genetico()

#pso()